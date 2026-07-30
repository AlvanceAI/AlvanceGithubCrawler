为 PyOCI 实现符合 Python Simple Repository API 的私有仓库优先 PyPI 回退代理，使其可作为唯一的 index-url，并在私有包名已存在但版本不匹配时阻止回退以避免依赖混淆。
