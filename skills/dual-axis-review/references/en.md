<!-- English companion to SKILL.md ｜ same decisions, shorter prose ｜ do not change the structure -->

# dual-axis-review

> Handbook step 6 | Outputs: two axis reports + a conclusion you ran yourself | Done when: no open findings on either axis, decision traceability rate 100%, and the ticket carries an `Accept:` line

## When to use / when not to
**Detection has three layers; never collapse them into one "test"** — that collapse is a common starting point for losing control of quality.

| When | What | Where |
|---|---|---|
| While writing | Red-green loop (instant detection, no extra tooling) | Built into `build-ticket` |
| After changes | Dual-axis review (this skill) | Step 6 |
| On a bug | Six-step diagnosis: sanitize → reproduce → minimize → hypothesize → instrument → fix plus regression | → call `bug-diagnosis` |

**Use** when a ticket is implemented (`Status: review`); before delivery; when deciding whether this ticket may enter step 7.

**Not** while code is being written (that is `build-ticket`'s red-green loop); while the requirement is still unsettled (back to `grill-with-ledger` — review cannot stop a wrong requirement); and never let the context that wrote the code also act as reviewer — the reviewer rereads the diff and inherits none of the implementation-time judgment.

## Inputs
1. **One fixed reference point**, pick one of four: commit / branch / tag / merge-base. **If the user does not give one, ask; do not guess.**
2. **The ticket** (`templates/ticket.md`): the header carries a `Verify:` line, and the end needs room for an `Accept:` line.
3. **The spec**: `.scratch/<feature>/spec.md`, the reference material for the spec axis.
4. **The decision ledger**: `ledger.md` or `docs/decisions.md`, the denominator of the traceability rate.
5. **This repo's own written standards**: `CONTRIBUTING.md`, `AGENTS.md`, lint / formatter config, conventions under `docs/`. The standards axis compares against **those**, not general taste and not your personal preference.

## Actions
1. **Set the reference point** — one ticket one commit uses the previous commit (before this ticket's commit); branch development uses merge-base by default, the common ancestor of branch and trunk. merge-base keeps other people's merged changes out of your work. Take the user's reference point if given; otherwise ask.
2. **Verify the reference point first**: does this ref resolve? Is `git diff <ref>..HEAD` empty? If it is empty, confirm the reference point before starting the review.
3. **Run the two axes in parallel subagents** so they cannot contaminate each other's context:

   | Axis | Reviews | Reference material | Output |
   |---|---|---|---|
   | The standards axis | Whether the code follows **this repo's own written** standards | `CONTRIBUTING.md` / `AGENTS.md` / lint config / existing conventions | Findings + location + severity |
   | The spec axis | Whether the code faithfully implements **every line** of the document | The spec's seven sections (especially success criteria and out-of-scope) + the ledger | Same as above |
4. **Each of the two subagent briefs states four things**: which axis, the reference material (give the path), the diff range (give the ref), the output format (a finding list, each finding with file and line number).
5. **Append one sentence verbatim to the end of both briefs** (Chinese original: 不要调用 code-review，也不要派发额外代理，直接完成本次评审。) — "Do not call code-review, and do not dispatch extra agents; complete this review directly." Known unfixed bug: subagents recurse, and one report hit 50+ agents in a single run. Watch the agent count when running unattended and inspect the background task list afterwards.
6. **Present the two reports side by side at the end; never merge them into one.** "Clean code but wrong" and "right but dirty" are different conclusions, and merging erases both.
7. **Compute the decision traceability rate**: decisions with evidence ÷ all decisions. **Target 100%.** Below 100% there are only two explanations: a decision was missed, or a decision was weakened. Anything that points at no evidence: file a ticket on the spot or write it into out-of-scope.
8. **Technical acceptance criteria**: no open findings on either axis. Every open finding must be written as "accepted risk + who accepts it" — a person's name, not "the team".
9. **Product acceptance is yours to do and cannot be outsourced**: really run it, really use it, answer "is this what I asked for". Leave one line in the ticket: `Accept: pass / fail + reason`. A skill can tell you "the code faithfully implements every line of the document"; it cannot tell you "the document itself is what you wanted". An agent accepting its own code is not acceptance.
10. **Criteria must land as two executables**: one runnable command (`Verify:`) plus one human-written conclusion (`Accept:`). No amount of planning is a gate (official issue #1060) — with acceptance criteria, out-of-bounds items and dependency chains all written out, delivered behavior can still contradict the acceptance criteria; criteria that live only in the document stop nothing.
11. **File hidden debt on the spot**: every "later", "next refactor" or "for now" needs a ticket on the tracker, or an ADR that explicitly accepts it.
12. **Fill in the header**: `Review:` (finding counts on both axes; metric: review rework), `Accept:`, `Status`. Only tickets that pass acceptance enter step 7; failures stay on the frontier.

## Outputs
- Two dual-axis review reports, presented side by side, each with findings, location and severity.
- In the ticket: the `Accept:` line (the conclusion you ran yourself), the `Review:` counts, the updated `Status`.
- Manual path: a filled-in `templates/manual-review.md`, including the three conclusion lines (open findings on both axes + decision traceability rate).
- Tickets filed / entries written into out-of-scope / ADRs where needed.
- Fix commits when there were findings.

## Done criteria
- [ ] The reference point is one ref, written down, and `git diff <ref>..HEAD` is not empty.
- [ ] The standards axis compares against **this repo's own written** standards; with none written down, the report says so explicitly and compares against existing conventions item by item.
- [ ] The spec axis went through the spec's success criteria and out-of-scope item by item, not from memory.
- [ ] The two reports are presented side by side, not merged into one.
- [ ] Both subagent briefs end with "Do not call code-review, and do not dispatch extra agents; complete this review directly."
- [ ] The reports carry no open findings; or every open finding has "accepted risk + who accepts it", and the acceptor is a person.
- [ ] Decision traceability rate = 100%; anything with no evidence was ticketed or written into out-of-scope.
- [ ] The ticket carries an `Accept:` line, written by someone other than the agent that wrote this code.
- [ ] The `Verify:` command really ran once during this review.
- [ ] Everything marked "later" has a ticket number; no hidden debt.
- [ ] The header `Review:` count is filled in.
- [ ] Regression tests pass after the fix; tickets that did not pass did not enter step 7.

## Manual fallback
- No subagents / no parallelism: run the two axes **serially**, clearing the context once in between. Run the standards axis and write down its conclusion, then open a fresh run for the spec axis — the order may swap, the contamination may not happen.
- No `code-review` (external skill): walk `templates/manual-review.md` item by item, six items per axis, and the three conclusion lines at the end are mandatory.
- The review report will not come back (too long or truncated): copy at least the findings into the ticket before touching code; never chat and edit at the same time.
- No diff reference point (`git` unavailable, or changes uncommitted): **no substitute** — commit first, or save the current changes as a patch; with no reference point there is no review input.
- No agent at all: you walk both lists yourself; product acceptance still has to be run by hand — that one was never outsourceable.
- Unattended environment: watch the agent count and kill the duplicate ones the moment recursion shows up.

## Next step
→ call `session-handoff` (continue into step 7 delivery); with open findings → fix, then back to `build-ticket`; a bug that will not move → call `bug-diagnosis`.

## Anti-patterns
- **Collapsing the three detection layers into one "test"** — you find out on a bug that there is no feedback loop, and after the fix nobody has looked at the diff → red-green while writing, dual-axis after changes, six-step diagnosis on a bug.
- **Merging the two axes into one report** — "clean code but wrong" gets buried → keep the two side by side, merge nothing.
- **Guessing the reference point, or using `HEAD` as one** — the diff is empty, or someone else's changes count as your work → ask the user; one ticket one commit uses the previous commit, branch work uses merge-base.
- **Leaving the anti-recursion sentence out of the subagent briefs** — recursion is known, one report hit 50+ agents and burned a large amount of tokens → copy that sentence verbatim at the end of both briefs; watch the agent count when unattended.
- **Letting an agent do product acceptance** — judging your own work is not acceptance → run it by hand and write the `Accept:` line yourself.
- **Marking findings "later" and leaving criteria only in the document** — the debt is forgotten and untrackable, and planning itself is not a gate, so delivered behavior can still contradict the acceptance criteria → file a ticket or write an ADR on the spot, and land each criterion as one runnable command plus one human conclusion.
