Repository `uazu/stakker` at commit `c26efe5072eb0dfb19d5b59e4d8159fee91c4b60` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

为 `Ret` 实现小对象内联优化，使仅捕获少量数据的 `FnOnce` 回调无需堆分配，同时在 `no-unsafe` 特性下保留现有装箱实现。
