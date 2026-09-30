# 发布前检查表

> 第 8 步的收尾清单 ｜ 判据：**全部勾上之后**才可以把仓库转公开
> 其中三项代理不能代做——见 `AGENTS.md` 的权限边界。

## 已完成（v0.1.0，2026-09-30）

- [x] 许可证三处一致：`LICENSE` 全文 / `pyproject.toml` 的 `license` / README 许可段
- [x] 仓库**全历史**无密钥：无密钥模式命中、无明文密钥文件
- [x] 零第三方依赖 → 许可污染风险为零（`D-06`）
- [x] 联系方式落地：`SECURITY.md` 与 `CODE_OF_CONDUCT.md` → `2055604701@qq.com`；`.github/CODEOWNERS` → `@naki-yami`
- [x] 第三方内容的许可说明：`CODE_OF_CONDUCT.md` 末尾写明正文为 Contributor Covenant v2.1（CC BY-SA 4.0），保留署名与链接
- [x] 四条门禁全绿：结构体检 28/28、技能契约 0 错 0 警、20 条测试 OK、依赖许可门禁通过
- [x] `CHANGELOG.md` 的 `[Unreleased]` 已切成 `[0.1.0] - 2026-09-30`
- [x] 本地 tag `v0.1.0` 已打（**未推**——推 tag 是发版动作，由维护者做）
- [x] 陌生人测试（机械版）：干净克隆 → 按 README 装到目标项目 → 三条门禁全过，且 clone 保持干净
- [x] 占位全部清除：`example.com` 邮箱 ×2、CODEOWNERS 占位 ×5（复查：0 处真实残留；本行出现的 `example.com` 只是在说明删了什么）
- [x] **默认分支名与 CI 触发条件一致**：分支从 `master` 改名为 `main`——`.github/workflows/ci.yml` 监听的是 `branches: [main]`，不改名的话推上去 CI 一次都不会跑。这类"名字对不上"的坑只有在推之前查一遍才发现得了。

## 已完成（第二阶段：接上远端与门禁，2026-09-30）

- [x] 推上远端：`main` + tag `v0.1.0`（`git push` 与 tag 都过了 SSH）
- [x] **CI 在 main 上跑绿**：run #8，两个矩阵 job 全过（3.9 用 14s、3.13 用 8s）
- [x] **CI 在 PR 上会跑，且失败会挡住合并**：故意失败的 PR #4 → CI 红 → `mergeStateStatus=BLOCKED`，而 `mergeable=MERGEABLE`（是门禁挡的，不是冲突）
- [x] **分支保护已配**（仓库公开后免费）：
  - 必须走 PR 才能合进 `main`；必须 `test (3.9)` 与 `test (3.13)` 全绿，且分支必须最新
  - 禁 force push、禁删除分支、必须解决对话
  - `enforce_admins: false` 是**刻意的**：一个人维护，给自己留一条热修通道；外部贡献者一律走门禁
- [x] 响应时限按维护者的意思改成「**尽力而为，不承诺时限**」（`SECURITY.md` / `CONTRIBUTING.md` / `CODE_OF_CONDUCT.md` 三处口径一致）
- [x] 仓库转为公开

## 陌生人 30 分钟测试（第 8 步的判据）——已做，2026-09-30

一个没读过本项目的人照 `docs/onboarding.md` 走完：

- **0–3 / 3–6 / 6–10 / 10–14 / 14–18 分钟全过**：README 说得清给谁用与不做什么；三条命令跑通（14 技能、0 错 0 警、`Ran 20 tests ... OK`）；`CONTEXT.md` 20 条术语；5 个模块 + `S1`–`S6` 接缝齐；三份 ADR 在位。
- **卡在 22–26 分钟**，两处，**都不是「缺件」，是文件与事实对不上**：`docs/onboarding.md` 让读者去 SECURITY.md 找「7 天 / 30 天」，而那里写的是「尽力而为，不承诺时限」；`CONTRIBUTING.md` 的 `git clone <仓库地址>` 占位没替换，且仍写着「远端还没接」。
- 另有 4 处小过期：frontier（03 已 done）、决议条数（12 vs 13）、用例数（11 vs 20）、工具入口数（3/4 vs 5）。**根子是同一类：文档里写死了「当前状态」。** 修法不只是把数字改对，还要把「写状态」改成「写规则 + 以文件为准」——见 `docs/onboarding.md` 末尾那条总则。
- **6 处全部已修**（含 `CONTRIBUTING.md` 的 clone 地址），见票据 `04-stranger-30-minutes.md` 的 Comments。

**这一格教的东西**：判据不只是「文件在不在」，还包括**文件里写的是不是当前事实**。前者机器能查（`check_project.py` 的 28 项），后者只能靠人读一遍——所以第 8 步的判据是「陌生人 30 分钟」，而不是「结构体检满分」。

### 配好的三条规则（原文，供复核）

```json
{
  "required_status_checks": {"strict": true, "contexts": ["test (3.9)", "test (3.13)"]},
  "enforce_admins": false,
  "required_pull_request_reviews": {"required_approving_review_count": 0},
  "allow_force_pushes": false,
  "allow_deletions": false,
  "required_conversation_resolution": true
}
```

### 推上远端的三条命令

```powershell
cd D:\idea2oss          # 换成你自己克隆的路径
git remote add origin git@github.com:naki-yami/idea2oss.git   # 用 HTTPS 就把这行换成 https 地址
git push -u origin main          # 默认分支已改为 main（与 ci.yml 的 branches: [main] 一致）
git push origin v0.1.0           # 推 tag 才算发版；没推之前，这个版本只在你机器上
```

推完去 Actions 页确认 `ci` 跑过一次；如果没跑，先查分支名和触发条件是否对得上。

### 分支保护三条（写在平台上，不写在文档里）

- 合并前必须 CI 通过
- 至少一次评审（个人项目可设成「作者以外」）
- 禁止 force push、禁止直推 `main`

## 只有维护者能做的（代理不做）

- 把仓库**转为公开**——不可逆，没有撤销按钮
- 对外发布、宣传、对他人做承诺
- 法务判断（CoC 的 CC BY-SA 归属怎么写、许可证要不要换）
- 发版动作与 tag 的推送

## 转公开之后的第一周

- [ ] 挂徽章（CI 状态、最新版本、许可证）——**只在 CI 真跑过之后**：挂一个指向不存在仓库的徽章，比不挂更伤
- [ ] 确认 issue 模板与标签可用（`good first issue` / `help wanted` / `bug` / `enhancement`）
- [ ] 履行 `CONTRIBUTING.md` 的「响应节奏」：一周至少看一次
- [x] 走一遍陌生人 30 分钟测试（票据 `04` 的判据）。**要的是「没读过本仓库的视角」**，不是某一类执行者：换人、换机器、或一个没有本仓库历史的会话都算——`flow-tuning` 的手工兜底节把三种做法并列写着
- [x] 有人提 PR 后，把票据 `03` 的验收记录补上——PR #5 已合，票据 `03` 已是 `done`
