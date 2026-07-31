Repository `tikv/raft-rs` at commit `ad13f3d90780f53aea2488c6a4b76c0d334bf136` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

将 Raft 节点内部触发的本地消息与需要通过网络传输的 protobuf 远程消息拆分为不同类型和处理路径，避免两者被误发送或误处理。
