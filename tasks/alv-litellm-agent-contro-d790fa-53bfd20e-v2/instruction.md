Repository `LiteLLM-Labs/litellm-agent-control-plane` at commit `53bfd20e2fec51fc8f665fb614512c6b138367da` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

为每个代理创建并复用独立的 Kubernetes PVC，将其挂载到 `/work/repo` 以跨会话保留工作区，并仅在删除代理时清理该 PVC。
