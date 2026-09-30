# 06 发第一个版本

Status: todo
Blocked by: 03            # 等 CI 在 PR 上跑起来、能挡住合并
Covers: D-09, D-10, D-11 # 覆盖台账里哪些决议
Verify: git tag
Rounds: -                # 尝试了几轮（指标：一次收敛率）
Sessions: -              # 跨了几个会话（>1 说明票切大了）
Accept: -                # 第 6 步填：你亲手跑一遍后的 通过/不通过 + 原因
Review: -                # 第 6 步填：两轴发现项计数（指标：评审返工）

## 要什么

使用者拿到的是一个有版本号的仓库：`v0.1.0` 有 tag、有发布说明、有对应的 CHANGELOG 段落，README 上的版本号与 tag 一致。升级认 tag 不跟 main——技能名会直接进提示词，改名就是改行为。

发版前先跑一遍体检（S2），把「发布那天站不住」的项当场补齐：LICENSE / README / SECURITY 三件齐、许可证名被平台识别、历史里搜不到密钥。

用户装的就是 tag 那一份：在干净目标目录上 `python tools/install.py --list` 照样退 0（S3 在 release 上没有退化）。

## 怎么算做完

- [ ] `git tag` 列出 `v0.1.0`，`git log --oneline` 能看到打 tag 的那个提交（现在 `git tag` 还是空的）
- [ ] `CHANGELOG.md` 的 `[0.1.0]` 段落有日期、Added 段写清这一版给了什么；`[Unreleased]` 里已发布的内容挪进 0.1.0
- [ ] 体检的「CHANGELOG 存在」「CONTRIBUTING + SECURITY 都在」两项转 `[x]`
- [ ] LICENSE、README 许可段、包元数据三处一致，平台识别出许可证名而不是 Unknown
- [ ] 发布说明与 tag 对应：说清这一版给别人用的是什么，以及已知限制
- [ ] D-11 的处置写进发布记录：本期不做英文版技能正文，台账里的期限仍是 v0.2.0（到期未定就改成「默认：不做」）
- [ ] D-09 过闸：交接文档只在系统临时目录，体检的「交接文档没进仓库」项通过，发布检查单里写明这一条
- [ ] 在 tag 那份代码上跑 `python tools/install.py --list`，退出码 0

## 不做什么

- 不发 v0.2.0，也不清空 `[Unreleased]` 里其余的条目
- 不做英文版正文（D-11 本期不做）
- 不重写 git 历史、不 force push；发现密钥先轮换，再另开票
- 不做 tag 触发的构建产物：本票只打 tag、写说明、发 release，流水线本身归 03

## 涉及

- 接缝：S3
- 文件：`CHANGELOG.md`、`LICENSE`、`README.md`、`SECURITY.md`、`CONTRIBUTING.md`、`.github/workflows/release.yml`

## Comments

<!-- 评论与历史追加到这里，不要写进头部 -->

- 2026-09-30：`CHANGELOG.md` 的 `[Unreleased]` 已切成 `[0.1.0] - 2026-09-30`；本地 tag `v0.1.0` 已打（`git tag` 可验）。
- **本票仍为 todo**：判据是「使用者拿到一个有版本号的仓库」，本地 tag 不算数——推 tag、发 release 要等 `03`（CI 在真实 PR 上验证过）之后由维护者做。剩余步骤见 `docs/release-checklist.md`。
