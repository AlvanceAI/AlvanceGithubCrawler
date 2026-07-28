Repository `crossplane-contrib/provider-kubernetes` at commit `6d946d51b467058a56023bd806977589735749bd` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

在 Object 被删除但外部 Kubernetes 资源被保留时，通过 SSA 撤销该 Object 对应字段管理器的所有权并清理 managedFields，避免字段成为孤儿。
