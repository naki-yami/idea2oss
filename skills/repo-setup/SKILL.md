---
name: repo-setup
description: 每个仓库跑一次的一次性配置——定 issue tracker 落点、定 triage 标签、定领域文档布局，往 `AGENTS.md` 插「## Agent skills」索引，并锁住技能集版本。当仓库刚能提交、准备写 spec 或拆票，或换了 tracker、升级技能集时使用。keywords: repo setup, one-time config, issue tracker, triage labels, AGENTS.md
whenToUse: 第 1 步之后、第 2 步之前，每个仓库一次；换 tracker、升级技能集、克隆了没配过的仓库时重跑对应节。
---

# 每仓库一次的一次性配置

> 对应手册第 2 章（二）（三）（四）｜ 产出物：`docs/agents/issue-tracker.md`、`docs/agents/triage-labels.md`、`docs/agents/domain.md` + `AGENTS.md` 的「## Agent skills」段 + 版本锁定行 ｜ 完成判据：tracker、triage 标签、领域文档布局三件事都有落点，技能集版本已锁

## 何时用 / 何时不用

**用**：每个仓库跑一次，位置在第 1 步（`repo-bootstrap`）之后、第 2 步（`grill-with-ledger`）之前。跳过它的代价很直接：写 spec、拆票、分类 issue 时不知道往哪写，工具跑到一半会让你先回去配置。

还有三种情况要重跑对应节：换了 issue tracker 平台（重跑 A 节）；升级了技能集（重跑第 7 步，并复核手册第二章与第十五章）；克隆了一个没配过的仓库（`docs/agents/` 不存在）。

**不用**：不要每个 feature 跑一次——这是每仓库一次，不是每需求一次。单个 feature 的规格与票据属于第 3、4 步，不在这里定。目录还不是 git 仓库时先走 `repo-bootstrap`，否则只能退到本地 markdown 模式。

**为什么需要它**：它是这条流水线的地基。三个落点定不下来，后面每一步的产物都无处安放；而它本身不做任何设计判断，只是把「记在哪」写死，让下一个会话不用猜。

## 输入（开工前必须到手的）

1. 一个已经 `git init` 过的仓库（没有 → 先 `repo-bootstrap`）。
2. 四条探查命令的输出（见「动作」第 1 步）——先看，再问。
3. `git --version`、`gh --version`、`glab --version` 有没有。
4. triage（外部技能/工具）装没装——它决定 B 节跑不跑。
5. 平台现有标签词：例如已经有人用 `bug:triage` 表示「待评估」。
6. 技能集的实际版本号（默认实现是 mattpocock/skills v1.2.3，MIT，2026-08-06 发布）。

## 动作

1. **探查**（先跑这四条，不要跳过探查直接问用户）：

   ```
   git remote -v                          # 是不是 GitHub / GitLab 仓库
   ls AGENTS.md CLAUDE.md CONTEXT.md 2>/dev/null
   ls -d docs/adr docs/agents .scratch 2>/dev/null
   ls pnpm-workspace.yaml 2>/dev/null     # monorepo 信号
   ```

   判读：有 GitHub remote → A 节默认 GitHub；有 monorepo 信号 → C 节要问是不是多上下文；`AGENTS.md` 与 `CLAUDE.md` 两份都在 → 先合并成一份，另一份留一行指针。

2. **先汇报，再一次只问一节**：A → B → C，每节给出默认建议，确认之后才写文件。它是提示驱动的流程，不是确定性脚本——一口气问完三节，用户答的往往是默认值的糊弄版。

3. **A 节：定 issue tracker 落点**。

   | 模式 | 落点 | 前提 | 什么时候选 |
   |---|---|---|---|
   | GitHub | 仓库的 GitHub Issues | 装了 `gh` 并登录 | 打算开源、要别人来提 issue |
   | GitLab | 仓库的 GitLab Issues | 装了 `glab` 并登录 | 团队用 GitLab |
   | 本地 markdown | 仓库里的 `.scratch/<feature>/` | 无，任何环境都能跑 | 单人开发、离线、不想被平台绑住（默认推荐） |

   默认建议：有 GitHub remote 就 GitHub，否则本地 markdown。**这不是可选项**——第 3、4 步要把东西发出去，得先有落点；没装 `gh` 不等于可以跳过规格与拆票。写进 `docs/agents/issue-tracker.md`（照 `templates/issue-tracker.md`）。

4. **B 节：定 triage 标签**（只有装了 triage 这个外部技能才问这一节；没装就整节跳过，见「手工兜底」）。五个标签，标签名等于它的角色名：

   | 标签 | 含义 |
   |---|---|
   | needs-triage | 待维护者评估 |
   | needs-info | 等报告者补信息 |
   | ready-for-agent | 规格完整，可交给无人值守的智能体 |
   | ready-for-human | 需要人工实现 |
   | wontfix | 不处理 |

   映射冲突：如果你的 tracker 已经在用别的词（例如 `bug:triage` 对应 `needs-triage`），**就在这一步改掉映射**，否则 triage 会重复创建标签、状态机自己跟自己打架。映射表写进 `docs/agents/triage-labels.md`（照 `templates/triage-labels.md`）。

   一个已知坑一并写进这份文件：spec 会被打上 `ready-for-agent`，按标签轮询的无人值守代理可能整份实现而不是捡票据切片——拆票跑完后把标签摘掉，或在代理提示词里明确排除父级文档。

5. **C 节：定领域文档布局**（默认单上下文）。单上下文＝根目录一份 `CONTEXT.md` + `docs/adr/` + 决议台账 `docs/decisions.md`。写进 `docs/agents/domain.md`（照 `templates/domain.md`），并把三条界限写清楚：
   - `CONTEXT.md` 只是**词汇表**，不是规格；
   - 多数决议不够格写 ADR——它们进台账（带编号、带证据）；
   - ADR 的门槛是三条同时满足：难逆转 + 脱离上下文会费解 + 有真实权衡。

6. **往 `AGENTS.md` 或 `CLAUDE.md` 插一段「## Agent skills」**。这一段是索引：哪个环节、用什么、干什么（骨架见 `templates/AGENTS.md.tpl`，复制到项目根时**改名为 `AGENTS.md`**——带 `.tpl` 后缀是为了不让模板本身被运行时当成生效的指令文件）。两份文件只留一份生效，另一份要么不存在，要么只有一行指针指向它——别让两份内容分叉。

7. **锁技能集版本**：把版本号写进 `README.md` 或 `docs/agents/` 下的一份短文件。

   - 升级**认 tag，不跟 main 走**：main 上随时在删技能、加技能，而技能名会直接进入代理读到的提示词，改名就改行为。
   - 升级后复核两处并重跑一次第 2 步做演练：手册**第二章**（技能表与改名对照）与**第十五章**（已知缺陷与规避手段）——那两处描述的是实现细节，最先过期。
   - 换环境前查一遍：原仓库用 `disable-model-invocation: true` 把一批技能锁成「只能手动触发」，这个字段换到不认它的环境里会被**静默忽略**，代理可能自己触发它们。碍事就把那一行删掉，或在代理配置里显式禁止。

8. **本地 markdown 模式的目录规矩**（选了这一模式才做）：

   ```
   .scratch/<feature-slug>/
   ├── brief.md                 # 第 0 步：立项（五句话）
   ├── spec.md                  # 第 3 步：产品设计文档
   └── issues/
       ├── 01-first-ticket.md   # 一票一文件，从 01 编号
       └── 02-second-ticket.md
   ```

   票据头按 `templates/ticket.md` 的六行照写（`Status` / `Blocked by` / `Covers` / `Verify` / `Rounds` / `Sessions`）；**评论与历史追加到文件底部的「## Comments」标题下，不要写进头部**——头部是机器读的，底部是人和历史。这条约定写进 `docs/agents/issue-tracker.md`。

## 产出物

- `docs/agents/issue-tracker.md`——tracker 模式与落点（模板 `templates/issue-tracker.md`）。
- `docs/agents/triage-labels.md`——五个标签、映射冲突表；未启用则写明原因（模板 `templates/triage-labels.md`）。
- `docs/agents/domain.md`——`CONTEXT.md` / `docs/adr/` / 台账三者的界限（模板 `templates/domain.md`）。
- `AGENTS.md`（或 `CLAUDE.md`）里的「## Agent skills」段。
- 一行版本锁定：`技能集：<名字> <版本>（来源，发布日）`。

## 完成判据

- [ ] 四条探查命令都真跑过，输出看过了（不是跳过探查直接发问）。
- [ ] `docs/agents/` 下三份文件都在，且每份里的 TODO 都填完了（没有留着空模板的文件）。
- [ ] `AGENTS.md` 与 `CLAUDE.md` 只留一份生效；另一份要么不存在，要么只有一行指针。
- [ ] `AGENTS.md` 里有「## Agent skills」段，能指到具体那几行。
- [ ] `docs/agents/issue-tracker.md` 里写明了模式，且第 3、4 步的产物有确定落点。
- [ ] 启用 triage：五个标签与平台现有标签的映射写在同一份文件里；未启用：文件里明确写了「本仓库不启用 triage 标签」。
- [ ] `docs/agents/domain.md` 写清了 `CONTEXT.md` / `docs/adr/` / 台账的界限，并写清台账放在哪一处。
- [ ] 技能集版本已写进 `README.md` 或 `docs/agents/`，并注明「升级认 tag，不跟 main」。
- [ ] 若用本地 markdown 模式：`.scratch/<feature>/issues/` 目录在，票据头六行与「## Comments」约定写进了 `issue-tracker.md`。

## 手工兜底

- 没装 setup 类技能（外部技能，如 `setup-matt-pocock-skills`；装了就用它）：**本技能本身就是手工路径**。照 `templates/issue-tracker.md`、`templates/triage-labels.md`、`templates/domain.md` 各抄一份，十分钟能抄完，判据一条都不用改。
- triage（外部技能）没装：**B 节整节跳过**，并在 `triage-labels.md` 里写明「本仓库不启用 triage 标签，issue 靠人工看」。不要为了凑齐文件而编一套没人执行的标签。
- 当前目录不是 git 仓库：只能选本地 markdown 模式（仓库类型靠 `git remote -v` 判断）。这正说明第 1 步该排在它前面——先 `repo-bootstrap`，再回来。
- 平台已有自己的标签体系：不要新建同名标签，直接写映射表。宁可少几个标签，也不要两套词并存。
- 团队只有 GitLab 但没装 `glab`：走本地 markdown，别手工去网页上开 issue——那种落点会分叉，spec 与票据两边各一份。
- 完全没有代理：这三份文件本来就是给人读的，手工写完后写进 `AGENTS.md` 一段索引即可。

## 下一步

→ 调用 `grill-with-ledger`（配置的目的，是让第 2 步谈定的东西有地方落盘）。

## 反模式

| 反模式 | 为什么错 | 改成 |
|---|---|---|
| 每个 feature 跑一次配置 | 三份文件被反复改写，落点开始分叉 | 每仓库一次；配置本身变了才重跑 |
| triage 没装还硬做 B 节 | 生成没人执行、没人维护的标签文件，下一个人照着它找活 | 整节跳过并写明原因，先装 triage 再回来 |
| 一口气把 A/B/C 三节问完 | 用户在没有上下文的情况下连答三题，答案糊弄 | 一次一节，给默认建议，确认后再写 |
| 只记「用 GitHub」不记映射 | 标签被重复创建，issue 状态机自相矛盾 | 映射冲突表当场写进 `triage-labels.md` |
| `AGENTS.md` 与 `CLAUDE.md` 两份都维护 | 内容必然分叉，代理读到哪份看运气 | 只留一份，另一份一行指针 |
| 技能集不锁版本、跟着 main 升 | 技能改名或删除会静默改变代理行为，手册里的规避手段过期 | 认 tag 升级；升完复核第二章与第十五章 |
| 本地模式把评论写进票据头部 | 头部是机器读的字段，混进历史后无法解析 | 评论一律追加到底部「## Comments」 |
