<!-- idea2oss ｜ 手册 第 8 步判据「陌生人 30 分钟测试」的操作版 ｜ 卡住即说明结构缺件 -->

<!-- 第 8 步 ｜ 判据：陌生人 30 分钟测试的操作版；卡住即说明结构缺件 ｜ 结构不要改，改内容 -->
# 接手者 30 分钟路径

<!-- 第 8 步判据「陌生人 30 分钟测试」的操作版：别人只读 README，能在干净环境里装起来、
     跑通一次、并知道要参与该改哪个文件。每一步卡住，就是结构缺了那一件。 -->

你是第一次打开 idea2oss 的人。**照这张表走 30 分钟，不要先通读任何文档。**
每一格都写了两件事：读哪个文件、卡住说明缺哪件。第三列里「卡住 → 缺」的那一件，就是这一格对应的结构缺了什么。

| 分钟 | 做什么 | 读哪个文件 ｜ 卡住说明缺哪件 |
|---|---|---|
| 0–3 | 知道这是什么、给谁用 | 读 `README.md` 第 1–7 行（一句话定位 + 给谁用）+「限制与不做什么」一节<br>**卡住 → 缺门面**：README 说不出「给谁用」和「不做什么」；两者的原始出处是 `docs/agents/brief.md` 的五句话 |
| 3–6 | 跑通一次，看到预期输出 | 读 `README.md` 的「30 秒上手」与「结构体检：把判据变成命令」两节；跑三条：`python tools/install.py --dry-run`（只打印不写盘）、`python tools/validate_skills.py`（应出现「技能数：14」「结果：0 个错误，0 个警告」）、`python -m unittest discover -s tests`（应出现 `Ran … OK`）<br>**卡住 → 缺跑通路径**：README 的三条命令在你机器上跑不出预期输出（第 8 步判据：陌生人 30 分钟测试要求「干净目录、只读 README、三条命令跑通」） |
| 6–10 | 学会项目黑话 | 读 `CONTEXT.md`——20 条术语，每条三列：术语 / 一句话定义 / 别叫它。「票据、台账、接缝、判据、兜底路径、frontier」都在这儿定死<br>**卡住 → 缺共享语言**：术语没进 `CONTEXT.md`，或同一件事有两个叫法（对照 `templates/CONTEXT.md` 的三列） |
| 10–14 | 知道模块边界与公共接缝 | 读 `docs/architecture.md`——5 个模块（`skills/`、`templates/`、`tools/`、`docs/`、`.scratch/`）+ 接缝 `S1`–`S5` + 数据流<br>**卡住 → 缺接缝清单**：新东西没写成「名字 / 通过它的是什么 / 谁调用它」三字段的一行；测试也就没地方挂 |
| 14–18 | 知道「为什么不是另一种做法」 | 读 `docs/adr/` 的三份 ADR（`0001` 并列式技能集、`0002` 中文正文加英文关键词、`0003` 判据做成体检器）+ `docs/decisions.md` 的 `D-01`…`D-12`（类型只有约束 / 默认 / 待定三种）；四处落点怎么分工见 `docs/agents/domain.md`<br>**卡住 → 缺落盘**：谈定的决议没编号、证据栏空着，或够格写 ADR 的决策只留在对话里 |
| 18–22 | 知道下一步该干什么 | 读 `.scratch/engineering-v0.1.0/issues/`——6 张票，头部按六行头写（本仓库的票已追加 `Accept:` 与 `Review:`）；能立刻开工的（frontier）是 `03-ci-blocks-merge.md` 与 `04-stranger-30-minutes.md`（`Blocked by: -`），`06-first-release.md` 被 03 挡着。落点规则与「当前状态」表在 `docs/agents/issue-tracker.md`<br>**卡住 → 缺 frontier**：票据图里没有一张 `Blocked by: -` 且 `Status: todo` 的票（为空说明依赖成环，或票切大了）；规格与「范围之外」在 `.scratch/engineering-v0.1.0/spec.md` |
| 22–26 | 知道怎么提改动、多久有人回 | 读 `CONTRIBUTING.md`（环境、三条必跑命令、改技能的四条规矩、PR 期望、响应节奏）与 `SECURITY.md`（私密报告渠道、7 天 / 30 天两个时限）<br>**卡住 → 缺贡献入口**：这两件有一件不在，别人就只能靠猜；`CODE_OF_CONDUCT.md` 回答的是「这里怎么待人」 |
| 26–30 | 改一行 → 提 PR → 看 CI 跑 | 挑一件最小的：改 `CONTEXT.md` 里一条术语的「别叫它」，或改 `skills/<技能名>/SKILL.md` 里一条判据。本地先跑 `python tools/validate_skills.py` 与 `python tools/check_project.py --dir . --level L2 --quiet`，再按 `.github/PULL_REQUEST_TEMPLATE.md` 的四问写 PR 正文；CI 在 `.github/workflows/ci.yml`，PR 上自动跑同一套命令<br>**卡住 → 缺门禁或缺版本纪律**：CI 红了 PR 还能合并，说明平台上的分支保护没配（这一下只能由仓库所有者亲手做，票据 `03-ci-blocks-merge.md` 记着）；`CHANGELOG.md` 的 `[Unreleased]` 里也没有对应段落 |

30 分钟后你应该能答：它是什么 / 怎么跑 / 下一步该做什么 / 怎么把改动提进来。
答不上来 —— 开一个 issue，说明卡在哪一步（落点见下面「卡住就开 issue」）。

## 交接包五文件定律

把活交给别人、或交给下一个会话时，**只给这五个路径，不抄内容**（这是第 7 步 `session-handoff` 的规矩，交接文档本身写到系统临时目录，不进仓库）：

| # | 文件 | 它回答什么 |
|---|---|---|
| 1 | `README.md` | 这是什么、给谁用、怎么跑 |
| 2 | `CONTEXT.md` | 我们管它叫什么——术语对不上，后面全拧 |
| 3 | `docs/architecture.md` | 模块边界与接缝 `S1`–`S5`：改哪里不动哪里 |
| 4 | `docs/decisions.md` | 已经定了什么——编号 `D-nn` 与证据 |
| 5 | 当前 feature 的票据 `.scratch/engineering-v0.1.0/issues/` | 这一次要做的垂直切片：六行头 + `Covers: D-nn`；一张票一个文件，从 `01` 编号 |

缺一件就是缺一件：缺 2 会重新吵一遍术语，缺 3 会新造接缝，缺 4 会把谈定的决议再做一遍，缺 5 会顺手做下一张票。
本仓库五件都在；最容易松掉的是第 5 件——票做完要手工改成 `Status: done` 并写上验证指针，别让 frontier 自己变干净（已知缺陷见 `docs/agents/triage-labels.md`）。

## 卡住就开 issue：写在哪、写什么

- **写在哪**：本仓库还没接远端（`git remote -v` 为空），平台的 issues 页暂时不存在。两个当下可用的落点——给自己的活开一张票，写进 `.scratch/<feature>/issues/NN-*.md`（六行头照 `templates/ticket.md`）；想按外部报告者的格式写，用 `.github/ISSUE_TEMPLATE/bug.md` 的字段（复现步骤 / 期望行为 / 实际行为 / 版本与环境），或照 `templates/issue-bug.md` 抄。
- **写什么**：卡在第几分钟、读了哪个文件、缺的是哪一件（直接抄上面表格里「卡住 → 缺」的那半句）。
- **别写什么**：不要在公开 issue 里贴密钥、生产凭据或真实用户数据，换成 `<REDACTED>`；安全问题走 `SECURITY.md` 的私密渠道。

**这张表本身就是判据**：任何一格让人卡住超过 5 分钟，缺的是仓库里的某一件东西，不是来的人不够聪明。
