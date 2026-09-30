# Changelog

本项目遵循[语义化版本](https://semver.org/lang/zh-CN/)，变更记录按
[Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 组织。

写给人看：同一件事的几次提交，在这里是一行。

## [Unreleased]

### Planned

- `D-11`：英文版技能正文——**期限 v0.2.0 之前定**，到期未定则默认不做，并把该条改成「默认：不做」
- 按源手册后续版本同步第二章（技能表与改名对照）与第十五章（已知缺陷状态）
- `03` `04`：CI 在真实 PR 上验证、真人陌生人测试（见 `.scratch/engineering-v0.1.0/issues/`）

## [0.1.0] - 2026-09-30

首次发布。这个仓库本身是**按它自己的九步流程走完的**：立项 → 台账 → spec → 票据图 →
测试挂在接缝上 → 结构体检器 → CI → 社区文件 → 打 tag。过程产物留在
`docs/` 与 `.scratch/engineering-v0.1.0/`，结构体检 28/28。

### Added

#### 技能集与工具

- 14 个技能，覆盖九步法的每一步与两条横向纪律（`idea2oss` 为入口）：
  - 入口与配置：`idea2oss`、`repo-setup`、`repo-bootstrap`
  - 想清楚：`project-brief`、`grill-with-ledger`、`decision-ledger`、`write-spec`
  - 做出来：`ticket-plan`、`build-ticket`、`dual-axis-review`、`bug-diagnosis`
  - 交出去：`session-handoff`、`oss-launch`、`flow-tuning`
- `templates/`：35 份可直接复制的模板与索引（源手册附录 A1–A7、B1–B4）
- `tools/install.py`：装到运行时技能目录，支持复制与目录联接（`--link`）、`--list`、`--uninstall`
- `tools/validate_skills.py`：技能契约校验——frontmatter、`name` 与目录名一致、八节骨架、判据条数、交叉引用、模板存在性（接缝 S1）
- `tools/dump_templates.py`：从生成器重放 `templates/`，避免两处维护

#### 工程化：让这个项目自己合规

- `tools/check_project.py`：结构体检器——28 条判据变成一条命令，有强制项未过时退出码 1，可直接作为票据的 `Verify:` 或 CI 门禁（接缝 S2）
- `tests/`：挂在 S1 / S2 / S3 三个接缝上的 12 个 `unittest` 用例，断言退出码与输出，不断言实现细节
- `.github/workflows/ci.yml`：Python 3.9 与 3.13 双版本矩阵 → 测试 → 技能契约校验 → 结构体检 → 依赖许可检查
- `.github/workflows/release.yml`：tag 触发，源码包带 `sha256` 校验，release 正文取自本文件
- `.github/`：PR 模板（四问）、issue 模板、`CODEOWNERS`、`dependabot.yml`
- 社区文件：`CONTRIBUTING.md`、`SECURITY.md`、`CODE_OF_CONDUCT.md`（正文为 Contributor Covenant v2.1，CC BY-SA 4.0）
- `docs/onboarding.md`：接手者 30 分钟路径；`AGENTS.md`：代理入口 + 三条铁律口令 + 权限边界
- `docs/`：`agents/brief.md`（立项五句话）、`decisions.md`（12 条决议，D-01…D-12）、`adr/0001`–`0003`、`architecture.md`（5 个接缝）、`release-checklist.md`（发布前剩余清单）
- `GUIDE.md`：介绍与使用手册；`README.md` 补「文档地图」与「结构体检」两节
- `.gitattributes`：仓库统一 LF

### Fixed

- 交付前逐份比对 14 份 `SKILL.md`，统一跨技能口径：
  - 「一次会话能做完的活」统一为「拷问后直接写一张票开工」，消除指向拆票图的分叉（涉及 `grill-with-ledger`、`write-spec`）
  - ADR 文件名统一为 `NNNN-*.md`
  - `decision-ledger` 不再代管 `ticket-plan` 的 `frontier` 判据
  - `oss-launch` 的术语表模板引用由 `templates/domain.md` 修正为 `templates/CONTEXT.md`
  - CI 骨架的版本矩阵注释与示例对齐
- 修 4 个工具缺陷（都有实跑证据）：`check_project` 的 4 处假阳性/假阴性并新增 `required` 字段；`validate_skills` 的 `keywords` 续行误报与目录缺失抛栈；`install` 的联接判定不再依赖 `cmd` 的本地化输出；`dump_templates` 改为写回本仓库、导出名 `AGENTS.md.tpl`、缺生成器时退出码 2
- **修一个 P0**：`install.py` 在缺省 `--target` 时抛 `TypeError`——`README` 的第一条命令就是它。抓到它的是陌生人测试（干净克隆照 README 做），不是单元测试；同时补上回归用例 `test_default_target_is_cwd`
