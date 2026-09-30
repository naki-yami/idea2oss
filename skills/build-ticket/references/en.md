<!-- English companion to SKILL.md ｜ same decisions, shorter prose ｜ do not change the structure -->

# build-ticket

> Handbook step 5 | Outputs: code + tests + one reviewable commit (or branch) | Done when: tests went red then green, the header `Verify:` command passes, and nothing from the ticket's "not doing" list slipped in

## When to use / when not to
**Use** when you hold a ticket with `Status: todo` whose acceptance criteria have not changed; when starting work in a new session; when the work is done and you are about to commit and review.

**Not** when the ticket is not sliced yet → `ticket-plan` first; when the requirement itself is ambiguous → back to `grill-with-ledger` or `write-spec` for one sentence, never decide it inside the implementation; when a finished ticket needs review → `dual-axis-review`; when a bug will not move → `bug-diagnosis`.

**One ticket, one session**: finish one ticket, then open a new session for the next. The second ticket reads only its own ticket file and inherits none of the first one's discussion or pitfalls — inherited context carries the previous ticket's trial and error into this ticket's budget.

## Inputs
Feed only three things. Anything you have to recall is the previous session's debt.

1. **The ticket itself**: `.scratch/<feature>/issues/NN-*.md` or the tracker ticket, with all six header lines (`Status` / `Blocked by` / `Covers` / `Verify` / `Rounds` / `Sessions`); template `templates/ticket.md`.
2. **`CONTEXT.md`**: the glossary. Names used in the implementation match it.
3. **The interfaces involved**: the 1–2 seams this ticket touches, from the spec's "implementation decisions" seam list or `docs/architecture.md`.

Before starting, list the files this ticket needs to read (usually 3–6 paths) in the ticket's `## Comments`. If you cannot list them, the ticket is not self-contained — stop and go back to `ticket-plan`.

## Actions
1. **Open a new session and feed only those three things** — no previous discussion, trial and error, or provisional conclusions. Set the ticket to `Status: doing`.
2. **Restate the job in one sentence**: after this ticket, who can do what. If it disagrees with the ticket's "what", stop and settle the wording first; do not edit the ticket outright.
3. **Recognize seams, do not invent them** — read the seams from the ticket's "involved" list; tests hang on those seams, internals change freely without touching tests. A seam you need but the ticket does not name → stop and follow step 11. A seam nobody agreed to becomes a review finding.
4. **Red first**: write one test, run it, watch it fail. Red is also what proves the test tests something — green without red proves nothing. Add one test at a time and run it immediately.
5. **Then green**: write the minimum implementation that passes. Do not also do the next ticket's work.
6. **Then refactor**: change internals freely, leave tests alone. A test that goes red on an internal change tests the implementation, not the behavior — change the test.
7. **Fill in the boundaries**: one case each for the error, boundary, empty-state and permission-facing paths the spec user stories cover; try a failure message, empty input and over-limit input once each.
8. **Good-test criteria** — walk this list item by item: reads like a spec ("a user can check out with a valid cart"), not like the implementation ("`_calc` called twice"); asserts behavior through the public interface, not internal structure, private methods or call counts; still holds after a refactor instead of going red on any internal change.
9. **Run the header's `Verify:` command** and keep the evidence: paste the command and its output into the ticket's `## Comments`. If it does not pass, the ticket is not done.
10. **One ticket, one commit or one branch** — the commit message states why, not what changed; the diff says what changed far more accurately. Example: `fix: stop clearing unsent content on retry (ticket 03 / D-02)`.
11. **If two attempts don't converge, go up a level**: two attempts on the same ticket in a row without convergence means stop, do not keep it on life support, and pick the case. Not sliced self-contained (the reading you need is not in the ticket, or too many seams) → back to `ticket-plan` to re-slice. The requirement itself is ambiguous (both readings are valid, the doc is silent) → back to `grill-with-ledger` / `write-spec` for the missing sentence, plus one new ledger line. Technical uncertainty (not knowing whether it can be done this way) → verify with a throwaway prototype, never experiment on the main line.
12. **Close-out self-check**: did anything from "not doing" slip in; were TODOs, commented-out code or temporary flags left behind just to pass. Delete them or file a ticket.
13. **Fill in the header**: `Rounds:` (attempts on this ticket), `Sessions:` (sessions spanned), `Status: review`. `Sessions:` above 1 means the ticket was sliced too large — write the reason into the ticket and consider re-slicing.
14. **Hold the permission boundary**: you may read and write code, run tests and read docs; you may **not** touch secrets, production credentials, force push, rewrite history, delete data, ship a release or change the license. Needing any of those means stop and find a human.

## Outputs
- Code + tests, hanging on pre-agreed seams and reading like a spec.
- One reviewable commit (or one branch) — the reference point for the step 6 dual-axis review.
- An updated header: `Status` / `Rounds` / `Sessions`, plus the `Verify:` command and output in `## Comments`.
- Requirement ambiguities found along the way: added to the spec or the ledger, or ticketed on the spot — never only mentioned in conversation.

## Done criteria
- [ ] Tests went red then green, and the red step is on record (which command ran, what the failure said).
- [ ] Tests hang on the pre-agreed seams from the ticket's "involved" list; no new seams were invented.
- [ ] Tests read like a spec and assert behavior through the public interface; changing internals does not turn them red.
- [ ] The error, boundary and empty-state paths in the spec user stories each have at least one case.
- [ ] The header `Verify:` command passes, with command and output on record.
- [ ] Nothing from the ticket's "not doing" list slipped in.
- [ ] One ticket, one commit (or one branch); the commit message states why.
- [ ] Header `Rounds:` / `Sessions:` hold real numbers, and any `Sessions: > 1` reason is written in the ticket.
- [ ] No TODOs, commented-out code or temporary flags added just to pass.
- [ ] No secrets / production credentials / force push / data deletion / release were touched (or a human approved it first).
- [ ] The file list written before starting is in the ticket, only those files were read, and anything extra read was added to the list.

## Manual fallback
- No `implement` / `tdd` (external skills): **do red-green by hand**, skipping no step of the order. Red: write one test, run it once, see it fail. Green: the minimum implementation. Then refactor. This is the handbook's manual path.
- Test framework will not install: fix the environment first — step 6's detection depends on tests that can run. A minimal executable verification script can stand in temporarily, but the red-green order is not optional, and the ticket must state what is missing and how to restore it.
- Commit hooks / CI will not install: run lint, typecheck and tests by hand before committing, and self-check the standards axis against `templates/manual-review.md`.
- `git` unavailable: **no substitute, install it first** — the step 6 dual-axis review needs a diff reference point, and with no reference there is no review input.
- No agent at all: a human writes it, same criteria — red before green, tests on the agreed seams, `Verify:` passes, commit message says why.

## Next step
→ call `dual-axis-review` (one ticket one commit uses the previous commit as the reference point; branch work uses merge-base).

## Anti-patterns
- **Writing the code first and adding tests after** — the red step never happened, so the tests prove nothing → write the test, run it once, see it red, then implement.
- **Hanging tests on a newly invented seam** — a seam nobody agreed to becomes a review finding → hang them only on the seams in the ticket's "involved" list; inventing one means going back to step 4.
- **Session boundaries that do not match tickets (two tickets in one session, or one ticket across two sessions)** — the first carries the previous ticket's trial-and-error budget; the second compresses to fit and loses exactly the precision of decisions → one ticket, one session; a ticket needing two sessions goes back to `ticket-plan`.
- **A commit message saying "changed xx files"** — that sentence is less accurate than the diff → state why, referencing the ticket number and `[D-nn]`.
- **Doing the "not doing" list anyway** — scope creep makes delivered behavior contradict the acceptance criteria → file a new ticket on the spot; do not stuff it in here.
- **Saying "one more try" after two attempts did not converge** — more context does not get better, only more expensive and messier → go up a level: re-slice the ticket, fix the requirement, or prototype.
