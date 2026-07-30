Repository `simonw/sqlite-utils` at commit `6a456830ca33eb5edaa634a9b0febe5d71bea2be` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

增强表 `.transform()` 的建表 SQL 解析与重建逻辑，在转换列结构时保留表级及列级 CHECK 约束、SQL 注释和列级 UNIQUE 约束，并避免因 SQLite 内部自动索引无 CREATE INDEX SQL 而抛出 TransformError。
