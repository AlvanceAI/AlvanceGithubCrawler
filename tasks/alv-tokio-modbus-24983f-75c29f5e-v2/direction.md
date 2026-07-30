将与 Tokio/I/O 无关的 Modbus 协议类型、帧定义及编解码逻辑拆分为可在 `no_std` 环境编译的核心 crate，并由 `tokio-modbus` 依赖和复用该核心实现。
