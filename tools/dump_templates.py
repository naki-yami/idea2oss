# -*- coding: utf-8 -*-
"""从外部生成器（scaffold_project.py）里导出模板到本仓库的 templates/。

用法：
    python tools/dump_templates.py                      # 写回本仓库 templates/
    python tools/dump_templates.py --out <目录>          # 写到别处（非破坏性重放，用来验证 D-08）
    python tools/dump_templates.py --scaffold <路径>     # 指定生成器位置

为什么要这个脚本：模板的事实来源是生成器，`templates/` 只是导出物（决议 D-08）。
两处手写件——`INDEX.md`（索引）与 `manual-review.md`（附录 A6）——不在导出范围内，重放时要排除。

注意：生成器不在本仓库内（它是流程手册的工具链）。没装生成器时本脚本会明确报错，
而不是写出一堆空文件。
"""
import argparse
import importlib.util
import os
import sys

DEFAULT_SCAFFOLD = r"C:\Users\Administrator\Desktop\新建文件夹\scaffold_project.py"
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HANDWRITTEN = ("INDEX.md", "manual-review.md")   # 不是导出物，见上面说明

MAP = [
    ("readme_l0", "readme-l0.md"),
    ("readme_l1", "readme-l1.md"),
    ("readme_l2", "readme.md"),
    ("gitignore", "gitignore.txt"),
    ("context", "CONTEXT.md"),
    ("brief", "brief.md"),
    ("spec", "spec.md"),
    ("ledger", "ledger.md"),
    ("ticket", "ticket.md"),
    ("adr_template", "adr.md"),
    ("pr_template", "pr.md"),
    ("handoff", "handoff.md"),
    ("architecture", "architecture.md"),
    ("runbook", "runbook.md"),
    ("onboarding", "onboarding.md"),
    ("contributing", "contributing.md"),
    ("security", "security.md"),
    ("coc", "code-of-conduct.md"),
    ("changelog", "changelog.md"),
    ("agents_md", "AGENTS.md.tpl"),      # 后缀是有意的：模板不能被运行时当成生效的 AGENTS.md
    ("issue_tracker", "issue-tracker.md"),
    ("triage_labels", "triage-labels.md"),
    ("domain", "domain.md"),
    ("ci_yml", "ci.yml"),
    ("release_yml", "release.yml"),
    ("issue_bug", "issue-bug.md"),
    ("issue_feature", "issue-feature.md"),
    ("codeowners", "CODEOWNERS"),
    ("dependabot", "dependabot.yml"),
    ("env_example", "env.example"),
    ("editorconfig", "editorconfig.txt"),
    ("specs_index", "specs-index.md"),
    ("license_todo", "license-todo.txt"),
]

HEADER = """<!-- idea2oss 模板 · 来自《AI 结对开发流程手册 V3》附录 A/B ｜ 复制过去改内容，结构不要改 -->

"""


def load_scaffold(path):
    spec = importlib.util.spec_from_file_location("scaffold_project", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv=None):
    ap = argparse.ArgumentParser(description="从生成器重放 templates/")
    ap.add_argument("--out", default=os.path.join(REPO, "templates"),
                    help="导出目录，默认写回本仓库 templates/")
    ap.add_argument("--scaffold", default=DEFAULT_SCAFFOLD,
                    help="生成器路径（事实来源，不在本仓库内）")
    args = ap.parse_args(argv)

    if not os.path.exists(args.scaffold):
        print(f"找不到生成器：{args.scaffold}", file=sys.stderr)
        print("用 --scaffold <路径> 指定，或手工维护 templates/（重放不是使用模板的前提）。", file=sys.stderr)
        return 2

    mod = load_scaffold(args.scaffold)
    T, META, BANNER = mod.T, mod.META, mod.BANNER
    os.makedirs(args.out, exist_ok=True)
    written = 0
    for key, fname in MAP:
        text = T.get(key)
        if text is None:
            print(f"  ! 生成器里缺模板: {key}")
            continue
        body = text.format(name="<项目名>", feature="<feature>")
        step, crit = META.get(key, ("", ""))
        if not body.strip():
            continue
        banner = BANNER.format(step=step, crit=crit) if step else HEADER.strip()
        content = HEADER + banner + "\n" + body if step else HEADER + body
        with open(os.path.join(args.out, fname), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(content)
        written += 1
        print(f"  + {fname}")
    print(f"共写出 {written} 份 -> {args.out}")
    print(f"手写件（不导出，重放时请排除）：{', '.join(HANDWRITTEN)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
