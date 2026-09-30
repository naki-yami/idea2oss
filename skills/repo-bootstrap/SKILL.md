---
name: repo-bootstrap
description: 第 1 步：把一个普通目录变成可用的本地 git 仓库——`git init`、配身份、写清四类边界的 `.gitignore`、完成首次提交，并立好后面每一步的落点目录。当你要开工却发现目录还不是 git 仓库，或刚拿到一份没有 `.git` 的代码时使用。keywords: git init, bootstrap repo, gitignore, first commit, secret leak, noreply email
whenToUse: 第 0 步立项之后、写第一行代码之前；目录还不是 git 仓库时；首次提交之前。
---

# 初始化本地 git 仓库

> 对应手册第 1 步（第四章）｜ 产出物：`.git/`、`.gitignore`、首次提交、三个落点目录 ｜ 完成判据：`git log` 至少一条提交，`git status --porcelain` 为空，`.gitignore` 覆盖四类边界，历史里没有密钥

## 何时用 / 何时不用

**用**：手上有一个要做的东西，但目录还不是 git 仓库；下载了一份没有 `.git` 的代码目录；在让代理动手写代码之前。

**不用**：已经是 git 仓库（直接去 `repo-setup`）；要给仓库接 GitHub（那是另一件事，见「动作」第 7 步）；已经 `git add .` 提交过一堆垃圾（先按「动作」第 4 步处理历史，再谈后面）。

**为什么这一步不能省**：整套技能集里没有一行 `git init`——所有技能都假设你已经在一个 git 仓库里干活，顺序是死的：先建仓库，技能才能在上面操作。更硬的理由是第 6 步：双轴评审的输入是「某个固定参照点之后的 diff」，参照点四选一（commit、分支、tag、merge-base），**四个全是 git 概念**。没有仓库，它没有输入。

## 输入（开工前必须到手的）

1. 一个准备开工的目录（可以是空的）。
2. `git --version` 的输出。
3. `git config user.name` 与 `user.email`——空的话首次 commit 会被拒。
4. 项目类型（决定 `.gitignore` 填哪几行）。
5. 这个目录里现存的密钥文件清单：`.env`、`*.pem`、`*.key`、凭据文件。

## 动作

1. **四件事，一个代码块**：

   ```
   git init
   git config user.name  "你的名字"      # 没配的话首次 commit 会被拒
   git config user.email "你的邮箱"
   git add .gitignore && git commit -m "chore: 初始化仓库"
   ```

   顺序是刻意的：**先写 `.gitignore`，再 `git add`**。首次提交只提交 `.gitignore`，等于第一件事就是把规矩立下来。

2. **划清 `.gitignore` 的四类边界**——这比 `git init` 重要得多。一上来 `git add .` 会在第一天把 `node_modules`、构建产物、编辑器缓存、`.env` 全吞进历史，之后清理很麻烦。直接抄 `templates/gitignore.txt`：

   | 边界 | 写什么 |
   |---|---|
   | 依赖目录 | `node_modules/`、`.venv/`、`venv/`、`__pycache__/`、`*.pyc` |
   | 构建输出 | `dist/`、`build/`、`out/`、`*.egg-info/`、`coverage/`、`.coverage`、各类工具缓存目录 |
   | 本机配置 | `.DS_Store`、`Thumbs.db`、`.idea/`、`.vscode/`、`*.local` |
   | 密钥文件 | `.env`、`.env.*`（用 `!.env.example` 留一个样板）、`*.pem`、`*.key`、`credentials.json`、`secrets.*` |

3. **提交前扫一眼 `git status`**：里面有没有 `.env`、`*.pem`、凭据文件。有 → 停手，先做下一步。

4. **密钥事故：已经进过历史怎么办**。删文件是不够的：

   - 先**轮换密钥**（假设它已泄露），再决定要不要重写历史；
   - 公开仓库上的泄露按「**已泄露**」处理，不是「已删除」——推上去那一刻就收不回来了；
   - 重写历史、force push 属于不可逆动作，**由你亲手做**，不要交给代理。

5. **顺手立三个落点目录**（后面每一步都要有地方放产物，先建目录比事后补规矩便宜）：

   ```
   docs/agents/          # 流程与代理配置（issue-tracker.md、domain.md、brief.md）
   docs/adr/             # 决策记录（第 2 步开始产生）
   .scratch/<feature>/   # 本地模式的规格与票据（第 3、4 步在这里落盘）
   ```

   git 不跟踪空目录：放一个 `.gitkeep` 或一行占位 README，别让它们在下一次提交后悄悄消失。

6. **首次提交**：提交信息写「为什么」，不写「改了什么」——改了什么看 diff 更准。

7. **只需本地 init，不必接 GitHub**。`git init` 和接 GitHub 是两件事：remote 只决定 `repo-setup` 选 tracker 时走 `gh issue` 还是本地 markdown。本地仓库加几次提交，就够第 6 步的双轴评审比对用了。真要接：`git remote add origin <url>`，那是你的事，不是这一步的判据。

8. **邮箱**：用 QQ 邮箱提交不会关联到你的 GitHub 账号，除非把该邮箱加进账号的 emails 列表。只是想把代码推上去，用 `用户名@users.noreply.github.com` 这种 noreply 地址更省事，也少泄露一个真实邮箱。

## 产出物

- 可用的本地仓库：`.git/`、`.gitignore`、首次提交。
- 三个落点目录：`docs/agents/`、`docs/adr/`、`.scratch/<feature>/`。
- 四类边界清单（从 `templates/gitignore.txt` 抄来并改成项目实际）。

## 完成判据

- [ ] `git log --oneline` 至少输出一条提交。
- [ ] `git status --porcelain` 输出为空（没有未跟踪的垃圾文件）。
- [ ] `.gitignore` 覆盖四类边界，每一类都能指出至少一行（依赖 / 构建输出 / 本机配置 / 密钥）。
- [ ] `git log --all --oneline -- .env "*.pem" "*.key" credentials.json` 输出为空——历史里没有密钥。
- [ ] `git config user.name` 与 `git config user.email` 都非空。
- [ ] 三个落点目录都在，且不是「空目录」状态（有 `.gitkeep` 或占位文件）。
- [ ] 首次提交的信息回答了「为什么」，不是「改了什么」。
- [ ] 若要推 GitHub：`user.email` 是 noreply 地址，或已确认该邮箱在账号的 emails 列表里。
- [ ] 本步没有执行任何不可逆动作（重写历史、force push）；有的话是你亲手做的。

## 手工兜底

- **这一步本来就没有技能替你做**：照「动作」第 1 步的代码块做即可，不依赖任何技能集或工具。这不是兜底，这是主路径。
- 没有 git：**先装 git，没有替代方案**——第 6 步的评审和第 8 步的发布都要它。
- `git commit` 被拒（提示 `Please tell me who you are`）：就是 `user.name` / `user.email` 为空，就地配置后重试。
- 已经把 `node_modules` 或产物提交进历史：还没推远端时，`git rm -r --cached <路径>` 补上 `.gitignore` 再提交一次即可。历史里只要出现过**密钥**，按「动作」第 4 步处理。
- 只想先写代码、不想建仓库：可以，但第 6 步的双轴评审会失去参照点，那时补仓库要重新划一次边界，更贵。
- 目录里有别人的代码或第三方素材：先确认你有没有权利把它带进来，再 `git add`。

## 下一步

→ 调用 `repo-setup`（定 tracker、triage 标签与领域文档布局，让第 2 步的产物有地方落）。

## 反模式

| 反模式 | 为什么错 | 改成 |
|---|---|---|
| 一上来就 `git add .` | 第一天就把 `node_modules`、构建产物、`.env` 吞进历史 | 先写 `.gitignore`，再按类添加 |
| 密钥进历史后只删文件 | 文件删了，那把密钥还在外面有效，历史里也还在 | 先轮换密钥，再决定要不要重写历史 |
| 把「接上 GitHub」当这一步的判据 | remote 只影响 tracker 模式，本地仓库就够用 | 本地 init + 几次提交，接远端另算 |
| 空目录直接提交 | git 不跟踪空目录，落点在下次提交后消失 | 放 `.gitkeep` 或占位 README |
| 让代理重写历史或 force push | 不可逆、影响别人，而代理的自信与正确无关 | 这类操作由你亲手做 |
| 提交信息写「update」 | 半年后没人能从日志里读出意图 | 写为什么；改了什么交给 diff |
