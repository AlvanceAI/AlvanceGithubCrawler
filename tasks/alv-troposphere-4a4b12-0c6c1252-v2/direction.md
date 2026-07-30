为 `troposphere.events.Rule.ScheduleExpression` 增加 AWS EventBridge/CloudWatch Events 的 `cron(...)` 与 `rate(...)` 表达式校验，并在模板序列化前拒绝无效值。
