为 Zarr v3 分片索引编解码器实现写入支持，使多个逻辑 chunk 可编码、更新并持久化到同一 shard，同时正确维护 shard 索引。
