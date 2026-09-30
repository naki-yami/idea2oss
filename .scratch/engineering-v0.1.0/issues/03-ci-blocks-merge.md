# 03 让 CI 在 PR 上跑并挡住合并

Status: todo
Blocked by: -            # 02 已 done，本票现在就能开工
Covers: D-12             # 覆盖台账里哪些决议
Verify: python tools/check_project.py --dir . --level L2 --quiet
Rounds: -                # 尝试了几轮（指标：一次收敛率）
Sessions: -              # 跨了几个会话（>1 说明票切大了）
Accept: -                # 第 6 步填：你亲手跑一遍后的 通过/不通过 + 原因
Review: -                # 第 6 步填：两轴发现项计数（指标：评审返工）

## 要什么

别人提 PR 时，流水线自动跑两个真接缝的检查——`validate_skills.py`（S1）与 `check_project.py`（S2）——再加上挂在这两个接缝上的测试。红了，合并按钮就不可用。

为什么要带测试：门禁里没有断言，CI 就只是「跑了一下」。用例只断言行为（退出码、输出字段），不断言实现细节，所以技能内部随便改，测试都不用动。

同一条流水线里还有一步依赖许可检查（D-12）：GPL / AGPL / 未知许可的依赖被单独标出来，而不是混在安装日志里没人看。

## 怎么算做完

- [ ] `.github/workflows/ci.yml` 在，体检的「CI 工作流在」项从 `[ ]` 变成 `[x]`
- [ ] 步骤顺序固定：setup-python → `python tools/validate_skills.py` → `python tools/check_project.py --dir . --level L2 --quiet` → `python -m unittest discover -s tests`
- [ ] `tests/` 里有用例挂在 S1 上：合法技能集退 0；缺一节 / `name` 与目录名不符 / 引用不存在的技能退 1，且错误文本含对应关键词
- [ ] `tests/` 里有用例挂在 S2 上：完整骨架通过数高；空目录缺 README 与 `.gitignore`；`--level L0` 只强制 4 项
- [ ] `python -m unittest discover -s tests` 先本地绿，再在 CI 上绿一次
- [ ] 许可检查是独立一步，输出里能看到每个依赖的许可证名；出现 GPL / AGPL / 未知许可时这一步失败
- [ ] 用一个故意失败的 PR 验过：CI 红、合并按钮不可用（这条只能人做，结果写进 `Accept:`）
- [ ] 分支保护配在平台上，不是只写在文档里

## 不做什么

- 不塞 `lint` / `typecheck` 步骤：本仓库是纯标准库 Python，没有 lint 工具链，别放空步骤充数
- 不做 tag 触发的发布流水线（那是 06 的活）
- 不替你在平台上点分支保护——那一下必须由仓库所有者亲手做
- 不测 S3（`install.py` 的行为测试挂在 04 上）

## 涉及

- 接缝：S1、S2
- 文件：`.github/workflows/ci.yml`、`tests/`、`CONTRIBUTING.md`

## Comments

<!-- 评论与历史追加到这里，不要写进头部 -->

- 2026-09-30：`ci.yml` 与 `release.yml` 已写好，并在本地跑通了三者的等价命令（12 个测试 OK、技能契约 0 错 0 警、结构体检 28/28）。
- **本票仍为 todo**：判据是「PR 上自动跑，而且失败会挡住合并」——这需要远端、一个故意失败的 PR、以及平台侧的分支保护，三件都还没做。步骤见 `docs/release-checklist.md`。
