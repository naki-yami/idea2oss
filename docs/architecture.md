# 架构与接缝

> 第 4 步 · 产出物：接缝清单 ｜ 判据：每个接缝一行，且与 spec 的每条成功判据对得上
> 用第 4 步的词汇：模块 / 接口 / 深度 / 接缝 / 适配器

## 模块

| 模块 | 接口（外面看进去的那一面） | 深度（藏在接口后面的是什么） |
|---|---|---|
| `skills/` | 一个目录一份 `SKILL.md`（中文正文），另附 `references/en.md` 英文伴随件；两边的八节同构，frontmatter 三字段 | 14 步流程的判据、话术、反模式、手工兜底路径 |
| `templates/` | 35 份可直接复制的文件（33 份为导出物 + 2 份手写件） | 《流程手册》附录 A/B 的全部结构约定 |
| `tools/` | 五个命令行入口：`install.py` / `validate_skills.py` / `check_project.py` / `check_licenses.py` / `dump_templates.py` | 安装、技能契约校验、结构判据、依赖许可门禁、模板重放 |
| `docs/` | 人读的知识层：brief / decisions / adr / architecture / onboarding / agents | 为什么这样做、接手从哪开始 |
| `.scratch/` | 过程层：spec 与票据 | 一次性工作区，用完归档 |

## 接缝清单

接缝 = 外面看进去只能通过它的那个边界。**测试挂在这里，内部随便改，测试都不用动。**

| 接缝 | 通过它的是什么 | 谁调用它 |
|---|---|---|
| `S1 validate_skills.py` | 技能契约是否成立：frontmatter 三字段、`name` == 目录名、八节骨架、判据条数、交叉引用、模板存在性；退出码 0/1 | CI、贡献者、PR 模板的自查项 |
| `S2 check_project.py --json` | 结构判据的结果：`ok / missing / warn / not_applicable` 与退出码；`--level` 决定哪些是强制项 | CI、票据的 `Verify:`、接手者 |
| `S3 install.py` | 技能能否被安装到运行时：`--list` 的输出、`--target` / `--link` / `--force` 的行为、`--uninstall` 只删自己装的 | 使用者、README 的 30 秒上手 |
| `S4 SKILL.md frontmatter` | 技能契约对外承诺的那一面：`name` / `description` / `whenToUse` | 运行时（触发）、S1（校验） |
| `S5 templates/*` | 模板的结构约定：「结构不要改，改内容」 | 技能正文、使用者的复制动作 |
| `S6 check_licenses.py` | 依赖许可判定的结果与退出码：`--report` 吃一份 JSON、`--json` 吐机器可读结果 | CI 的 D-12 门禁、贡献者本地自检 |

**适配器**：一个适配器是假想的接缝，两个才是真的。

- `S1`/`S2` 各有**两个真实调用方**（CI + 本地命令行），所以它们是真接缝，值得为它们写测试。
- `S6` 也是真接缝（CI 的 D-12 门禁 + 本地自检），所以它一进仓库就带了 5 个测试。
  它是在 CI 连续五次全红之后才从 `ci.yml` 的 heredoc 里搬出来的——**内联在流水线里的判断逻辑，本地复现不了、测试覆盖不到，红了只能猜**。
- `S5` 目前只有一个调用方（技能正文），所以它**还不是**真接缝——等出现第二个消费方（比如 `scaffold_project.py` 之外的生成器）再考虑给它加契约测试。

## 数据流

```
               ┌──────────────┐
使用者 ──安装──▶ │ tools/install.py │ ──▶ <工作区>/.dsh/skills/<14 个技能>
               └──────────────┘
                                    运行时按 frontmatter 触发（S4）
               ┌──────────────────┐
贡献者 ──改技能─▶ │ validate_skills  │ ──0/1──▶ CI 挡住合并（S1）
               └──────────────────┘
               ┌──────────────────┐
任何人 ──体检──▶ │ check_project.py │ ──0/1──▶ 票据 Verify: / CI 门禁（S2）
               └──────────────────┘
```

## 与本集技能对应的环节

- 第 1 步「初始化仓库」→ `.gitignore` 四类边界 + `docs/agents/`、`docs/adr/`、`.scratch/` 三个落点
- 第 2 步「拷问」→ `CONTEXT.md`（术语表）+ `docs/decisions.md`（14 条决议）
- 第 4 步「方案与计划」→ 本文档的接缝清单 + `.scratch/engineering-v0.1.0/issues/` 的票据图
- 第 6 步「检测」→ `S1` + `S2` 两条命令就是这一票的 `Verify:`
