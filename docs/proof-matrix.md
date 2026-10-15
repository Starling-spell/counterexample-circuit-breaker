# Proof matrix

| Scenario | Required behavior | Local evidence | Live evidence |
|---|---|---|---|
| AI-synthesized concrete mismatch | FALSIFIED; guarded interpreter disabled | direct mock | Pending |
| Known matching example | MATCH_ONLY; never approves correctness | direct mock | Pending |
| Ambiguous interpretation | UNKNOWN; no false counterexample | direct mock | Pending |
| Forged interpreter output | Validator rejects | Actual callback unit test | Not claimed |
| Disagreeing semantic label | Validator rejects | Actual callback unit test | Not claimed |
| Witness/spec/implementation substitution | Reject | Actual callback and direct tests | Not claimed |
| Duplicate trial nonce | Revert before AI | direct mock | Pending |
| Post-falsification author challenge/reset | Reject; failure immutable | direct mock | Pending |
| Invalid DSL or stack underflow/overflow | Reject | direct/helper tests | Not claimed |

36 tests pass locally. Direct tests use mocked AI and run only the leader. Callback tests execute the actual AST-extracted validator with independent label results; they are not distributed consensus. No live success is claimed until finalized SUCCESS receipts and state readback are recorded in LIVE_PROOFS.md.
