# 决议台账

> 第 2 步建立，全程回指 ｜ 谈定一条追加一行，**编号不复用**
> 类型只有三种：**约束**（不可违背，违反即缺陷）/ **默认**（可改但要写理由）/ **待定**（还没定，必须带期限）
> 回指规则：spec 的实现决策与测试决策句末写 `[D-nn]`；票据头写 `Covers: D-nn`；第 6 步算决议追溯率（目标 100%）

| 编号 | 类型 | 决议（精确到可验证） | 证据 |
|---|---|---|---|
| D-01 | 约束 | 每个 `SKILL.md` 必须能被单独拿走使用：正文里提到的技能只能是本集 14 个名字，提到外部技能时必须同时给出手工兜底路径 | `python tools/validate_skills.py` 报 0 个「调用了不存在的技能」 |
| D-02 | 约束 | `SKILL.md` 的八节骨架标题固定，改名或缺失即校验失败 | `validate_skills.py` 的八节检查全过 |
| D-03 | 约束 | 每条「完成判据」必须可检查（能跑一条命令、能指到一个文件、能回答一个问题），且每份技能至少 4 条 `- [ ]` | `validate_skills.py` 判据条数检查 |
| D-04 | 约束 | 决议台账只放一处（`docs/decisions.md`），编号永不复用，删掉的划掉保留 | `check_project.py` 的「台账只有一处」项通过 |
| D-05 | 约束 | 结构判据里机器能判断的部分，必须有一条命令能验证，且失败时退出码非 0 | `check_project.py --json` 退出码 1/0 |
| D-06 | 默认 | `tools/` 只用 Python 标准库，不引入第三方依赖 | 干净环境（无 site-packages）能跑通全部工具；`pyproject.toml` 无 `dependencies` |
| D-07 | 默认 | 技能正文中文，`description` 末尾带英文 `keywords:`，保证中英环境都能触发 | `validate_skills.py` 的 keywords 检查无警告 |
| D-08 | 默认 | 模板的事实来源是生成器，`templates/` 是导出物；两份手写件（`INDEX.md`、`manual-review.md`）不在此列 | `python tools/dump_templates.py --out <临时目录>` 重放：33 份逐字节一致、无多余文件；生成器缺失时退出码 2 且不写盘 |
| D-09 | 约束 | 交接文档（handoff）不进仓库：写到系统临时目录 | `check_project.py` 的「交接文档没进仓库」项通过 |
| D-10 | 约束 | 发布用语义化版本，升级认 tag 不跟 main；破坏性变更写在 CHANGELOG 的 Changed 段首行 | 仓库有 `v0.1.0` tag；CHANGELOG 有对应段落 |
| D-11 | 待定 | 是否提供英文版技能正文（`skills/*/SKILL.md` 的英文平行版本） | **期限：v0.2.0 发布前定**；到期未定则默认不做，并把本条改成「默认：不做」 |
| D-12 | 默认 | 依赖许可检查放进 CI，任何 GPL / AGPL / 未知许可依赖单独评估 | CI 里有许可检查步骤，且失败会挡住合并 |
| D-13 | 默认 | README 必须写明对 `mattpocock/skills` 的致谢，并写清"参考了什么、没复制什么"的边界；**不照搬其 MIT 全文**（本项目没有分发它的代码或文本，无此义务；将来若真的复制了内容，再另开票处理） | README「致谢」段；来源核实记录：GitHub API `license.spdx_id = MIT`、LICENSE 原文 `Copyright (c) 2026 Matt Pocock`、最新 tag 为 `v1.2.3` |

## 用法

- spec（`.scratch/engineering-v0.1.0/spec.md`）的实现决策与测试决策句末带 `[D-nn]`
- 票据头写 `Covers: D-nn`
- 第 6 步算决议追溯率：找到实现与验证证据的决议 ÷ 全部决议，**目标 100%**
