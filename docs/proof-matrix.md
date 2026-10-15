# Proof matrix

| Scenario | Required behavior | Local evidence | Live evidence |
|---|---|---|---|
| AI-synthesized concrete mismatch | FALSIFIED; guarded interpreter disabled | direct mock | SUCCESS: `386df7d8…` |
| Known matching example | MATCH_ONLY; never approves correctness | direct mock | SUCCESS: `2969d5a6…` |
| Ambiguous interpretation | UNKNOWN; no false counterexample | direct mock | SUCCESS: `a0dbd441…` |
| Forged interpreter output | Validator rejects | Actual callback unit test | Not claimed |
| Disagreeing semantic label | Validator rejects | Actual callback unit test | Not claimed |
| Witness/spec/implementation substitution | Reject | Actual callback and direct tests | Not claimed |
| Duplicate trial nonce | Revert before AI | direct mock | Expected ERROR: `e3d2582d…` |
| Post-falsification author challenge/reset | Reject; failure immutable | direct mock | Expected ERROR: `b0172ed4…` |
| Invalid DSL or stack underflow/overflow | Reject | direct/helper tests | Not claimed |

39 tests pass locally. Direct tests use mocked AI and run only the leader. Callback tests execute the actual AST-extracted validator with independent label results; they are not distributed consensus. Live outcomes and actual receipts are tracked separately in LIVE_PROOFS.md.
