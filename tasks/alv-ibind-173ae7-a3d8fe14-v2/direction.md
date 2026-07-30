为 IbkrWsClient 增加市场数据（smd）订阅的后台自动续订机制，在服务端 15 分钟失效前按“umd+conid”后“smd+conid”的顺序透明刷新，并与取消订阅及连接生命周期同步。
