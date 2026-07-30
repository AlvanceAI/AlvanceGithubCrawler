Repository `zhiburt/tabled` at commit `9619c06d06e738a3fd632ae98724c7cbe9245f1d` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

为 `CellOption` 和 `TableOption` 增加对象安全的动态分发机制，使函数可返回并直接应用 `Box<dyn CellOption<...>>` 与 `Box<dyn TableOption<...>>`，同时保持现有消费式设置语义。
