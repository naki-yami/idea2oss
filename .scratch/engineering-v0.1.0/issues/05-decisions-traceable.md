# 05 让每条决策可追溯

Status: done
Blocked by: -            # 无则写 -
Covers: D-04, D-08       # 覆盖台账里哪些决议
Verify: python tools/check_project.py --dir . --level L2 --quiet
Rounds: 1                # 尝试了几轮（指标：一次收敛率）
Sessions: 1              # 跨了几个会话（>1 说明票切大了）
Accept: 通过 —— 维护者亲手跑（2026-09-30）：台账四列 / 只有一处 / 决议覆盖率 100%（12/12）
Review: 1 项，已修（D-08 原证据「导出后 git 无差异」不可复现：生成器把 `AGENTS.md` 写成不带 `.tpl` 的名字、`OUT` 硬编码到另一份拷贝——已改成可重放写法，实测 33 份逐字节一致、无多余文件）

## 要什么

**已完成。** 验证指针：`python tools/check_project.py --dir . --level L2 --quiet` 里的「决议台账存在且四列」「台账只有一处」「决议被票据覆盖（覆盖率）」三项，实跑输出见文件底部的 Comments 段。

你想知道「为什么是 14 个技能而不是 1 个」，不必翻 git 历史：台账一行一条决议，够格的写 ADR，spec 句末 `[D-nn]`、票据头 `Covers:` 一路回指。第 6 步算决议追溯率，缺哪条当场看得见。

台账只有一处（`docs/decisions.md`），编号永不复用：删掉的划掉保留，新的往后排。

## 怎么算做完

- [ ] 台账只在 `docs/decisions.md` 一处，体检的「台账只有一处」项为 `[x]`
- [ ] 每条决议四列齐全（编号 / 类型 / 决议 / 证据），证据栏非空，且能落到一条命令或一个文件上
- [ ] 类型只用三种：约束 / 默认 / 待定；「待定」必须带期限（D-11 带的是 v0.2.0）
- [ ] `D-01`…`D-12` 编号连续、不复用
- [ ] 六张票的 `Covers:` 合起来覆盖全部 12 条决议，体检的「决议被票据覆盖（覆盖率）」项是 100%
- [ ] 三条架构决策各有一份 ADR（`docs/adr/0001…0003`），spec 里只留一行指针
- [ ] 模板是导出物（D-08）：`templates/` 35 份都在，技能正文引用得到的模板全都存在（`python tools/validate_skills.py` 的模板检查 0 错误）

## 不做什么

- 不给 S5 加契约测试：`templates/*` 现在只有一个消费方，还不是真接缝（等第二个消费方出现再说）
- 不修 `tools/dump_templates.py` 与 `templates/` 的对不齐（已知缺口记在 Comments 段）——那不是台账的活，等下一轮拆票
- 不重写台账历史：编号不复用，删掉的划掉保留

## 涉及

- 接缝：S2、S5
- 文件：`docs/decisions.md`、`docs/adr/`、`docs/architecture.md`、`templates/ledger.md`

## Comments

<!-- 评论与历史追加到这里，不要写进头部 -->

- 验证指针（本步实跑）：`python tools/check_project.py --dir . --level L2 --quiet` → 「决议台账存在且四列」docs/decisions.md（12 条决议）、「台账只有一处」找到 1 份、「决议被票据覆盖（覆盖率）」100%（12/12），退出码 0。
- 已知缺口（D-08）：拿同一份 `scaffold_project.py` 重放生成器，33 份产出里 32 份与仓库逐字节一致，对不齐的是三处——① 脚本写出的是 `templates/AGENTS.md`，仓库里叫 `AGENTS.md.tpl`；② `INDEX.md` 与 `manual-review.md` 不是导出物；③ 脚本里 `OUT` 写死 `D:\dsh\idea2oss\templates`，那是机器上另一份拷贝。所以「导出后 git 无差异」现在不成立：重放会多出一个未跟踪文件，而且写不到本仓库里。这条缺口留到下一轮拆票。
