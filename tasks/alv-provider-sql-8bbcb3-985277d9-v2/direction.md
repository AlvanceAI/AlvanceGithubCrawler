为集群级和命名空间级 MySQL User 控制器实现既有用户接管：未配置 passwordSecretRef 时生成新密码、更新数据库用户，并将凭据写入 writeConnectionSecretToRef。
