修复全天重复事件的时区解析，使 get_recurrence() 使用日历的 X-WR-TIMEZONE 而非系统本地时区，并保证跨主机生成一致的日期与 UTC 时刻。
