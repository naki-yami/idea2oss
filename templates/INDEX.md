<!-- idea2oss 模板索引 ｜ 结构不要改，改内容 -->

# templates/ 索引

这些模板来自《AI 结对开发流程手册 V3》的附录 A/B。**复制过去改内容就行，不要改结构——结构本身在替你做检查。**

> 注意：本目录里 `readme.md` 是「README 七段骨架」模板（小写），不要和仓库根目录的 `README.md` 混淆；Windows 上大小写不敏感，加文件前先看这里。

| 模板 | 用在哪一步 | 谁用它 | 结构里的关键点 |
|---|---|---|---|
| `brief.md` | 第 0 步 | `project-brief` | 五句话；「不做什么」与「放弃条件」各至少一条 |
| `license-todo.txt` | 第 0 / 8 步 | `project-brief` / `oss-launch` | 许可证四选一；落地三处必须一致 |
| `gitignore.txt` | 第 1 步 | `repo-bootstrap` | 四类边界：依赖 / 构建输出 / 本机配置 / 密钥 |
| `CONTEXT.md` | 第 2 步 | `grill-with-ledger` | 术语表，非空；只放词，不放决议 |
| `ledger.md` | 第 2 步起 | `decision-ledger` | 四列：编号 / 类型 / 精确到可验证的决议 / 证据 |
| `adr.md` | 第 2 步起 | `decision-ledger` | 三门槛：难逆转 + 脱离上下文费解 + 真实权衡 |
| `spec.md` | 第 3 步 | `write-spec` | 七段；「范围之外」非空；决策句末带 `[D-nn]` |
| `ticket.md` | 第 4 步 | `ticket-plan` | 六行头 + `Accept` / `Review`；`## Comments` 在文件底部 |
| `architecture.md` | 第 4 步 | `ticket-plan` | 接缝清单：名字 / 通过它的是什么 / 谁调用 |
| `issue-tracker.md` | 每仓库一次 | `repo-setup` | GitHub / GitLab / 本地 markdown 三选一 |
| `triage-labels.md` | 每仓库一次 | `repo-setup` | 五个标签与平台现有标签的映射 |
| `domain.md` | 每仓库一次 | `repo-setup` | 术语表 / ADR / 台账三者的界限 |
| `manual-review.md` | 第 6 步 | `dual-axis-review` | 标准轴 + 规格轴；结论必须写未决项与接受人 |
| `handoff.md` | 第 7 步 | `session-handoff` | 六段；关键路径只给路径；写到系统临时目录 |
| `pr.md` | 第 7 步 | `session-handoff` | 四个问题；缺「风险与回滚」没人敢合并 |
| `readme-l0.md` | L0 档 | `idea2oss` | 三行：是什么 + 怎么跑 |
| `readme-l1.md` | L1 档 | `idea2oss` | 四段：定位 / 跑法 / 限制 / 现状 |
| `readme.md` | 第 8 步（L2） | `oss-launch` | 七段；30 秒上手 ≤3 条命令 |
| `contributing.md` | 第 8 步 | `oss-launch` | 起环境、测试命令、PR 期望、响应节奏 |
| `security.md` | 第 8 步 | `oss-launch` | 私密渠道 + 响应时限；三件必须先有的之一 |
| `code-of-conduct.md` | 第 8 步 | `oss-launch` | Contributor Covenant 全文 + 联系方式 |
| `changelog.md` | 第 8 步 | `oss-launch` | Keep a Changelog 六段；不抄 commit |
| `ci.yml` | 第 8 步 | `oss-launch` | 安装 → lint → typecheck → test → 构建 |
| `release.yml` | 第 8 步 | `oss-launch` | tag 触发；产物带哈希或签名 |
| `dependabot.yml` | 第 8 步 | `oss-launch` | 依赖升级与漏洞告警 |
| `CODEOWNERS` | 第 8 步 | `oss-launch` | 谁必须看一眼 |
| `issue-bug.md` | 第 8 步 | `oss-launch` | 复现步骤、版本、环境 |
| `issue-feature.md` | 第 8 步 | `oss-launch` | 场景、替代方案、不做的后果 |
| `onboarding.md` | 第 8 步 | `oss-launch` | 接手者 30 分钟路径（卡住 = 缺件） |
| `runbook.md` | 第 8 步 | `oss-launch` | 发布 / 回滚 / 故障处置 |
| `env.example` | 第 8 步 | `oss-launch` | 示例配置里绝不放真实凭证 |
| `editorconfig.txt` | 第 1 / 7 步 | `repo-bootstrap` / `session-handoff` | 本地与 CI 用同一套格式约定 |
| `AGENTS.md.tpl` | 每仓库一次 | `repo-setup` | 「## Agent skills」索引 + 权限边界；复制到项目根时**改名为 AGENTS.md** |
| `specs-index.md` | 第 3 步（归档） | `write-spec` | 长命规格归档，标明状态 |

> 模板里的 `{name}` / `{feature}` 是占位符，复制后替换。
> 重新生成：`python tools/dump_templates.py`（事实来源是生成器，不是本目录——改模板请改生成器再导出）。
