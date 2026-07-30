Repository `hoodie/icalendar` at commit `27d4f11b7626f2640810ad63749771a46937d3c6` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

修复全天重复事件的时区解析，使 get_recurrence() 使用日历的 X-WR-TIMEZONE 而非系统本地时区，并保证跨主机生成一致的日期与 UTC 时刻。
