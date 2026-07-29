为原生 clickhouse.Conn 提供连接作用域 API，使调用方能在同一底层池连接上依次执行 SET ROLE、业务查询及角色复位，并确保连接安全释放回池。
