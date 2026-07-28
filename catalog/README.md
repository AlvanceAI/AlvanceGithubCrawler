# E2B Harbor Catalog

This directory contains only lightweight metadata and Harbor task envelopes. Repository
source trees, dependency caches, compiler caches, and images stay in persistent E2B
templates and are never stored here.

Each qualified repository is represented by:

- one line in `e2b-packages.jsonl`;
- one tiny task directory under `harbor/`;
- one persistent Harbor-compatible E2B template alias recorded in `e2b.json`.

Launch a packaged task from the repository root:

```bash
export E2B_API_KEY="${E2B_API_KEY:-$E2B_KEY}"
harbor run \
  --path catalog/harbor/<task-name> \
  --env e2b \
  --no-force-build \
  --agent nop \
  --disable-verification
```

Do not use `harbor tasks start-env` for these envelopes because that command currently
forces a rebuild. `harbor run` defaults to reusing the prepared E2B alias.
