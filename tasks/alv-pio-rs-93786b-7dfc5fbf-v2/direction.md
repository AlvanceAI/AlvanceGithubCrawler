扩展 `pio_asm!` 过程宏，使调用方可通过 `define(NAME = CONST_EXPR)` 将 Rust 常量或 const 泛型注入 PIO 汇编，并在编译期完成指令编码与错误校验。
