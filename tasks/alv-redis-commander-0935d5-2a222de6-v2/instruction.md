Repository `joeferner/redis-commander` at commit `2a222de65ed15832d4d4adfbbce564539b80115f` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

重构 Redis 后端连接管理，为树视图保留自动连接的基础连接，并为每个用户会话惰性创建、复用及过期关闭独立的 CLI 连接，以正确支持 SELECT、MULTI 和 Pub/Sub。
