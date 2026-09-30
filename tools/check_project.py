# -*- coding: utf-8 -*-
r"""结构体检器：对照《项目结构与接手标准》扫描一个真实项目，把"判据"变成一条能跑的命令。

用法：
    python tools/check_project.py --dir D:\projects\my-app
    python tools/check_project.py --dir . --level L1        # L0/L1/L2，默认 L2
    python tools/check_project.py --dir . --json            # 给 CI 用
    python tools/check_project.py --dir . --quiet            # 只输出失败项

退出码：0 = 所有"强制项"通过；1 = 有强制项未通过（可直接当第 6/8 步的 Verify 命令）。

说明：它只查**存在性与可机械判断的一致性**，不查质量。
"测试是否挂在接缝上""文档是不是你要的"这类永远要人判断——那部分只有你的 Accept: 能负责。

其中「活文档里没有与事实相反的断言」一项，会拿文档里的断言去核对仓库事实
（远端 / tag / 用例数 / 工具入口数 / 判据条数 / 台账编号区间与条数 / 自报分数）。
**快照不参与核对**——CHANGELOG、票据、ADR 记的是某个时点发生了什么，改它们等于伪造证据。
取不到事实的项跳过并打印，不假装查过。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

SKIP_DIRS = {".git", "node_modules", "dist", "build", "out", ".venv", "venv",
             "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
             "coverage", ".idea", ".vscode", ".dsh", ".next", "target"}
LEVELS = ("L0", "L1", "L2")

# 测试文件所在的目录名（「N 个用例」这一项的事实来源）
TEST_DIRS = ("tests", "test", "spec", "__tests__")

# 「活文档」= 声明仓库**现在**长什么样的文档。只扫它们，快照不扫。
LIVE_DOCS = (r"^README\.md$", r"^CONTRIBUTING\.md$", r"^SECURITY\.md$",
             r"^CODE_OF_CONDUCT\.md$", r"^AGENTS\.md$", r"^GUIDE\.md$",
             r"^docs/[^/]+\.md$", r"^docs/agents/[^/]+\.md$")

# 快照：记的是「某个时点发生了什么」，回头改反而是伪造证据（CONTEXT.md 的「快照」条）
SNAPSHOT_DOCS = (r"^docs/release-checklist\.md$",)

# 文档自己声明「表里的数字都会过期、以文件里的实际内容为准」的（`docs/onboarding.md` 末段）：
# 它那里的数字是「文件还在不在」的路标，不是承诺，所以只核对非数字断言。
NUMBER_EXEMPT_DOCS = (r"^docs/onboarding\.md$",)

# 可证伪断言：只认指向**整个仓库**的写法。不认「N 个测试」——它常是局部计数
# （架构文档里「S6 一进仓库就带了 5 个测试」），泛化会带来假阳性。
REMOTE_CLAIM = re.compile(r"远端(还|也)?没接|还没接远端|计划托管在")
TAG_CLAIM = re.compile(r"git tag[^\n。]{0,14}?(空|没有)")
TEST_COUNT_CLAIM = re.compile(r"(\d+)\s*个用例")
# 「N 个命令行入口 / 脚本 / 工具」说的是同一件事：`tools/` 下有几个能跑的入口。
# 前面挡掉「另一个工具」这类泛指——它不是计数。
TOOL_COUNT_CLAIM = re.compile(r"(?<![另这那每某几半])"
                              r"([0-9零一二两三四五六七八九十]+)\s*个(?:命令行入口|脚本|工具)")
# 「检查 N 项」= 体检器一共有几条判据。分档只改哪些是强制项、不改清单长度，
# 所以这个数对任何项目都一样，是静态事实（不随扫描档位变）。
ITEM_COUNT_CLAIM = re.compile(r"检查\s*(\d+)\s*项")
# 自报分数「结构体检 N/N」= 上次全过时的 N。真值要等本次全部判完才知道，
# 所以它只在**其余项全过**时比对——不全过时文档写多少都不算与事实相反。
SCORE_CLAIM = re.compile(r"结构体检\s*(\d+)\s*/\s*(\d+)")
LEDGER_RANGE_CLAIM = re.compile(r"D-01[`\s]*…[`\s]*D-(\d+)")
# 「N 条决议」与上面的区间说的是同一个事实的两个侧面：到哪一条、一共几条。
LEDGER_COUNT_CLAIM = re.compile(r"(\d+)\s*条决议")

# 数字类断言（事实源是仓库里的文件与 git）。文档若自称「数字会过期」，这几条不核对。
NUMBER_CLAIMS = (TEST_COUNT_CLAIM, TOOL_COUNT_CLAIM, ITEM_COUNT_CLAIM, SCORE_CLAIM,
                 LEDGER_RANGE_CLAIM, LEDGER_COUNT_CLAIM)

# 「N 个用例」只认阿拉伯数字：中文数字在正文里多半是「写一个用例」这种泛称，
# 认了就是假阳性。「N 个命令行入口」反过来——它只可能指总数，所以中文数字也认。
CN_DIGITS = {"零": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4,
             "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}


def to_int(token):
    """把「5」「三」「十四」都读成 int；读不出来给 None。"""
    token = token.strip()
    if token.isdigit():
        return int(token)
    if "十" not in token:
        return CN_DIGITS.get(token)
    head, _, tail = token.partition("十")
    tens = CN_DIGITS.get(head, 1) if head else 1
    ones = CN_DIGITS.get(tail, 0) if tail else 0
    return tens * 10 + ones


# 九步判据里"哪些档位必须交"
NEED = {
    "brief":            {"L1", "L2"},
    "context":          {"L1", "L2"},
    "ledger":           {"L1", "L2"},
    "tickets":          {"L1", "L2"},
    "readme":           {"L0", "L1", "L2"},
    "gitignore":        {"L0", "L1", "L2"},
    "adr_dir":          {"L1", "L2"},
    "tests":            {"L1", "L2"},
    "agents_md":        {"L1", "L2"},
    "spec":             {"L2"},
    "architecture":     {"L2"},
    "onboarding":       {"L2"},
    "license":          {"L2"},
    "license_meta":     {"L2"},
    "community":        {"L2"},
    "changelog":        {"L2"},
    "ci":               {"L2"},
    "release_flow":     {"L2"},
    "env_example":      {"L2"},
    "pr_template":      {"L2"},
    "issue_template":   {"L2"},
    "metrics_rows":     {"L1", "L2"},
    "traceability":     {"L1", "L2"},
    "frontier":         {"L1", "L2"},
    "no_secrets":       {"L0", "L1", "L2"},
    "handoff_not_committed": {"L0", "L1", "L2"},
    "single_agent_entry":    {"L1", "L2"},
    "no_dup_ledger":    {"L1", "L2"},
    "stale_claims":     {"L2"},
}

results = []


CURRENT_LEVEL = "L2"


def add(cid, title, status, detail="", fix="", level="L2"):
    """status: OK / MISS / WARN / NA

    level      = 这一项在哪个档位被定义（固定值，不随扫描档位变）
    required   = 按本次扫描的档位，这一项是否是强制项（这才是你要判断的那个字段）
    """
    results.append({"id": cid, "title": title, "status": status,
                    "detail": detail, "fix": fix, "level": level,
                    "required": CURRENT_LEVEL in NEED.get(cid, {"L2"})})


def read(path, limit=200_000):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read(limit)
    except OSError:
        return ""


def walk(root):
    files, dirs = [], []
    for base, dnames, fnames in os.walk(root):
        dnames[:] = [d for d in dnames if d not in SKIP_DIRS]
        rel = os.path.relpath(base, root)
        if rel != ".":
            dirs.append(rel.replace(os.sep, "/"))
        for f in fnames:
            files.append(os.path.join(rel, f).replace(os.sep, "/") if rel != "." else f)
    return sorted(files), sorted(dirs)


def find(files, *patterns):
    """按 basename 或相对路径正则找文件"""
    out = []
    for p in patterns:
        rx = re.compile(p)
        out += [f for f in files if rx.search(f)]
    return sorted(set(out))


def git_facts(root):
    """远端与 tag 的现状。取不到的给 None——那一项跳过并打印出来，不误报也不假装查过。"""
    def run(*argv):
        try:
            proc = subprocess.run(["git", "-C", root] + list(argv), capture_output=True,
                                  text=True, encoding="utf-8", errors="replace", timeout=20)
        except (OSError, subprocess.SubprocessError):
            return None
        return proc.stdout if proc.returncode == 0 else None

    remote, tags = run("remote", "-v"), run("tag")
    # 浅克隆（CI 的 checkout 默认就是）不把 tag 取下来：`git tag` 空着不是"没有 tag"，
    # 是"看不见 tag"。空 + 浅克隆 → 当作取不到，跳过并打印——否则「`git tag` 为空」
    # 这类断言会被静默放行，而那正是这条检查要防的。
    shallow = os.path.exists(os.path.join(root, ".git", "shallow"))
    if tags is None:
        has_tag = None
    elif tags.strip():
        has_tag = True
    else:
        has_tag = None if shallow else False
    return {"has_remote": None if remote is None else bool(remote.strip()),
            "has_tag": has_tag}


def count_tests(root, files):
    """测试目录下 def test_ 的条数——「N 个用例」这类断言的事实来源。"""
    total = 0
    for f in files:
        if f.endswith(".py") and any(p.lower() in TEST_DIRS for p in f.split("/")[:-1]):
            total += len(re.findall(r"^\s*def test_\w+", read(os.path.join(root, f)), re.M))
    return total


def ledger_ids(root, files):
    """台账里出现过的编号（去重、升序）。编号不复用，所以它一次给出两个事实：
    最大值 = 「D-01…D-NN」该写到哪；条数 = 「N 条决议」该写几。"""
    led = find(files, r"^docs/decisions\.md$", r".*/ledger\.md$", r".*/decisions\.md$")
    if not led:
        return []
    ids = {int(i) for i in re.findall(r"\bD-(\d+)\b", read(os.path.join(root, led[0])))}
    return sorted(ids)


def live_docs(files):
    """活文档 = 声明仓库**现在**长什么样的那一批；快照不在其中。"""
    return [f for f in find(files, *LIVE_DOCS)
            if not any(re.search(p, f) for p in SNAPSHOT_DOCS)]


def number_exempt(rel):
    """这份文档是不是自称「表里的数字会过期、以文件为准」。"""
    return any(re.search(p, rel) for p in NUMBER_EXEMPT_DOCS)


def silent_number_docs(root, docs):
    """自称数字会过期、而确实写了数字断言的文档——它们的数字按声明跳过，得打印出来。"""
    return sorted(rel for rel in docs if number_exempt(rel)
                  and any(rx.search(line) for line in read(os.path.join(root, rel)).splitlines()
                          for rx in NUMBER_CLAIMS))


def claim_errors(rel, no, line, facts):
    """一行文本里，有哪些断言与仓库事实相反。

    自称「数字会过期」的文档（`NUMBER_EXEMPT_DOCS`）只核对非数字断言。
    """
    out = []
    numbers = not number_exempt(rel)

    def hit(msg):
        out.append((rel, no, msg))

    if facts["has_remote"] is True and REMOTE_CLAIM.search(line):
        hit("说「远端还没接」，实际 `git remote -v` 非空")
    if facts["has_tag"] is True and TAG_CLAIM.search(line):
        hit("说「`git tag` 为空」，实际已经有 tag")
    if numbers and facts["test_count"] is not None:
        m = TEST_COUNT_CLAIM.search(line)
        if m and int(m.group(1)) != facts["test_count"]:
            hit(f"说「{m.group(1)} 个用例」，实际 {facts['test_count']} 条")
    if numbers and facts["tool_count"]:
        m = TOOL_COUNT_CLAIM.search(line)
        if m and to_int(m.group(1)) != facts["tool_count"]:
            hit(f"说「{m.group(0)}」，实际 {facts['tool_count']} 个")
    if numbers and facts["item_count"]:
        m = ITEM_COUNT_CLAIM.search(line)
        if m and int(m.group(1)) != facts["item_count"]:
            hit(f"说「{m.group(0)}」，实际 {facts['item_count']} 项")
    if numbers and facts["ledger_max"] is not None:
        m = LEDGER_RANGE_CLAIM.search(line)
        if m and int(m.group(1)) != facts["ledger_max"]:
            hit(f"说决议区间到 D-{m.group(1)}，台账实际到 D-{facts['ledger_max']}")
        m = LEDGER_COUNT_CLAIM.search(line)
        if m and int(m.group(1)) != facts["ledger_count"]:
            hit(f"说「{m.group(0)}」，台账实际 {facts['ledger_count']} 条")
    if numbers and facts.get("score"):
        m = SCORE_CLAIM.search(line)
        if m and f"{m.group(1)}/{m.group(2)}" != facts["score"]:
            hit(f"说「{m.group(0)}」，本次跑下来是 {facts['score']}")
    return out


def scan_claims(root, docs, facts):
    """扫一遍活文档，返回全部「与事实相反」的位置。"""
    out = []
    for rel in docs:
        for no, line in enumerate(read(os.path.join(root, rel)).splitlines(), 1):
            out += claim_errors(rel, no, line, facts)
    return out


def has_score_claim(root, docs):
    """文档里有没有自报分数——决定要不要打印「这一项跳过」。"""
    return any(SCORE_CLAIM.search(line)
               for rel in docs for line in read(os.path.join(root, rel)).splitlines())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=".")
    ap.add_argument("--level", choices=LEVELS, default="L2")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--quiet", action="store_true", help="只输出未通过项")
    args = ap.parse_args()

    root = os.path.abspath(args.dir)
    lvl = args.level
    global CURRENT_LEVEL
    CURRENT_LEVEL = lvl
    if not os.path.isdir(root):
        print(f"目录不存在：{root}")
        return 2
    files, dirs = walk(root)
    def req(cid):  # 这一项在当前档位是否必须
        return lvl in NEED.get(cid, {"L2"})
    def mark(cid, title, ok, detail_ok="", fix="", warn=False, level="L2"):
        if not req(cid):
            add(cid, title, "NA", "本档不要求", level=level)
        elif ok:
            add(cid, title, "OK", detail_ok, level=level)
        else:
            add(cid, title, "WARN" if warn else "MISS", detail_ok, fix, level)

    # ---------- 门面层 ----------
    readmes = find(files, r"^README\.md$", r"^readme\.md$", r".*/README\.md$")
    if readmes:
        txt = read(os.path.join(root, readmes[0]))
        secs = sum(1 for k in ("##", "为什么", "上手", "用法", "限制", "现状", "许可")
                   if k in txt)
        one_screen = len(txt) > 200
        mark("readme", "README 存在且成段", one_screen and secs >= 3,
             f"{readmes[0]}（{len(txt)} 字符，命中 {secs} 类段落）",
             "补 README 七段：定位 / 为什么用 / 30 秒上手 / 用法 / 限制 / 现状与路线 / 许可与贡献")
    else:
        mark("readme", "README 存在且成段", False, "没有 README",
             "先写 README：一句话定位 + 30 秒上手（≤3 条命令）", level="L0")

    gi = find(files, r"^\.gitignore$")
    if gi:
        t = read(os.path.join(root, gi[0]))
        cats = sum(1 for k in ("node_modules", "dist", "build", ".env", ".DS_Store", "venv")
                   if k in t)
        mark("gitignore", ".gitignore 覆盖四类边界", cats >= 3,
             f"{gi[0]}（命中 {cats} 类关键词）",
             "补四类边界：依赖目录 / 构建输出 / 本机配置 / 密钥文件", level="L0")
    else:
        mark("gitignore", ".gitignore 覆盖四类边界", False, "没有 .gitignore",
             "先写 .gitignore 再 add，别把依赖和密钥吞进历史", level="L0")

    lic = find(files, r"^LICENSE(\.md|\.txt)?$")
    mark("license", "LICENSE 文件在根目录", bool(lic), lic[0] if lic else "没有 LICENSE",
         "选定许可证（第 0 步）并把全文放到根目录 LICENSE")

    meta_files = find(files, r"^package\.json$", r"^pyproject\.toml$", r"^Cargo\.toml$")
    if meta_files:
        mt = read(os.path.join(root, meta_files[0]))
        has = ('"license"' in mt) or re.search(r"^license\s*=", mt, re.M)
        mark("license_meta", "包元数据有 license 字段", bool(has),
             f"{meta_files[0]}: {'有' if has else '没有'} license 字段",
             "在包元数据里写标准 SPDX 标识，与 LICENSE、README 三处一致")
    else:
        add("license_meta", "包元数据有 license 字段", "WARN",
            "没找到 package.json / pyproject.toml / Cargo.toml", "有包元数据时再检查")

    community = [f for f in ("CONTRIBUTING.md", "SECURITY.md") if any(
        x.split("/")[-1].lower() == f.lower() for x in files)]
    mark("community", "CONTRIBUTING + SECURITY 都在", len(community) == 2,
         f"命中 {community}" if community else "两个都没有",
         "先补 SECURITY（私密报告渠道 + 响应时限）与 CONTRIBUTING（怎么起环境、跑测试）")

    ch = find(files, r"^CHANGELOG\.md$")
    mark("changelog", "CHANGELOG 存在", bool(ch), ch[0] if ch else "没有 CHANGELOG",
         "按 Keep a Changelog 建六段骨架")

    # ---------- 知识层 ----------
    ctx = find(files, r"^CONTEXT\.md$")
    if ctx:
        t = read(os.path.join(root, ctx[0]))
        rows = len([l for l in t.splitlines() if l.strip().startswith("|")])
        mark("context", "CONTEXT.md 术语表非空", rows >= 3, f"{ctx[0]}（表格行 {rows}）",
             "术语表要非空：术语 / 一句话定义 / 别叫它", level="L1")
    else:
        mark("context", "CONTEXT.md 术语表非空", False, "没有 CONTEXT.md",
             "第 2 步拷问时建，术语当场写进去", level="L1")

    adr_files = find(files, r"^docs/adr/.*\.md$")
    has_adr_dir = "docs/adr" in dirs
    mark("adr_dir", "docs/adr/ 目录在", has_adr_dir or bool(adr_files),
         f"{len(adr_files)} 份 ADR" if adr_files else ("目录在，暂无 ADR" if has_adr_dir else "没有 docs/adr/"),
         "建 docs/adr/；够格（难逆转+费解+真实权衡）的决策才写 ADR，0 条也正常", level="L1")

    ag = find(files, r"^AGENTS\.md$")
    cl = find(files, r"^CLAUDE\.md$")
    if ag or cl:
        txt = read(os.path.join(root, (ag or cl)[0]))
        guard = any(k in txt for k in ("权限", "不可以", "force push", "密钥"))
        mark("agents_md", "AGENTS.md 有权限边界", guard,
             f"{(ag or cl)[0]}（{'含' if guard else '未见'}权限边界）",
             "把权限边界写进 AGENTS.md：不碰密钥、不 force push、不发版、不替你签字", level="L1")
        mark("single_agent_entry", "只留一份代理入口", not (ag and cl),
             "AGENTS.md 与 CLAUDE.md 同时存在" if (ag and cl) else "只有一份",
             "两份必然分叉：只留一份，另一份改成一行指针", level="L1")
    else:
        mark("agents_md", "AGENTS.md 有权限边界", False, "没有 AGENTS.md / CLAUDE.md",
             "写一份 AGENTS.md，含九步索引 + 三条铁律口令 + 权限边界", level="L1")
        add("single_agent_entry", "只留一份代理入口", "OK", "都没有，无分叉风险", level="L1")

    arch = find(files, r"docs/architecture\.md$", r"docs/.*架构.*\.md$")
    seam_in_spec = False
    specs = find(files, r"\.scratch/.*/spec\.md$", r"docs/specs/.*\.md$", r"spec\.md$")
    for s in specs[:3]:
        if "接缝" in read(os.path.join(root, s)):
            seam_in_spec = True
    mark("architecture", "接缝清单写下来了", bool(arch) or seam_in_spec,
         (arch[0] if arch else ("spec 里有接缝段" if seam_in_spec else "没找到")),
         "每个接缝一行：名字 / 通过它的是什么 / 谁调用它")

    onboard = find(files, r"docs/onboarding\.md$", r"docs/.*接手.*\.md$")
    mark("onboarding", "接手路径文档在", bool(onboard), onboard[0] if onboard else "没有 docs/onboarding.md",
         "写 30 分钟接手路径：读什么、跑什么、下一步做什么")

    # ---------- 过程层 ----------
    briefs = find(files, r"docs/agents/brief\.md$", r"\.scratch/.*/brief\.md$", r"brief\.md$")
    if briefs:
        t = read(os.path.join(root, briefs[0]))
        five = sum(1 for k in ("给谁", "解决", "成功", "不做", "放弃") if k in t)
        mark("brief", "brief 五句话在", five >= 4, f"{briefs[0]}（命中 {five}/5）",
             "五句话：给谁用 / 解决什么 / 成功长什么样 / 不做什么 / 什么条件下放弃", level="L1")
    else:
        mark("brief", "brief 五句话在", False, "没有 brief.md",
             "第 0 步先写一页 brief，10 分钟、不许开代理", level="L1")

    ledgers = find(files, r"docs/decisions\.md$", r"\.scratch/.*/ledger\.md$")
    d_ids = set()
    if ledgers:
        for lg in ledgers:
            body = re.sub(r"<!--.*?-->", "", read(os.path.join(root, lg)), flags=re.S)
            body = "\n".join(l for l in body.splitlines()
                             if not l.lstrip().startswith(("#", ">", "```")))
            d_ids |= set(re.findall(r"\bD-\d+\b", body))
        mark("ledger", "决议台账存在且四列", len(d_ids) > 0,
             f"{ledgers[0]}（{len(d_ids)} 条决议）" if ledgers else "没有台账",
             "四列表头：编号 / 类型 / 决议（精确到可验证）/ 证据", level="L1")
        mark("no_dup_ledger", "台账只有一处", len(ledgers) == 1,
             f"找到 {len(ledgers)} 份：" + ", ".join(ledgers),
             "同一台账只留一处，另一处改成指针", level="L1")
    else:
        mark("ledger", "决议台账存在且四列", False, "没有 docs/decisions.md 或 ledger.md",
             "谈定一条就追加一行，编号不复用", level="L1")
        add("no_dup_ledger", "台账只有一处", "OK", "没有台账，无分叉", level="L1")

    tickets = find(files, r"\.scratch/.*/issues/.*\.md$", r"issues?/\d+.*\.md$")
    tickets = [t for t in tickets if t.split("/")[-1].lower() not in ("readme.md",)]
    if tickets:
        heads = {"Status": 0, "Blocked by": 0, "Covers": 0, "Verify": 0, "Rounds": 0, "Sessions": 0}
        covered, status_of, blocked_by = set(), {}, {}
        for tk in tickets:
            t = read(os.path.join(root, tk))
            for k in heads:
                if re.search(rf"^{re.escape(k)}\s*:", t, re.M):
                    heads[k] += 1
            num = re.match(r"^(\d+)", os.path.basename(tk))
            st = re.search(r"^Status\s*:\s*([\w-]+)", t, re.M)
            bl = re.search(r"^Blocked by\s*:\s*([^#\n]*)", t, re.M)
            if num:
                if st:
                    status_of[num.group(1)] = st.group(1).lower()
                blocked_by[num.group(1)] = [
                    x.strip() for x in (bl.group(1) if bl else "").split(",")
                    if x.strip() and x.strip() != "-"]
            for m in re.findall(r"^Covers\s*:\s*([^#\n]*)", t, re.M):
                covered |= set(re.findall(r"D-\d+", m))

        def _frontier(num):
            """能立刻开工 = 自己是 todo/doing，且**每一条**前置都已 done。

            前置是否解除要看那张票的 Status，不能只看 `Blocked by:` 里写没写东西——
            写 `Blocked by: 03` 而 03 早已 done 的票，本来就在 frontier 上。
            （早期版本只认 `Blocked by: -`，于是 03 一完工，frontier 就假报为空。）
            """
            if status_of.get(num) not in ("todo", "doing"):
                return False
            return all(status_of.get(b) == "done" for b in blocked_by.get(num, []))

        todo_free = [tk for tk in tickets
                     if _frontier(os.path.basename(tk).split("-")[0])]
        complete = sum(1 for k, v in heads.items() if v == len(tickets))
        mark("tickets", "票据六行头齐全", heads["Status"] == len(tickets) and complete >= 5,
             f"{len(tickets)} 张票；六行齐全的 {complete}/6 项",
             "票据头六行：Status / Blocked by / Covers / Verify / Rounds / Sessions", level="L1")
        mark("frontier", "frontier 非空（至少一张无阻塞可开工）", bool(todo_free),
             f"{len(todo_free)} 张可开工" + (f"：{todo_free[0]}" if todo_free else ""),
             "要么把票切小，要么解开阻塞；frontier 为空说明依赖成环或票切大了", level="L1")
        if d_ids:
            missing = sorted(d_ids - covered, key=lambda s: int(s.split("-")[1]))
            rate = 100 * len(d_ids & covered) / len(d_ids)
            mark("traceability", "决议被票据覆盖（覆盖率）", rate == 100,
                 f"{rate:.0f}%（{len(d_ids & covered)}/{len(d_ids)}）"
                 + (f"，未覆盖：{', '.join(missing)}" if missing else ""),
                 "给未覆盖的决议补一张票，或写进「范围之外」", level="L1")
        else:
            add("traceability", "决议被票据覆盖（覆盖率）", "NA", "没有台账，无从计算", level="L1")
    else:
        mark("tickets", "票据六行头齐全", False, "没找到票据文件（.scratch/<feature>/issues/）",
             "一票一文件，从 01 编号，头部六行照写", level="L1")
        mark("frontier", "frontier 非空（至少一张无阻塞可开工）", False, "没有票据",
             "先拆票", level="L1")
        add("traceability", "决议被票据覆盖（覆盖率）", "NA", "没有票据", level="L1")

    if specs:
        seven = all(k in read(os.path.join(root, specs[0])) for k in
                    ("问题陈述", "解决方案", "用户故事", "实现决策", "测试决策", "范围之外"))
        scope = "范围之外" in read(os.path.join(root, specs[0]))
        mark("spec", "spec 七段齐、范围之外非空", seven and scope,
             f"{specs[0]}", "复制 templates/spec.md 补齐七段；「范围之外」不许留空")
    else:
        mark("spec", "spec 七段齐、范围之外非空", False, "没有 spec.md",
             "只有一次会话装不下时才需要写；要写就用七段模板")

    # ---------- 工程与交付 ----------
    tests = [d for d in dirs if d.lower() in ("tests", "test", "spec", "__tests__")]
    mark("tests", "测试目录在", bool(tests), tests[0] if tests else "没有 tests/",
         "测试挂在事先约定的接缝上，断言行为而不是实现细节", level="L1")

    workflows = find(files, r"^\.github/workflows/.*\.(yml|yaml)$")
    mark("ci", "CI 工作流在", bool(workflows),
         f"{len(workflows)} 个：{workflows[0]}" if workflows else "没有 .github/workflows/",
         "最小流水线：安装 → lint → typecheck → test → 构建；并配分支保护（在平台上）")
    relf = find(files, r"^\.github/workflows/release.*\.(yml|yaml)$")
    mark("release_flow", "发布流水线在", bool(relf), relf[0] if relf else "没有 release 工作流",
         "tag 触发构建发布，产物带哈希或签名")

    prt = find(files, r"^\.github/PULL_REQUEST_TEMPLATE\.md$")
    itu = find(files, r"^\.github/ISSUE_TEMPLATE/.*\.(md|yml|yaml)$")
    mark("pr_template", "PR 模板在", bool(prt), prt[0] if prt else "没有 PR 模板",
         "四个问题：改了什么 / 为什么 / 怎么验证 / 风险与回滚")
    mark("issue_template", "issue 模板在", bool(itu), f"{len(itu)} 个" if itu else "没有 issue 模板",
         "bug 要复现步骤、版本、环境；feature 要场景、替代方案")

    envex = find(files, r"^\.env\.example$", r"^\.env\.sample$", r"^\.env\.template$")
    mark("env_example", "有 .env.example 且不放真值", bool(envex),
         envex[0] if envex else "没有示例配置",
         "示例配置只放占位值；真实凭证走环境变量")

    # 指标采集行：票据里有没有 Rounds / Sessions / Accept / Review
    if tickets:
        t = read(os.path.join(root, tickets[0]))
        rows = sum(1 for k in ("Rounds", "Sessions", "Accept", "Review") if re.search(rf"^{k}\s*:", t, re.M))
        mark("metrics_rows", "指标采集行在（Rounds/Sessions/Accept/Review）", rows >= 2,
             f"命中 {rows}/4", "第 6 步在票据里补 Accept: 与 Review: 两行", level="L1")
    else:
        add("metrics_rows", "指标采集行在（Rounds/Sessions/Accept/Review）", "NA", "没有票据", level="L1")

    # ---------- 安全与卫生 ----------
    VENDORED = (".deps/", "vendor/", "third_party/", "site-packages/", "node_modules/", "certifi")
    secret_files = [f for f in files
                    if re.search(r"(^|/)(\.env|id_rsa|.*\.pem|.*\.key|credentials\.json|secrets?\.\w+)$", f)
                    and not f.endswith(".example")
                    and not any(v in f.lower() for v in VENDORED)]
    gitignored = read(os.path.join(root, ".gitignore")) if gi else ""
    leaked = [f for f in secret_files if not any(
        pat in gitignored for pat in (".env", ".pem", ".key", "credentials", "secrets"))]
    mark("no_secrets", "没有明文密钥文件", not leaked,
         ("发现：" + ", ".join(leaked[:3])) if leaked else "未发现",
         "密钥一旦进过历史：先轮换，再决定要不要重写历史（按已泄露处理）", level="L0")

    ho = [f for f in files if re.search(r"(^|/)handoff[-_].*\.md$|.*\.handoff\.md$", f, re.I)]
    mark("handoff_not_committed", "交接文档没进仓库", not ho,
         ("发现：" + ", ".join(ho[:3])) if ho else "未发现",
         "交接文档写系统临时目录；它是一次性输入，且可能含敏感信息", level="L0")

    # ---------- 活文档里的「可证伪断言」 ----------
    # 文档说 X，仓库实际是不是 X。只扫活文档——快照记的是某个时点发生了什么，
    # 回头改它反而是伪造证据（CONTEXT.md 的「快照」条）。
    # 它排在所有项之后：自报分数要等本次全部判完才知道真值。
    ids = ledger_ids(root, files)
    facts = dict(git_facts(root),
                 test_count=count_tests(root, files),
                 tool_count=len(find(files, r"^tools/.*\.py$")),
                 item_count=len(NEED),
                 ledger_max=ids[-1] if ids else None,
                 ledger_count=len(ids))
    docs = live_docs(files)
    others = [r for r in results if r["status"] != "NA"]
    if others and all(r["status"] == "OK" for r in others):
        # 全过时自报分数才可比：本次跑下来就是这个数（这一项自己也进分母）
        denom = len(others) + (1 if req("stale_claims") else 0)
        facts["score"] = f"{denom}/{denom}"
    bad = scan_claims(root, docs, facts)
    notes = []
    no_facts = [k for k, v in (("远端", facts["has_remote"]), ("tag", facts["has_tag"])) if v is None]
    if no_facts:
        notes.append(f"取不到{'、'.join(no_facts)}的事实，跳过")
    if facts.get("score") is None and has_score_claim(root, docs):
        notes.append("本次不是全过，自报分数跳过")
    for rel in silent_number_docs(root, docs):
        notes.append(f"{rel} 自称数字会过期，那里的数字按它的声明跳过")
    detail = (f"{len(docs)} 份活文档，未发现" if not bad else
              f"{len(bad)} 处：" + "；".join(f"{f}:{n} {msg}" for f, n, msg in bad[:3])
              + ("……" if len(bad) > 3 else ""))
    mark("stale_claims", "活文档里没有与事实相反的断言", not bad,
         detail + (f"（{'；'.join(notes)}）" if notes else ""),
         "把断言改成事实；数字类断言要么由命令产出、要么留着由这项核对，嫌它总变就删掉数字指向文件")

    # ---------- 输出 ----------
    order = ["readme", "gitignore", "license", "license_meta", "community", "changelog",
             "context", "adr_dir", "agents_md", "single_agent_entry", "architecture", "onboarding",
             "stale_claims",
             "brief", "ledger", "no_dup_ledger", "spec", "tickets", "frontier", "traceability",
             "tests", "ci", "release_flow", "pr_template", "issue_template", "env_example",
             "metrics_rows", "no_secrets", "handoff_not_committed"]
    results.sort(key=lambda r: order.index(r["id"]) if r["id"] in order else 99)

    ok = [r for r in results if r["status"] == "OK"]
    miss = [r for r in results if r["status"] == "MISS"]
    warn = [r for r in results if r["status"] == "WARN"]
    na = [r for r in results if r["status"] == "NA"]

    if args.json:
        print(json.dumps({"root": root, "level": lvl, "ok": len(ok), "missing": len(miss),
                          "warn": len(warn), "not_applicable": len(na),
                          "results": results}, ensure_ascii=False, indent=2))
        return 1 if miss else 0

    marks = {"OK": "[x]", "MISS": "[ ]", "WARN": "[~]", "NA": "[-]"}
    print(f"结构体检  {root}")
    print(f"档位 {lvl}   通过 {len(ok)}   缺失 {len(miss)}   警告 {len(warn)}   不适用 {len(na)}")
    print("=" * 78)
    for r in results:
        if args.quiet and r["status"] in ("OK", "NA"):
            continue
        line = f"{marks[r['status']]} {r['title']}"
        print(line)
        if r["detail"]:
            print(f"      {r['detail']}")
        if r["status"] == "MISS" and r["fix"]:
            print(f"      → {r['fix']}")
    print("=" * 78)
    total = len([r for r in results if r["status"] != "NA"])
    if total:
        print(f"完整度：{len(ok)}/{total} = {100 * len(ok) // total}%（不含不适用项）")
    if miss:
        print("\n最该先补的三件：")
        for r in miss[:3]:
            print(f"  {order.index(r['id']) + 1}. {r['title']} —— {r['fix']}")
    else:
        print("\n强制项全过。别忘了剩下两件机器查不了的事：产品验收你亲手跑过没、文档是不是你要的。")
    return 1 if miss else 0


if __name__ == "__main__":
    sys.exit(main())
