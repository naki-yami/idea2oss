<!-- English companion to SKILL.md ｜ same decisions, shorter prose ｜ do not change the structure -->

# decision-ledger

> Handbook step 2 (threads through steps 3/4/6) | Outputs: `docs/decisions.md` or `.scratch/<feature>/ledger.md` | Done when: every decision is precise enough to verify, has an evidence cell, and lands in both implementation and acceptance

## When to use / when not to

**Use** after any conversation where something got settled ("this is how it's going to be"); before writing the spec; when splitting tickets, to mark each one `Covers:`; at step 6, to count the decision traceability rate.

**Don't use** for terminology (that belongs in `CONTEXT.md`, not the ledger); for one-off temporary calls (the ticket's "not doing" section holds them); for architecture decisions that qualify for an ADR — the ADR carries the full text, the ledger keeps a one-line pointer.

**Why it exists**: the pipeline's most substantial hole is that decisions get weakened as they travel. `CONTEXT.md` is a glossary by design, most decisions don't qualify for an ADR, and the step-3 spec re-synthesizes everything from the conversation — nothing guarantees a settled decision survives to the end. A precise conclusion flattens into a weak phrase: "label order must survive a restart" becomes "persist sessions", and any implementation satisfying that weak phrase counts as done. **This happens inside one session; context does not have to expire.** The decision ledger numbers each decision so every step can point back to it.

## Inputs

1. A conversation whose decisions are settled (or its record).
2. **One** decision on where the ledger lives (Action 1, pick one — never write both).
3. The existing ledger in full (append, do not rewrite).

## Actions

1. **Pick the ledger location (one per project)**
   - `.scratch/<feature>/ledger.md`: solo, single feature, short term.
   - `docs/decisions.md`: **the default** when someone may take over or the repo may go open source. IDs are never reused globally, so a newcomer reads one file and knows every settled decision.
   - Write the choice into `AGENTS.md`; don't make the next session guess.
2. **Create the header** (four columns, do not rename them):

   | ID | Type | Decision (precise enough to verify) | Evidence |
   | --- | --- | --- | --- |
   | D-01 | constraint | Label order survives a restart | Compare order after restart |

3. **Write it down the moment it's agreed** — append one row on the spot, don't batch to the end (clearing the session voids all of it).
4. **Only three types allowed**:
   - `constraint` — cannot be violated; a violation is a defect and needs a ticket to fix.
   - `default` — changeable, but write down why; when it changes, put the new reason in this row.
   - `TBD` — not decided yet; **must carry a decided-by date**, and if the date lapses it escalates to a step-0 question.
5. **Write decisions "precise enough to verify"**. The criterion runs backwards: **can you write a command or action that proves it**.
   - ✗ weak: "persist sessions" → ✓ strong: "label order survives a restart" (evidence: compare order after restart)
   - ✗ weak: "robust error handling" → ✓ strong: "a failed message can be retried without clearing existing or unsent messages" (evidence: the retry-after-failure case)
   - If you cannot fill the evidence cell, the decision isn't settled: mark it TBD and give it a date.
6. **IDs are never reused**. Strike through a deleted decision and keep the row — one back-reference pointing at the wrong thing makes the ledger worthless.
7. **Three back-reference points** (this is where the ledger earns its keep):
   - Step 3: the spec's "implementation decisions" and "test decisions" each carry `[D-01]`. A decision that won't land has two legal outcomes: move it to "out of scope", or say the spec missed it. **Both beat letting it vanish quietly.**
   - Step 4: ticket headers read `Covers: D-01, D-03`. After splitting, check once: **every decision is covered by at least one ticket** — the only automatic way to catch a decision dropped while splitting.
   - Step 6: on the spec axis, check line by line that every decision points at implementation and verification evidence.
8. **Count the decision traceability rate**: decisions with evidence ÷ all decisions. **Target 100%.** Below 100% there are only two explanations: the decision was dropped, or it was weakened. Anything with no evidence gets a ticket on the spot or goes to "out of scope".
9. **Ask two questions before closing** (cheap, and they regularly surface real risk and one silent overreach):
   - "What three questions did you not ask?"
   - "Which conclusions this round did you decide for me?" — every one of them goes into the ledger.

## Outputs

- One decision ledger file (`docs/decisions.md` or `.scratch/<feature>/ledger.md`), four columns, IDs consecutive and never reused.
- Template: `templates/ledger.md` (appendix A7 skeleton, do not change its structure).
- Back-reference traces: `[D-nn]` in the spec, `Covers:` in ticket headers, the traceability number at step 6.

## Done criteria

- [ ] Ledger location decided, and it exists in **exactly one place**; `AGENTS.md` says where it is.
- [ ] Every decision is precise enough to write one executable piece of evidence (not an adjective, not a slogan).
- [ ] The `Evidence` cell is non-empty on every row.
- [ ] Types are only constraint/default/TBD; every TBD has a date.
- [ ] IDs are consecutive and never reused.
- [ ] After the spec: every decision has a `[D-nn]` in the spec or appears explicitly under "out of scope".
- [ ] After splitting tickets: every decision is covered by at least one ticket's `Covers:` (a non-empty `frontier` is `ticket-plan`'s own criterion; this skill does not manage it).
- [ ] Before acceptance: decision traceability rate = 100% (anything with no evidence already has a ticket or sits under "out of scope").

## Manual fallback

- No `to-spec` / `to-tickets` skills: **write the ledger anyway**. It is a four-column table any editor can maintain; when you write the spec and tickets by hand, walk them against the ledger line by line (the handbook budgets 30 minutes for a hand-written spec).
- No tracker: keep the ledger at `.scratch/<feature>/ledger.md`, write back-references the same way, traceability still counts.
- The conversation was too scattered to find decisions: record only the ones that "changed what the later work is" — the test is "would the implementation get it wrong without this?" Yes → record; no → skip.

## Next step

→ call `write-spec` (land each decision in the seven-section doc, ending lines with `[D-nn]`); when splitting tickets → call `ticket-plan`.

## Anti-patterns

| Anti-pattern | Why it's wrong | Instead |
|---|---|---|
| Not recording after the talk, trusting "the next session will remember" | An unwritten agreement never happened | Append a row on the spot |
| Decisions written as adjectives ("robust", "fast") | Unverifiable, so nothing was decided | Write a sentence you can produce evidence for |
| The ledger lives in two places (`.scratch` and `docs/`) | It forks immediately and nobody knows which to trust | Keep one; delete the other or turn it into a pointer |
| Stuffing terminology, TODOs and ideas into the ledger | It becomes a diary and traceability stops meaning anything | Terminology → `CONTEXT.md`, tasks → tickets |
| Reusing IDs (delete D-03, number a new decision D-03) | Old back-references now point at the new decision | Never reuse; strike through and keep |
| Decisions only in the spec, with no IDs | Coverage can't be checked automatically | End the line with `[D-nn]` |
