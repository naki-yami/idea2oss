<!-- English companion to SKILL.md ｜ same decisions, shorter prose ｜ do not change the structure -->

# bug-diagnosis

> Handbook step 6 (iii) | Outputs: a minimal reproduction + a regression test + (when the stop-loss line triggers) one ADR and one "redesign X" ticket | Done when: all six steps ran, the reproduction went red-to-green, and the regression test stays in the repo

## When to use / when not to

**Use** when behaviour is wrong, something throws, failures are intermittent, performance regressed, it only breaks in some environments, one round of fixing didn't help, or someone reported a bug you can't reproduce.

**Don't use** for bugs you pinpoint at a glance, fix in one pass and cover with a regression test on the way — just go; for requirements that were never clear (a step-2 problem, go back to `grill-with-ledger`); for a whole class of problems already confirmed as a design flaw — handle them as design, write the ADR first, then open a ticket.

**Why it exists**: skipping step 2 and guessing the cause is the classic reason this kind of bug survives repeated fixes. Without a reproduction that goes red for *this* bug, you can't tell whether a change fixed it or covered the symptom. Fix loops burn time not because the bug is hard but because **nothing ever went red**.

## Inputs

1. A describable symptom: what you expected, what happened, when it started (which commit, after which upgrade).
2. A runnable environment: versions, platform, lockfiles — reproduction relies on these, not on memory. Plus a terminal that runs commands and a way into logs and metrics.
3. A list of "values that must be replaced": which are secrets, credentials or personal data (this decides what step 1 scans for).
4. The current branch and recent history (`git log --oneline`; bisect needs it).

## Actions

Six steps, in order, no skipping. Each step's last line says what "done enough" means.

1. **Redact (before any output at all)**
   - Before any command, terminal output, captured artifact, screenshot or issue body goes anywhere, replace secrets with `<REDACTED>`: API keys, tokens, cookies, sessions, connection strings, private keys, webhook URLs, real emails and phone numbers. Treat everything you post as permanently public: **redact first, post the first line of output second** — in the other order your only remedy is rotating keys.
   - Credentials come from environment variables (`export TOKEN=...`, or a `.env` listed in `.gitignore`) — not in a command, not in a test fixture, not committed.
   - Done: searching the text you're about to post for `api[_-]?key|token|secret|password|BEGIN .*PRIVATE KEY` finds no real values.
2. **Build a feedback loop (first get a reproduction that goes red for this bug)**
   - Target shape: one command plus one assertion, red right now. It can be a failing unit or integration test, a minimal script, a curl call, or a benchmark run — for performance regressions, fixed input, fixed iteration count, a recorded baseline number. Can't reproduce it yet? Shrink the dimensions: smaller input, concurrency off, fixed random seed, fixed clock and timezone, a local stub for the service, a snapshot of the data.
   - Done: the loop goes red for **this** bug and green on unmodified main — if main is red too, either the loop is wrong or the bug is older, and you must write down which; run it once and remember what red looks like.
3. **Minimize**
   - Cut until you can't: unrelated modules, unrelated config, unrelated data, unrelated steps. Done: the reproduction script fits on one screen, and every cut was followed by a rerun that was still red.
4. **Hypothesize (write the guess down, don't keep it in your head)**
   - Write 1–3 candidate causes, each as "if it's true, I should observe ___ / should not see ___"; sort by easiest to falsify and hit the cheapest first. Done: paper or a ticket holds "I think it's ___ because ___; if right, I should see ___", with one observation that could disprove it.
5. **Instrument (test the guess, don't confirm it)**
   - Tools: logs, counters, timers, breakpoints, printing intermediate variables, `git bisect`. Change one variable at a time (five at once verifies nothing) and run every observation back through the step-2 loop.
   - You want observed facts, not a plausible-looking cause; when a hypothesis is disproved, cross it out and write the next one — **ruling a hypothesis out is progress too**. Done: you can point at one output and say "this rules out A and points at B".
6. **Fix + regression test**
   - Turn the loop green first, then freeze the loop into a regression test in the repo — into the default test suite, not a scratch script on your machine. Prove the test tests something: temporarily revert the fix and it must go red.
   - Ask once whether the same class of mistake exists elsewhere; if yes, **open a ticket** — don't fix other modules in the same commit. Done: loop green, full suite green, the regression test red without the fix, temporary instrumentation deleted or demoted to debug level.
7. **Stop-loss line: three rounds without convergence escalates to a design problem**
   - Counting rule: one round = one "changed code and ran the loop"; reading code, reading docs and thinking don't count. Still not converged after three rounds → **stop** and do two things: (1) write an ADR (`docs/adr/NNNN-<kebab-title>.md`) covering the current state, why it won't move, what it costs and how to back out if the call was wrong, and record it in the decision ledger with `decision-ledger`; (2) open a separate ticket titled "redesign X" and put it on the frontier (→ call `ticket-plan`).
   - The other half of the same discipline: two consecutive attempts on one ticket without convergence means go up a level — re-split the ticket, fill in requirements, or prototype first.
   - Reason: what burns the most time in real projects is rarely a hard bug but a **fix loop that refuses to concede**; "try once more" is the most expensive action, and more context doesn't get better, only pricier and messier.

## Outputs

- One minimal reproduction command (or one minimal test file).
- One regression test committed to the repo (the default suite runs it).
- One fix commit (one commit tells one story; no unrelated refactoring smuggled in).
- A written diagnosis record — symptom, hypotheses, eliminations, conclusion (paste it into the ticket; no separate file needed) — or, when the stop-loss line triggered, one ADR + one "redesign X" ticket + the matching decision ledger row.

## Done criteria

- [ ] No real secret is findable in posted commands, logs or artifacts (all `<REDACTED>`); credentials come from environment variables and no `.env` sits in the repo.
- [ ] One command goes red for this bug, and I ran it and saw red — not "it should go red".
- [ ] The reproduction is minimized: one screen or less, and deleting any element makes the red disappear.
- [ ] At least one hypothesis was written, and at least one was **ruled out** by evidence (proof that instrumentation falsifies rather than confirms).
- [ ] After the fix: the reproduction loop is green and the full suite is green.
- [ ] The regression test goes red when the fix is reverted (verified locally once).
- [ ] Problems found outside the fix's scope are ticketed, not smuggled into the same commit.
- [ ] Temporary logs, debug switches and print statements are cleaned up or demoted.
- [ ] If round three still didn't converge: the ADR is written, the redesign ticket is open, and this fix loop has stopped.

## Manual fallback

- **If an external diagnosis skill such as `diagnosing-bugs` is installed, use it to run the six actions; otherwise follow this skill.** The six steps are exactly the six above and need no tooling — paper works (the handbook's chapter-15 manual fallback says "just do the six: redact → reproduce → minimize → hypothesize → instrument → fix plus regression").
- **Can't reproduce**: write "cannot reproduce" into the ticket as a first-hand fact, list every path you tried and what you observed, then switch to "instrument now, wait for the next occurrence" — save the input and a snapshot of the scene so the next one can be replayed. Guessing the cause first is the main way these bugs die.
- **No test framework**: write a script where a non-zero exit code means red; the regression test becomes one command in a pre-commit checklist or in CI. **No usable git history** (one commit, or a squashed history): skip bisect, shrink the input space by hand, and state "no bisect performed" in the conclusion.
- **Only reproducible in production**: don't make experimental changes in production; capture the scene first (input, logs, metrics, data snapshot) and replay it locally. This is not optional — touching production credentials needs human approval and is best done by you in person.
- **Performance regression with no known baseline**: build the baseline first (fixed input, fixed duration, recorded numbers), then talk about optimizing. "It got faster" without numbers is not a conclusion.

## Next step

→ call `dual-axis-review` (after the fix and the regression run); when the stop-loss line triggers → call `ticket-plan` to open the "redesign X" ticket and record the ADR in `decision-ledger`.

## Anti-patterns

| Anti-pattern | Why it's wrong | Instead |
|---|---|---|
| Skipping step 2, or editing code before the reproduction is red | With no red light, every change looks like a fix and you can't tell a fix from a cover-up | Build a loop that goes red for this bug, then run it once and see red |
| Posting output while thinking "this one's probably fine" | A posted secret is leaked; rotation is the only remedy | Replace with `<REDACTED>` before posting |
| Changing five things, then running | You don't know which one mattered and learn nothing from the failure | One variable at a time |
| Collecting only evidence that supports the guess | Confirmation bias; you fix the wrong place | Every hypothesis needs an observation that could disprove it |
| Keeping the loop alive with "try once more" | Context gets pricier and messier; the loop eats the whole session | Three-round stop-loss, escalate to a design problem |
| Leaving temporary logs and debug switches in the commit | Noise for the next debugger, easily mistaken for a feature | Clean up or demote to debug |
| A regression test as a script outside the repo | Nobody runs it again and the same bug returns | Put it in the default suite and verify it goes red |
