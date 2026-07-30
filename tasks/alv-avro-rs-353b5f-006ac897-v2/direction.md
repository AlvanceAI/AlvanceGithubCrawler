实现符合 Avro JSON Encoding 规范的 schema-aware JSON 序列化与反序列化模块，提供 `from_reader(reader, schema)` 和 `to_writer(writer, schema, value)` API，并正确处理 union 与 named type。
