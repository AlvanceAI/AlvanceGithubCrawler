修复 cargo set-version 的元数据更新逻辑，使仅设置 SemVer build metadata 时保留现有的 pre-release 标识，例如将 0.1.17-beta.3 更新为 0.1.17-beta.3+11.ge8fe5ff。
