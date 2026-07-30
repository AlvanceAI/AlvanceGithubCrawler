Repository `pytest-dev/pytest-xdist` at commit `bda3903d384fcb8d06e19ea85bdad5f7c211ca0c` is preloaded in `/app`.

Work in `/app`. The validated fuzzy direction is:

为 pytest-xdist 增加 `--sf`/`--slow-first` 调度功能，持久化上次运行的测试耗时，并按当前分发粒度聚合耗时后优先调度慢测试，同时正确处理 `--failed-first` 和 `--new-first` 的兼容规则。
