Repository `Manishearth/rust-gc` at commit `b7405c95a1956e930d8e5a26f6b68d7077f5b6f7` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

新增不含任何 GC 引用的 unsafe 标记 trait `GcDeadEnd`，为基础类型及满足递归约束的标准容器实现该 trait，并将其集成到 `Trace` 机制与派生宏的边界检查中。
