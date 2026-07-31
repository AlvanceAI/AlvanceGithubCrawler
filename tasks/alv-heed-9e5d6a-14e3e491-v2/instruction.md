Repository `meilisearch/heed` at commit `14e3e4914ad5128c68f6bbf4ab40ae1de19b342e` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

放宽写事务的借用约束，使数据库写入 API 接受共享的 `&RwTxn`，从而支持在同一写事务中迭代一个数据库并将条目写入另一个数据库（包括源、目标为同一数据库的场景）。
