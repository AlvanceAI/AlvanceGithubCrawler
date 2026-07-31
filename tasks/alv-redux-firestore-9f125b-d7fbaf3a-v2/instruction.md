Repository `prescottprue/redux-firestore` at commit `d7fbaf3a326634443e1372f216e3969657a288ba` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

在 props.firestore 中新增 uniqueSet()，通过 Firestore 事务仅在目标文档尚不存在时原子写入，以避免多个客户端并发覆盖同一文档。
