<!-- English companion to SKILL.md ｜ same decisions, shorter prose ｜ do not change the structure -->

# ticket-plan

> Handbook step 4 | Outputs: seam list + ticket graph | Done when: the seams are written down, and at least one ticket is unblocked and can start now

## When to use / when not to
**Use** when the seven spec sections are complete and you must answer "how do we build it" and "what first"; when tickets need blocking relations; when a design argument (state-machine boundary, UI variant, concurrency ordering) will not settle in conversation.

**Not** when one session can finish the work — grill it and call `build-ticket` directly; this extra step only buys another chance to drift. Requirements still open → `grill-with-ledger`. Project too big to write the spec at all → `write-spec` first.

**Two jobs, never one step**: technical design answers "how to build it" (module and seam list, ADRs where needed); development plan answers "what first" (ticket graph with `Blocked by`, plus the frontier). A first, then B.

## Inputs
1. `.scratch/<feature>/spec.md` or the tracker copy: all seven sections, with success criteria and out-of-scope. Template `templates/spec.md`.
2. Decision ledger: every decision carries an id `D-nn`, used by the ticket header `Covers:` and by the coverage check after slicing.
3. `CONTEXT.md`: the glossary. Ticket wording matches it, or the next session can only guess.
4. Tracker home: local markdown (`.scratch/<feature>/issues/`) or GitHub / GitLab Issues. Settle it first; never slice tickets inside a conversation.
5. Large projects need one more home: the path to `map.md`.

## Actions
**A. Technical design: how to build it**

1. **Use this vocabulary, no synonyms** — a shared vocabulary makes agent output dramatically shorter: **module** (anything with an interface and an implementation; scale-free — a function, a class, a package); **interface** (the face seen from outside); **depth** (deep module = much behavior behind a small interface; the shape to aim for); **seam** (the boundary you can only see it through); **adapter** (one adapter is a hypothetical seam, two make it real).
2. **List modules, judge depth** — one line each: name / interface / what is hidden behind it. A shallow module whose interface is as large as its implementation is a smell: it tears one ticket into two and leaves tests nowhere to hang.
3. **Draw seams, one line each** — name / what passes through it / who calls it. Write the list into the spec's "implementation decisions" section; if it grows long, save it as `docs/architecture.md` (skeleton `templates/architecture.md`) and give the path.
4. **Match seams to success criteria** — read every spec criterion and ask "through which seam is this one visible?" A criterion that points at no seam means the design missed it.
5. **Architectural decisions become ADRs** — `templates/adr.md`, written to `docs/adr/NNNN-*.md`. Never stuff them into the product design doc: that template is story-shaped, the wrong shape for "what should this module's interface look like". The spec keeps one pointer line.
6. **When debate will not settle, use a throwaway prototype** — shareable HTML so non-coders can push it themselves; a technical prototype, not product UI design, discarded after use, conclusion into an ADR or the ledger. If `prototype` (external skill) is installed, use it; otherwise a minimal runnable script plus one ASCII state diagram, equally disposable.

**B. Development plan: what first**

7. **Slice by five rules, each checkable**: (1) slice by user-visible behavior, not by technical layer — "can export CSV" is a ticket, "write the export module" is not; (2) one ticket, one verifiable result — `Verify:` names a concrete command or action, and if it cannot, this is still a task list; (3) a ticket touches at most two seams — more usually means two tickets were written as one; (4) ask **could a fresh session that never read the spec finish this ticket?** If not, it is not self-contained enough; (5) write `Covers:` in the header, then check that every ledger decision is covered by at least one ticket.
8. **Write the six ticket header lines; do not change the structure** (template `templates/ticket.md`):

   ```
   Status: todo
   Blocked by: -            # use - when unblocked
   Covers: D-01, D-03       # which ledger decisions this covers
   Verify: <one command or action that proves the ticket is done>
   Rounds: -                # attempts made
   Sessions: -              # sessions spanned
   ```

   > Wording note: handbook chapter 2 (4) says "five fixed header lines" — that predates revision 1. Revision 1 added `Covers:`, so **the current shape is six lines**. Step 6 appends `Accept:` and `Review:` for eight lines, and those eight are the collection points for the six metrics in chapter 14.
9. **A ticket graph, not a task list** — each ticket declares which tickets block it. At any moment some tickets have no blockers and can be picked up now: that set is the **frontier**. The frontier is never empty; empty means cyclic dependencies or tickets sliced too large. You always know which one to grab next.
10. **Size by one session** — a ticket runs about 100k tokens. Merge tickets that clearly cannot fill a session; split any that need two sessions. Never compress to fit: compression loses exactly the precision of decisions.
11. **Too large for one session: build the decision map first** — add `map.md` and one more header line `Type: research / prototype / grilling / task`. Each ticket resolves one decision, not one piece of implementation; the map is complete when nothing is undecided and someone else can execute it. Use `wayfinder` (external skill) if installed; otherwise maintain `map.md` and the `Type:` lines by hand.
12. **Land it in the tracker, then close out** — local mode is one file per ticket, numbered from `01`; append comments and history to `## Comments` at the file bottom, never into the header. Then remove the spec's `ready-for-agent` label: an unattended agent polling labels will try to implement the whole parent document instead of picking up a ticket slice.

## Outputs
- Seam list in the spec's "implementation decisions" section (each line: name / what passes through it / who calls it); long version in `docs/architecture.md` (skeleton `templates/architecture.md`).
- Ticket graph: `.scratch/<feature>/issues/NN-*.md`, or tracker tickets with native blocking links; all six header lines present.
- ADRs where needed (`docs/adr/NNNN-*.md`); large projects also `map.md` (decision map, with `Type:` lines).

## Done criteria
- [ ] Every seam has one line with all three fields (name / what passes through it / who calls it).
- [ ] Every spec success criterion points at least one seam; the ones that did not were added to the design or moved to out-of-scope.
- [ ] Architectural decisions live in ADRs; the spec's "implementation decisions" section holds only pointers, no long arguments.
- [ ] Every ticket title is a user-visible result, not a technical-layer noun (action 7, rule 1).
- [ ] Every ticket's `Verify:` is a runnable command or action, taken from the acceptance agreed at step 2, not invented while slicing.
- [ ] No ticket touches more than 2 seams.
- [ ] Every ticket can go to a fresh session that has not read the spec (the self-check answers yes; the rest were re-sliced).
- [ ] Every ticket header has all six lines: `Status` / `Blocked by` / `Covers` / `Verify` / `Rounds` / `Sessions`.
- [ ] Every ledger decision is covered by at least one ticket's `Covers:`; uncovered ones were ticketed or written into out-of-scope.
- [ ] The frontier is not empty: at least one ticket shows `Blocked by: -`, and you can name the one you grab now.
- [ ] No ticket needs two sessions; tickets that clearly cannot fill one session were merged.
- [ ] Large projects: `map.md` exists, every research ticket has a `Type:` line, and nothing in the map is undecided.
- [ ] The `ready-for-agent` label is removed from the spec on the tracker.

## Manual fallback
- No `to-tickets` / `codebase-design` / `wayfinder` / `prototype` (all external skills): **slicing by hand works end to end** — the five rules and the six header lines are the criteria; copy `templates/ticket.md` and edit it, use `templates/architecture.md` for the seam table.
- Tracker unavailable: go local markdown (`.scratch/<feature>/issues/NN-*.md`), keep the six header lines, put blocking in `Blocked by:`, append history to `## Comments`.
- Seams will not settle: compare the options with a throwaway prototype, or record both options and the trade-off in an ADR; mark what cannot be decided yet as "pending + deadline" in the ledger.
- No HTML capability for prototyping: a minimal runnable script plus one ASCII state or sequence diagram, conclusion into the ADR, equally disposable.
- Tickets will not slice cleanly (still messy at ticket five): the scope is too large — go back to `write-spec` and cut scope, or build the decision map first, instead of forcing more slices.

## Next step
→ call `build-ticket` (grab one ticket from the frontier and work it in a new session).

## Anti-patterns
- **Merging technical design and development plan into one step** — "what should the interface look like" and "what first" contaminate each other, so neither settles → A first, then B: A yields the seam list, B yields the ticket graph.
- **Slicing by technical layer ("write the export module"), or one ticket touching three or four seams** — no ticket is verifiable: a pile of finished tickets still leaves users nothing to use, and one session cannot hold it → slice by user-visible behavior; above two seams, split into two tickets.
- **`Verify:` saying "works fine" or "tests pass"** — if no concrete command can be written, this is still a task list → write one runnable command or action.
- **Swapping in synonyms (component / boundary layer / the outer layer)** — every swapped word costs the agent an extra detour, and the seams stop lining up → module / interface / depth / seam / adapter, swap none of them.
- **Skipping the `Covers:` coverage check after slicing** — decisions drop out at slicing time and surface at step 6 as the decision traceability rate, when it is already too late → run the coverage check right after slicing.
- **Leaving tickets on `ready-for-agent` forever** — the frontier fills with finished work and you cannot tell what to pick up next → when a ticket is done, set `Status: done` by hand and add the evidence pointer.
