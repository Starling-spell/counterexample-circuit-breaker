import ast
import hashlib
import itertools
import json
import re
from pathlib import Path
from types import SimpleNamespace
import pytest

TREE = ast.parse(Path('contracts/CounterexampleCircuitBreaker.py').read_text())
NS = {'hashlib': hashlib, 'json': json, 're': re, 'LABELS': ('ALLOW', 'DENY', 'UNKNOWN')}
exec(compile(ast.Module(body=[n for n in TREE.body if isinstance(n, ast.FunctionDef)
     and n.name != 'fail'], type_ignores=[]), 'actual-helpers', 'exec'), NS)
RUBRIC = ('ALLOW only a message explicitly reporting a current real physical fire and requesting immediate help. '
          'DENY negated reports, historical reports, hypotheticals, quotations, and planned fire drills. '
          'If whether a current real emergency is reported is ambiguous, return UNKNOWN.')
WITNESS = 'There is no fire here; the fire drill is scheduled for next week.'


@pytest.fixture
def breaker(direct_vm, direct_deploy, direct_alice):
    direct_vm.sender = direct_alice
    return direct_deploy('contracts/CounterexampleCircuitBreaker.py')


def mock(vm, label='DENY', witness=WITNESS):
    vm.clear_mocks()
    vm.mock_llm(r'(?s).*COUNTEREXAMPLE SYNTHESIS.*', json.dumps({'input': witness}))
    vm.mock_llm(r'(?s).*INDEPENDENT RUBRIC JUDGMENT.*', json.dumps({'label': label}))


def test_generated_witness_disables_actual_classifier(breaker, direct_vm):
    key = breaker.register('fire', RUBRIC, 'has.fire')
    before = breaker.get_implementation(key)
    assert breaker.classify_guarded(key, before['spec_root'], WITNESS) == 'ALLOW'
    mock(direct_vm)
    trial = breaker.synthesize('search', key)
    stored = breaker.get_trial(trial)
    assert stored['outcome'] == 'COUNTEREXAMPLE'
    assert stored['report']['semantic'] == 'DENY' and stored['report']['observed'] == 'ALLOW'
    assert stored['report']['input'] == WITNESS
    root = stored.pop('root')
    assert root == NS['digest'](stored)
    after = breaker.get_implementation(key)
    assert after['state'] == 'FALSIFIED' and after['failure_trial'] == trial
    assert after['spec'] == before['spec'] and after['spec_root'] == before['spec_root']
    with direct_vm.expect_revert('Circuit disabled'):
        breaker.classify_guarded(key, before['spec_root'], WITNESS)
    with direct_vm.expect_revert('Circuit already falsified'):
        breaker.test_input('reset', key, 'A real fire needs immediate help!')
    with direct_vm.expect_revert('Registration nonce used'):
        breaker.register('fire', RUBRIC, 'true')


@pytest.mark.parametrize('label,outcome', [('ALLOW', 'MATCH_ONLY'), ('UNKNOWN', 'UNKNOWN')])
def test_non_counterexamples_never_certify(breaker, direct_vm, label, outcome):
    key = breaker.register('fire', RUBRIC, 'has.fire')
    mock(direct_vm, label)
    trial = breaker.test_input('test', key, 'A real fire needs immediate help!')
    assert breaker.get_trial(trial)['outcome'] == outcome
    assert breaker.get_implementation(key)['state'] == 'UNFALSIFIED'


def test_replay_and_identity(breaker, direct_vm, direct_bob):
    key = breaker.register('fire', RUBRIC, 'has.fire')
    mock(direct_vm, 'ALLOW')
    first = breaker.test_input('test', key, 'A real fire needs immediate help!')
    with direct_vm.expect_revert('Trial nonce used'):
        breaker.test_input('test', key, 'A real fire needs immediate help!')
    direct_vm.sender = direct_bob
    second = breaker.test_input('test', key, 'A real fire needs immediate help!')
    assert first != second


def test_other_stream_cannot_receive_failure(breaker, direct_vm):
    a = breaker.register('a', RUBRIC, 'has.fire')
    b = breaker.register('b', RUBRIC, 'false')
    mock(direct_vm)
    trial = breaker.synthesize('test', a)
    assert breaker.get_trial(trial)['report']['binding']['implementation'] == a
    assert breaker.get_implementation(b)['state'] == 'UNFALSIFIED'
    assert breaker.get_implementation(a)['state'] == 'FALSIFIED'
    with direct_vm.expect_revert('specification mismatch'):
        breaker.classify_guarded(b, breaker.get_implementation(a)['spec_root'], WITNESS)


@pytest.mark.parametrize('program', ['', 'and', 'has.fire,or', 'true,false', 'has.__import__',
    'has.A', 'word.fire,not,and', 'has.fire,,not', ','.join(['true']*33), ','.join(['true']*17 + ['or']*16)])
def test_invalid_program(breaker, direct_vm, program):
    with direct_vm.expect_revert('Invalid program'):
        breaker.register('bad', RUBRIC, program)


@pytest.mark.parametrize('program,text,result', [
    ('has.fire', 'A firefly on the wall.', 'ALLOW'),
    ('word.fire', 'A firefly on the wall.', 'DENY'),
    ('word.fire', 'FIRE! Send help now.', 'ALLOW'),
    ('prefix.urgent', 'URGENT assistance needed', 'ALLOW'),
    ('has.fire,has.drill,not,and', 'A fire drill tomorrow.', 'DENY'),
    ('has.fire,has.flood,or', 'There is a flood here.', 'ALLOW'),
    ('true,not', 'Any input at all.', 'DENY')])
def test_actual_program_semantics(program, text, result):
    assert NS['execute'](program, text) == result


@pytest.mark.parametrize('witness', ['', ' short ', '\x00bad input', '💡'*151])
def test_witness_bounds(breaker, direct_vm, witness):
    key = breaker.register('fire', RUBRIC, 'has.fire')
    with direct_vm.expect_revert('Invalid test input'):
        breaker.test_input('test', key, witness)


@pytest.mark.parametrize('label', [[], True, 1, 'APPROVE', 'allow', None])
def test_malformed_label(label):
    with pytest.raises((ValueError, TypeError)):
        NS['parse_label']({'label': label})


def test_duplicate_json_fields():
    with pytest.raises(ValueError):
        NS['parse_label']('{"label":"ALLOW","label":"DENY"}')


def test_label_outcome_truth_table():
    for semantic, observed in itertools.product(NS['LABELS'], ('ALLOW', 'DENY')):
        out = NS['derive_outcome'](semantic, observed)
        assert (out == 'COUNTEREXAMPLE') == (semantic != 'UNKNOWN' and semantic != observed)
        assert (out == 'UNKNOWN') == (semantic == 'UNKNOWN')


def test_actual_validator_rejects_disagreement_and_forged_execution():
    cls = next(n for n in TREE.body if isinstance(n, ast.ClassDef))
    method = next(n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == '_challenge')
    fn = next(n for n in method.body if isinstance(n, ast.FunctionDef) and n.name == 'validator')
    class Return:
        def __init__(self, data): self.calldata = data
    binding = {'implementation': 'a', 'spec_root': 'original'}
    nondet = SimpleNamespace(exec_prompt=lambda *a, **kw: {'label': 'DENY'})
    ns = dict(NS, gl=SimpleNamespace(vm=SimpleNamespace(Return=Return), nondet=nondet),
              binding=binding, spec={'program': 'has.fire', 'rubric': RUBRIC}, supplied=None)
    exec(compile(ast.Module(body=[fn], type_ignores=[]), 'actual-validator', 'exec'), ns)
    report = {'binding': binding, 'input': WITNESS, 'observed': 'ALLOW', 'semantic': 'DENY'}
    assert ns['validator'](Return(report))
    nondet.exec_prompt = lambda *a, **kw: {'label': 'ALLOW'}
    assert not ns['validator'](Return(report))
    nondet.exec_prompt = lambda *a, **kw: {'label': 'DENY'}
    assert not ns['validator'](Return(dict(report, observed='DENY')))
    assert not ns['validator'](Return(dict(report, binding={'implementation': 'b', 'spec_root': 'original'})))
    ns['supplied'] = 'Another exact witness'
    assert not ns['validator'](Return(report))
    assert not ns['validator'](object())


def test_interpreter_boolean_properties():
    for text in ('Fire drill', 'Flood now', 'Nothing here', 'FIRE and FLOOD'):
        a = NS['execute']('has.fire', text) == 'ALLOW'
        b = NS['execute']('has.flood', text) == 'ALLOW'
        assert (NS['execute']('has.fire,not,not', text) == 'ALLOW') == a
        assert (NS['execute']('has.fire,has.flood,or', text) == 'ALLOW') == (a or b)
        assert (NS['execute']('has.fire,has.flood,and', text) == 'ALLOW') == (a and b)
