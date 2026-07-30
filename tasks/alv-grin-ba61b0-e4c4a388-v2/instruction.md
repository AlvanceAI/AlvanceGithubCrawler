Repository `mimblewimble/grin` at commit `e4c4a38825c2dd3a822d7cdbe8bd4cd6f390e380` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

将 output/rangeproof PMMR 的 leaf set（UTXO 位图）迁移为由数据库事务维护的权威索引，仅保留内存缓存，并在 IBD 收发 txhashset.zip 时按需生成或导入位图文件。
