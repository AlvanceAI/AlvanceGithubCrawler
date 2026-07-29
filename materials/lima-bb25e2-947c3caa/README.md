# lima-bb25e2-947c3caa

Immutable E2B-only repository material for `lima-vm/lima` at
`947c3caaf08a6958180168f0b9f1289f722a18a8`. Source, dependency caches, compiler caches, and images are
stored only in the persistent E2B templates recorded by `material.toml` and
`receipts/e2b.json`.

This directory intentionally contains no checkout, direction, instruction, verifier,
solution, model credential, or rollout output. Do not force-build the fingerprint
Dockerfile; Harbor must reuse the recorded ready template alias.
