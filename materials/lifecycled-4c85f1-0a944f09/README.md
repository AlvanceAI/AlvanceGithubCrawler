# lifecycled-4c85f1-0a944f09

Immutable E2B-only repository material for `buildkite/lifecycled` at
`0a944f09a9b6cf96e8c92e8a3ceb915dbebfd46f`. Source, dependency caches, compiler caches, and images are
stored only in the persistent E2B templates recorded by `material.toml` and
`receipts/e2b.json`.

This directory intentionally contains no checkout, direction, instruction, verifier,
solution, model credential, or rollout output. Do not force-build the fingerprint
Dockerfile; Harbor must reuse the recorded ready template alias.
