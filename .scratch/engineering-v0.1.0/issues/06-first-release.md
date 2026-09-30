# 06 发第一个版本

Status: done
Blocked by: 03            # 03 已 done
Covers: D-09, D-10, D-11, D-13 # 覆盖台账里哪些决议（D-13 是 README 的致谢口径，随本版出厂）
Verify: git tag
Rounds: 1                # 尝试了几轮：发版本体一次到位，多出来的一轮是补远端与产物的证据
Sessions: 2              # 跨了几个会话：打 tag 一轮；接远端之后的核对与产物校验一轮
Accept: 通过 —— 2026-09-30 实跑核对（远端 + 产物，逐条对「怎么算做完」）：① `gh api .../tags` 有 `v0.1.0`，release 也在（有发布说明、非 draft）；② release 挂着 `v0.1.0.tar.gz` + `SHA256SUMS.txt`，下载后 sha256 对得上（`ef5b03dd…82d2`），包里 14 份 `SKILL.md` 齐；③ 在 tag 那份代码上 `python tools/install.py --list` → 退出码 0；④ `CHANGELOG.md` 有 `[0.1.0] - 2026-09-30` 段；⑤ 体检的「CHANGELOG 存在」「CONTRIBUTING + SECURITY 都在」「LICENSE 三处一致」全 `[x]`（29/29）。命令原文见本票 Comments 段——本行是照那些输出填的，不是打勾
Review: 2 项，都已处理 —— ① 判据里「D-11 的处置写进发布记录：本期不做英文版技能正文」在 D-11 真做了之后作废（英文伴随件已进仓库）：发布记录是快照，不回头改，只标注；② `README.md` 的目录树还写着「此刻还没有 release」——收尾时才抓到，已改，并顺手让它落进第 13 项判据的覆盖范围

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
- **2026-09-30 收尾核对：上面那条已经过期了——推 tag、发 release 都做完了。** 逐条实跑（不是打勾）：
  - `gh api repos/naki-yami/idea2oss/tags` → `v0.1.0`；`.../releases` → 一条 `v0.1.0`，有发布说明、非 draft，产物两个：`v0.1.0.tar.gz`、`SHA256SUMS.txt`。
  - `gh release download v0.1.0` 之后 `Get-FileHash -Algorithm SHA256 .\v0.1.0.tar.gz` → `ef5b03dd8fd7bd6cf88904cc61f63401e575c9b18230861586c1a4b6338182d2`，与 `SHA256SUMS.txt` 里那一行逐字符相同；包里 125 项、14 份 `SKILL.md`。
  - 把包解开，在解出来的 `v0.1.0/` 里跑 `python tools/install.py --list --target <一个空目录>` → 退出码 0，打印「（目录不存在，尚未安装）」。
  - `release.yml` 在打 tag 时跑过一次并成功（run `2026-09-30T08:57:38Z`）。
  - 所以「有 tag、有发布说明、有对应的 CHANGELOG 段落」三条都成立，本票改 `done`。
- 2026-09-30：判据里那条「D-11 的处置写进发布记录：本期不做英文版技能正文」在 D-11 真做了之后作废（英文伴随件已进仓库）。**发布记录是快照，不回头改**，只在这里标注。
