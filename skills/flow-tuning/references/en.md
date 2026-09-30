<!-- English companion to SKILL.md ｜ same decisions, shorter prose ｜ do not change the structure -->

# flow-tuning

> Handbook chapter 14 | Outputs: six metric trends + one conclusion on which step to change | Done when: all six metrics have a reviewable trace (command / number / minutes) and a baseline recorded before you changed the flow

## When to use / when not to

**Use**: to find out whether this flow is worth anything; two weeks of worsening trend; review rework or escaped defects running high; **before changing the flow** (measure a baseline first); a retro after shipping a batch of tickets.

**Don't**:
- Use it to score or rank people. The point of the metrics is to tell you which step to change, not to grade you.
- Ask "is the flow good" before a single ticket is finished — the sample is too small; and skip it entirely for L0 work done in half a day that only you use.

**Collection is just the ticket header lines** (`Verify:` / `Rounds:` / `Sessions:` / `Review:` / `Accept:`), plus the acceptance conclusion step 6 writes into the ticket and the numbers in the ledger. **Fill them in while writing the ticket; no extra bookkeeping.**

## Inputs

1. Ticket files (six header lines + Comments): `templates/ticket.md` — `Rounds:` and `Sessions:` feed the first two metrics.
2. The ledger (numbers + evidence column) — the denominator of the decision traceability rate (→ call `decision-ledger`).
3. Step 6's acceptance conclusion (the `Accept:` line) and the two-axis finding counts (the `Review:` line).
4. **The same table from the previous cycle.** Without one, collect for two weeks first — those two weeks are the baseline, and the baseline is itself an output.
5. Bug fixes after release + tickets delivered (escaped defects); a clean environment + README (stranger onboarding time).

## Actions

1. **Measure a baseline first; don't rush to change the flow.** DORA 2025's conclusion: AI is an amplifier — it amplifies a team's existing strengths and its existing weaknesses. Without a baseline you know neither whether the flow improved anything nor which side is being amplified. The method is crude: record these metrics on the current flow for two weeks, then touch the flow.
2. **Collect the six metrics**, all from files you already have:
   - **First-pass convergence rate** — share of ticket headers with `Rounds:` = 1. Wanted: rising. Low means tickets are cut too big or the requirements weren't clear.
   - **Decision traceability rate** — share of ledger decisions with evidence in implementation and acceptance. Wanted: 100%. Below 100% means decisions were dropped or weakened along the line.
   - **Review rework** — `Review:` finding count per ticket. Wanted: falling. High means step 2 was skipped or the seams were never fixed.
   - **Escaped defects** — bugs fixed after release ÷ tickets delivered. Wanted: falling. High means step 6's acceptance was a formality.
   - **Context cost** — ticket header `Sessions:`, and whether handoff was used. Wanted: steady at 1. Rising means the ticket is too big or discipline slipped.
   - **Stranger onboarding time** — minutes from a clean environment following the README to a working run. Wanted: under 30 minutes. Over 30 minutes means step 8 isn't finished.
3. **Every number keeps a reviewable trace**: a command, a number, a minute count. **Never write "it felt faster".**
4. **Judge ticket size with the context budget as the ruler**: the smart zone is on the order of ~150k tokens, and the industry gives one estimate of about 100k tokens per ticket. Two practical calls follow: a ticket that clearly won't fill one session can be merged; **a ticket that needs two sessions should be split, not forced through with compaction** — compaction converges information, and what's lost here is exactly the precision of decisions. Also: the handling order is "continue the current session → clear → hand off → dispatch subagents → compact"; when you need a handoff → call `session-handoff`.
5. **Three hard rules** (all with external evidence, not your preference):
   - **Don't trust self-reported data.** METR ran a randomized controlled trial: 16 experienced open-source developers, 246 real tasks; the group allowed to use AI finished 19% slower, while the same people had predicted 24% faster beforehand and still believed they were about 20% faster afterwards. **Subjective feeling and measured result can have opposite signs** — that's why all six metrics must leave a reviewable trace, and "it felt faster" is not data.
   - **Measure a baseline before talking about improvement.** See rule 1.
   - **Don't let one metric rule everything.** DORA's current delivery performance metrics are five: deployment frequency, change lead time, change failure rate, failed deployment recovery time, deployment rework rate (MTTR from the early "four keys" is replaced by failed deployment recovery time). It explicitly calls "looking at a single metric" a trap: speed alone sacrifices stability, stability alone sacrifices delivery. Same for these six — **read the combination, not any single one.**
6. **Only your own project's trend, never a cross-project comparison**: ticket sizes, languages and dependencies differ, so most of the difference you'd measure isn't caused by the flow.
7. **Two weeks of worsening trend → go back and change the flow**, usually by returning to steps 2 and 4 (requirements and ticket cutting), not by writing code harder.
8. **Write the conclusion down**: which metrics moved / which step they point to / what to change next cycle / which metrics to re-measure afterwards.

## Outputs

- The cycle record for the six metrics (one table), every number with a reviewable trace.
- **One conclusion**: which of the nine steps to change, and what to change next cycle.
- Two records, before and after the flow change (for comparison; the first one is the baseline).
- For every ticket with `Sessions:` > 1, one line of disposition: merge / split / watch.

## Done criteria

- [ ] All six metrics were collected; any that couldn't be says "not applicable + why", never left blank.
- [ ] Every number points to a command, a number or a minute count — no "it felt faster" descriptions in the table.
- [ ] At least one baseline record spanning two weeks or more (on the first run, the baseline is this run's output).
- [ ] The conclusion points at **one specific step** of the nine, not "be more careful from now on".
- [ ] The conclusion rests on a combination of at least three metrics; no single metric drove it alone.
- [ ] `Rounds:` / `Sessions:` / `Review:` were filled in while writing the ticket; anything reconstructed afterwards is marked and excluded from the statistics (numbers from memory are exactly what the first hard rule blocks).
- [ ] Every ticket with `Sessions:` > 1 has a disposition.
- [ ] If the flow was changed: the same metrics were re-measured, and the two records sit side by side for comparison.

## Manual fallback

- **No tracker**: tickets are local markdown (`.scratch/<feature>/issues/NN-*.md`); write the six header lines as usual and collection still works.
- **Header lines missing and unrecoverable**: **exclude that ticket from the statistics** and state the sample size in the record — don't invent numbers from memory.
- **No CI / no release process**: approximate escaped defects with "bug fixes ÷ tickets delivered" and note the changed definition in the record.
- **No second person**: time the stranger run yourself — wipe the virtual environment (or use another machine / a new directory), follow only the README from scratch, write down the minutes. If no clean environment exists, record "cannot measure"; don't guess.
- **No two-axis review skill**: go through `templates/manual-review.md` by hand and fill the `Review:` count the same way.
- **Can't parse token counts**: `Sessions:` and `Rounds:` are your proxy metrics; don't go counting tokens.

## Next step

→ Go back to the step the conclusion points at: requirements or acceptance unclear → call `grill-with-ledger`; tickets cut wrong → call `ticket-plan`; acceptance a formality with escaped defects high → call `dual-axis-review`; one ticket spanning sessions → call `session-handoff`; stranger onboarding time won't come down → call `oss-launch`; the tier needs trimming → call `project-brief`.

## Anti-patterns

| Anti-pattern | Why it's wrong | Instead |
|---|---|---|
| Using "it felt faster" as data | METR: the group allowed to use AI measured 19% slower, the same people had predicted 24% faster and still believed ~20% faster afterwards — subjective and measured can have opposite signs | Only accept a command, a number, a minute count |
| Changing the flow without a baseline | You don't know what improved, or which side the amplifier is amplifying | Record these metrics for two weeks first, then touch the flow |
| Letting one metric rule everything | Speed alone sacrifices stability, stability alone sacrifices delivery (DORA's five metrics; single-metric is a trap) | Read the combination — at least three metrics together |
| Skipping step 2 and implementing straight away | Requirements surface mid-implementation and rework doubles — convergence rate and review rework both get worse | Grill first for L1 / L2, then split tickets |
| Doing two tickets in one session | The second ticket carries the first one's trial-and-error budget and `Sessions:` creeps up | One ticket, one session, and fill `Sessions:` in the header on the spot |
| Using "try again" instead of "go up a level" | Running out of context brings no convergence, only more cost and mess | If two attempts don't converge, re-cut the ticket / ask more about requirements / build a prototype |
| Marking findings "handle later" without opening a ticket | The debt is forgotten and the review rework number loses its meaning | Open a ticket on the spot, or record the acceptance explicitly in an ADR |
| Letting the agent accept the code it wrote itself | Judging your own work is no acceptance, and escaped defects rise afterwards | Technical acceptance through two-axis review, product acceptance by your own hand |
| Running unattended agents without watching agent count or tokens | Known to recurse, measured to burn hundreds of thousands of tokens; context cost blows up | Cap the agent count and budget, and check the background task list afterwards |
| A repo with no explanation anyone else can follow | Stranger onboarding time never gets under 30 minutes and only you can use the project | Finish step 8's front door and accept it with the stranger-in-30-minutes test |
