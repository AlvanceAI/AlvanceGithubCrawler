使所有 Temporal 自定义资源的 status/conditions 遵循 kstatus 约定，并通过测试验证其在部署进行中、失败和成功时分别被 Argo 与 Helm 判定为 InProgress、Failed 和 Current。
