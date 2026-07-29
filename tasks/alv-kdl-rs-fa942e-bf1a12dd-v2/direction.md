扩展 Serde 反序列化字段重命名规则，使 `#[serde(rename = "#child or #0")]` 可声明多个候选 KDL 映射，并支持通过 `#child` 显式引用子节点。
