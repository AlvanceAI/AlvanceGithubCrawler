将 output/rangeproof PMMR 的 leaf set（UTXO 位图）迁移为由数据库事务维护的权威索引，仅保留内存缓存，并在 IBD 收发 txhashset.zip 时按需生成或导入位图文件。
