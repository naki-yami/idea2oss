# -*- coding: utf-8 -*-
"""把 idea2oss 技能集安装到 DSH 的技能目录。

用法：
    python tools/install.py                     # 安装到 D:\\dsh\\.dsh\\skills（工作区技能）
    python tools/install.py --target D:\\proj   # 安装到别的项目
    python tools/install.py --link              # 建目录联接（junction），改源码立即生效，不用重装
    python tools/install.py --list              # 看当前装了哪些、是不是联接
    python tools/install.py --uninstall         # 卸载（只删指向本仓库的联接/副本）
    python tools/install.py --dry-run

说明：
  - 默认是**复制**；--link 用 Windows 目录联接（junction），适合边开发边用。
  - 已存在同名技能时默认跳过；要覆盖加 --force。
  - 不碰任何不是本仓库装上去的东西（卸载时会核对联接目标）。
"""
from __future__ import annotations

import argparse
import filecmp
import os
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(REPO, "skills")
DEFAULT_TARGET = r"D:\dsh"


def skill_names():
    return sorted(d for d in os.listdir(SKILLS)
                  if os.path.isdir(os.path.join(SKILLS, d))
                  and os.path.exists(os.path.join(SKILLS, d, "SKILL.md")))


def dest_root(target):
    return os.path.join(os.path.abspath(target), ".dsh", "skills")


def is_junction(path):
    try:
        out = subprocess.run(["cmd", "/c", "dir", "/AL", os.path.dirname(path)],
                             capture_output=True, text=True, encoding="gbk", errors="replace")
        return os.path.basename(path) in (out.stdout or "") and "<JUNCTION>" in (out.stdout or "")
    except Exception:
        return False


def make_junction(src, dst):
    if os.path.exists(dst):
        return False
    r = subprocess.run(["cmd", "/c", "mklink", "/J", dst, src],
                       capture_output=True, text=True, encoding="gbk", errors="replace")
    return r.returncode == 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default=DEFAULT_TARGET, help="项目目录（技能装到 <target>\\.dsh\\skills）")
    ap.add_argument("--link", action="store_true", help="建目录联接而不是复制")
    ap.add_argument("--force", action="store_true", help="覆盖已存在的技能")
    ap.add_argument("--list", action="store_true", help="只列出目标目录里已装的技能")
    ap.add_argument("--uninstall", action="store_true", help="卸载本仓库装上去的技能")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = dest_root(args.target)
    names = skill_names()

    if args.list:
        print(f"目标：{root}")
        if not os.path.isdir(root):
            print("  （目录不存在，尚未安装）")
            return 0
        for d in sorted(os.listdir(root)):
            p = os.path.join(root, d)
            mark = "联接" if is_junction(p) else "副本"
            print(f"  {mark}  {d}")
        return 0

    if args.uninstall:
        removed = 0
        for name in names:
            dst = os.path.join(root, name)
            if not os.path.exists(dst):
                continue
            if is_junction(dst):
                if not args.dry_run:
                    os.rmdir(dst)
                print(f"  - 卸载联接 {name}")
                removed += 1
            else:
                # 只删与本仓库内容一致的副本
                src = os.path.join(SKILLS, name)
                same = filecmp.dircmp(src, dst).diff_files == [] and \
                    filecmp.dircmp(src, dst).left_only == []
                if same or args.force:
                    if not args.dry_run:
                        shutil.rmtree(dst)
                    print(f"  - 卸载副本 {name}")
                    removed += 1
                else:
                    print(f"  ! 跳过 {name}：内容与本仓库不一致，不是我们装的")
        print(f"卸载 {removed} 个")
        return 0

    if not args.dry_run:
        os.makedirs(root, exist_ok=True)
    done, skipped = [], []
    for name in names:
        src = os.path.join(SKILLS, name)
        dst = os.path.join(root, name)
        if os.path.exists(dst) and not args.force:
            skipped.append(name)
            continue
        if args.dry_run:
            done.append(name)
            continue
        if os.path.exists(dst) and args.force:
            if is_junction(dst):
                os.rmdir(dst)
            else:
                shutil.rmtree(dst)
        if args.link:
            ok = make_junction(src, dst)
            if not ok:
                shutil.copytree(src, dst)
                print(f"  ! {name}: 建联接失败，已改为复制")
        else:
            shutil.copytree(src, dst)
        done.append(name)

    mode = "联接（--link）" if args.link else "复制"
    print(f"目标：{root}")
    print(f"模式：{mode}")
    print(f"安装 {len(done)} 个：{', '.join(done) if done else '（无）'}")
    if skipped:
        print(f"跳过已存在 {len(skipped)} 个：{', '.join(skipped)}（要覆盖加 --force）")
    if not args.dry_run and done:
        print("\n下一步：新开一个会话，技能目录才会被重新扫描；之后可用 /idea2oss 或直接说需求触发。")
    if args.dry_run:
        print("\n（--dry-run：未写盘）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
