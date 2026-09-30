# 04 让陌生人在 30 分钟内上手

Status: todo
Blocked by: -            # 无则写 -
Covers: D-06             # 覆盖台账里哪些决议
Verify: python tools/install.py --list
Rounds: -                # 尝试了几轮（指标：一次收敛率）
Sessions: -              # 跨了几个会话（>1 说明票切大了）
Accept: -                # 第 6 步填：你亲手跑一遍后的 通过/不通过 + 原因
Review: -                # 第 6 步填：两轴发现项计数（指标：评审返工）

## 要什么

一个没读过本仓库的人，在一台干净机器上只读 README，30 分钟内做完三件事：装上、跑通一次、知道下一步该改哪个文件。

判据是行为不是文档：他卡在第几分钟、卡在哪一步，就是结构缺了哪一件。所以这张票交三样——一条 0–30 分钟路径、一套在干净目录里跑得起来的安装、以及它不需要任何第三方包（D-06）。

## 怎么算做完

- [ ] `python tools/install.py --target <一个没装过的新目录> --list` 退 0，打印「（目录不存在，尚未安装）」而不是报错
- [ ] 装上之后再跑同一条命令：列出 14 个技能，并标出每个是「联接」还是「副本」
- [ ] `docs/onboarding.md` 在，体检的「接手路径文档在」项转 `[x]`；内容按 `templates/onboarding.md` 的 0–30 分钟表写，每一行指到的文件都真实存在
- [ ] README 的「30 秒上手」在三条命令以内，在一个干净克隆里逐条能跑通
- [ ] 文档里的每条路径在当前仓库根上成立——`GUIDE.md` §2.2 的 `cd D:\dsh\idea2oss` 现在指到机器上另一份同名拷贝，改成相对路径或删掉（证据在 Comments 段）
- [ ] 干净环境验证：不装任何第三方包，`install.py` / `validate_skills.py` / `check_project.py` / `dump_templates.py` 四个工具都能跑，输出里没有 ImportError
- [ ] `tests/` 里有用例挂在 S3 上：`--list` 退 0；`--dry-run` 不写盘；`python -m unittest discover -s tests` 全绿
- [ ] 陌生人测试结果写进 `Accept:`：谁跑的、第几分钟卡住、卡在哪一步

## 不做什么

- 不改技能正文：能不能被触发是 S4 与运行时的事，不是上手路径的事
- 不做英文版 README，也不做英文版正文（D-11 本期不做）
- 不引入任何依赖：D-06 是「只用标准库」，不是「锁版本」
- 不追求体检满分：`license` 元数据、`env.example` 两项取决于项目类型，缺了就在 README 的「限制」里写明
- 不补 `CONTRIBUTING.md` / `SECURITY.md`（社区文件与发版一起做，见 06）

## 涉及

- 接缝：S3
- 文件：`docs/onboarding.md`、`README.md`、`GUIDE.md`、`tests/`、`tools/install.py`（只在发现缺陷时改）

## Comments

<!-- 评论与历史追加到这里，不要写进头部 -->

- 开工前先看：`GUIDE.md` §2.2 写着 `cd D:\dsh\idea2oss`，而 `D:\dsh\idea2oss` 是机器上另一份真实目录（不是联接、不是本仓库）。陌生人照它走会改错树。

- 2026-09-30：上面那条已修——`GUIDE.md` 改成占位路径 + 「默认当前目录」，`README.md` 的 30 秒上手改成装到「你正在开发的项目」，并在 `install.py` 里加了「目标是本仓库自己」的提醒。
- 2026-09-30：**机械版陌生人测试已跑**（干净克隆 → 按 README 装到目标项目 → 三条门禁全过 → clone 保持干净，全程 0.04 分钟）。它抓到一个 P0：`install.py` 缺省 `--target` 时抛 `TypeError`——而那是 README 的第一条命令。已修，并补上回归用例 `test_default_target_is_cwd`（单测当初没拦住，因为每次都显式传了 `--target`）。
- **本票仍为 todo**：判据里的「陌生人」是**没看过这个项目的人**，代理顶替不了。转公开后第一周找一个人走一遍 `docs/onboarding.md`，把结论写在这里。
