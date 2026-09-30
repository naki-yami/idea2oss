# Changelog

本项目遵循[语义化版本](https://semver.org/lang/zh-CN/)，变更记录按
[Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 组织。

写给人看：同一件事的几次提交，在这里是一行。

> **当前状态：还没有 release。** 仓库里没有 tag，所以下面 `Unreleased` 里的内容会在票据
> `.scratch/engineering-v0.1.0/issues/06-first-release.md` 执行时切成 `[0.1.0]`——发布动作由人做，代理不代发（见 `AGENTS.md` 的权限边界）。

## [Unreleased]

### Added

#### 技能集与工具

- 14 个技能，覆盖九步法的每一步与两条横向纪律（`idea2oss` 为入口）：
  - 入口与配置：`idea2oss`、`repo-setup`、`repo-bootstrap`
  - 想清楚：`project-brief`、`grill-with-ledger`、`decision-ledger`、`write-spec`
  - 做出来：`ticket-plan`、`build-ticket`、`dual-axis-review`、`bug-diagnosis`
  - 交出去：`session-handoff`、`oss-launch`、`flow-tuning`
- `templates/`：36 份可直接复制的模板与索引（源手册附录 A1–A7、B1–B4）
- `tools/install.py`：装到运行时技能目录，支持复制与目录联接（`--link`）、`--list`、`--uninstall`
- `tools/validate_skills.py`：技能契约校验——frontmatter、`name` 与目录名一致、八节骨架、判据条数、交叉引用、模板存在性（接缝 S1）
- `tools/dump_templates.py`：从生成器重放 `templates/`，避免两处维护

#### 工程化：让这个项目自己合规

- `tools/check_project.py`：结构体检器——28 条判据变成一条命令，有强制项未过时退出码 1，可直接作为票据的 `Verify:` 或 CI 门禁（接缝 S2）
- `tests/`：挂在 S1 / S2 / S3 三个接缝上的 `unittest`，断言退出码与输出，不断言实现细节
- `.github/workflows/ci.yml`：Python 3.9 与 3.13 双版本矩阵 → 测试 → 技能契约校验 → 结构体检 → 依赖许可检查
- `.github/workflows/release.yml`：tag 触发，源码包带 `sha256` 校验，release 正文取自本文件
- `.github/`：PR 模板（四问：改了什么 / 为什么 / 怎么验证 / 风险与回滚）、issue 模板、`CODEOWNERS`、`dependabot.yml`
- 社区文件：`CONTRIBUTING.md`、`SECURITY.md`、`CODE_OF_CONDUCT.md`
- `docs/onboarding.md`：接手者 30 分钟路径；`AGENTS.md`：代理入口 + 三条铁律口令 + 权限边界
- `docs/`：`agents/brief.md`（立项五句话）、`decisions.md`（12 条决议，D-01…D-12）、`adr/0001`–`0003`、`architecture.md`（5 个接缝）、`agents/` 三处落点
- `GUIDE.md`：介绍与使用手册；`README.md` 补「文档地图」与「结构体检」两节
- `.gitattributes`：仓库统一 LF，消除 Windows 与 Linux CI 之间的换行噪音

### Fixed

- 交付前逐份比对 14 份 `SKILL.md`，统一跨技能口径：
  - 「一次会话能做完的活」统一为「拷问后直接写一张票开工」，消除指向拆票图的分叉（涉及 `grill-with-ledger`、`write-spec`）
  - ADR 文件名统一为 `NNNN-*.md`（原 `bug-diagnosis`、`session-handoff` 写作 `000N-`）
  - `decision-ledger` 不再代管 `ticket-plan` 的 `frontier` 判据
  - `oss-launch` 的术语表模板引用由 `templates/domain.md` 修正为 `templates/CONTEXT.md`
  - CI 骨架的版本矩阵注释与示例对齐

### Planned

- `D-11`：英文版技能正文——**期限 v0.2.0 之前定**，到期未定则默认不做，并把该条改成「默认：不做」
- 按源手册后续版本同步第二章（技能表与改名对照）与第十五章（已知缺陷状态）
