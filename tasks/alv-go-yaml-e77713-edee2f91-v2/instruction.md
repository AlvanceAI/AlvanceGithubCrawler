Repository `goccy/go-yaml` at commit `edee2f91616c6d73112a13e7c0dbde72ce938877` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

重构 YAML 编码器对长切片的序列化流程，使其增量写入目标 io.Writer，避免构建并长期保留完整中间 AST，从而将峰值内存控制在不随切片总长度等比例暴涨的范围内。
