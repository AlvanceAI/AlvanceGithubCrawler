实现可变 OpenType 字体的完整序列化，使加载后通过 download、toArrayBuffer 或 Node.js 写出时保留 fvar、gvar、avar、cvar、HVAR 等变体表及全部字形变化，而不会退化为静态字体。
