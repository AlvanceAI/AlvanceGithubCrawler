Repository `sktime/skpro` at commit `a1a0d7fcf406d308392bb653ed6d243d017a3d1c` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

将已停止维护的 cyclic_boosting 代码完整内嵌到 skpro.libs，并替换 np.product 等失效 NumPy API以保证新版 NumPy 兼容性，同时让现有概率回归适配器改用内嵌实现。
