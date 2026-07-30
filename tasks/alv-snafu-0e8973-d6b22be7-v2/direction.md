为 SNAFU 派生宏增加 feature-gated 的 `defmt::Format` 代码生成，支持通过 `#[snafu(defmt(...))]` 为错误结构体和枚举变体定义嵌入式格式化消息，并提供名称型默认消息。
