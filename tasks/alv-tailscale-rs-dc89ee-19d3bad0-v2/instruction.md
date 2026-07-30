Repository `tailscale/tailscale-rs` at commit `19d3bad00a7442cfab57f58cbe56ccd7a206c82d` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

为 ts_keys 的所有私钥类型移除直接 Serde 序列化能力，并引入只能通过显式转换使用的“for export”中间类型来安全持久化私钥。
