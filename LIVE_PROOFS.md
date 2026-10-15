# Live proofs

## Deployment and matching source — 2026-10-14

- Network: gasless StudioNet, chain ID 61999.
- Contract: [0x15817b0cB312D60FB71042e3A8738647dED6F727](https://explorer-studio.genlayer.com/address/0x15817b0cB312D60FB71042e3A8738647dED6F727).
- Dedicated test signer: `0x7a413BB4AB62E31d62d4cD9efC8C8a8Dae37FB42`. Native encrypted keystore/OS-vault signing; no key export.
- Contract source commit: `11e5ef1` (contract file unchanged in subsequent proof/document commits).
- Explorer/RPC source equals `contracts/CounterexampleCircuitBreaker.py` after LF/trailing-newline normalization.
- Source SHA-256: `378567c2de65fe462f1f56039347e4a4e6fbf3721a9c50e1ca39ba10044f092b`.

## Successful finalized receipts

Every transaction below was checked for **FINALIZED**, leader execution **SUCCESS**, and **MAJORITY_AGREE**. These are five successful executions, not seven; expected-error transactions are separate below.

| Operation | Transaction | Stored effect |
|---|---|---|
| Deploy | [e81f9385…](https://explorer-studio.genlayer.com/tx/0xe81f93853b0ca04ae5b3ff734d2b7a51234e2acce4973a9c92e5c1f338944cbe) | Contract created; source equality verified |
| Register | [9b9ae4cc…](https://explorer-studio.genlayer.com/tx/0x9b9ae4ccc095c67d4093fb3fd7b3a0e658ba35ef72799f5b8c3b0cee98e9e1b6) | Immutable rubric and executable `has.fire`; UNFALSIFIED |
| Matching test | [2969d5a6…](https://explorer-studio.genlayer.com/tx/0x2969d5a6c060837975d37cfc23fc637d19dd568ffd4b823472260fc9f43c8c91) | Actual program ALLOW; semantic ALLOW; MATCH_ONLY |
| Ambiguous test | [a0dbd441…](https://explorer-studio.genlayer.com/tx/0xa0dbd441bc082a4362bb5d80eb510ad8ac6749ce400a975744bb6552f8d2698d) | Actual program ALLOW; semantic UNKNOWN; no false counterexample |
| AI synthesis | [386df7d8…](https://explorer-studio.genlayer.com/tx/0x386df7d8ab6a91a9a4a3d0e7c0651c4d2202b645e895e9ae85c0055bdba62918) | Actual program ALLOW; semantic DENY; COUNTEREXAMPLE; permanently FALSIFIED |

## Actual generated counterexample

> Reminder: fire drill tomorrow at 10am, please exit calmly, no actual emergency.

This input was generated inside the nondeterministic synthesis flow, not supplied as the synthesis transaction argument. The contract executed its stored `has.fire` program on the exact generated text and returned ALLOW. Independent semantic judgment against the original rubric returned DENY. The exact witness, labels, implementation association and root are stored onchain.

The authored rubric requires an explicit current real physical fire and immediate-help request; planned drills, negations, historical reports, hypotheticals and quotations are denied. Ambiguous interpretation is UNKNOWN. These are specifications and test strings, not reports of actual emergencies.

## Expected failures — not successful executions

| Attack | Transaction | Verified result |
|---|---|---|
| Reuse completed trial nonce | [e3d2582d…](https://explorer-studio.genlayer.com/tx/0xe3d2582d4d88355cf3a932b796164aeec65f58f2288cc17ec15ab583407a6251) | FINALIZED / ERROR / MAJORITY_AGREE; stderr contains `Trial nonce used` |
| Challenge after falsification | [b0172ed4…](https://explorer-studio.genlayer.com/tx/0xb0172ed40cfab154b6816727d4f002a3b19066616dc0f54a696a3849c6925526) | FINALIZED / ERROR / MAJORITY_AGREE; stderr contains `Circuit already falsified` |

## Readback and roots

- Implementation ID: `32756dce2273a5cb980ac20c837b7aa0c2025c201ff942e318deca845d7350cb`.
- Immutable specification root: `d97bb1b7e2ea4abe37caee227cf161625f84dcfe028d29e2ce4b1896a7a793d0`.
- Matching trial root: `56bbe1d646d3690f2e39b9cffae6fed4a90265f31dcc010a38ac3f3f57f7394c`.
- UNKNOWN trial root: `5f5b29caf97f74aab5d451f30cc42d229c17ac62e47de1a3ea365b4dd41991fe`.
- Generated counterexample root: `7e0144bd8460fa7e6a5a12d0854bce7cbbfa18bad4731cbd0c0b64e06db88138`.
- Failure trial ID: `976e8d94bfbea9c0711ce22155daccd95fd467da25c1948184080dd25edb4643`.
- Final state: FALSIFIED, exactly three completed trials. Expected-error transactions did not advance the counter or replace history.
- `classify_guarded` worked before falsification and fails afterward. The read RPC reports contract execution failure (`-32000`, `execution failed`), not a transport error. The separate terminal write above provides the precise contract error string.

Recheck with `node scripts/check.mjs source ADDRESS`, `success TX`, `error TX EXPECTED_TEXT`, and `state ADDRESS SIGNER`. The state verifier independently recomputes SHA-256 roots, identity/implementation bindings, program behavior, deterministic outcome and failure linkage. It rejects transport errors instead of treating them as a disabled circuit.

## Test scope

39 local direct/helper/callback tests and four SDK calldata roundtrips pass. Unit mocks are not live consensus proofs. The actual validator callback was tested for disagreement, forged execution and binding substitution; a real distributed disagreement/appeal was not induced. No formal correctness proof or production audit is claimed. UNFALSIFIED is never approval. StudioNet is a development network and persistence is not guaranteed.
