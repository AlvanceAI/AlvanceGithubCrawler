为 cmp.Diff 增加对 sync/atomic.Pointer[T] 的原生比较支持，通过原子加载其指针值并按普通指针语义递归比较，同时正确处理 nil、嵌套路径和差异报告。
