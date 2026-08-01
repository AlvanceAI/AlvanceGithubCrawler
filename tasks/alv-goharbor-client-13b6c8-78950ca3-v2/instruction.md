Repository `mittwald/goharbor-client` at commit `78950ca3611b7b52b67adf8c3dd3b5adfc92ab5f` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

将 `*config.Options` 从 REST 客户端级别移除，改为作为输入参数传入各个 API 方法，并取消在 `NewRESTClient` 中统一设置。
