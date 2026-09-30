<!-- English companion to SKILL.md ｜ same decisions, shorter prose ｜ do not change the structure -->

# session-handoff

> Handbook step 7 (includes the chapter-12 discipline) | Outputs: a pre-commit check + a PR description + a handoff document | Done when: the check ran once, the PR answers all four questions, and the handoff document gives paths only and is redacted

## When to use / when not to

**Use** when a ticket passed acceptance and you're about to commit or push a branch; when opening a PR; when a handoff signal appears (see Action 6); when one round is done and the next begins.

**Don't use** before the ticket passes acceptance (go back to `dual-axis-review`); for everyday mid-work commits (no PR description needed, but the pre-commit check still runs); for a one-off local experiment (nothing reaches main, so no handoff document).

**Three things, none optional**: move the check before the commit, prepare the PR, hand the session off. The first two answer to other people; the third answers to the next session.

## Inputs

1. An accepted ticket carrying `Verify:` (one command that runs) and `Accept:` (your own written conclusion).
2. The current branch and the changes being delivered (`git status`, `git diff` — you should know which change belongs to this ticket), plus the project's check commands: what lint / typecheck / test are.
3. The relevant paths — spec, tickets, ADRs, decision ledger, architecture doc (the handoff document copies paths, never content) — and the OS temp directory to write into (Linux/macOS `$TMPDIR` or `/tmp`; Windows `%TEMP%`).

## Actions

1. **Move the check before the commit** — pick one, matching the project
   - **Node**: a pre-commit hook — Husky `pre-commit` + lint-staged formatting the staged files + typecheck and test inside `pre-commit`. Installing it **stages and commits everything you currently have, once**, as a smoke test, so do it only in a clean project directory, never one full of loose files.
   - **Not Node**: skip the hook and put the same checks in CI, or write a pre-commit checklist (the three commands lint / typecheck / test) into `CONTRIBUTING.md` or `AGENTS.md`.
   - **No tooling at all**: run the three commands by hand before committing and document them so the next person can run them too. Done: the hook or checklist **exists** and **ran successfully once** — not "installed but never run".
2. **Write the PR description — answer four questions** (structure from `templates/pr.md`, don't change it)
   - **What changed** — one paragraph, not a transcription of the diff. **Why** — links to the ticket / issue, what problem it solves, what happens without it.
   - **How to verify** — commands, steps, expected result; paste output snippets when useful.
   - **Risk and rollback** — the worst case, the blast radius, how to back out.
   - **A PR missing the last one is a PR nobody dares merge when things go wrong.** Put `Closes #NN` in the links section; one ticket, one PR — or one ticket, one branch. Boundary: this skill doesn't do Git itself; committing, tagging and pushing are yours.
3. **Write the handoff document** (structure from `templates/handoff.md`, six sections, don't change it)
   1. **Current state**: which step, which ticket is half done.
   2. **Done**: **results only, not process** (process lives in the diff and the tickets).
   3. **Not done and next**: the next session's first action, **down to file and function**.
   4. **Key paths**: **paths only, never content** — spec `.scratch/<feature>/spec.md`, tickets `.scratch/<feature>/issues/NN-*.md`, decisions `docs/adr/NNNN-*.md`, ledger `docs/decisions.md`.
   5. **Suggested skills**: which skills the next agent should call, in order; where a skill is missing, write the matching manual fallback path.
   6. **Known traps**: pitfalls hit and what they taught; write "none" if there are none.
4. **Store the handoff document in the OS temp directory** — not the workspace, not the repo, not committed; if it shows up in `git status` it's in the wrong place. The reason: a handoff document is the easiest thing to paste somewhere else, and inside the repo it stays forever and forks from the docs.
5. **Re-check the redaction yourself before relying on it** — scan for API keys, tokens, passwords, cookies, connection strings, private keys and personal data (names, emails, phone numbers, customer data) and replace all of it with `<REDACTED>`. Example: `Select-String -Path <file> -Pattern 'api[_-]?key|token|secret|password|PRIVATE KEY'` (on macOS/Linux, `grep -niE '<the same pattern>' <file>`). **Don't just trust "the skill says it redacts".** Redaction failure is the defect you can't see until it's unrecoverable — read the document end to end yourself before handing it over.
6. **Decide: hand off, or push through** (any one of these is a handoff signal)
   - You're explaining the same thing again (usually the second time).
   - There are more files to read than conversation to recall.
   - The ticket's acceptance criteria changed — this is no longer the same ticket.
   - Hand off on any one of them, or open a fresh session; pushing through to context exhaustion ends in a handoff anyway, just a worse one.
7. **Treat a second round as its own discipline**
   - Don't keep chatting in the original session: make round two a brand-new small cycle and walk requirement alignment → ticket splitting → implementation again (→ call `project-brief` / `grill-with-ledger` → `ticket-plan` → `build-ticket`). The context at the end of round one is full of expired assumptions — they no longer help you, they only decide for you.
8. **Name clarification** (one line is enough, put it in the handoff document) — the `/spawn` floating around online doesn't exist; spawn is just an English verb in these skills' prose ("spawn sub-agents"), and **the handoff skill writes a document only, it starts no processes**. A variant that dispatches a background agent (claude-handoff) supports Claude only and calls `claude --bg`; without the Claude CLI installed it won't run, and the flow needs no change for it.

## Outputs

- A pre-commit hook or a pre-commit checklist (one of the two, existing and run once), and a PR description with all four questions answered, structured like `templates/pr.md`.
- A handoff document (`templates/handoff.md`, six sections), in the OS temp directory, redacted.
- The next ticket's input list: which files to read, which command to run.

## Done criteria

- [ ] The pre-commit hook is installed and ran successfully once; or (non-Node / can't install) the same checks are in CI, or the pre-commit checklist is written into the docs.
- [ ] All four PR questions have answers, and `Risk and rollback` is neither empty nor the words "no risk".
- [ ] The PR links its ticket (`Closes #NN` or an equivalent link).
- [ ] The handoff document has all six sections; the `Key paths` section holds paths and nothing pasted from the content.
- [ ] The handoff document sits in my OS temp directory and does not appear in `git status`.
- [ ] I reread the handoff document myself and found no real secrets or personal data (with the result of that search attached).
- [ ] `Not done and next` is specific down to file and function; the next session can start working straight away.
- [ ] The next ticket's input list is written (which files to read, which command to run, what the acceptance criteria are).

## Manual fallback

- **If external skills such as `handoff` / `pr` / `setup-pre-commit` are installed, use them; otherwise it's all manual**: copy `templates/pr.md` for the PR description and `templates/handoff.md` for the handoff document.
- **No redaction tooling**: read it section by section yourself and replace `api_key`, `token`, `password`, private keys and real names/emails/phone numbers with `<REDACTED>` — this can't be skipped and can't be outsourced. **Can't install a pre-commit hook**: put the three commands lint / typecheck / test into CI, or write a pre-commit checklist; never skip the check because the tooling is missing.
- **Temp directory not writable** (locked-down environment/sandbox): write anywhere outside the workspace that won't be committed, note "do not commit" on the document's first line, and confirm `.gitignore` covers it.
- **The next session is you again**: write the document anyway — written down is written down; memory is not a file and a conversation is not a file.
- **No platform to open a PR on** (purely local repo): turn the PR description into a delivery note in the ticket or the commit message — all four questions, none skipped.

## Next step

→ call `oss-launch` for a repo going public; back to `dual-axis-review` if the ticket hasn't passed acceptance; → call `project-brief` to start the next cycle.

## Anti-patterns

| Anti-pattern | Why it's wrong | Instead |
|---|---|---|
| A PR with no "risk and rollback" | Nobody dares merge it when things break, and nobody knows how to back out | Write the worst case plus the rollback steps |
| A handoff document that copies the spec, or just says "keep working on X" | Content forks and goes stale, and the next session has to ask everything again | Paths only, down to file and function, plus the input list |
| Putting the handoff document in the repo | It gets committed and is the easiest thing to paste elsewhere | OS temp directory, never committed |
| Trusting automatic redaction without reading it | A redaction failure stays invisible until it's unrecoverable | Reread and search it yourself after writing |
| Waiting for context exhaustion to hand off | Handoff quality drops with the remaining context | Hand off on the first signal |
| Continuing round two in the original session | Expired assumptions decide for you, and the first round's trial and error comes along | Treat it as a new cycle: requirements → tickets → implementation |
| Installing pre-commit hooks in a directory full of loose files | It stages every change at once | Do it in a clean project directory |
