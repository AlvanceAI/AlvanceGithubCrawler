为 AbstractTree 新增批量写入 API，使一批插入、删除和弱删除操作复用一次当前版本读取并直接写入活跃 memtable，同时返回批次写入总大小及更新后的 memtable 大小，并补充与逐项 append_entry 的基准对比。
