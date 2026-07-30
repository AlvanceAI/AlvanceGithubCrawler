将共识层与 clientpb.Server 和 clientpb.Cache 解耦：由提交者返回或分发区块执行结果，并让提议者接收外部传入的命令而非直接访问命令缓存。
