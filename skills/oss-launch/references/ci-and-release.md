<!-- idea2oss · oss-launch 参考件 ｜ 手册 8.4 / 8.5 + 附录 B3/B4 ｜ SKILL.md 引用本文件，不要在两处重复维护 -->

# CI、质量门、版本与发布

## 一、最小 CI 骨架

照 `templates/ci.yml` 抄，结构不要改：

```yaml
name: ci
on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # 换成你的语言：setup-node / setup-python / rust-toolchain ...
      - uses: actions/setup-node@v4
        with:
          node-version: '20'      # 只留你真正支持的版本；要两个就换成 matrix，多一个都是在烧你的时间
      - run: npm ci
      - run: npm run lint --if-present
      - run: npm run typecheck --if-present
      - run: npm test
      - run: npm run build --if-present
      # 依赖许可检查（GPL / AGPL / 未知许可要单独看）
```

顺序固定：**安装依赖 → lint → typecheck → test → 构建产物**。矩阵只留你真正支持的两个版本，多一个都是在烧你的时间。

判据：**别人提 PR 时 CI 会自动跑，而且失败会挡住合并。** 做不到这两点，等于没有 CI。注意这两个条件是"与"——只在 push 时跑，或跑红了也能合，都不算。

## 二、分支保护清单（写在平台上，不是写在文档里）

- 主分支合并前必须 CI 通过。
- 至少一次评审（个人项目可设成"作者以外的仓库必须有"）。
- 禁止 force push，禁止直接推主分支。
- 依赖与漏洞告警（Dependabot 等）开着，并把告警当 issue 处理。

**验证方式**：开一个故意让 test 失败的 PR，确认「合并」按钮被禁用；再确认没有 review 时也合不了。没验证过的分支保护，等于猜。

## 三、依赖与安全扫描

| 工具 | 管什么 | 落地 |
|---|---|---|
| Dependabot | 依赖升级与漏洞告警 | `templates/dependabot.yml` |
| CodeQL 或同类 | 代码扫描 | 平台的安全页签里开 |
| Scorecard | 给仓库做一次安全体检 | 定期跑一次，结果当 issue 处理 |
| license-checker / pip-licenses | 依赖许可清单（GPL / AGPL / 未知） | 放进 CI 的一行 |

依赖升级节奏：每月一次小版本升级，安全告警即时处理。**升级必须过 CI——不看日志的升级等于没升。**

## 四、发布流水线

- 打 tag 触发构建与发布（`templates/release.yml`）。
- 产物带校验：哈希或签名，让下载的人能验证来源。
- 每个 release 要有 **tag、说明、对应的 CHANGELOG 段落**三件；只有 tag 没有说明，使用者不知道要不要升级。
- 发布凭据、签名密钥属于权限边界内的动作：代理不碰，要你显式批准并最好亲手做。

## 五、版本与变更日志

语义化版本三句话：主版本号是破坏性变更，次版本号是向后兼容的新功能，补丁号是向后兼容的修复。

判断一个变更是否破坏性，问三个问题——任一为「是」，就是主版本：

1. 有没有人依赖现在这个行为？
2. 旧调用会不会报错？
3. 数据格式变了吗？

CHANGELOG 按 Keep a Changelog 组织，六段：`Added` / `Changed` / `Deprecated` / `Removed` / `Fixed` / `Security`。骨架见 `templates/changelog.md`。

- 它面向使用者，不是 commit 记录的抄写：**同一个功能的三次提交，在日志里是一行**。
- 破坏性变更写在 `Changed` 段首行，并给出迁移说明。
- 未发布的改动放 `[Unreleased]`。
- 刚开始可以先发 0.x，明确声明接口还会变——这比硬撑 1.0 再破坏一次体面得多。

## 六、没有 CI 平台时的退路

1. 在 `CONTRIBUTING.md` 里写清本地要跑哪几条命令（和提交前自查清单是同一套）。
2. 在同一处**明确说明当前没有自动检查**——诚实比假装好。
3. 把"合并前必须本地跑过 + 必须有人看过 diff"写成显式规则，并注明这是靠自觉。
4. 有条件时，哪怕只搭一条"安装 + test"的流水线，也比零条强：它至少能把"依赖装不上"这类问题挡在合并前。
