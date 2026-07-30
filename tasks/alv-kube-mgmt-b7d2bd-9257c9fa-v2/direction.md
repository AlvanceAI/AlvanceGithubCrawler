为 kube-mgmt 实现基于 OPA 自定义健康策略的存活检测：启动时通过 REST API 写入标记策略，并由 Kubernetes liveness probe 定期验证该策略以发现 OPA 重启或协调失效。
