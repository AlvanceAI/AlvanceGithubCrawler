Repository `google/go-cmp` at commit `b133f1f1932e48f466f597a3346ce6f5a49a0dc1` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

为 cmp.Diff 增加对 sync/atomic.Pointer[T] 的原生比较支持，通过原子加载其指针值并按普通指针语义递归比较，同时正确处理 nil、嵌套路径和差异报告。
