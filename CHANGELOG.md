# Changelog

本项目遵循[语义化版本](https://semver.org/lang/zh-CN/)，变更记录按
[Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 组织。

写给人看：同一件事的几次提交，在这里是一行。

## [Unreleased]

### Added

- `tools/check_licenses.py`（接缝 `S6`）：依赖许可门禁，**标准库实现**（符合 `D-06`），许可按 `License-Expression` → Trove classifiers → 旧 `License` 字段三级回退解析；`--report` / `--json` / `--ignore`
- **分支保护**：`main` 必须走 PR、必须 `test (3.9)` 与 `test (3.13)` 通过且分支最新、禁 force push、禁删除（公开仓库免费；`enforce_admins: false` 是刻意留的热修通道）
- 测试从 12 条增到 20 条：新增 `S6` 许可门禁 5 条、纯点号模板引用回归、`install.py` 默认目标回归、忽略名单
- **英文伴随件（`D-11`）**：14 个技能各附 `skills/<name>/references/en.md`（判据与动作的英文版，八节与中文同构）；`validate_skills.py` 校验其存在与完整性，另加两条回归测试
- **体检器第 13 项判据：活文档里没有与事实相反的断言**（`D-14`，票据 `07`）——拿文档里的断言去核对仓库事实：远端 / tag / 用例数 / 工具入口数 / 判据条数 / 台账编号区间与条数 / 自报分数。对不上就报「文件:行 + 实际值」。**快照不参与**：`CHANGELOG.md`、票据、ADR、发布检查单记的是某个时点发生了什么，回头改等于伪造证据；取不到事实的项（浅克隆里的 `git tag`）跳过并打印，不假装查过；`docs/onboarding.md` 自称「表里的数字都会过期、以文件为准」，它那里的数字按声明跳过
- 7 条回归测试钉住这条判据：对不上要红、对得上要绿、快照不查、工具入口数对不上要红、浅克隆跳过、其余项没全过时不比对自报分数、本仓库自己全过

### Fixed

- **三次 CI 真红，三种根因**（每一次都有本地复现与回归测试）：
  - `pip-licenses` 只读包元数据的旧字段 `License:`，而按 PEP 639 发布的新包把它写在 `License-Expression:` 里——它一行都判不出来、输出空清单，门禁空转。改为自带解析，并把判断逻辑从流水线的 heredoc 搬进 `tools/check_licenses.py`（能本地复现、能测）
  - **Windows 把 `templates/...` 规范化成 `templates` 目录本身**，`os.path.exists` 返回 True——夹具里一处悬空的模板引用被掩盖，本地 17 条测试全绿而 Linux 必红。修夹具 + 校验器显式拦掉纯点号引用
  - 门禁把**解释器自带的 `setuptools`**（Python 3.9 的 runner 上三个许可字段全空）当成"项目依赖未声明"。改为默认忽略 `pip` / `setuptools` / `wheel`，且**忽略不等于看不见**：跑的时候会打出来
- 响应时限按维护者口径改写：**尽力而为，不承诺时限**（`SECURITY.md` / `CONTRIBUTING.md` / `CODE_OF_CONDUCT.md` 三处一致）——一个人维护的项目不写做不到的承诺
- **陌生人测试发现的 6 处「文件与事实对不上」全部修掉**（票据 `04`）：`docs/onboarding.md` 让读者去 SECURITY.md 找「7 天 / 30 天」（那里早已改成「尽力而为」）；`CONTRIBUTING.md` 的 clone 地址占位没替换、且仍写着「远端还没接 / tag 是空的 / 分支保护还没配」；另有 frontier、决议条数（12→13）、用例数（11→20）、工具入口数（3/4→5）四处过期
- `check_project.py` 的 frontier 判定修正：**前置票已 `done` 就算解除**，不再只看 `Blocked by:` 里写没写 `-`（03 一完工，旧逻辑就假报「frontier 为空」）
- 文档纪律：`docs/onboarding.md` 末尾加一条总则——**表里的数字都会过期，以文件里的实际内容为准**
- **活文档里 7 处「与事实相反」的断言改成事实**（`D-14`）：`README.md` 的判据条数（28→29）、自报分数（28/28→29/29）、工具数（四个→五个）；`SECURITY.md` 的「远端还没接」「`git tag` 为空」「四个脚本」；`docs/agents/domain.md` 的决议区间（D-12→D-13）。这 7 处是人肉测不出来的那一类——第 13 项一上线就当场报了出来
- `D-14` 之后跟着飘的几处数字已同步：`README.md` 目录树、`docs/agents/domain.md` 的编号区间、`docs/architecture.md` 的决议条数、`docs/onboarding.md` 的编号区间与票数——是这项判据报出来的，不是人找的
- `README.md` 说测试「挂在 S1 / S2 / S3 三个接缝上」，而 `S6` 一进仓库就带了 5 条测试——这处机器查不出（测试挂没挂在接缝上要人判断），顺手改对
- **同一处漏在 `.github/PULL_REQUEST_TEMPLATE.md` 里**：它的自查清单还写着「S1 / S2 / S3 三个接缝」。上一行只修了 `README.md`——同一句话在仓库里有两处，改一处不等于改完
- 又一轮「文件与事实对不上」，这次是照 `docs/onboarding.md` 走一遍抓的：`CONTRIBUTING.md` 的体检项数（28→29）、用例数（20→30）、分支保护（「还没配」→已配）、D-11（「英文版还没做」→已做）、产物校验（「没人真走过」→走过，附实测 sha256）；`README.md` 目录树的「此刻还没有 release」；`docs/agents/issue-tracker.md` 的「本仓库目前没有远端」；`docs/agents/triage-labels.md` 的「还没有对接平台标签」（平台上是默认标签集，五个自定义名没建）；票据 `06` 的 `Status`（`todo`→`done`，远端与产物都已核过）
- `docs/onboarding.md` 18–22 那一格写过两个互相打架的 frontier 定义：前半句是「`Status: todo` 且每条前置都已 `done`」，后半句又退回「没有一张 `Blocked by: -` 的票」——后者正是票据 `04` 从 `check_project.py` 里删掉的旧口径。现在只留一个定义，并补上第三种原因：**票全做完了**，那不是缺陷
- `docs/release-checklist.md` 的「转公开之后的第一周」里，两条早已完成的待办补上勾（陌生人测试、票据 `03` 的验收记录）；推远端的命令块补上「换成你自己克隆的路径」——`GUIDE.md` 那次已经补过，这里漏了

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
