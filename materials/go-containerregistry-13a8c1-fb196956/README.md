# go-containerregistry-13a8c1-fb196956

Immutable E2B-only repository material for `google/go-containerregistry` at
`fb196956b1853752ed7fe13d3dd4572c45c16709`. Source, dependency caches, compiler caches, and images are
stored only in the persistent E2B templates recorded by `material.toml` and
`receipts/e2b.json`.

This directory intentionally contains no checkout, direction, instruction, verifier,
solution, model credential, or rollout output. Do not force-build the fingerprint
Dockerfile; Harbor must reuse the recorded ready template alias.
