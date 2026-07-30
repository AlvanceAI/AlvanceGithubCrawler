Repository `smartcorelib/smartcore` at commit `3febb4cee5ec81fd8e8220192eeac3103d2c55fb` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

将 DenseMatrix 与 DenseMatrixMutView 的可变轴向迭代器改为基于安全切片拆分的实现，彻底移除裸指针运算和 unsafe，同时保持迭代顺序、无别名保证及行主序热路径零分配。
