将 ArbitraryImputer 的类型专用子类公开并注册，分别实现可离线提取 Polars/Narwhals 转换表达式的 get_transform_exprs，同时弃用旧 ArbitraryImputer 并补齐兼容性测试。
