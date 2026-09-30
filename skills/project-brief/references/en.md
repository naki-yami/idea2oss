<!-- English companion to SKILL.md ｜ same decisions, shorter prose ｜ do not change the structure -->

# project-brief

> Handbook step 0 (ch. 3) | Outputs: `brief.md` (one page max) | Done when: all five sentences are written, "won't do" ≥ 1, "kill criteria" ≥ 1, the smallest verifiable slice fits in one sentence, and a license is chosen

## When to use / when not to

- Use: you have an idea but haven't decided whether to build it or how big it should be; you're about to spend more than half a day on it; you plan to open source it or give it to others (the license is decided here, not at step 8).
- Don't use: an L0 one-off (done within half a day, only you use it, never lands on main) — one sentence of kickoff is enough, don't write a page for it. Adding a brief after the spec is already written is backfilling a document, not kicking off.
- One discipline: **10 minutes, one person, no agent allowed**. This step saves more money than any step after it; an agent-written brief is the agent thinking for you, and you still haven't thought.
- Why it can't be skipped: between idea and repo sits the one judgment that really loses money — is this worth doing, how big, and what counts as success. Skip it and the scope only surfaces at step 4 when you cut tickets, the tickets don't divide cleanly, context burns on redefining the problem, and by then you have written a lot of code.

## Inputs

1. An idea (one sentence counts).
2. Target user or usage scenario — the more specific the better.
3. How this is worked around today: a manual process, another tool, or just putting up with it.
4. Whether you plan to open source it ("haven't thought" counts as input; it becomes a TODO line in the brief).
5. A 10-minute timer.

## Actions

1. **Five sentences, each written precisely.** Every one must be checkable by a second person:

   | # | What to write | Counter-example (doesn't count) | Good example |
   |---|---|---|---|
   | 1 | for whom | collective nouns like "developers", "everyone" | "the ops person who exports a report by hand every week" |
   | 2 | solves what | "it's a pain right now" | "today I copy 40 rows into Excel one by one, about 20 minutes" |
   | 3 | success looks like | "it works", "faster and better" | "a new user completes one export within 5 minutes" |
   | 4 | what you won't do | left blank, or "later maybe" | "no accounts, no permissions, no database" |
   | 5 | when to kill it | "depends" | "if nobody wants to try it within two weeks, or I have to implement login myself, stop" |

   The criterion for sentence 3 in one line: **"it works" is not a criterion; "a new user completes one export within 5 minutes" is**. It must be observable — read it to a second person and they can say what counts as achieved.
2. **Sentences 4 and 5 are hard requirements**: at least one each. Scope only inflates, it never shrinks by itself; if the stop-loss line isn't written down in advance, sunk cost will decide for you.
3. **Write the smallest verifiable slice**: the smallest feature that validates the core assumption. It is usually step 4's first ticket — write it now and step 4 doesn't have to renegotiate scope.
4. **Pick the license now** (this step is where it saves the most). Answer one question first: **do you want people to use it as widely as possible, or do you want derivative works to stay open?**
   - Most widely used, including inside closed-source products → MIT (shortest, most permissive, most familiar to enterprises; the cost is no patent grant).
   - Equally permissive but with an explicit patent grant → Apache-2.0 (preferred by big-company compliance; requires noting which files you changed).
   - Derivative works must stay open → GPL-3.0 (copyleft; corporate policy often bans it outright).
   - Changes to a network service must stay open → AGPL-3.0 (covers SaaS; most likely to be blocked by corporate policy).
   Libraries lean permissive (MIT / Apache-2.0) because more users is better; self-hosted apps may be stricter. The three delivery steps (full LICENSE text / `license` field in package metadata / end of README) wait for step 8, but **which one must be decided now**.
5. **Write the three reasons into the brief** (why here and not step 8): the license **decides your dependencies** — **one GPL dependency contaminates your license**, and finding out at step 8 leaves you swapping the dependency or the license; it decides whether you can accept contributions and whether you need a CLA / DCO; it decides whether enterprises dare to use your thing. One more: once there are external contributors, **changing the license means contacting every contributor for consent** — very expensive.
6. **Read it back at the end**: is any of the five sentences an adjective, is any one you don't believe yourself? Then rewrite that sentence in place and don't move on.

## Outputs

- `brief.md`, one page max (`docs/agents/brief.md` or `.scratch/<feature>/brief.md`, keep only one of the two).
- Template: `templates/brief.md` — copy it and change the content; do not change the structure.
- Input for the next two steps: sentences 2 and 4 feed step 2's grilling directly; the smallest verifiable slice becomes step 4's first ticket directly; the license conclusion carries into step 8 without renegotiation.

## Done criteria

- [ ] `brief.md` exists and is at most one page (readable in one screen).
- [ ] All five sentences are there, and each points at a specific line.
- [ ] "Won't do" ≥ 1 and "when to kill it" ≥ 1 — countable.
- [ ] Sentence 3 is an observable statement with no words like "works", "better", "faster".
- [ ] Read it to a second person and they can say what counts as achieved.
- [ ] The smallest verifiable slice fits in one sentence, and is marked as step 4's first ticket or not.
- [ ] Whether it's open source is stated; if yes, one of the four licenses is chosen with a reason.
- [ ] No agent was opened this step: you wrote the five sentences yourself (an agent may at most help with formatting).
- [ ] This step took no more than 10 minutes; if it ran over, cut scope instead of writing more.

## Manual fallback

- No skill set installed: this step is manual by nature — fill in `templates/brief.md`, 10 minutes, and not one criterion changes.
- **Can't write the success criterion**: you haven't thought through what you're building. **Stopping here saves time** — don't paper over it with "I'll write it and see"; that vague brief will take its revenge with interest at step 4.
- The idea is too big for one session: cut the smallest verifiable slice (i.e. the first ticket). If you can't even cut a slice, write a one-page "what's still undecided" (use an external skill like `wayfinder` if installed; otherwise by hand, one line each).
- Someone else must decide (budget, compliance, open source or not): send it as a questionnaire (use an external skill like `to-questionnaire` if installed; otherwise a three-sentence email — what we want to build, what you need to decide, when we need it), **don't guess**.
- Fully offline, no agent allowed: this is the step that never allows an agent anyway, just do it.
- Code already exists and you're backfilling the kickoff: write it anyway, and put the current state in sentence 2 (how they do it today) — more useful than pretending to start from zero.

## Next step

→ call `repo-bootstrap` (when the repo doesn't exist yet); otherwise → call `grill-with-ledger`.

## Anti-patterns

| Anti-pattern | Why it's wrong | Instead |
|---|---|---|
| "Works" or "faster" as the success criterion | unobservable and unverifiable, equivalent to not defining it | write one observable sentence: who finishes what within how long |
| Not writing "won't do" | scope only inflates and step 4's tickets don't divide | at least one line, and say why not |
| Not writing "when to kill it" | sunk cost will decide for you | write the stop-loss line in advance |
| Letting an agent write the brief for you | kickoff is judgment, not document work; it thinks it through and you still haven't | you write it; an agent may at most format |
| Pushing the license to step 8 | changing it mid-way means contacting every contributor and auditing GPL dependencies | pick one of four at step 0 and write it into the brief |
| Spending two hours turning the brief into ten pages | the output of kickoff is judgment, not document thickness | one page max; past 10 minutes, go cut the slice |
