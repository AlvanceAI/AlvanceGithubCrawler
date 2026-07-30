Repository `tqwewe/kameo` at commit `b4aaee797cc3fd12e8194db406d9d73a6bc021ce` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

将 kameo_actors 中除 Scheduler 外的跨 Actor 强引用在内部降级为 WeakActorRef 或 WeakRecipient，并在投递时升级及清理已失效的订阅者或接收者，避免辅助 Actor 阻止动态 Actor 销毁。
