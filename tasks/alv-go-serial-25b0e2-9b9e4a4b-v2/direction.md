为串口 Port API 增加与 os.File.SetDeadline 一致的动态绝对读写截止时间设置能力，并在 Linux、BSD/macOS、Windows 和 WASM 后端统一实现超时行为。
