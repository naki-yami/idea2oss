# -*- coding: utf-8 -*-
r"""idea2oss 技能集校验器。

检查项：
  1. 每个 skills/<name>/SKILL.md 存在，且 frontmatter 三字段齐全（name / description / whenToUse）
  2. frontmatter 的 name == 目录名
  3. description 里有 keywords（英文关键词，保证英文环境触发）
  4. 八节骨架标题齐全
  5. SKILL.md 行数在 80–240 之间
  6. 「完成判据」节里至少 4 条 `- [ ]`
  7. 「手工兜底」节非空
  8. 交叉引用：`→ 调用 \`x\`` 里的 x 必须是本集真实技能；templates/ 引用必须真实存在
  9. 没有孤儿技能（每个技能至少被另一个技能引用，入口技能除外）

用法：python tools/validate_skills.py [--root D:\\dsh\\idea2oss]
退出码 0 = 全过；1 = 有错误。
"""
from __future__ import annotations

import argparse
import os
import re
import sys

SECTIONS = [
    "## 何时用 / 何时不用",
    "## 输入（开工前必须到手的）",
    "## 动作",
    "## 产出物",
    "## 完成判据",
    "## 手工兜底",
    "## 下一步",
    "## 反模式",
]

ENTRY_SKILL = "idea2oss"          # 入口技能，允许不被别人引用
CALL_RE = re.compile(r"调用\s*`([a-z0-9][a-z0-9-]*)`")
TEMPLATE_RE = re.compile(r"templates/([A-Za-z0-9._\-]+)")


def parse_frontmatter(text: str):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    raw = text[3:end].strip("\n")
    body = text[end + 4:]
    fm = {}
    for line in raw.splitlines():
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
        elif line.startswith((" ", "\t")) and fm:
            last = list(fm)[-1]
            fm[last] += " " + line.strip()
    return fm, body


def section_text(body: str, title: str) -> str:
    idx = body.find(title)
    if idx == -1:
        return ""
    rest = body[idx + len(title):]
    m = re.search(r"\n## ", rest)
    return rest[:m.start()] if m else rest


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    skills_dir = os.path.join(root, "skills")
    templates_dir = os.path.join(root, "templates")

    names = sorted(d for d in os.listdir(skills_dir)
                   if os.path.isdir(os.path.join(skills_dir, d)))
    errors, warns = [], []
    referenced = {}

    for name in names:
        path = os.path.join(skills_dir, name, "SKILL.md")
        rel = f"skills/{name}/SKILL.md"
        if not os.path.exists(path):
            errors.append(f"{rel}: 文件不存在")
            continue
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        lines = text.count("\n") + 1

        fm, body = parse_frontmatter(text)
        if fm is None:
            errors.append(f"{rel}: 缺 frontmatter")
            continue
        for field in ("name", "description", "whenToUse"):
            if not fm.get(field):
                errors.append(f"{rel}: frontmatter 缺 {field}")
        if fm.get("name") != name:
            errors.append(f"{rel}: name={fm.get('name')!r} 与目录名不符")
        if "keywords:" not in fm.get("description", ""):
            warns.append(f"{rel}: description 里没有 keywords:")
        if len(fm.get("description", "")) > 400:
            warns.append(f"{rel}: description 过长（{len(fm['description'])} 字）")

        for sec in SECTIONS:
            if sec not in body:
                errors.append(f"{rel}: 缺小节 {sec}")

        if not (80 <= lines <= 240):
            warns.append(f"{rel}: 行数 {lines}，超出 80–240")

        judges = re.findall(r"^\s*- \[ \]", section_text(body, "## 完成判据"), re.M)
        if len(judges) < 4:
            errors.append(f"{rel}: 完成判据只有 {len(judges)} 条（至少 4 条）")

        fallback = section_text(body, "## 手工兜底").strip()
        if len(fallback) < 30:
            errors.append(f"{rel}: 手工兜底节过短或为空")

        for target in CALL_RE.findall(body):
            referenced.setdefault(target, set()).add(name)
            if target not in names:
                errors.append(f"{rel}: 调用了不存在的技能 `{target}`")

        for tpl in set(TEMPLATE_RE.findall(body)):
            if not os.path.exists(os.path.join(templates_dir, tpl)):
                errors.append(f"{rel}: 引用了不存在的模板 templates/{tpl}")

    for name in names:
        if name == ENTRY_SKILL:
            continue
        if name not in referenced:
            warns.append(f"skills/{name}/SKILL.md: 没有被任何技能引用（孤儿）")

    print(f"技能数：{len(names)}  ->  {', '.join(names)}")
    print(f"模板数：{len([f for f in os.listdir(templates_dir) if os.path.isfile(os.path.join(templates_dir, f))])}")
    print("-" * 60)
    for w in warns:
        print("  warn  " + w)
    for e in errors:
        print("  ERROR " + e)
    print("-" * 60)
    print(f"结果：{len(errors)} 个错误，{len(warns)} 个警告")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
