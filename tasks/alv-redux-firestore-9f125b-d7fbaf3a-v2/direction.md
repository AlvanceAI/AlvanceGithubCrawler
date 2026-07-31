在 props.firestore 中新增 uniqueSet()，通过 Firestore 事务仅在目标文档尚不存在时原子写入，以避免多个客户端并发覆盖同一文档。
