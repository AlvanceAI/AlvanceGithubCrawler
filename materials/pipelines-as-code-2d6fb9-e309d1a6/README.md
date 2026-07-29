# pipelines-as-code-2d6fb9-e309d1a6

Immutable E2B-only repository material for `tektoncd/pipelines-as-code` at
`e309d1a679af9684f4540952686fb0ba9971126d`. Source, dependency caches, compiler caches, and images are
stored only in the persistent E2B templates recorded by `material.toml` and
`receipts/e2b.json`.

This directory intentionally contains no checkout, direction, instruction, verifier,
solution, model credential, or rollout output. Do not force-build the fingerprint
Dockerfile; Harbor must reuse the recorded ready template alias.
