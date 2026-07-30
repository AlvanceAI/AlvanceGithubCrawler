新增默认关闭的命令行选项，将每个 Compose 服务及卷、网络分别生成独立 Nix 模块，并由目录中的 default.nix 统一导入且保留前导配置与根 target。
