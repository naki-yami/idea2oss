# -*- coding: utf-8 -*-
r"""依赖许可门禁（D-12）：列出已安装包各自是什么许可，把 GPL / AGPL / 未知的挑出来。

    python tools/check_licenses.py                 # 扫当前解释器环境（默认）
    python tools/check_licenses.py --json          # 给 CI 吃的机器可读输出
    python tools/check_licenses.py --report x.json # 也认 pip-licenses 的 JSON 报告

为什么不用 pip-licenses（本仓库踩过的坑，记在这里免得下次再踩）：
  1. 它读的是包元数据里的旧字段 `License:`。而按 PEP 639，新发布的包把许可写在
     `License-Expression:` 里，`License:` 是空的——于是它对 pip / setuptools / prettytable
     **一行都判不出来，直接输出空清单 `[]`**。CI 里"空清单按失败处理"的守卫随即触发，
     门禁在什么都没做的情况下永远红（ci #1–#5 全红就是这个）。
  2. 装 setuptools 不管用——空清单不是枚举失败，是许可解析不出来。
  3. 它还得额外装第三方包，与本项目的 D-06（只用标准库）冲突。

本工具只依赖标准库：许可按 `License-Expression` → classifiers → `License` 三级回退解析。

退出码：0 = 只有放行许可；1 = 有需要单独评估的项（GPL / AGPL / 未知 / 空）。
"""
from __future__ import annotations

import argparse
import json
import sys

BANNED = ("GPL", "AGPL")      # LGPL 里含 GPL，一并拦下——传染性许可要单独评估

# 解释器自带的打包工具，不是项目依赖。默认忽略，理由：
#   · 门禁该管的是「项目拉了哪些依赖」，不是「这台解释器自带什么」；
#   · 它们的许可元数据本身也不可靠——Python 3.9 的 runner 上 setuptools 三个许可字段
#     全是空的（3.13 上写的是 MIT），拿它当"未声明依赖"卡构建，就是自己给自己找红。
# 忽略不等于看不见：跑的时候会把忽略了哪几个打出来。
BOOTSTRAP = ("pip", "setuptools", "wheel")


def resolve_license(meta) -> str:
    """三级回退解析一个包的许可：PEP 639 表达式 → classifiers → 旧 License 字段。"""
    # 1) PEP 639（新包走这里）
    expr = (meta.get("License-Expression") or "").strip()
    if expr:
        return expr
    # 2) Trove classifiers
    for c in (meta.get_all("Classifier") or []):
        if c.startswith("License ::"):
            return c.split("::")[-1].strip()
    # 3) 旧字段（可能是整篇许可证正文，截断显示）
    legacy = (meta.get("License") or "").strip()
    if legacy:
        first = legacy.splitlines()[0].strip()
        return first[:60] if first else legacy[:60]
    return ""


def scan_env():
    import importlib.metadata as md
    rows = []
    for dist in md.distributions():
        meta = dist.metadata
        name = meta.get("Name") or "?"
        version = meta.get("Version") or ""
        rows.append({"Name": name, "Version": version, "License": resolve_license(meta)})
    return sorted(rows, key=lambda r: r["Name"].lower())


def judge(rows):
    bad = []
    for row in rows:
        lic = str(row.get("License", "")).strip()
        upper = lic.upper()
        if not upper or any(b in upper for b in BANNED):
            bad.append((row.get("Name", "?"), lic or "（未声明）"))
    return bad


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="依赖许可门禁（标准库实现）")
    ap.add_argument("--report", help="改用一份 pip-licenses JSON 报告，而不是扫当前环境")
    ap.add_argument("--json", action="store_true", help="输出机器可读结果")
    ap.add_argument("--ignore", action="append", default=[],
                    help="额外忽略的包名（可重复）。默认已忽略 pip / setuptools / wheel")
    args = ap.parse_args(argv)

    if args.report:
        try:
            with open(args.report, encoding="utf-8") as fh:
                rows = json.load(fh)
        except FileNotFoundError:
            print(f"找不到报告文件：{args.report}", file=sys.stderr)
            return 1
        except json.JSONDecodeError as exc:
            print(f"报告不是合法 JSON（{exc}）", file=sys.stderr)
            return 1
        if not rows:
            print("报告里 0 个包——这不是「没有违规依赖」，是生成报告的那一步没工作。",
                  file=sys.stderr)
            return 1
    else:
        rows = scan_env()

    ignore = {n.lower() for n in list(args.ignore) + list(BOOTSTRAP)}
    skipped = sorted(r["Name"] for r in rows if r["Name"].lower() in ignore)
    rows = [r for r in rows if r["Name"].lower() not in ignore]

    bad = judge(rows)
    if args.json:
        print(json.dumps({"scanned": len(rows), "ignored": skipped,
                          "flagged": [b[0] for b in bad],
                          "rows": rows}, ensure_ascii=False, indent=2))
        return 1 if bad else 0

    print(f"扫描到 {len(rows)} 个已安装包"
          + (f"（另有 {len(skipped)} 个解释器自带的打包工具已忽略：{', '.join(skipped)}）"
             if skipped else ""))
    print("（扫的是当前解释器环境；CI 的 runner 环境干净，本地可能带上你自己装的无关包）")
    if not bad:
        worst = ", ".join(sorted({r["License"] for r in rows if r["License"]})[:6])
        print(f"没有 GPL / AGPL / 未声明许可的依赖。（看到的许可：{worst}）")
        return 0

    print("以下依赖的许可需要单独评估（GPL / AGPL / 未声明）：")
    for name, lic in bad:
        print(f"  ✗ {name}  ->  {lic}")
    print("处理方式：换成宽松许可的替代品，或在 docs/decisions.md 里记一条决议说明为什么接受它。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
