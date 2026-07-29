在 multicalc 全库中按既有规则为值返回型访问器、查询方法和 builder 方法一致添加 `#[must_use]`，同时排除可变方法及已由返回类型提供警告的 `Result`、`Vector` 和 `Matrix` 返回方法。
