<!-- idea2oss ｜ 手册 第 2 章 / 第 12 章 ｜ 判据：代理入口 + 权限边界；只留一份，避免与 CLAUDE.md 分叉 -->

<!-- 第 2 章 / 第 12 章 ｜ 判据：代理入口 + 权限边界；只留一个，避免与 CLAUDE.md 分叉 ｜ 结构不要改，改内容 -->
# AGENTS.md

<!-- 代理入口 ｜ 本仓库只用这一份；不建 CLAUDE.md，要建就先删这份，别让两份内容分叉 -->

这是本仓库对代理生效的规矩。**一次只调一个技能**，做完再换下一个；同时调多个只会互相挤占上下文。技能正文在 `skills/<name>/SKILL.md`，手册见 `GUIDE.md` 第五章。

## Agent skills

| 环节 | 用什么技能 | 干什么 |
|---|---|---|
| 判档与路由 | `idea2oss` | 判 L0 / L1 / L2，写下「当前：第 N 步 ｜ 下一步：<技能名>」；跳过的步要写清凭什么跳 |
| 第 0 步 立项 | `project-brief` | 五句话 brief + 最小可验证切片 + 许可证先定；产出 `docs/agents/brief.md` |
| 第 1 步 初始化仓库 | `repo-bootstrap` | `git init`、四类边界 `.gitignore`、提交前扫密钥、立三个落点目录 |
| 每仓库一次配置 | `repo-setup` | issue tracker 落点、triage 标签、领域文档布局、锁技能集版本；本仓库的产物在 `docs/agents/` |
| 第 2 步 拷问 | `grill-with-ledger` | 一轮 3–5 个问题附推荐答案；谈定一件当场落盘，术语进 `CONTEXT.md` |
| 第 2→6 步 决议台账 | `decision-ledger` | 谈定一条就往 `docs/decisions.md` 追加一行带编号的决议，spec / 票据按 `D-nn` 回指 |
| 第 3 步 设计文档 | `write-spec` | 七段产品设计文档（快照），实现决策与测试决策句末写 `[D-nn]` |
| 第 4 步 方案与计划 | `ticket-plan` | 接缝清单 + 垂直切片 + 票据六行头 + `frontier` 非空 |
| 第 5 步 实行 | `build-ticket` | 只喂票据 + `CONTEXT.md` + 涉及的接口；测试先红后绿；一票一提交 |
| 第 6 步 检测 | `dual-axis-review` | 标准轴 + 规格轴两份报告不合并；产品验收由人亲手跑，票据留 `Accept:` |
| 第 6 步 出错时 | `bug-diagnosis` | 六步诊断循环；三轮不收敛就停手写 ADR，另开「重新设计 X」的票 |
| 第 7 步 交付 | `session-handoff` | 检查前移到提交前、PR 四问、交接文档写系统临时目录且只给路径 |
| 第 8 步 开源发布与运营 | `oss-launch` | 法务与安全闸门、门面、社区文件、CI、版本与日志、运营节奏 |
| 全程（横向） | `flow-tuning` | 六个指标体检，结论必须指向九步里具体的一步 |

## 本仓库的规矩

**三条铁律（设成口令，不是知识）**

- **一票一会话**：做完一张票就开新会话。下一票只喂三样——票据本身 + `CONTEXT.md` + 这张票要动的 1–2 个接缝（`docs/architecture.md`）。口令：「做完这张票，我开新会话。」
- **谈完立刻落盘**：每次谈定一件事，当场落盘，不要隔夜。口令：「这条定下来了吗？定下来现在就写进台账。」
- **两次不收敛就上移一层**：同一件事两次没做完，停手回上一层——重切票 / 补需求 / 做原型，而不是「再试一次」。第 6 步的强化线：同一个 bug 三轮不收敛（只有「改了代码去跑回路」算一轮）→ 写一条 ADR 记下现状与代价，另开一张「重新设计 X」的票。

**落盘落点**（术语 / 决议 / ADR / 架构这四处的分工见 `docs/agents/domain.md`）

- 术语 → `CONTEXT.md`（三列：术语 / 一句话定义 / 别叫它）。同一个词改一个，全套技能都要跟着改。
- 决议 → `docs/decisions.md`，**必须带编号**（`D-nn`），编号永不复用，删掉的划掉保留。类型只有三种：约束 / 默认 / 待定（「待定」必须带期限）。
- 架构性决策 → `docs/adr/NNNN-*.md`（难逆转 + 脱离上下文会费解 + 真实权衡，三条同时满足才写；0 条也正常，但要明写「本步无 ADR」）。
- 票据 → 落点写在 `docs/agents/issue-tracker.md`。本仓库是**本地 markdown 模式**：一票一文件、从 `01` 编号、头部六行照 `templates/ticket.md`、评论只追加到文件底部的 `## Comments`。当前 feature 是 `engineering-v0.1.0`，票据在 `.scratch/engineering-v0.1.0/issues/`。
- 交接文档 → 系统临时目录，**不进仓库**（`D-09`）：它是一次性输入，且可能带敏感信息。

**改技能后必跑的两条校验命令**（都退出码 0 才算改完；CI 跑的是同一套，见 `.github/workflows/ci.yml`）

```bash
python tools/validate_skills.py                            # 技能契约：frontmatter / 八节骨架 / 判据条数 / 交叉引用 / 模板存在性
python tools/check_project.py --dir . --level L2 --quiet    # 结构判据：28 项，只列没过的
```

改技能正文时四条硬规矩（违反即缺陷）：八节骨架标题不改名、不合并、不调序（`D-02`）；每条完成判据可检查、每份至少 4 条 `- [ ]`（`D-03`）；正文里的 `` `技能名` `` 只能是本集这 14 个，提到外部技能必须同时给出手工兜底路径（`D-01`）；新技能至少被一个已有技能引用。完整编写契约在 `.scratch/skill-contract.md`，基准样板是 `skills/decision-ledger/SKILL.md`。

## 权限边界

**可以做的**

- 读代码、文档、票据、台账、命令输出。
- 写代码、写文档、写测试——范围限于当前票据说的那件事。
- 跑测试与校验器：`python -m unittest discover -s tests`、`python tools/validate_skills.py`、`python tools/check_project.py --dir . --level L2 --quiet`。
- 跑只读的 git 命令：`status` / `diff` / `log` / `show` / `tag`（只看）。
- 把 `Verify:` 的输出贴进票据的 `## Comments`，更新票据头 `Status` / `Rounds` / `Sessions`。

**不可以做的**（要人来做，或要明确授权）

- **碰密钥与生产凭据**：不读、不打印、不猜 `.env`、`*.pem`、`*.key`、`credentials.json` 的值，不把它们写进提交、日志、PR 或交接文档。密钥一旦进过历史，按已泄露处理——先轮换，由人决定要不要重写历史。
- **force push / 重写历史 / 删数据**：不 `git push --force`，不 `rebase` / `filter-branch` / `reset --hard` 已经推出去的提交，不删分支，不删文件、目录或 `.scratch/` 里的记录。
- **发版与改变公开状态**：不打 tag、不触发发布流水线、不发 release、不接或更换远端、不改分支保护、不改仓库可见性（尤其**不能把仓库转公开**）、不改仓库元信息。
- **改许可证**：不动 `LICENSE` 与 `pyproject.toml` 的 `license` 字段，也不动 `docs/agents/brief.md` 里的许可证决定（MIT）。
- **替你签字**：法务判断、隐私声明、对外承诺、给别人的安全承诺，一律不由代理代写、代发、代答。

越界的事写成一条「要人做」的请求，放进票据 `## Comments` 或交接文档，由人执行。**不要自己代劳，也不要换个说法绕过去。**

**未经明确许可不得开始实现。** 给了方向不等于给了许可：先一句话复述「做完之后谁能做什么」，拿到确认再动手（`build-ticket` 第 2 步）；复述与「要什么」对不上就停手，先回 `grill-with-ledger`。
