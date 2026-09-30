# idea2oss

把《从想法到开源 · AI 结对开发流程手册 V3》的**九步法**做成一套可独立使用的技能集：立项 → 初始化仓库 → 拷问 → 产品设计文档 → 技术方案与计划 → 实行 → 检测 → 交付 → 开源发布与运营。

给**用 AI 智能体写代码、并打算把成果交给别人用**的人。核心不是"让代理更聪明"，而是让每一步的产出物都落在一个具体文件上、每一条"做完了"都能被检查、被拒收。

> **流程是判据，技能是加速器。** 不装任何别的技能集也能走完全流程——每个技能都自带「手工兜底」路径。

## 为什么用它

| 与同类技能集的差别 | 说明 |
|---|---|
| 两头是齐的 | 大多数技能集从"已经有需求"开始；这套补上了第 0 步（这件事值不值得做、许可证先定）和第 8 步（开源发布与运营，判据是**陌生人 30 分钟测试**） |
| 每步都有完成判据 | 不是"做什么"，而是"做到什么程度算完、怎么查、查不过怎么拒收" |
| 有决议台账 | 给每条谈定的决议加编号，spec / 票据 / 验收逐条回指，用**决议追溯率**发现"决议在传递中被压弱" |
| 不绑死技能 | 流程与实现解耦：技能改名、失效、换环境，照着兜底路径手工走完，判据一样成立 |
| 可剪裁 | L0 一次性 / L1 常规功能 / L2 正式工程三档，明确"哪几步可以跳、哪一步不能省" |

## 30 秒上手

```bash
# 1. 装到「你正在开发的项目」里（技能会落到 <项目>\.dsh\skills\）
python tools/install.py --target "D:\projects\我的项目"

# 开发这套技能本身时才用 --link（目录联接，改源码立即生效，不用重装）
python tools/install.py --link --target "D:\projects\我的项目"

# 2. 新开一个会话（技能目录在会话启动时扫描）

# 3. 直接说事，或点名调用
> 我想做一个把 Markdown 转成公众号排版的工具，帮我立项
> /idea2oss 这活该走几步？
> 这个 bug 修了两次还没好
```

不带 `--target` 时装到**当前目录**；`python tools/install.py --list` 看装了哪些。（别把它装进 clone 下来的仓库里——那只会让这个仓库多一个没人用的目录。）

## 技能表

| 技能 | 对应 | 干什么 |
|---|---|---|
| `idea2oss` | 入口 | 判你这活走几步（L0/L1/L2），告诉你下一步该调哪个技能 |
| `project-brief` | 第 0 步 | 五句话立项 + 最小可验证切片 + 许可证先定 |
| `repo-bootstrap` | 第 1 步 | git init、四类边界 `.gitignore`、密钥检查、三个落点目录 |
| `repo-setup` | 每仓库一次 | issue tracker 落点、triage 标签、领域文档布局、AGENTS.md 索引 |
| `grill-with-ledger` | 第 2 步 | 轮到它问你：一轮问题一轮答案，谈定就落盘 |
| `decision-ledger` | 第 2→6 步 | 决议台账：编号 / 类型 / 精确到可验证的决议 / 证据，全程回指 |
| `write-spec` | 第 3 步 | 七段产品设计文档，每条决议带 `[D-nn]` 回指 |
| `ticket-plan` | 第 4 步 | 接缝清单 + 垂直切片 + 票据六行头 + 非空的 frontier |
| `build-ticket` | 第 5 步 | 只喂三样、测试先红后绿、一票一提交 |
| `dual-axis-review` | 第 6 步 | 标准轴 + 规格轴；产品验收必须你亲手跑 |
| `bug-diagnosis` | 第 6 步（出错时） | 六步诊断顺序 + 三轮不收敛的止损线 |
| `session-handoff` | 第 7 步 | 提交前检查、PR 四问、交接文档（只给路径不抄内容） |
| `oss-launch` | 第 8 步 | 法务与安全闸门、门面、社区文件、CI、版本与日志、运营 |
| `flow-tuning` | 全程 | 六个指标、三条硬规则（含"不要采信自报数据"）、反模式清单 |

## 文档地图

| 想知道什么 | 看哪里 |
|---|---|
| 这是什么、怎么装 | 本文件 |
| 怎么用、出问题怎么办、三条完整走法 | [GUIDE.md](GUIDE.md) |
| 接手这个仓库该按什么顺序读 | [docs/onboarding.md](docs/onboarding.md) |
| 某个技能到底干什么 | `skills/<name>/SKILL.md` |
| 黑话是什么意思 | [CONTEXT.md](CONTEXT.md) |
| 模块边界与接缝（S1–S6） | [docs/architecture.md](docs/architecture.md) |
| 为什么当初这么定 | [docs/decisions.md](docs/decisions.md) + [docs/adr/](docs/adr/) |
| 这个项目为谁做、什么条件下放弃 | [docs/agents/brief.md](docs/agents/brief.md) |
| 下一步要做什么 | [.scratch/engineering-v0.1.0/issues/](.scratch/engineering-v0.1.0/issues/) |
| 怎么参与 | [CONTRIBUTING.md](CONTRIBUTING.md) |
| 改了什么 | [CHANGELOG.md](CHANGELOG.md) |

## 结构体检：把判据变成命令

技能提出判据，但**不会自己去执行**。要让它变成保证，用体检器：

```bash
python tools/check_project.py --dir <项目>          # 对照完整结构清单，逐项给证据与修复建议
python tools/check_project.py --dir . --level L1    # 按档位放宽（L0 只查 4 项）
python tools/check_project.py --dir . --quiet       # 只看没过的
python tools/check_project.py --dir . --json        # 给 CI 用
```

它检查 28 项：README 成段、`.gitignore` 四类边界、LICENSE 三处一致、`CONTEXT.md` 非空、台账四列、票据六行头、**frontier 非空**、**决议覆盖率**、接缝清单、CI、密钥、交接文档没进仓库……有强制项未通过时退出码为 1——可以直接当第 6 / 8 步的 `Verify:` 命令或 CI 门禁。

**它查不了的**（这部分只能人来）：测试是不是真挂在接缝上、文档是不是你要的、产品验收、陌生人 30 分钟测试、CI 是否真的挡住了合并。

## 目录结构

```
idea2oss/
├── README.md              门面（本文件）
├── GUIDE.md               介绍与使用手册（装、用、三条走法、排错、定制）
├── CONTEXT.md             术语表（唯一权威）
├── CHANGELOG.md           Keep a Changelog（此刻还没有 release，内容都在 Unreleased）
├── CONTRIBUTING.md        怎么参与
├── SECURITY.md            漏洞私密报告渠道与响应时限
├── CODE_OF_CONDUCT.md     Contributor Covenant v2.1
├── AGENTS.md              代理入口：技能索引 + 三条铁律口令 + 权限边界
├── LICENSE                MIT
├── pyproject.toml         包元数据（license = MIT，零第三方依赖）
├── .gitattributes         仓库统一 LF
├── skills/<name>/SKILL.md 14 个技能，每个都能独立使用
├── templates/             35 份模板与索引
├── docs/                  知识层（接手者从这里进）
│   ├── onboarding.md      30 分钟接手路径
│   ├── architecture.md    模块与接缝清单 S1–S6
│   ├── decisions.md       决议台账 D-01…D-13
│   ├── adr/               0001–0003 三条架构决策
│   └── agents/            brief / issue-tracker / triage-labels / domain
├── .scratch/              过程层
│   ├── skill-contract.md  技能编写契约
│   └── engineering-v0.1.0/  本次的 spec 与票据图
├── tests/                 挂在 S1 / S2 / S3 三个接缝上的 unittest
├── tools/                 五个命令行入口（install / validate / check / licenses / dump）
└── .github/               CI、release、PR 与 issue 模板、CODEOWNERS、dependabot
```

## 兼容性

技能采用通用的 Agent Skills 格式（`SKILL.md` + YAML frontmatter：`name` / `description` / `whenToUse`）。装到别的运行时里，把 `skills/<name>/` 整个目录拷进它的技能目录即可；不支持 `whenToUse` 的运行时忽略该字段即可正常工作。

如果你已经装了同类技能（例如拷问、TDD、代码评审、调研），每个技能会告诉你"优先用哪个"，没有也能按内置的手工路径走完。

## 限制与不做什么

- **不是又一个提示词集合。** 技能只写判据和动作，不写"你是一位资深工程师"这类角色扮演。它管流程，不管你的技术栈。
- **不替你选技术栈、不替你选许可证、不替你签字。** 法务判断、隐私声明、对外承诺这三类必须人来做。
- **不保证代理会自动触发。** 描述里做了中英双语关键词，但复杂流程建议点名调用。
- **不保证项目自动合规。** 技能只提出判据，真正拦住你的是 `tools/check_project.py` 与 CI——判据不落成命令，就只是纸面话术。
- **判据不能省。** 文档可以降级成随手记，判据不行——这是整套东西唯一不能省的部分。

## 现状与路线

- 现状：**v0.1.0**（已打 tag）。技能集九步全覆盖、可独立使用；仓库自身是按本集流程走完的一个完整项目——第 0–8 步的产物在 `docs/` 与 `.scratch/engineering-v0.1.0/`，结构体检 28/28。
- 自评口径：`python tools/check_project.py --dir . --quiet`。分数与验收记录写在票据里，不写在这里——README 里的数字会过期。
- 还没做完的一件（记在票据里，不藏着）：**真人陌生人测试**没做过（票据 `04`）——这条代理顶替不了。CI 已在 PR 上验证过、分支保护已配、其余检查见 [docs/release-checklist.md](docs/release-checklist.md)。
- 路线：`D-11` 决定英文版正文做不做（期限 v0.2.0）；正文里的「手册第 N 步」随源手册版本走。

## 致谢

本项目的**技能组织方式**与若干工作流方法，参考了 [mattpocock/skills](https://github.com/mattpocock/skills)
（MIT License, Copyright (c) 2026 Matt Pocock）：一步一个技能 + 一个入口路由器 + 每仓库一次配置这个形状，
以及第 2–7 步里的做法——被拷问而不是自己憋需求、规格只合成不访谈、按用户可见行为垂直切票、
测试先红后绿、标准轴与规格轴分开评审、交接文档只给路径——都能在那一套里找到对应。

**没有复制它的代码或文本**：14 份 `SKILL.md` 是中文重写；判据、兜底路径、35 份模板、四个工具都是本项目自己的。
独立的部分是：九步骨架、第 0 步立项、第 8 步开源发布与运营、决议台账与决议追溯率、六个体检指标、三档剪裁矩阵。

对照版本：`mattpocock/skills` **v1.2.3**（MIT，已核实是最新 tag）。本项目**不依赖它**——它只是对照组；
升级认 tag，不跟 `main`（见 `docs/decisions.md` 的 `D-13`）。

## 许可与贡献

- 许可：[MIT](LICENSE)——三处必须一致：`LICENSE` 全文 / `pyproject.toml` 的 `license` 字段 / 本段落。
- 贡献：[CONTRIBUTING.md](CONTRIBUTING.md)。改技能或工具后，先过这两条命令：`python tools/validate_skills.py`、`python -m unittest discover -s tests`。
- 维护节奏：见 `CONTRIBUTING.md` 的「响应节奏」一节。
