<!-- English companion to SKILL.md ｜ same decisions, shorter prose ｜ do not change the structure -->

# repo-bootstrap

> Handbook step 1 (ch. 4) | Outputs: `.git/`, `.gitignore`, first commit, three destination directories | Done when: `git log` has at least one commit, `git status --porcelain` is empty, `.gitignore` covers the four boundaries, no secrets in history

## When to use / when not to

- Use: you have something to build but the directory is not a git repo yet; you downloaded a code directory with no `.git`; before letting an agent write any code. This step can't be skipped — not one line of the skill set runs `git init`, every skill assumes a git repo already exists, and step 6's dual-axis review takes "the diff since a fixed reference point" where the reference point is one of four (commit, branch, tag, merge-base), **all four git concepts**. No repo, no input.
- Don't use: it is already a git repo (go to `repo-setup`); you want to connect the repo to GitHub (a different job, see Actions 7); you already `git add .`-ed a pile of junk (handle history per Actions 4 first).

## Inputs

1. A directory ready to start in (may be empty), and the output of `git --version`.
2. `git config user.name` and `user.email` — if empty, the first commit is rejected.
3. Project type (decides which lines go into `.gitignore`).
4. Inventory of secret files already in the directory: `.env`, `*.pem`, `*.key`, credential files.

## Actions

1. **Four things, one code block**:

   ```
   git init
   git config user.name "your name" && git config user.email "your email"   # both non-empty, or the first commit is rejected
   git add .gitignore && git commit -m "chore: initialize repository"
   ```

   The order is deliberate: **write `.gitignore` first, then `git add`**. The first commit contains only `.gitignore` — the very first act is laying down the rules.
2. **Draw the four `.gitignore` boundaries** — this matters far more than `git init`. A `git add .` on day one swallows `node_modules`, build output, editor cache, and `.env` into history, and cleaning that up later is painful. Copy `templates/gitignore.txt`:

   | Boundary | What to write |
   |---|---|
   | dependency dirs | `node_modules/`, `.venv/`, `venv/`, `__pycache__/`, `*.pyc` |
   | build output | `dist/`, `build/`, `out/`, `*.egg-info/`, `coverage/`, `.coverage`, tool cache dirs |
   | local config | `.DS_Store`, `Thumbs.db`, `.idea/`, `.vscode/`, `*.local` |
   | secret files | `.env`, `.env.*` (keep a sample with `!.env.example`), `*.pem`, `*.key`, `credentials.json`, `secrets.*` |

3. **Scan `git status` before committing**: any `.env`, `*.pem`, or credential file in there? Then stop and do the next step first.
4. **Secret incident: what if it already entered history.** Deleting the file is not enough:
   - **rotate the secret first** (assume it leaked), then decide whether to rewrite history;
   - treat a leak on a public repo as **leaked**, not deleted — the moment it is pushed it cannot be recalled;
   - rewriting history and force pushing are irreversible, **do them yourself**, never hand them to an agent.
5. **Set up the three destination directories** while you're here — every later step needs somewhere to put outputs, and creating dirs now is cheaper than adding rules later: `docs/agents/` for process and agent config (`issue-tracker.md`, `domain.md`, `brief.md`); `docs/adr/` for ADRs (starting at step 2); `.scratch/<feature>/` for spec and tickets in local mode (steps 3 and 4 land here). git does not track empty directories: drop a `.gitkeep` or a placeholder README so they don't vanish silently on the next commit.
6. **First commit**: the message states **why**, not what changed — the diff is more accurate about what.
7. **Local init only; connecting GitHub is optional.** `git init` and connecting GitHub are two jobs: the remote only decides whether `repo-setup` picks `gh issue` or local markdown for the tracker. A local repo plus a few commits is enough for step 6's dual-axis review to compare against. If you really want it: `git remote add origin <url>` — your call, not this step's criterion.
8. **Email**: commits from a QQ email won't link to your GitHub account unless you add that email to the account's emails list. If you just want to push code, a noreply address like `username@users.noreply.github.com` is easier and leaks one less real address.

## Outputs

- A working local repo: `.git/`, `.gitignore`, first commit.
- Three destination directories: `docs/agents/`, `docs/adr/`, `.scratch/<feature>/`.
- The four-boundary list (copied from `templates/gitignore.txt` and adapted to the project).

## Done criteria

- [ ] `git log --oneline` prints at least one commit.
- [ ] `git status --porcelain` prints nothing (no untracked junk).
- [ ] `.gitignore` covers the four boundaries and you can name at least one line for each (dependencies / build output / local config / secrets).
- [ ] `git log --all --oneline -- .env "*.pem" "*.key" credentials.json` prints nothing — no secrets in history.
- [ ] `git config user.name` and `git config user.email` are both non-empty.
- [ ] All three destination directories exist and are not in an "empty directory" state (they hold a `.gitkeep` or placeholder file).
- [ ] The first commit message answers "why", not "what changed".
- [ ] If pushing to GitHub: `user.email` is a noreply address, or you confirmed the address is in the account's emails list.
- [ ] This step performed no irreversible action (history rewrite, force push); if any happened, you did it by hand.

## Manual fallback

- No git: **install git, there is no alternative** — step 6's review and step 8's release both need it. Also true in spirit: **no skill does this step for you anyway**; run Actions 1's code block, which depends on no skill set or tool. This is not a fallback, it is the main path.
- `git commit` rejected (`Please tell me who you are`): `user.name` / `user.email` are empty — configure in place and retry.
- `node_modules` or build output already committed: while nothing is pushed yet, `git rm -r --cached <path>`, add `.gitignore`, commit again. If a **secret** ever appeared in history, follow Actions 4.
- You just want to write code and skip the repo: fine, but step 6's dual-axis review loses its reference point, and adding the repo later means drawing the boundaries again — more expensive.
- The directory contains someone else's code or third-party assets: confirm you have the right to bring it in before `git add`.

## Next step

→ call `repo-setup` (fix tracker, triage labels, and domain doc layout so step 2's outputs have somewhere to land).

## Anti-patterns

| Anti-pattern | Why it's wrong | Instead |
|---|---|---|
| `git add .` on day one | swallows `node_modules`, build output, `.env` into history on day one | write `.gitignore` first, then add by category |
| Deleting the file after a secret entered history | the file is gone but the secret still works out there, and it's still in history | rotate the secret first, then decide about rewriting history |
| Treating "connect GitHub" as this step's criterion | the remote only affects the tracker mode; a local repo is enough | local init + a few commits; wiring a remote is separate |
| Committing empty directories | git doesn't track empty dirs, so the destination disappears on the next commit | add a `.gitkeep` or placeholder README |
| Letting an agent rewrite history or force push | irreversible, affects others, and agent confidence is unrelated to correctness | do these yourself |
| Writing "update" as the commit message | in six months nobody can read intent from the log | write why; leave what changed to the diff |
