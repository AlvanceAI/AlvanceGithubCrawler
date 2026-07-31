Repository `lovoo/goka` at commit `b8856157710989eeaa37832bfa8fe12aaf3f8b87` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

修复多个 Processor 共用取消上下文并发停止时，ConsumerGroup 最终提交 offset 因协调器或 leader 变更而导致 Run 错误退出的问题，并增加可重复的并发关闭测试。
