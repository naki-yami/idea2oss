<!-- English companion to SKILL.md ｜ same decisions, shorter prose ｜ do not change the structure -->

# idea2oss

> Handbook TL;DR, ch. 12, ch. 13 | Outputs: one tier verdict + one line of "current step / next skill" | Done when: the tier is decided, current step and next skill are both nameable, and every skipped step says why it was skipped

## When to use / when not to

- Use: at the start of any session; the user says "I want to build something" or asks how many steps this takes, what to do next, or which skill to use now; every time you upgrade or downgrade the tier. Also when handing the flow to someone else (or another agent).
- Don't use: you already know you're at step N and which skill to call — call it, don't detour through the front door. Per-skill detail lives in each skill.
- One criterion: skills can be swapped, criteria cannot be dropped. All nine steps can be walked by hand; without criteria nobody knows whether it came out right.

## Inputs

1. The user's request verbatim ("I want to build something" counts as input).
2. Current state of the target directory: is it a git repo, is there an `AGENTS.md`, a `.scratch/`, a `docs/adr/`.
3. Three properties of the work: just for you or for others; open source or not; does it touch user data or secrets.
4. How far along you are: which files exist now (brief / spec / ticket / ledger).

## Actions

1. **Decide the tier first** (match the table, don't go by feel):

   | Tier | Situation | Steps | You may not drop |
   |---|---|---|---|
   | L0 one-off | done in half a day, only you use it, never lands on main | 0 (one sentence) → 5 → 6 (self-check) | git hygiene; secrets and data boundaries |
   | L1 normal feature | 1–3 days, fits in one session, affects you or a small team | 0 → 1 → 2 → 5 → 6 → 7 | step 2 grilling (or step 5 reworks); step 6 review |
   | L2 real project | does not fit in one session / for others / open source / multiple people / touches user data | all nine, 0–8 | criteria, health metrics, step 8 |

2. **Check the upgrade criteria** — any single hit sends you straight to L2: a second person will use your code, or you plan to open source it; you will cut releases with version numbers; there is a second contributor (even a colleague reviewing); you handle user data, credentials, or money, or integrate a third-party service.
3. **Check the downgrade criteria** — two consecutive tickets finished in one pass with zero rework: the tier's "must" documents may drop to casual notes. **The criteria do not drop**; they are the one thing this flow never gives up.
4. **Locate the current step** (nine-step map; copy the criterion column, do not rewrite it into adjectives):

   | Step | What | Outputs | Done criterion (one line) | Skill |
   |---|---|---|---|---|
   | 0 | kickoff | `brief.md` | five sentences are writable: for whom, solves what, success looks like, what you won't do, when to kill it | `project-brief` |
   | 1 | init the local git repo | `.git/` + `.gitignore` + first commit | first commit exists, `git status` clean, no secrets in history | `repo-bootstrap` |
   | — | one-time env config per repo | three files in `docs/agents/` + `## Agent skills` in `AGENTS.md` | tracker, triage labels, and domain doc layout all have a destination; skill-set version locked | `repo-setup` |
   | 2 | grilling | `CONTEXT.md` + decision ledger + possibly ADRs | glossary non-empty; every ledger decision verifiable; such decisions have an ADR or a written "no ADR this step" | `grill-with-ledger` (discipline: `decision-ledger`) |
   | 3 | product spec | `.scratch/<feature>/spec.md` | all seven sections present, "out of scope" non-empty, every sentence points back to something you said | `write-spec` |
   | 4 | technical plan and dev plan | seam list + ticket graph | seams match the success criteria; at least one ticket unblocked (frontier non-empty) | `ticket-plan` |
   | 5 | build | code + tests | tests red before green, hung on the seams agreed up front | `build-ticket` |
   | 6 | review | dual-axis report + your own acceptance verdict | no open findings on either axis; you ran it yourself and left a verdict | `dual-axis-review` (bug → `bug-diagnosis`) |
   | 7 | handoff | commit hook + PR + handoff doc | hook has run; PR says how to verify; handoff doc gives paths only | `session-handoff` |
   | 8 | open-source launch and operation | LICENSE + README + CI + community files + first release | the stranger-in-30-minutes test passes, and they know how to contribute | `oss-launch` |

5. **Copy the routing table** — turn "the state you are in" into a skill name; one call, one skill. Map: a one-liner that can't yet say what it is → `project-brief`; don't know how many steps or what can be skipped → this skill (tier); an empty directory with no `git init` → `repo-bootstrap`; repo commits fine but no idea where spec and tickets go → `repo-setup`; starting work with the requirement still only in your head → `grill-with-ledger`; just finished a round and afraid decisions will be lost → `decision-ledger`; too big for one session and you need a document to show → `write-spec`; a spec or a pile of requirements with no idea which part is first → `ticket-plan`; the ticket graph exists and you want to build one → `build-ticket`; one ticket done, going to review or self-check → `dual-axis-review`; a bug that won't die or a performance regression → `bug-diagnosis`; context nearly full, switching sessions, or handing off a finished ticket → `session-handoff`; the code runs and others should use it or you're going public → `oss-launch`; several rounds in and you want to know whether this flow works and what to change → `flow-tuning`; the same thing hasn't converged twice → stop, go up a level: `ticket-plan` / `grill-with-ledger` / build a throwaway prototype.
6. **Write the three laws down as exact phrases** (copy them verbatim into the target repo's `AGENTS.md`; that file is for the next session):
   - One ticket, one session: **"I'll open a new session once this ticket is done."** Ticket 2 reads the ticket file only, it does not inherit ticket 1's discussion or scars.
   - Write it down the moment it's agreed: **"Is this settled? Then it goes into the ledger now."** Never let a night pass between agreeing and writing, and don't insert other work in between.
   - If two attempts don't converge, go up a level: **"Two rounds without convergence: stop, go back up."** Recut the ticket / add one requirement line / prototype, instead of "try once more".
7. **Put the permission boundary in the same `AGENTS.md`.** An agent may read code, write code, run tests, read docs. These it may **not** do without your explicit approval, and you should preferably do them yourself: touching secrets, production credentials, release credentials; force pushing shared branches, rewriting history, deleting data; cutting releases, making a repo public, changing a license or making public commitments; signing for you — legal calls, privacy statements, promises to others. One-line reason: these actions are irreversible or affect others, and an agent's confidence does not correlate with being right.
8. **Write this round's verdict as two lines**, in the session or in `AGENTS.md`: `Tier: L1 | Current: step 2 | Next: grill-with-ledger`. Append why each skipped step was skipped (e.g. "L1 skips steps 3 and 4: one ticket finishes it").

## Outputs

- One tier verdict line with the upgrade-criteria check recorded, and one "current step / next skill" line.
- Three things in the target repo's `AGENTS.md`: the nine-step index, the three laws verbatim, the permission boundary list.
- Optional: cut this skill's nine-step map into `docs/agents/flow.md`.

## Done criteria

- [ ] Tier (L0 / L1 / L2) is decided and a `Tier: L?` line is written.
- [ ] All four upgrade criteria were checked one by one and the result is written (which one hit, or none).
- [ ] A `Current: step N | Next: <skill>` line is written, and the skill name is a real one from the fourteen.
- [ ] Every skipped step says why it was skipped; "seemed unnecessary" does not count.
- [ ] The three laws are in the target repo's `AGENTS.md`, and you can point at those lines.
- [ ] The permission boundary list is in the same `AGENTS.md`, and no out-of-bounds action is running now.
- [ ] Every criterion delivered this round is a `- [ ]` item that runs one command, points at one file, or answers one question.

## Manual fallback

- No skill set installed: walk the nine steps anyway — print appendix C1's nine criteria on one page and tape it to the monitor; the TL;DR nine-row table is the whole map (step 4's table is copied from it), and each skill's own manual fallback covers the rest. Only one sticky note's worth of time: write three lines — tier, current step, next step.
- Can't judge the tier: **round up one tier** — one extra step always costs less than reworking at step 5. The user refuses to pick a tier and just wants to code: even L0 requires git hygiene and secrets boundaries, and if those two can't be agreed, don't start coding.
- Fully offline, no agent allowed: appendix A's templates plus each skill's manual fallback are the agent-free version, and not one criterion changes.

## Next step

→ call that one skill; no brief → `project-brief`, no repo → `repo-bootstrap`, repo without config → `repo-setup`.

## Anti-patterns

| Anti-pattern | Why it's wrong | Instead |
|---|---|---|
| Walking all nine steps from 0 every time | flow eats a one-day job and people start routing around it | decide the tier first; L0 runs 0 → 5 → 6 only |
| Skipping step 2 and implementing | requirements surface mid-build; rework doubles | L1 and up must grill; only L0 may skip |
| Tier set too high and never lowered, or too low and never raised | criteria are tailored per tier, so a wrong tier makes every criterion wrong | re-judge at the start of every session; downgrade has criteria |
| Calling several skills at once "to save time" | several rule sets crowd the context and the output gets worse | one at a time, finish, then switch |
| Writing "Next: figure it out" into AGENTS.md | the next session still doesn't know where to start | write a concrete skill name; never leave it vague |
| Letting an agent decide the license, make the repo public, or sign | irreversible or affects others; agent confidence is unrelated to correctness | you do it by hand; the agent may at most lay out the options |
