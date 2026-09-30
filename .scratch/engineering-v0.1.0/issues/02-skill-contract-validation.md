# 02 让技能契约可机械校验

Status: done
Blocked by: -            # 无则写 -
Covers: D-01, D-02, D-03, D-07   # 覆盖台账里哪些决议
Verify: python tools/validate_skills.py
Rounds: 2                # 尝试了几轮：写完校验器 → 修 2 处缺陷后再验
Sessions: 1              # 跨了几个会话（>1 说明票切大了）
Accept: 通过 —— 维护者亲手跑（2026-09-30）：14 个技能、0 个错误、0 个警告、退出码 0
Review: 2 项，全部已修（`keywords:` 落在 description 续行时误报缺失；`skills/` 目录不存在时抛 FileNotFoundError 而不是给一条干净的错误）

## 要什么

**已完成。** 验证指针：`python tools/validate_skills.py`，实跑输出见文件底部的 Comments 段。

改技能的人不必等维护者回信：跑一条命令，它告诉你哪一节缺了、`name` 与目录名不符、交叉引用指到了不存在的技能或模板、哪份技能的完成判据不足 4 条。CI 与贡献者跑的是同一条命令。

14 个技能是并列的：每个目录拿出去都得能独立工作，所以契约也必须能一次校验完，而不是靠人逐份读。

## 怎么算做完

- [ ] `python tools/validate_skills.py` 在本仓库退出码 0，末行是「0 个错误，0 个警告」，技能数 14、模板数 35
- [ ] frontmatter 三字段齐全（`name` / `description` / `whenToUse`），且 `name` == 目录名
- [ ] `description` 里带 `keywords:`（D-07）——缺了是警告，不是错误
- [ ] 八节骨架标题逐个核对，改名或缺失即报错（D-02）
- [ ] 「完成判据」节至少 4 条 `- [ ]`（D-03）
- [ ] 交叉引用为真：正文里的 `→ 调用` 指向的技能必须是本集真实技能，引用的 `templates/` 文件必须真实存在（D-01）
- [ ] 先看红：故意删掉一节或改坏一个技能名，命令退 1，错误文本里含那一节的名字

## 不做什么

- 不自动改技能：校验器只负责说「不通过」，改是你的事
- 不校验文案质量（说得清不清楚、话术好不好用）——那是评审的活
- 不做英文版正文（D-11 是待定项，期限 v0.2.0）
- 不测 `install.py`（S3 的行为测试挂在 04 上）

## 涉及

- 接缝：S1
- 文件：`tools/validate_skills.py`、`skills/*/SKILL.md`（只读）、`.scratch/skill-contract.md`

## Comments

<!-- 评论与历史追加到这里，不要写进头部 -->

- 验证指针（本步实跑）：`python tools/validate_skills.py` → 技能数 14 / 模板数 35 / 结果 0 个错误，0 个警告 / 退出码 0。
