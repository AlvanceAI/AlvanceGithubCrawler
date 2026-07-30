Repository `etcd-io/raft` at commit `56e32004b1af3a4cb625fbfe5dbca24fb6023d09` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

将复制流控状态从公开的 tracker.Progress 中拆出并隐藏为内部实现，同时为 RawNode.Status() 提供独立、稳定的公开复制进度快照类型。
