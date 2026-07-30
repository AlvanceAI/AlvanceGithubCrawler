为 React Start 的 fetchSession 增加基于签名与过期时间校验的 JWT 会话缓存，在配置的 cookieCache 有效期内直接从 JWT 返回会话而不查询 Convex 数据库。
