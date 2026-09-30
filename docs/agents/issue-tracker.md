# issue tracker 落点

> setup 一次性配置的产物之一 ｜ 每个仓库跑一次，位置在第 1 步之后、第 2 步之前

- **模式**：本地 markdown（`.scratch/<feature>/issues/NN-*.md`）
- **为什么**：远端已经接上了（`git remote -v` 指向 `github.com/naki-yami/idea2oss`），但「我自己要做的活」仍然不进公开 issue——本地模式是完全正规的选项，规格与拆票一步都不用省。
- **平台上的 issue**（外部报告、依赖升级）走 GitHub 模式；**本仓库自己的活**继续走本地票据。真要整体搬到 Issues 时记住：**规格（`spec.md`）必须在本地留一份唯一权威副本**，因为 tracker 的 issue 有体积上限，截断时没有兜底。

## 本地模式的约定（照 `templates/issue-tracker.md`）

1. 一票一文件，从 `01` 编号，标题就是那个用户可见结果。
2. 头部六行结构不要改：`Status` / `Blocked by` / `Covers` / `Verify` / `Rounds` / `Sessions`；第 6 步再追加 `Accept:` 与 `Review:`。
3. **评论与历史追加到文件底部的 `## Comments` 下，不要写进头部**——头部是机器读的（指标采集点），底部是人和历史。
4. `Blocked by:` 无阻塞写 `-`；`Covers:` 指向 `docs/decisions.md` 里的编号。

## 当前状态

| feature | 位置 | 状态 |
|---|---|---|
| `engineering-v0.1.0` | `.scratch/engineering-v0.1.0/issues/` | 8 张票（7 张 done、1 张 todo） |
