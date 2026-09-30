<!-- English companion to SKILL.md ｜ same decisions, shorter prose ｜ do not change the structure -->

# grill-with-ledger

> Handbook step 2 | Outputs: `CONTEXT.md` + decision ledger + `docs/adr/` (possibly 0) + acceptance method | Done when: the glossary is non-empty; every ledger decision is verifiable; the ADRs cover that class of decision (or the repo says "no ADR this step"); the acceptance method is executable

## When to use / when not to

**Use**: requirements still only in your head; before L1 / L2 work starts; before writing a spec; when splitting tickets reveals you can't say clearly what you want. It grills you back: a round of questions → waits for you → the next round, each question carrying its recommended answer, so you can just say "agreed". You never have to produce a perfect requirements description first.

**Don't**:
- Project too big for one session → build a decision map instead of forcing it here (→ call `ticket-plan`: an extra `map.md`, an extra `Type:` line per ticket; if the external `wayfinder` is installed, use it).
- The answers live in someone else's head (user, colleague, client) → make a questionnaire (see Manual fallback); don't answer for them.
- L0 (done in half a day, only you use it, never lands on main) → skip grilling, just work.

| What got agreed | Where it lands | When to write |
|---|---|---|
| A term — the project's official name for this thing | `CONTEXT.md` | **on the spot, never saved to the end** |
| A decision meeting all three gates: hard to reverse + confusing out of context + a real trade-off | an ADR under `docs/adr/` | the round it's agreed |
| Everything else agreed | the conversation only, never written down | — |

**The third row costs the most**: `CONTEXT.md` is a glossary, not a spec; the ADR gates are strict and most sessions produce none. So write it down the moment it's agreed and move to step 3, or what was agreed dies with the context.

**Three known issues**:
1. **Decisions get weakened in transit — the most important one.** The step 3 spec synthesizes from the conversation again, and nothing checks that every settled decision reached the user stories, the acceptance items and the implementation. Precision gets compressed into weak statements: "tag order must stay identical across restarts" becomes "persist sessions". This happens inside one session too, no context expiry needed. That is why the ledger exists (→ call `decision-ledger`).
2. **A pile of questions at once, no recommended answers, no mention of `CONTEXT.md`** → dependencies didn't load. Ask it: "which skills did you load?"
3. **Installed alone it doesn't work** → without its dependencies grilling degrades into ordinary Q&A that writes nothing down.

## Inputs

1. An initialized repo (step 1 output): git works and the first commit is in — otherwise what you agree has nowhere to land.
2. A one-line idea, ideally `brief.md` already (step 0's "what we're not doing" and "give-up conditions").
3. Locations of the three drop-off points (defaults: repo root `CONTEXT.md`, `docs/decisions.md`, `docs/adr/`).
4. This run's tier: L0 may skip, L1 / L2 must do it.

## Actions

1. **Fix the drop-off points once, for good.** Where the glossary, ledger and ADR directory live goes into `AGENTS.md`, so the next session doesn't have to guess.
2. **Give it the prompt and let it grill you**: 3–5 questions per round, each with its recommended answer; it asks the next round only after you answer. Write "don't ask everything at once" and "don't decide for me" explicitly. "Agreed" means you accept its recommendation.
3. **Write it down the moment it's agreed — never save it to the end** (clearing the session voids all of it):
   - term → append a line to `CONTEXT.md`: term / one-line definition / don't call it.
   - decision → append a numbered line to the ledger; numbers are never reused (→ call `decision-ledger`).
4. **Gate ADRs strictly on three conditions**: hard to reverse + confusing out of context + a real trade-off — **all three at once** before writing `docs/adr/NNNN-*.md`. Producing none is normal; then write "no ADR this step" in the repo instead of leaving it blank for people to guess.
5. **Ask specifically about boundaries and "what we're not doing"**: what happens on error, what the empty state looks like, who can see and who can change (permissions), what is explicitly out. These four surface mid-implementation most often, and rework doubles there.
6. **You must get an acceptance method**: every success criterion lands on "how to verify" — one runnable command or one concrete action. It carries through to step 3's test decisions, the `Verify:` line in ticket headers, step 6's acceptance. **Acceptance bolted on afterwards is no acceptance.** A criterion with no verification gets marked "pending" on the spot, with a deadline.
7. **Two questions before closing** (cheap, and they often dig out real risk plus one silent overreach): "which three questions haven't you asked?" and "which conclusions this round did you decide for me?" — the ones it decided go into the ledger row by row.
8. **Convergence check**: still asking "should we do this" after several rounds instead of "how" means the blocker is the go/no-go call, not requirement detail — stop, go back to step 0 and fill in the success criteria (→ call `project-brief`); don't keep asking detail.

## Outputs

- `CONTEXT.md` (glossary, non-empty).
- Decision ledger: `docs/decisions.md` or `.scratch/<feature>/ledger.md` (non-empty, four columns, numbers never reused).
- 0 or more ADRs under `docs/adr/` (0 requires the line "no ADR this step").
- The acceptance method written into `brief.md` or a ticket (every criterion → how to verify).
- Templates: `templates/CONTEXT.md`, `templates/ledger.md`, `templates/adr.md`.

## Done criteria

- [ ] `CONTEXT.md` exists and is non-empty; every term explains itself in one line and has a "don't call it".
- [ ] The ledger exists and is non-empty; every row has all four columns (number / type / decision precise enough to verify / evidence), and the evidence column is non-empty.
- [ ] Ledger numbers are consecutive and never reused.
- [ ] Every decision yields a verification command or action; the ones that don't are marked "pending" with a deadline.
- [ ] Every ADR in `docs/adr/` passes all three gates; if there are none, the repo says "no ADR this step".
- [ ] Every success criterion states how to verify it (one command or one action).
- [ ] Both closing questions were asked; the answers to "which conclusions did you decide for me?" went into the ledger row by row.
- [ ] The three drop-off point locations are in `AGENTS.md`.
- [ ] Questions still stuck on "should we do this" went back to step 0 instead of being discussed as requirement detail.

## Manual fallback

- **No external skill such as grilling / grill-with-docs**: list 20 questions yourself and answer them one by one, covering two classes without fail — edge cases and what we're not doing. Add terms with `templates/CONTEXT.md`, decisions in the ledger (`templates/ledger.md`), the three qualifying decisions with `templates/adr.md`. Use a grilling skill if you have one; otherwise this path holds the same criteria.
- **The answers live in someone else's head**: make a questionnaire (same questions + your pre-filled recommended answers), send it, get it back, then land it row by row. Don't answer for them.
- **The skill goes silent and writes nothing**: switch to another session, paste the transcript back, and land it by hand with step 3's three-row table — writing it down depends on no skill.
- **You are the only person**: treat the recommended answers as a hypothetical colleague's and ask yourself "would they object" for each; where they would object is the real question.

## Next step

One session finishes the work: → call `build-ticket` (write one ticket now from `templates/ticket.md`, skip the ticket graph). Several tickets or across sessions: → call `write-spec`, then `ticket-plan`.

## Anti-patterns

| Anti-pattern | Why it's wrong | Instead |
|---|---|---|
| Dumping 20 questions at once and waiting for each answer | You answer the easy ones; the hardest question is exactly the one that vanishes | 3–5 per round, each with a recommended answer |
| Letting the agent decide for you and carrying on | The project ends up carrying constraints you never agreed to | Always ask "which conclusions did you decide for me" at the close, then ledger them row by row |
| Not writing it down, trusting the next session to remember | An agreement nobody wrote down didn't happen | Write it down the moment it's agreed |
| Using `CONTEXT.md` as a spec | It's a glossary; implementation detail is more than it can carry | Decisions into the ledger, qualifying ones into an ADR, the rest straight into step 3 |
| Writing every decision up as an ADR | Loosen the gate and ADRs carry no information; nobody reads them again | All three gates at once; if none qualify, write "no ADR this step" |
| Skipping this step and implementing straight away | Requirements surface mid-implementation and rework doubles | Grill first for L1 / L2; if two attempts don't converge, go up a level |
