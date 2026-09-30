# 08 票全做完时，frontier 不再报缺陷

Status: todo
Blocked by: -            # 无则写 -
Covers: D-14             # 同一条纪律作用到体检器自己身上：判据的判定与文案不许和事实相反
Verify: python tools/check_project.py --dir . --level L2 --quiet
Rounds: -                # 尝试了几轮（指标：一次收敛率）
Sessions: -              # 跨了几个会话（>1 说明票切大了）
Accept: -                # 第 6 步填：你亲手跑一遍后的 通过/不通过 + 原因
Review: -                # 第 6 步填：两轴发现项计数（指标：评审返工）

## 要什么

`frontier` 这一项现在把「这一批票全做完了」判成红：`0 张可开工`，退出码 1，提示写「要么把票切小，要么解开阻塞；frontier 为空说明依赖成环或票切大了」。

事实是第三种原因——**票做完了**。`Blocked by: -` 且 `Status: todo` 的票为零，是因为已经没有待办的票，不是因为票切得不对。

后果不是文案难看，是**判据开始制造工作**：想让门禁转绿，就得凭空开一张票；不开，就得把 `06` 从 `done` 改回 `todo`（那是伪造状态，「文件与事实对不上」）。一个已经收尾的 feature 永远拿不到 29/29。

做完之后：全部票 `done` 时这一项报 `[x]` 并写明「这一批已收尾」；只要还存在 `todo` / `doing` 的票而 frontier 为空，照旧报红——那才是依赖成环或票切大。

## 怎么算做完

- [ ] 全部票 `done` 时，`frontier` 报 `[x]`，详情写「N 张票全部 `done`，这一批已收尾」
- [ ] 还有 `todo` / `doing` 的票、但 frontier 为空时，照旧报红，提示里保留「依赖成环 / 票切大了」
- [ ] 一张票据都没有时照旧报红——「还没拆票」和「拆完做完了」不是一回事
- [ ] 提示文案补上第三种原因，并与 `docs/onboarding.md` 18–22 那一格（本 PR 刚统一过）说法一致
- [ ] 回归测试钉住三种情形：全 `done` 报绿 / 有 `todo` 且能开工报绿 / 有 `todo` 且前置全未 `done` 报红
- [ ] `python tools/check_project.py --dir . --level L2 --quiet` 退出码 0（29/29）

## 不做什么

- 不放松「存在可开工的票时 frontier 必须非空」——那条正是本票要保住的
- 不改 `Blocked by:` 的解析口径（前置票 `done` 即算解除，`04` 已定）
- 不动 `docs/release-checklist.md` 的「已完成」两段：那是快照，记的是 v0.1.0 那天的事

## 涉及

- 接缝：S2
- 文件：`tools/check_project.py`、`tests/test_tools.py`、`docs/onboarding.md`

## Comments

<!-- 评论与历史追加到这里，不要写进头部 -->

- 2026-09-30：**这张票是判据制造出来的**，记一下来历。把票据 `06` 的 `Status` 从 `todo` 改成 `done`（一个纯粹的事实修正：远端、tag、release、产物都已核过）之后，`check_project.py` 当场转红 28/29，`unittest` 的 `test_real_repo_has_no_missing_items` 跟着红，唯一红的就是这一项。当时为了让门禁能过，开了这张票——它此刻的内容就是那句判据本身。留在这里，而不是悄悄改掉，是因为**「为了让判据变绿而开票」正是这条判据的失效方式**。
- 2026-09-30：同一类还有两处，本票不碰，留给下一张：① `.github/workflows/ci.yml` 第 51 行的注释仍写着「接缝测试（S1 / S2 / S3）」，实际有四个（`S6` 也带测试）——CI 文件要 `workflow` scope 才推得上去，当前令牌没有，改不了；② `check_project.py` 的快照豁免是**按文件**给的（`docs/release-checklist.md` 整份豁免），而那份文件里混着「已完成」（快照）与「转公开之后的第一周」（活待办）两段——豁免粒度比事实粗了一级。
