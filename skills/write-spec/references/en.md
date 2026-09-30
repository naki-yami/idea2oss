<!-- English companion to SKILL.md ｜ same decisions, shorter prose ｜ do not change the structure -->

# write-spec

> Handbook step 3 | Outputs: `.scratch/<feature>/spec.md` (or a spec issue on the tracker) | Done when: all seven sections are present, "out of scope" is non-empty, every ledger decision has a `[D-nn]` back-reference, and the document asserts nothing you don't know

## When to use / when not to

**It only synthesizes; it doesn't ask.** No new interviews — it consolidates what you already agreed; it verifies nothing and decides nothing. It records decisions already made, and is not the place to make new ones. The official criterion is a good one: **an assertion in the document that you never said is a defect.**

**Worth it only when the project is too big for one session.** Work that fits one session goes straight to step 5 after grilling and **skips this step** — the official guidance says "often you should skip the spec"; the extra step is one more chance for the model to drift. **Don't** use it while requirements are still being discussed (back to step 2 → call `grill-with-ledger`), or to pick a technical approach or fix seams (that's step 4 → call `ticket-plan`).

**Lifecycle, four rules — the most counter-intuitive part.** Nothing keeps the document in sync: it is a snapshot of what you knew at that moment, and the first time implementation teaches you something it is out of date.

| Trigger | What to do |
|---|---|
| Implementation taught you something | **Don't go back and edit the document.** `CONTEXT.md` and the ADRs are the long-lived things; what's worth keeping goes there (the official wording: "it's not to edit the spec") |
| The work shipped | Treat it as disposable |
| Direction changed, you're pivoting | Delete unfinished tickets, keep the document — the document is the destination, the tickets are disposable execution steps on the way there |
| The destination itself changed | Redo steps 2 and 3, produce a new one |

**Three known issues**:
1. **It gets labeled `ready-for-agent`** (meaning "no further triage needed"), and unattended agents polling by label implement the whole document instead of picking up ticket slices. Before running unattended: remove the label after splitting tickets, or exclude the parent document explicitly in the agent prompt; state "do not start implementation without permission" in the wrap-up.
2. **Very long documents can come back truncated from the tracker**, with no local copy as a fallback. The fix is context hygiene: keep a local `spec.md` as the single authoritative copy, **don't clear or compact context between steps 3 and 4**, and run both in the same window.
3. **Decisions get compressed at this step** — it synthesizes from the conversation again. That is why the ledger exists (→ call `decision-ledger`).

## Inputs

1. Step 2's outputs: a non-empty ledger + `CONTEXT.md` (+ maybe 0 ADRs).
2. The transcript of that conversation (traceable line by line, not from memory).
3. The landing spot: `.scratch/<feature>/spec.md` is **mandatory**, and local.
4. The seven-section template: `templates/spec.md`.

## Actions

1. **Copy `templates/spec.md`; don't change the structure, only the content.** Keep the seven headings as they are — they are the checklist.
2. **Fill it section by section. What "done" means for each**:
   - **1 Problem statement**: who hits what problem in what situation, and how they work around it today. If you can't write the workaround, the problem isn't real enough.
   - **2 Solution**: one line on what the feature does; no implementation detail.
   - **3 User stories**: `As a <role>, I want <capability>, so that <purpose>`. Cover six facets — **first use / repeat use / errors / edge cases / empty state / permissions** — naming each one; **longer is better**.
   - **4 Implementation decisions**: technical choices already made and why, ending `[D-nn]`; architectural decisions go to an ADR, here only a pointer. **Seam list**, one per line: name / what passes through it / who calls it.
   - **5 Test decisions**: how each success criterion is verified and which seams the tests hang on, ending `[D-nn]`.
   - **6 Out of scope**: what we are explicitly not doing, and why not. **Usually the most useful few lines; never leave it empty.**
   - **7 Notes**: open questions, assumptions, dependencies, references.
3. **Do the ledger back-references (the only mechanical check here)**: land every decision in the step 2 ledger in "implementation decisions" or "test decisions" with a `[D-nn]`. Only two ways a decision can fail to land: it never belonged in scope (write it into "out of scope"), or the spec dropped it. **Both beat letting it quietly disappear.**
4. **Self-check every sentence with "did I say this?"**: ask of each one "which line of the conversation did this come from". Can't trace it back → delete it, or demote it to an open question under "notes". A success criterion with no verification: go back to step 2 and ask, don't guess here.
5. **Store it twice, keep one authoritative**: write the local `spec.md`; the tracker copy is a copy. Run steps 3 and 4 back-to-back in the same context window.
6. **Do label hygiene**: remove `ready-for-agent` once tickets are split, or exclude the parent document explicitly in the agent prompt.

## Outputs

- `.scratch/<feature>/spec.md` (or a tracker spec issue): seven sections, `[D-nn]` at the end of sentences.
- A non-empty "out of scope" list, each item with its "why not".
- The seam list (step 4 splits tickets straight from it).
- Ledger back-reference traces: a `[D-nn]` for every decision, or an explicit disposition in "out of scope".

## Done criteria

- [ ] All seven sections are present; no heading renamed, merged or reordered (check against `templates/spec.md`).
- [ ] "Out of scope" is non-empty and every item says why not.
- [ ] "User stories" names all six facets: first use / repeat use / errors / edge cases / empty state / permissions (facets that truly don't apply state their reason).
- [ ] Every ledger decision has a `[D-nn]` in "implementation decisions" or "test decisions", or is written into "out of scope".
- [ ] The seam list in "implementation decisions" is one seam per line with all three columns (name / what passes through it / who calls it).
- [ ] Every success criterion in "test decisions" has a verification (command or action).
- [ ] Every sentence passes the "did I ever say this?" check: anything that can't be traced back to the conversation is deleted or demoted to an open question.
- [ ] The document asserts nothing you don't know (read it once; anything surprising is a defect — and that also means the grilling was too shallow, not that the document is too long).
- [ ] The local `spec.md` exists and is the single authoritative copy; context was not cleared or compacted between steps 3 and 4.
- [ ] The tracker copy: the label is removed after splitting, or the parent document is excluded in the prompt.

## Manual fallback

- **No external skill such as to-spec**: write it by hand with `templates/spec.md` — **30 minutes is enough**, and doing it by hand walks you down the ledger row by row, so back-references are actually harder to miss. Use a spec skill if you have one; otherwise this path holds.
- **The tracker can't be read back (document truncated)**: the local `spec.md` is the single authoritative copy; split tickets and review from local, and treat the tracker copy as a publication only.
- **User stories won't fill six facets**: go back to step 2 for another round (→ call `grill-with-ledger`); don't invent them in the document.
- **The document keeps growing and reads more and more like an implementation plan**: stop and move the technical choices to step 4's seam list; this step is only "what", not "how to build it".

## Next step

→ call `ticket-plan` (compress it into a seam list + ticket graph, with `Covers: D-nn` in the ticket headers).

## Anti-patterns

| Anti-pattern | Why it's wrong | Instead |
|---|---|---|
| Asking the agent to "make the spec a bit more detailed while you're at it" | It adds assertions you never made, and you're the last to find out | Only synthesize; trace every sentence back; delete what won't trace |
| Making new decisions inside the spec | The decision never reached the ledger or got a number, so nothing downstream can point at it | Settle it back in step 2, ledger it, then fill in the `[D-nn]` |
| Leaving "out of scope" empty | The most useful few lines are gone and scope inflates on its own | Write at least 3 things you're explicitly not doing, with reasons |
| User stories that only cover "first use" | Errors / edge cases / empty state surface during implementation and rework doubles | Name all six facets |
| Editing the document because implementation taught you something | It's a snapshot; editing it means maintaining a document that can never catch up | Write it into `CONTEXT.md` and `docs/adr/` |
| Writing a spec even for work that fits one session | One more chance for the model to drift, for zero gain | Skip step 3 (and the ticket graph), write one ticket and start → call `build-ticket` |
