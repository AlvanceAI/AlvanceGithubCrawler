Repository `Mirantis/cri-dockerd` at commit `83d711fce4f8d6803138020da3faac2d81108173` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

实现并随 cri-dockerd 安装一个 Docker 日志驱动，将容器输出同时写入 Docker JSON 日志和 Kubernetes CRI 格式日志，并在驱动不可用时通过 Docker Attach/Logs API 回退流式采集。
