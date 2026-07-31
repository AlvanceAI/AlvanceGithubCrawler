移除 MP4 字段解析中的 `string=c_p` 标签及其依赖 `Seek` 的 `unmarshalString_C_P` 逻辑，并将定长填充字符串的读取迁移到 `OnReadField` 处理器。
