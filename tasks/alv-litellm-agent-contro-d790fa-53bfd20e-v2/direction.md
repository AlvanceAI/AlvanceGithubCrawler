为每个代理创建并复用独立的 Kubernetes PVC，将其挂载到 `/work/repo` 以跨会话保留工作区，并仅在删除代理时清理该 PVC。
