# -*- coding: utf-8 -*-
r"""tools/ 三个命令行入口的行为测试——只挂在三个真接缝上（见 docs/architecture.md）。

    S1  validate_skills.py  技能契约 + 退出码
    S2  check_project.py    结构判据结果（--json）+ 退出码
    S3  install.py          安装行为（--list / --dry-run）

原则（spec 第 5 节 / D-03）：**只通过 subprocess 调命令行，断言退出码与输出里的关键词**，
不断言实现细节（不 import 内部函数、不断言函数名与调用顺序）。工具的写法随便改，
只要这三个接缝的对外行为不变，本文件一行都不用动。

跑法（仓库根）：
    python -m unittest discover -s tests -v

零第三方依赖，Python 3.8+ 标准库（D-06）。
Windows：一律用 sys.executable 起子进程，text=True + encoding="utf-8" + errors="replace"，
并给子进程加 PYTHONUTF8=1，避免控制台代码页（GBK）把中文输出变成乱码。
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest

# tests/ 的上一级就是仓库根：本文件被拷走后仍能算对
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(REPO, "tools")

# Windows 上给子进程一个能输出中文的环境；顺带让本地与 CI 行为一致
CHILD_ENV = dict(os.environ)
CHILD_ENV["PYTHONUTF8"] = "1"
CHILD_ENV["PYTHONIOENCODING"] = "utf-8"


def run_tool(*args, cwd=REPO):
    """跑一个 tools/ 下的脚本，返回 (退出码, stdout+stderr 全文)。"""
    cmd = [sys.executable] + [str(a) for a in args]
    proc = subprocess.run(cmd, cwd=cwd, env=CHILD_ENV,
                          capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


# --------------------------------------------------------------------------
# 造一个"合法技能集"当作夹具：只有它合法，才是对"坏的那一处"做对照
# --------------------------------------------------------------------------

SKILL_TEMPLATE = """# 测试技能

> 对应手册第 N 步 ｜ 产出物：<文件/字段> ｜ 完成判据：<一句话>

## 何时用 / 何时不用

- 用它：当你要验证 S1 的行为时——技能集改过名、加过技能、动过交叉引用。
- 用它：当 CI 报出技能契约错误，你要在本地复现时。
- 用它：当你把技能集拷到新环境，先确认契约没被环境差异弄坏时。
- 不用它：当技能集本身还没写完时，写了也校验不过。
- 不用它：当你只想看某个技能的正文时，直接读 `SKILL.md`。
- 不用它：当你要检查的是仓库结构而不是技能契约时，那是体检器（S2）的活。

## 输入（开工前必须到手的）

| 输入 | 从哪来 | 缺了怎么办 |
|---|---|---|
| 仓库根目录 | `--root` 参数 | 停下，先问清是哪个仓库 |
| 技能目录 | `<root>/skills/` | 建目录，一个技能一个子目录 |
| 模板目录 | `<root>/templates/` | 建目录；交叉引用要指到真实文件 |
| 待校验的改动 | 你自己的分支 | 先提交，别边改边校 |
| 八节标题清单 | 技能编写契约 | 照抄标题，别凭记忆写 |
| 退出码约定 | 0 全过 / 1 有错 | 先谈定，否则 CI 接不上 |

## 动作

1. **列出技能**：读 `<root>/skills/` 下的每个目录，跳过文件。
   做到什么程度算完：你能报出一共有几个技能、都叫什么。
2. **查 frontmatter**：每个 `SKILL.md` 必须有 `name` / `description` / `whenToUse`。
   做到什么程度算完：缺哪个字段，错误文本里就有哪个字段名。
3. **查身份一致**：frontmatter 的 `name` 必须等于目录名。
   做到什么程度算完：不一致时打印 `name=... 与目录名不符`。
4. **查八节骨架**：八个 `##` 标题一个都不能改名或缺失。
   做到什么程度算完：缺哪节就报哪节，标题照抄。
5. **查判据条数**：「完成判据」节里至少 4 条 `- [ ]`。
   做到什么程度算完：少于 4 条时报出实际条数。
6. **查手工兜底**：「手工兜底」节不能空——它是这套技能集的卖点。
   做到什么程度算完：这一节短于一行实际内容就报错。
7. **查交叉引用**：正文里出现的「调用 + 反引号包住的技能名」必须是真实技能，
   `templates/...` 必须是真实文件。
   做到什么程度算完：指向不存在的目标时，错误文本里能读到那个名字。
8. **查关键词**：`description` 末尾要有英文 `keywords:`，保证英文环境也能触发。
   做到什么程度算完：没有就出警告，不拦合并。
9. **查孤儿**：每个技能至少被另一个技能引用，入口技能除外。
   做到什么程度算完：没人引用的技能列进警告里。
10. **汇总**：按严重程度分开列警告与错误，最后给出退出码。
    做到什么程度算完：有错误返回 1，只有警告返回 0。

## 产出物

- 一份人读结果：技能清单、模板数、逐条警告与错误、结果汇总行。
- 一个退出码：0 = 契约成立，1 = 有错误（可直接当 CI 门禁）。
- 一份可复现的判据：把命令连同退出码贴进票据的 `Verify:` 行。
- 一份可直接回给贡献者的错误清单：哪一行、缺什么、怎么改。

## 完成判据

- [ ] 每一节都有内容，没有空节。
- [ ] 结果条数与输入条数对得上，不多不少。
- [ ] 退出码 0 表示全过，1 表示有错，没有第三种含义。
- [ ] 错误文本里能指到具体文件与具体字段，不含"出错了"这类空话。
- [ ] 警告不影响退出码：行数、孤儿技能只提示，不拦合并。
- [ ] 八个标题按名字精确匹配：改名就是缺节，不留模糊空间。

## 手工兜底

- 工具不可用时：照着上面的判据逐条人工核对，把结论写进票据的 `Accept:` 行，
  一条判据一行；没核对过的不许打勾。
- 只有 grep 时：`grep -rn "^name:" skills/*/SKILL.md` 逐个对目录名，八节标题用
  `grep -c "^## " skills/*/SKILL.md` 粗查一遍。
- 环境里连 Python 都没有：改用编辑器的目录树核对"一个技能一个目录一份 SKILL.md"，
  这一步能查出来的问题比你想的多。
- 拿不准某节是否合规：把那节原文和技能编写契约并排放，逐行对，别凭印象判断。
- 一时找不到契约文件：先把判据抄进票据，再跑工具——判据在票据里比在脑子里可靠。
- 工具报的错看不懂：把错误原文整段贴给一个全新会话，附上 `skills/<name>/SKILL.md` 的路径，
  只让它回答"缺哪一节、怎么补"，不让它改文件。
- 结论要留痕：把命令、退出码、时间写进票据的 `## Comments`，下一个会话才接得住。
- 技能集是别人交来的：先跑一遍工具留基线，再动手改——否则你分不清哪些问题是你引入的。

## 下一步

→ 回第 0 步，确认这件事还值不值得做。

## 反模式

| 反模式 | 为什么错 | 改成 |
|---|---|---|
| 判据写成"做完了" | 谁都能勾上，等于没写 | 写成能跑的一条命令 |
| 出错只打印不返回码 | CI 拦不住，门禁形同虚设 | 有错就 return 1 |
| 把警告当错误 | 噪音太大，真错误被淹没 | 警告只提示，不拦合并 |
| 校验器顺手改文件 | 校验和修改混在一起，没人敢跑 | 校验器只说不通过 |
| 八节标题随手改同义词 | 机器只认精确标题，改了就是缺节 | 标题照抄契约 |
| 技能里写死别的技能的名字 | 那个技能一改名，这句引用就指错 | 只引用本集存在、且不打算改名的技能 |
| 判据只写在正文、不写进票据 | 交付时没人记得去查，等于没写 | 把命令连同预期结果抄进票据的 `Verify:` |
| 让校验器顺手把警告也修了 | 校验器一旦会写文件，就没人敢在脏工作区跑它 | 警告只提示，改动由人做 |
| 测试断言工具的中间变量 | 重构一次就红，测试反过来挡路 | 只断言退出码与输出字段 |
| 给校验器加"忽略这一项"的开关 | 门禁一旦可以绕过，就等于没有门禁 | 要么修问题，要么把该项降成警告 |
"""


def write_skill_set(root, name="good-skill", body=SKILL_TEMPLATE, front_name=None):
    """在 root 下造一个最小技能集：skills/<name>/SKILL.md + templates/ 目录。

    templates/ 必须有目录——S1 会去数它有多少个模板文件。
    """
    os.makedirs(os.path.join(root, "templates"), exist_ok=True)
    skill_dir = os.path.join(root, "skills", name)
    os.makedirs(skill_dir, exist_ok=True)
    real_name = front_name if front_name is not None else name
    text = (
        "---\n"
        f"name: {real_name}\n"
        "description: 测试用技能：校验技能契约时当夹具。keywords: fixture, skill contract\n"
        "whenToUse: 只在跑单元测试时。\n"
        "---\n"
        "\n"
        + body
    )
    path = os.path.join(skill_dir, "SKILL.md")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    return path


class S1ValidateSkills(unittest.TestCase):
    """S1：技能契约是否成立，只认退出码和错误文本。"""

    def test_real_repo_passes(self):
        """真实仓库的技能集必须过——这是本仓库自己的门禁。"""
        code, out = run_tool(os.path.join(TOOLS, "validate_skills.py"), "--root", REPO)
        self.assertEqual(code, 0, f"真实仓库未通过 S1：\n{out}")
        self.assertIn("结果：", out, "没看到结果汇总行，工具的输出契约变了")

    def test_minimal_valid_skill_set_passes(self):
        """对照夹具：只有一处毛病的坏技能之外，合法技能集必须是 0。"""
        with tempfile.TemporaryDirectory() as tmp:
            # 夹具自己得在 S1 的行数区间内，否则"合法"就是自欺欺人
            self.assertTrue(80 <= len(SKILL_TEMPLATE.splitlines()) <= 240,
                            f"夹具行数 {len(SKILL_TEMPLATE.splitlines())} 超出 S1 的 80–240")
            write_skill_set(tmp)
            code, out = run_tool(os.path.join(TOOLS, "validate_skills.py"), "--root", tmp)
            self.assertEqual(code, 0, f"合法技能集竟然没过：\n{out}")

    def test_missing_section_fails(self):
        """缺一节 → 退出码 1，且错误文本点到"缺小节"。"""
        with tempfile.TemporaryDirectory() as tmp:
            # 把「手工兜底」整节拿掉，其余保持合法：只留这一处毛病当对照
            before, _, after = SKILL_TEMPLATE.partition("## 手工兜底")
            _, _, rest = after.partition("\n## 下一步")
            body = before + "## 下一步" + rest
            self.assertNotIn("## 手工兜底", body)
            write_skill_set(tmp, body=body)
            code, out = run_tool(os.path.join(TOOLS, "validate_skills.py"), "--root", tmp)
            self.assertEqual(code, 1, f"缺小节竟然通过了：\n{out}")
            self.assertIn("缺小节", out, out)

    def test_name_mismatch_fails(self):
        """frontmatter 的 name 与目录名不符 → 退出码 1，错误文本含"与目录名不符"。"""
        with tempfile.TemporaryDirectory() as tmp:
            write_skill_set(tmp, name="dir-name", front_name="other-name")
            code, out = run_tool(os.path.join(TOOLS, "validate_skills.py"), "--root", tmp)
            self.assertEqual(code, 1, f"name 与目录名不符竟然通过了：\n{out}")
            self.assertIn("与目录名不符", out, out)

    def test_unknown_skill_reference_fails(self):
        """正文调用了本集不存在的技能 → 退出码 1，错误文本含"调用了不存在的技能"。"""
        with tempfile.TemporaryDirectory() as tmp:
            body = SKILL_TEMPLATE.replace(
                "→ 回第 0 步，确认这件事还值不值得做。",
                "→ 调用 `nonexistent-helper-skill` 接着做。")
            write_skill_set(tmp, body=body)
            code, out = run_tool(os.path.join(TOOLS, "validate_skills.py"), "--root", tmp)
            self.assertEqual(code, 1, f"引用不存在的技能竟然通过了：\n{out}")
            self.assertIn("调用了不存在的技能", out, out)


class S2CheckProject(unittest.TestCase):
    """S2：结构判据结果。断言 JSON 的字段与计数自洽，不断言具体项的实现。"""

    STATUSES = {"OK", "MISS", "WARN", "NA"}
    FIELDS = {"id", "title", "status", "detail", "fix", "level"}

    def check_json(self, *args):
        """跑 --json，返回 (退出码, 解析后的对象)。

        体检器有强制项未过时**故意**返回 1，所以这里不能 assert 退出码为 0——
        退出码本身是被断言的对象（见 test_real_repo_json_shape）。
        """
        code, out = run_tool(os.path.join(TOOLS, "check_project.py"), *args, "--json")
        try:
            data = json.loads(out)
        except json.JSONDecodeError as exc:  # 输出不是 JSON，直接给出原文
            self.fail(f"--json 的输出不是合法 JSON（{exc}）：\n{out[:2000]}")
        return code, data

    def assert_self_consistent(self, data, level):
        """三条硬契约：计数自洽、档位回显、每条结果字段齐全。"""
        results = data["results"]
        self.assertEqual(data["level"], level, "回显的档位与传入的不一致")
        self.assertEqual(
            data["ok"] + data["missing"] + data["warn"] + data["not_applicable"],
            len(results), "ok/missing/warn/not_applicable 之和与结果条数不等")
        for row in results:
            self.assertTrue(self.FIELDS <= set(row), f"结果缺字段：{sorted(row)}")
            self.assertIn(row["status"], self.STATUSES, f"未知状态：{row['status']}")
            self.assertTrue(row["title"], "结果条目的 title 为空")
        return results

    def test_real_repo_json_shape(self):
        """真实仓库：--json 是给 CI 吃的，结构必须自洽，且退出码与 missing 一致。"""
        code, data = self.check_json("--dir", REPO)
        results = self.assert_self_consistent(data, "L2")
        self.assertGreater(len(results), 0, "一条结果都没有，体检器没在干活")
        # 每个结果都标了它属于哪个档位
        for row in results:
            self.assertIn(row["level"], ("L0", "L1", "L2"), f"未知档位：{row['level']}")
        # 退出码契约（D-05）：有强制项缺失就是 1，没有就是 0
        self.assertEqual(code, 1 if data["missing"] else 0,
                         f"退出码与 missing={data['missing']} 不一致")

    def test_empty_dir_reports_readme_and_gitignore_missing(self):
        """空目录：L0 只强制 4 项，README 与 .gitignore 必在其中。"""
        with tempfile.TemporaryDirectory() as tmp:
            code, data = self.check_json("--dir", tmp, "--level", "L0")
            self.assert_self_consistent(data, "L0")
            self.assertEqual(code, 1, "空目录不该全过")
            missing = [r for r in data["results"] if r["status"] == "MISS"]
            missing_ids = {r["id"] for r in missing}
            missing_text = " ".join(r["id"] + r["title"] for r in missing)
            self.assertIn("readme", missing_ids, f"空目录没报 README：{missing_text}")
            self.assertIn("gitignore", missing_ids, f"空目录没报 .gitignore：{missing_text}")
            self.assertIn("README", missing_text)
            self.assertIn(".gitignore", missing_text)
            # 每条缺失项都得给出"先补什么"，空目录的用法就是"告诉我先补哪三件"
            for row in missing:
                self.assertTrue(row["fix"], f"{row['id']} 缺了却没给修复建议")
            # 空目录里没有票据/台账可查，L0 下这些项不该算缺失
            self.assertGreater(data["not_applicable"], 0, "L0 应有大量不适用项")

    def test_broken_dir_fails(self):
        """只有一个 README 的目录：README 过、其余缺 → 退出码 1。"""
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "README.md"), "w", encoding="utf-8") as fh:
                fh.write("# 只有门面\n\n## 快速开始\n\n```\npython -c pass\n```\n\n## 为什么\n\n因为。\n\n## 限制\n\n很多。\n")
            code, data = self.check_json("--dir", tmp, "--level", "L0")
            self.assert_self_consistent(data, "L0")
            self.assertEqual(code, 1, "只有 README 的目录不该通过 L0")
            self.assertGreaterEqual(data["ok"], 1, "README 成段了却没算通过")


class S3Install(unittest.TestCase):
    """S3：安装行为。只在临时目录上跑，绝不碰使用者的真实技能目录。"""

    def test_list_on_empty_target(self):
        """--list 在没装过的目录上要能正常返回 0，并指出它看的是哪个目录。"""
        with tempfile.TemporaryDirectory() as tmp:
            code, out = run_tool(os.path.join(TOOLS, "install.py"),
                                 "--list", "--target", tmp)
            self.assertEqual(code, 0, f"--list 在空目录上返回了 {code}：\n{out}")
            self.assertIn(".dsh", out, f"--list 没说清目标目录：\n{out}")

    def test_dry_run_writes_nothing(self):
        """--dry-run 不许写盘：临时目录必须还是空的。"""
        with tempfile.TemporaryDirectory() as tmp:
            code, out = run_tool(os.path.join(TOOLS, "install.py"),
                                 "--dry-run", "--target", tmp)
            self.assertEqual(code, 0, f"--dry-run 返回了 {code}：\n{out}")
            left = os.listdir(tmp)
            self.assertEqual(left, [], f"--dry-run 竟然写盘了：{left}")
            self.assertIn("dry-run", out.lower(), "没看到 --dry-run 的提示语")

    def test_real_install_copies_skills(self):
        """真装一次（临时目录）：技能落在 <target>/.dsh/skills/ 下，且与仓库技能数一致。"""
        names = sorted(d for d in os.listdir(os.path.join(REPO, "skills"))
                       if os.path.isdir(os.path.join(REPO, "skills", d)))
        self.assertTrue(names, "仓库里一个技能都没有")
        with tempfile.TemporaryDirectory() as tmp:
            code, out = run_tool(os.path.join(TOOLS, "install.py"), "--target", tmp)
            self.assertEqual(code, 0, f"安装返回了 {code}：\n{out}")
            root = os.path.join(tmp, ".dsh", "skills")
            self.assertTrue(os.path.isdir(root), f"没建出目标目录：{root}")
            got = sorted(os.listdir(root))
            self.assertEqual(got, names, "装出来的技能集与仓库不一致")
            for name in names:
                self.assertTrue(
                    os.path.isfile(os.path.join(root, name, "SKILL.md")),
                    f"{name} 没装上 SKILL.md")

    def test_default_target_is_cwd(self):
        """不带 --target 时必须装到当前工作目录——README 的第一条命令就是它。

        这条是补出来的回归测试：`DEFAULT_TARGET` 曾经被改成 None，而 main() 忘了兜底，
        结果 README 的第一条命令直接抛 TypeError。抓到它的是陌生人测试（干净克隆照 README 做），
        不是单元测试——这就是为什么第 8 步的判据是"陌生人 30 分钟"，而不是"测试全绿"。
        """
        with tempfile.TemporaryDirectory() as tmp:
            code, out = run_tool(os.path.join(TOOLS, "install.py"), cwd=tmp)
            self.assertEqual(code, 0, f"不带 --target 时返回了 {code}：\n{out}")
            root = os.path.join(tmp, ".dsh", "skills")
            self.assertTrue(os.path.isdir(root), f"没装到当前工作目录：{root}")
            self.assertTrue(sorted(os.listdir(root)), "装是装上了，但一个技能都没有")


if __name__ == "__main__":
    unittest.main(verbosity=2)
