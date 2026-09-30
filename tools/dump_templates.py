# -*- coding: utf-8 -*-
"""从 scaffold_project.py 里导出模板到 idea2oss/templates/（单一事实来源，避免两处维护）。"""
import importlib.util
import os
import sys

SCAFFOLD = r"C:\Users\Administrator\Desktop\新建文件夹\scaffold_project.py"
OUT = r"D:\dsh\idea2oss\templates"

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
    ("agents_md", "AGENTS.md"),
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


def main():
    mod = load_scaffold(SCAFFOLD)
    T, META, BANNER = mod.T, mod.META, mod.BANNER
    os.makedirs(OUT, exist_ok=True)
    written = 0
    for key, fname in MAP:
        text = T.get(key)
        if text is None:
            print(f"  ! 缺模板: {key}")
            continue
        body = text.format(name="<项目名>", feature="<feature>")
        step, crit = META.get(key, ("", ""))
        if not body.strip():
            continue
        banner = BANNER.format(step=step, crit=crit) if step else HEADER.strip()
        content = HEADER + banner + "\n" + body if step else HEADER + body
        with open(os.path.join(OUT, fname), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(content)
        written += 1
        print(f"  + templates/{fname}")
    print(f"共写出 {written} 份模板 -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
