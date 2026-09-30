# 发布前检查表

> 第 8 步的收尾清单 ｜ 判据：**全部勾上之后**才可以把仓库转公开
> 其中三项代理不能代做——见 `AGENTS.md` 的权限边界。

## 已完成（v0.1.0，2026-09-30）

- [x] 许可证三处一致：`LICENSE` 全文 / `pyproject.toml` 的 `license` / README 许可段
- [x] 仓库**全历史**无密钥：无密钥模式命中、无明文密钥文件
- [x] 零第三方依赖 → 许可污染风险为零（`D-06`）
- [x] 联系方式落地：`SECURITY.md` 与 `CODE_OF_CONDUCT.md` → `2035116682@qq.com`；`.github/CODEOWNERS` → `@naki-yami`
- [x] 第三方内容的许可说明：`CODE_OF_CONDUCT.md` 末尾写明正文为 Contributor Covenant v2.1（CC BY-SA 4.0），保留署名与链接
- [x] 三条门禁全绿：结构体检 28/28、技能契约 0 错 0 警、12 个测试 OK
- [x] `CHANGELOG.md` 的 `[Unreleased]` 已切成 `[0.1.0] - 2026-09-30`
- [x] 本地 tag `v0.1.0` 已打（**未推**——推 tag 是发版动作，由维护者做）
- [x] 陌生人测试（机械版）：干净克隆 → 按 README 装到目标项目 → 三条门禁全过，且 clone 保持干净
- [x] 占位全部清除：`example.com` 邮箱 ×2、CODEOWNERS 占位 ×5

## 还差三件

| # | 事项 | 谁 | 怎么做 | 判据 |
|---|---|---|---|---|
| 1 | 推上远端，让 CI 真跑一次 | 维护者（命令可代跑） | `git remote add origin git@github.com:naki-yami/idea2oss.git` → `git push -u origin main` → `git push origin v0.1.0` | Actions 页出现一次绿色运行 |
| 2 | 用一个故意失败的 PR 验证 CI 挡合并 | 维护者 | 建分支改坏一个技能（例如删掉某节标题）→ 提 PR | CI 变红，且合并被挡住 |
| 3 | 配分支保护 | 维护者（平台侧） | Settings → Branches，三条规则见下 | 规则已保存并对 `main` 生效 |

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
- [ ] 找**一个没看过这个项目的人**走一遍 `docs/onboarding.md`（票据 `04` 的判据）——这一条代理顶替不了
- [ ] 有人提 PR 后，把票据 `03` 的验收记录补上（那张票到那时才能 done）
