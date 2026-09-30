# Changelog

本项目遵循[语义化版本](https://semver.org/lang/zh-CN/)，变更记录按
[Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 组织。

写给人看：同一件事的几次提交，在这里是一行。

## [Unreleased]

### Added

- `tools/check_project.py`：结构体检器——把 28 条结构判据变成一条命令（`--level` / `--json` / `--quiet`，有强制项未过时退出码 1，可直接作为票据的 `Verify:` 或 CI 门禁）
- `GUIDE.md`：介绍与使用手册（安装与卸载、核心概念、14 个技能速查卡片、L0/L1/L2 三条完整走法、日常作息、12 条排错 FAQ、定制与扩展）
- `README.md` 补「文档地图」与「结构体检」两节

### Fixed

- 交付前逐份比对 14 份 SKILL.md，统一跨技能口径：
  - 「一次会话能做完的活」统一为「拷问后直接写一张票开工」，消除了指向拆票图的分叉（涉及 `grill-with-ledger`、`write-spec`）
  - ADR 文件名统一为 `NNNN-*.md`（原 `bug-diagnosis`、`session-handoff` 写作 `000N-`）
  - `decision-ledger` 不再代管 `ticket-plan` 的 `frontier` 判据
  - `oss-launch` 的术语表模板引用由 `templates/domain.md` 修正为 `templates/CONTEXT.md`
  - CI 骨架的版本矩阵注释与示例对齐（一个版本 + 需要时的 matrix 写法）

### Planned

- 按手册后续版本同步第 2 章与第 15 章（技能集改名、缺陷状态）

## [0.1.0] - 2026-09-30

### Added

- 首个可用版本：九步法全流程技能集，14 个技能
  - 入口与配置：`idea2oss`、`repo-setup`、`repo-bootstrap`
  - 想清楚：`project-brief`、`grill-with-ledger`、`decision-ledger`、`write-spec`
  - 做出来：`ticket-plan`、`build-ticket`、`dual-axis-review`、`bug-diagnosis`
  - 交出去：`session-handoff`、`oss-launch`、`flow-tuning`
- `templates/`：33 份可直接复制的模板（手册附录 A1–A7 与 B1–B4）
- `tools/install.py`：安装到技能目录，支持复制与目录联接（`--link`）、`--list`、`--uninstall`
- `tools/validate_skills.py`：校验 frontmatter、八节骨架、完成判据条数、交叉引用与模板存在性
- `tools/dump_templates.py`：从 `scaffold_project.py` 重新导出模板，避免两处维护
