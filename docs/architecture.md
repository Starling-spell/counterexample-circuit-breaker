# Boundary and architecture

## Mechanism

A bounded text classifier is registered with its normative natural-language rubric and executable postfix program. Programs are immutable; each starts UNFALSIFIED, which means **untested/not yet disproved**, never safe or correct. Anyone may ask GenLayer to synthesize an adversarial input or submit a test input. The contract executes the program itself. Leader and validators independently classify the same input under the rubric. A known semantic/program mismatch changes the circuit to FALSIFIED permanently. An ambiguous interpretation records UNKNOWN without changing the circuit. A matching example records MATCH_ONLY and proves nothing beyond that one example.

```
immutable rubric + executable program
                 |
      AI-generated adversarial input
                 |
        actual onchain interpreter
                 + independent rubric judgments
                 |
         exact semantic-label agreement
           /           |           \
     mismatch        match       UNKNOWN
     FALSIFIED     MATCH_ONLY     UNKNOWN
         |
   guarded classifier view disabled
```

## Ownership

The frontend may preview programs; previews are not authoritative. The contract owns execution, witness binding, semantic classification consensus, append-only test records, and the monotonic circuit breaker. The registering author cannot clear a falsification. New revisions require new immutable registrations; there is no versioned graph or head advancement.

The rubric is a specification, not a claim of external reality. The input is test data, not an execution log. Actual behavior is obtained by executing stored code in the contract's small interpreter, not from caller-provided outcomes. No URLs, hashes standing in for evidence, service-delivery claims, certificates, funds, or arbitrary code execution.

## Consequential AI boundary

Different synthesized inputs can produce different falsification outcomes. Validators do not repeat deterministic graph arithmetic: each independently performs a substantive semantic interpretation of the concrete input against the full rubric. Exact labels, exact bindings and actual interpreter output must agree. A consensus failure does not become a fabricated application CONFLICTED receipt.

## Consumer warning

`classify_guarded` refuses a FALSIFIED implementation and requires its exact specification root. UNFALSIFIED is **not approval**; this is an advisory negative-evidence breaker, not a sufficient authorization or safety gate. Consumers must not assume a finite failed search establishes correctness.
