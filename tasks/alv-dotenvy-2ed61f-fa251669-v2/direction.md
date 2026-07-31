为 dotenvy 属性宏增加 async-std 入口函数支持，确保环境加载与修改发生在异步运行时启动前，并兼容空返回值、Result 等不同 main 函数签名。
