<!-- English companion to SKILL.md ｜ same decisions, shorter prose ｜ do not change the structure -->

# repo-setup

> Handbook ch. 2 (2)(3)(4) | Outputs: `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, `docs/agents/domain.md` + the `## Agent skills` section and version-lock line in `AGENTS.md` | Done when: tracker, triage labels, and domain doc layout all have a destination, and the skill-set version is locked

## When to use / when not to

- Once per **repo**, after step 1 (`repo-bootstrap`) and before step 2 (`grill-with-ledger`). Not per feature — a feature's spec and tickets belong to steps 3 and 4. Skip it and a tool sends you back here mid-run: writing the spec, cutting tickets, or triaging issues, you won't know where things go.
- Rerun the matching section in three cases: the issue tracker platform changed (section A); the skill set was upgraded (step 7, plus re-check handbook ch. 2 and ch. 15); you cloned a repo that was never configured (no `docs/agents/`).
- Not a git repo yet → `repo-bootstrap` first, otherwise local markdown mode is all you get.
- Why it exists: it is the foundation of this pipeline. With these three destinations undecided, every later step's output has nowhere to live. It makes no design judgment — it pins down where things are recorded so the next session doesn't have to guess.

## Inputs

1. A repo that has already been `git init`ed (if not → `repo-bootstrap` first).
2. Output of the four probe commands (see Actions 1) — look before you ask.
3. Whether `git --version`, `gh --version`, `glab --version` exist.
4. Whether triage (external skill/tool) is installed — it decides whether section B runs.
5. Labels the platform already uses (e.g. `bug:triage` meaning "needs evaluation"), and the actual skill-set version number (reference implementation: mattpocock/skills v1.2.3, MIT, released 2026-08-06).

## Actions

1. **Probe** (run these four first; never skip probing and ask the user directly): `git remote -v` (GitHub / GitLab?); `ls AGENTS.md CLAUDE.md CONTEXT.md`; `ls -d docs/adr docs/agents .scratch`; `ls pnpm-workspace.yaml` (monorepo signal).
   Read it: GitHub remote → section A defaults to GitHub; monorepo signal → section C must ask whether it is multi-context; both `AGENTS.md` and `CLAUDE.md` present → merge into one first, leave one pointer line in the other.
2. **Report first, then ask one section at a time**: A → B → C, each with a default recommendation, and only write files after confirmation. This is a prompt-driven flow, not a deterministic script — ask all three at once and the answers are a half-hearted version of your defaults.
3. **Section A: pick the issue tracker destination.**

   | Mode | Destination | Prerequisite | When to pick |
   |---|---|---|---|
   | GitHub | the repo's GitHub Issues | `gh` installed and logged in | you plan to open source, others will file issues |
   | GitLab | the repo's GitLab Issues | `glab` installed and logged in | your team uses GitLab |
   | local markdown | `.scratch/<feature>/` in the repo | none, works anywhere | solo, offline, don't want platform lock-in (default recommendation) |

   Default: GitHub if there is a GitHub remote, otherwise local markdown. **This is not optional** — steps 3 and 4 have to publish something, so the destination must exist first; no `gh` does not excuse you from skipping spec and tickets. Write it into `docs/agents/issue-tracker.md` (follow `templates/issue-tracker.md`).
4. **Section B: triage labels** (ask only if the external triage skill is installed; otherwise skip the whole section, see Manual fallback). Five labels, the label name equals its role name: `needs-triage` (maintainer evaluation pending), `needs-info` (waiting on the reporter), `ready-for-agent` (spec complete, safe to hand to an unattended agent), `ready-for-human` (needs a human implementation), `wontfix` (won't be handled).
   Mapping conflict: if your tracker already uses other words (e.g. `bug:triage` for `needs-triage`), **fix the mapping here** — otherwise triage creates duplicate labels and the state machine fights itself. Write the mapping table into `docs/agents/triage-labels.md` (follow `templates/triage-labels.md`), including this known trap: specs get labeled `ready-for-agent`, and an unattended agent polling by label may implement the whole document instead of picking a ticket slice — drop the label once ticket cutting is done, or explicitly exclude parent documents in the agent prompt.
5. **Section C: domain doc layout** (single-context by default). Single-context = one `CONTEXT.md` at the root + `docs/adr/` + decision ledger `docs/decisions.md`. Write it into `docs/agents/domain.md` (follow `templates/domain.md`) and state three boundaries clearly:
   - `CONTEXT.md` is a **glossary only**, not a spec;
   - most decisions don't qualify for an ADR — they go into the ledger (numbered, with evidence);
   - the ADR bar is all three at once: hard to reverse + confusing without context + a real trade-off.
6. **Insert a `## Agent skills` section into `AGENTS.md` or `CLAUDE.md`.** It is an index: which stage, which tool, does what (skeleton in `templates/AGENTS.md.tpl`, and **rename to `AGENTS.md`** when copying to the project root — the `.tpl` suffix exists so the runtime never treats the template itself as an active instruction file). Keep exactly one of the two files live; the other either does not exist or holds a single pointer line — never let the two diverge.
7. **Lock the skill-set version**: write the version into `README.md` or a short file under `docs/agents/`. Upgrade **by tag, never follow main** — skills are added and deleted on main all the time, and skill names go straight into the prompts an agent reads, so a rename changes behavior. After upgrading, re-check handbook **ch. 2** (skill table and rename map) and **ch. 15** (known defects and workarounds) and rerun step 2 as a drill; they describe implementation details and expire first. Before changing environments, check once: the original repo used `disable-model-invocation: true` to lock a batch of skills to manual trigger only, and an environment that doesn't know the field **silently ignores** it, so the agent may trigger them itself — delete the line or block them explicitly in the agent config.
8. **Local markdown mode layout** (only if you picked that mode): `.scratch/<feature-slug>/` holds `brief.md` (step 0, five sentences), `spec.md` (step 3), and `issues/` with one ticket file per ticket numbered from `01-first-ticket.md`. Copy the ticket header from `templates/ticket.md` exactly, six lines (`Status` / `Blocked by` / `Covers` / `Verify` / `Rounds` / `Sessions`); **append comments and history under the `## Comments` heading at the bottom of the file, never into the header** — the header is machine-read, the bottom is for people and history. Write this convention into `docs/agents/issue-tracker.md`.

## Outputs

- `docs/agents/issue-tracker.md` — tracker mode and destination (template `templates/issue-tracker.md`).
- `docs/agents/triage-labels.md` — the five labels plus the mapping-conflict table; if disabled, say why (template `templates/triage-labels.md`).
- `docs/agents/domain.md` — the boundaries between `CONTEXT.md` / `docs/adr/` / ledger (template `templates/domain.md`).
- The `## Agent skills` section in `AGENTS.md` (or `CLAUDE.md`).
- One version-lock line: `Skill set: <name> <version> (source, release date)`.

## Done criteria

- [ ] All four probe commands were actually run and their output read (not skipped in favor of asking).
- [ ] All three files under `docs/agents/` exist and every TODO in them is filled (no half-empty template left behind).
- [ ] Only one of `AGENTS.md` and `CLAUDE.md` is live; the other is missing or a single pointer line.
- [ ] `AGENTS.md` has a `## Agent skills` section and you can point at those lines.
- [ ] `docs/agents/issue-tracker.md` states the mode, and steps 3 and 4 have a definite destination.
- [ ] Triage enabled: the mapping between the five labels and the platform's existing labels is in the same file; not enabled: the file explicitly says "this repo does not enable triage labels".
- [ ] `docs/agents/domain.md` states the boundaries between `CONTEXT.md` / `docs/adr/` / ledger, and where the ledger lives.
- [ ] The skill-set version is written into `README.md` or `docs/agents/`, noting "upgrade by tag, never follow main".
- [ ] If local markdown mode: `.scratch/<feature>/issues/` exists, and the six-line ticket header and `## Comments` convention are written into `issue-tracker.md`.

## Manual fallback

- No setup-type skill installed (external skills such as `setup-matt-pocock-skills`; use it if present): **this skill is itself the manual path**. Copy `templates/issue-tracker.md`, `templates/triage-labels.md`, `templates/domain.md`, ten minutes of copying, and not one criterion changes.
- Triage (external skill) not installed: **skip section B entirely** and write in `triage-labels.md` that "this repo does not enable triage labels; issues are reviewed by hand". Never invent a label set nobody will execute just to complete the file list.
- Current directory is not a git repo: local markdown mode is the only option (repo type comes from `git remote -v`). Exactly why step 1 goes first — run `repo-bootstrap`, then come back.
- The platform already has its own label scheme: don't create same-name labels, just write the mapping table. Better a few labels missing than two vocabularies coexisting. Team on GitLab without `glab`: go local markdown; opening issues by hand in the web UI forks the destination and leaves spec and tickets in two places.
- No agent at all: these three files are written for humans anyway; write them by hand, then add one index section to `AGENTS.md`.

## Next step

→ call `grill-with-ledger` (the point of configuring is that what step 2 agrees on has somewhere to land).

## Anti-patterns

| Anti-pattern | Why it's wrong | Instead |
|---|---|---|
| Running setup once per feature | the three files get rewritten repeatedly and destinations fork | once per repo; rerun only when the config itself changes |
| Doing section B without triage installed | produces a label file nobody executes or maintains, and the next person looks for work by it | skip the section, write why, install triage first |
| Asking sections A/B/C all in one go | users answer three questions without context and the answers are sloppy | one section at a time, give a default, write after confirmation |
| Recording "we use GitHub" without the mapping | labels are created twice and the issue state machine contradicts itself | write the mapping-conflict table into `triage-labels.md` on the spot |
| Maintaining both `AGENTS.md` and `CLAUDE.md` | the contents will diverge, and which one an agent reads is luck | keep one, one pointer line in the other |
| Not locking the version and upgrading with main | renames or deletions silently change agent behavior, and the handbook's workarounds expire | upgrade by tag; re-check ch. 2 and ch. 15 after |
| Writing comments into the ticket header in local mode | the header is machine-read fields; history mixed in makes it unparsable | always append comments under `## Comments` at the bottom |
