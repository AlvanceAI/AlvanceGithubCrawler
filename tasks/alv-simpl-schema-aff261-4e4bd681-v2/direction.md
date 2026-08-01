为 schema 清理流程增加异步 AutoValue 支持，使返回 Promise 的 autoValue 函数可被等待并将解析结果正确写入文档，同时保持现有同步行为兼容。
