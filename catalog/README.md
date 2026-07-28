# Trace Repository Material Catalog

This repository emits the same three-layer layout consumed by `/home/inuyasha/Trace`:

- `catalog/repo-materials.toml` indexes immutable qualified materials;
- `materials/<material-id>/` stores provenance, E2B receipts, baseline entrypoints, and
  the Harbor environment fingerprint;
- `tasks/<task-id>/` stores the initial Harbor-compatible direction task referencing
  its material.

Repository source, `.git`, dependencies, compiler caches, and images live only inside
persistent E2B templates. The checked-in material/task records are small control-plane
artifacts and contain no credentials.

Launch a task without rebuilding:

```bash
export E2B_API_KEY="${E2B_API_KEY:-$E2B_KEY}"
harbor run \
  --path tasks/<task-id> \
  --env e2b \
  --no-force-build \
  --agent nop \
  --disable-verification
```

Do not use `harbor tasks start-env`: the installed Harbor version forces a build for
that command. `harbor run` reuses the ready E2B alias recorded in the material receipt.
