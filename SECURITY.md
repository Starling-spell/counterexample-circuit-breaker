# Security and limitations

Experimental, unaudited. Semantic labels can be wrong even when models agree. Prompt injection, ambiguous rubrics, malicious authors, shared-model bias and denial-of-service remain risks. Rubrics are public immutable specifications, not real-world facts. Test witnesses do not establish real events.

Every program is a bounded allowlisted interpreter, not arbitrary executable code. The observed result is always computed onchain. Trial bindings include contract, implementation, spec root, challenger, nonce and ordinal. Validators recheck exact bindings and actual execution and independently reason on the rubric. No score tolerance or caller-supplied result exists.

FALSIFIED is terminal; no owner reset exists. Anyone may submit a challenge to avoid author censorship. Per-author/per-challenger and per-implementation caps bound growth, but Sybil registrations are possible and 64 completed tests can exhaust an implementation's test budget. UNFALSIFIED and UNKNOWN must never be interpreted as affirmative safety. Consumers of `classify_guarded` receive the original program's output, not a consensus endorsement of that new input. Consumers must add their own trust/admission policy.

No funds, native transfers, external writes, proxies or upgrade controls. Registering a replacement creates a new identity; consumers must explicitly select it. No stored evidence can be overwritten under an existing nonce. Report issues privately to the repository maintainer.
