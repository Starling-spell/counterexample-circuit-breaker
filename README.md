# CounterexampleCircuitBreaker

Experimental GenLayer adversarial testing and monotonic falsification for bounded text classifiers.

## Problem

Keyword filters often disagree with their intended natural-language specification. A keyword can appear in a negation, hypothetical, quotation or unrelated word. Caller statements that a filter works are not evidence of its behavior.

## Why GenLayer

The contract executes the stored classifier itself. AI synthesizes concrete adversarial text, and validators independently interpret that exact text against the immutable rubric. This semantic decision is not reducible to the classifier's deterministic arithmetic. A known mismatch permanently trips the implementation's circuit breaker and disables `classify_guarded`.

```
Register rubric + executable program
              |
AI synthesize input / submit input
              |
Onchain execution + independent rubric judgments
              |
Exact semantic-label agreement
       /             |             \
COUNTEREXAMPLE     MATCH_ONLY      UNKNOWN
   FALSIFIED      UNFALSIFIED    UNFALSIFIED
```

**UNFALSIFIED means not disproved, not approved.** One passing example or failed search cannot certify a program. This is an advisory negative-evidence primitive, not a standalone safety or authorization gate.

## Program language

Comma-separated postfix boolean instructions: `has.word` (case-insensitive substring), `word.word` (ASCII word membership), `prefix.word`, `true`, `false`, `not`, `and`, `or`. Literals contain 1–32 ASCII lowercase letters. Maximum 32 instructions, stack depth 16, and program length 640. No eval, arbitrary regex, network requests or code execution.

Example: `has.fire,has.drill,not,and`. The contract runs the complete interpreter; no caller-supplied output or execution summary is accepted.

## Consensus and security

The leader proposes a witness and derives a semantic label. Validators re-execute the program and independently derive a label from the original rubric and exact witness. Exact decision equality is required. UNKNOWN cannot trip the breaker. Disagreement/malformed output does not become a fabricated successful conflict record. The deterministic layer rechecks binding and execution and derives the only allowed outcome.

Immutable specification roots, contract/principal/nonce separation, full witness storage, bounded input sizes, append-only trial records, cross-implementation binding and irreversible FALSIFIED states. The author cannot reset a failed circuit. No graphs, certificates, escrow or source-attestation workflow. Rubrics are authored specifications and test inputs are data—not claims about actual emergencies or external delivery.

## API

`register`, `synthesize`, `test_input`, `get_implementation`, `get_trial`, `classify_guarded`.

## Test and deploy

```
python -m pip install -r requirements.txt
genvm-lint check contracts/CounterexampleCircuitBreaker.py
python -m pytest tests -q
npm ci
npm run test:sdk
genlayer network set studionet
genlayer account use YOUR_ENCRYPTED_TEST_ACCOUNT
genlayer deploy --contract contracts/CounterexampleCircuitBreaker.py
```

Verify FINALIZED **and execution SUCCESS**, read the state, and compare Explorer source to this file. Direct tests run only the leader; callback tests execute the actual validator separately, not distributed consensus. Real network proof status is recorded in [LIVE_PROOFS.md](LIVE_PROOFS.md).

The optional sanitized CLI wrapper requires `CIRCUIT_TEST_ACCOUNT` (an unlocked encrypted test keystore name) and `CIRCUIT_CLI_PATH` if the CLI entrypoint is not in the neighboring development workspace. It uses the built-in StudioNet preset, native OS-vault signing and one-shot broadcast transport. Raw validator debug/config output is suppressed. No key export or global account switch occurs. `scripts/demo.cjs` passes the public fixture arguments directly, avoiding shell JSON quoting hazards. Check receipts between writes; never blindly repeat an uncertain broadcast.

See [architecture](docs/architecture.md), [threat model](SECURITY.md), and [proof matrix](docs/proof-matrix.md). No audit, production safety, correctness proof, or reviewer acceptance is claimed.

## Live demonstration

[StudioNet contract](https://explorer-studio.genlayer.com/address/0x15817b0cB312D60FB71042e3A8738647dED6F727). Deployed source matches the contract file. Real trials recorded MATCH_ONLY, UNKNOWN, then an AI-generated fire-drill counterexample that permanently tripped the classifier. Five successful finalized executions and two separately identified expected-error transactions are documented in [LIVE_PROOFS.md](LIVE_PROOFS.md).
