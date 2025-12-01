AXIOM HIVE — Conformance — C=0
Document ID: AH-Ω-C0-2025-11-30

| Requirement | Mechanism | Evidence |
| Deterministic evaluation | Fixed seeds, explicit types, reproducible builds | Environment manifests |
| Proof-carrying outputs | Certificates with full derivation and hash commitments | Certificate schemas, verifier recomputation documentation |
| Gate enforcement | accept iff verify(P, y; A_v, R_v) ∧ provenance_intact | Gate logic spec, acceptance predicate, rejection reasons |
| Provenance integrity | Hash chaining + Ed25519 signatures | Audit procedure and results |
| Temporal sovereignty | SSOT version tagging and immediate constraint enforcement | Versioned entries, pre/post-update compliance analysis |
| Performance transparency | Measured t_inf/t_proof | Methodology description, ratio reporting with deterministic inputs |
