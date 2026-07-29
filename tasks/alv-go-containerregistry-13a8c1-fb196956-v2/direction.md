为 daemon.Write 实现基于本地镜像与层存在性检查的增量加载，避免重复下载远端基础层并向 Docker daemon 重复传输已有层。
