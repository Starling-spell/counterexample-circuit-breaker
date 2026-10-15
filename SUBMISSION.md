# Builder → Intelligent Contracts

## Title

CounterexampleCircuitBreaker — AI-Synthesized Classifier Falsification

## Notes / Description

CounterexampleCircuitBreaker tests bounded text classifiers against immutable natural-language rubrics. GenLayer AI synthesizes adversarial inputs; the contract executes the registered postfix program itself. Validators independently classify the exact input against the full rubric and must agree exactly on its semantic label and actual execution.

A known mismatch permanently marks the implementation FALSIFIED and disables guarded classification. Matching examples never certify correctness; ambiguous judgments record UNKNOWN. Specification roots, exact witness binding, principal/nonces and append-only trials prevent substitution and replay. No graph, source-attestation workflow, certificate or caller-reported execution result is used.

StudioNet recorded MATCH_ONLY, UNKNOWN, then an AI-generated fire-drill counterexample. Five executions finalized successfully; replay and terminal-state attacks failed as expected. Source matches Explorer; 39 local tests pass.

## Evidence

- GitHub Repository: https://github.com/Starling-spell/counterexample-circuit-breaker
- GitHub File: https://github.com/Starling-spell/counterexample-circuit-breaker/blob/main/contracts/CounterexampleCircuitBreaker.py
- GitHub File: https://github.com/Starling-spell/counterexample-circuit-breaker/blob/main/LIVE_PROOFS.md
- GitHub File: https://github.com/Starling-spell/counterexample-circuit-breaker/blob/main/docs/proof-matrix.md
- GenLayer Explorer Contract: https://explorer-studio.genlayer.com/address/0x15817b0cB312D60FB71042e3A8738647dED6F727
- Other — AI-generated counterexample: https://explorer-studio.genlayer.com/tx/0x386df7d8ab6a91a9a4a3d0e7c0651c4d2202b645e895e9ae85c0055bdba62918
- Other — matching input: https://explorer-studio.genlayer.com/tx/0x2969d5a6c060837975d37cfc23fc637d19dd568ffd4b823472260fc9f43c8c91
- Other — ambiguous input: https://explorer-studio.genlayer.com/tx/0xa0dbd441bc082a4362bb5d80eb510ad8ac6749ce400a975744bb6552f8d2698d

The complete proof ledger separately links deployment, registration, and two expected execution errors. No formal correctness, production safety or approval guarantee is claimed. UNFALSIFIED is not approval.
