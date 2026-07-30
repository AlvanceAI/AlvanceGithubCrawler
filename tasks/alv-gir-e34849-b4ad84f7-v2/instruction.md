Repository `gtk-rs/gir` at commit `b4ad84f7c5548fbab3972436e1a000fb5f829cdc` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

生成 signal connect 函数的版本门控时，应结合所属类的最低版本，省略与类相同或更早的冗余版本检查，同时保留晚于类版本的 signal 门控。
