<!-- idea2oss · oss-launch 参考件 ｜ 手册 8.3 + 附录 B1/B2 ｜ SKILL.md 引用本文件，不要在两处重复维护 -->

# 社区文件：完整表与最小内容

| 文件 | 回答什么问题 | 最小内容 | 模板 |
|---|---|---|---|
| `README.md` | 这值不值得我看下去 | 七段：一句话定位 / 为什么用它 / 30 秒上手（三条命令以内）/ 用法示例 / 限制与不做什么 / 现状与路线 / 许可与贡献入口 | `templates/readme.md` |
| `LICENSE` | 我能怎么用它 | 选定许可证的全文（不是链接、不是一句话） | `templates/license-todo.txt` |
| `CONTRIBUTING.md` | 我怎么参与 | 开发环境怎么起、跑测试的命令、提交规范、PR 期望（多久回、要不要先开 issue） | `templates/contributing.md` |
| `CODE_OF_CONDUCT.md` | 这里怎么待人 | 直接用 Contributor Covenant，填上联系方式 | `templates/code-of-conduct.md` |
| `SECURITY.md` | 有漏洞跟谁说 | 私密报告渠道、响应时限、不要公开 issue 贴漏洞 | `templates/security.md` |
| `.github/ISSUE_TEMPLATE/*.md` | 怎么提问题 | bug 要复现步骤、版本、环境；feature 要场景、替代方案 | `templates/issue-bug.md` / `templates/issue-feature.md` |
| `.github/PULL_REQUEST_TEMPLATE.md` | PR 该写什么 | 改了什么 / 为什么 / 怎么验证 / 风险与回滚 | `templates/pr.md` |
| `CODEOWNERS` | 谁必须看一眼 | 维护者与其负责的目录 | `templates/CODEOWNERS` |
| 标签体系 | 我怎么找活干 | `good first issue`、`help wanted`、`bug`、`enhancement` | `templates/triage-labels.md` |

## 先做哪三件

**LICENSE、README、SECURITY 必须先有。** 没许可证的仓库别人连用都不敢用；没有 README 的仓库对陌生人等于不存在；没有 SECURITY 的仓库，发现漏洞的人只能在公开 issue 里贴出来。

其余可以晚一点补，顺序建议：CONTRIBUTING → PR 模板 → issue 模板 → 标签 → CODEOWNERS → CODE_OF_CONDUCT。

## 逐件的落地要点

### README

- 七段齐全，顺序不要改；「30 秒上手」**三条命令以内**，且你在干净目录里亲手跑过。
- 「为什么用它」写取舍差别，不写"更快更强"。
- 「限制与不做什么」写清楚——它能挡掉一半无效 issue。
- 徽章只挂你真的在维护的：CI 状态、最新版本、许可证。挂着红的 CI 徽章比不挂更伤。
- 末尾的「许可与贡献」要有三个入口：LICENSE 链接、CONTRIBUTING 链接、issue 入口。
- 文档地图（README 模板最后一段）把术语表、架构、决策、运行手册、票据 frontier 都指向路径——30 分钟测试的第 6–22 分钟全靠它。

### 三处许可证一致

| 要做的 | 落地位置 | 自检 |
|---|---|---|
| 放全文 | 仓库根目录 `LICENSE` | 平台能识别出许可证名称，而不是 "Unknown" |
| 写元数据 | `package.json` / `pyproject.toml` / `Cargo.toml` 的 `license` 字段 | 与 LICENSE 一致，且是标准 SPDX 标识 |
| 写进文档 | README 的许可段落 | 三处说法完全一致，没有 "MIT OR Apache" 这种含糊话 |

### CONTRIBUTING

- 从克隆到能跑测试的命令，和 CI 用的是同一套（不一致就是给贡献者挖坑）。
- 提交规范写"为什么"、不写"改了什么"（改了什么看 diff 更准）；一票一提交或一票一分支。
- PR 期望写清：多久会有人回、要不要先开 issue、CI 必须通过才会合并。
- 有一节「当前没有的东西（诚实说明）」：例如暂时没有自动发布、测试覆盖还不全。

### SECURITY

- 私密报告渠道（邮箱或平台的私密报告入口），并明确"不要在公开 issue 里贴漏洞细节"。
- 两个时限：确认收到、修复或给出说明。
- 支持范围表：哪个版本会修安全问题。

### 标签体系

四个基础标签就够起步：`good first issue`（第一次参与的人能做的）、`help wanted`（欢迎外部帮）、`bug`、`enhancement`。

如果平台在跑五态分类机，另有一套角色标签（`needs-triage` / `needs-info` / `ready-for-agent` / `ready-for-human` / `wontfix`），映射关系写在 `templates/triage-labels.md` 里，注意别和平台已有的标签名冲突。

**已知坑**：`ready-for-agent` 标签会让无人值守代理整份实现文档而不是捡票据切片——拆票跑完后把它摘掉，或在代理提示词里排除父级文档。

## 手工兜底

- 没有平台模板功能：把这些文件直接放在仓库里（`SECURITY.md` 等平台也能识别根目录文件），或写成 `docs/` 下的文档并在 README 里链接。
- 只有一个人维护：CODE_OF_CONDUCT 可以先用 Contributor Covenant 原文，只改联系方式；CODEOWNERS 可以只有一行（你自己 + `*`）。
- 一个文件都不想多写：至少写 README + LICENSE + SECURITY，把其余内容塞进 README 的一个「怎么参与」小节，并在里面说明"其他社区文件还没补"。
