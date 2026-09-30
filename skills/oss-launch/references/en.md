<!-- English companion to SKILL.md ｜ same decisions, shorter prose ｜ do not change the structure -->

# oss-launch

> Handbook step 8 (8.1–8.6 + appendix B) | Outputs: LICENSE + README + community files + CI + first release + CHANGELOG | Done when: the stranger-in-30-minutes test passes

## When to use / when not to

**Use** before the repo is meant to be used or read by others; before the first tag; when someone reports "I can't install it" or "I don't know which file to change"; when you're ready to take outside PRs. **Don't use** for a weekend tool only you use — no license or community files needed, but **secrets and data boundaries are never optional**; for a closed-source internal repo — take just 8.4 (CI and branch protection) and 8.5 (versions and changelog).

**The order can't be reversed**: pass the gates (legal and security) first, build the façade second — a beautiful façade on the wrong license gets torn down. The criterion is only one, but hard: **the stranger-in-30-minutes test** — in a clean directory, reading only the README, a stranger installs it, runs it once, and knows which file to change to take part. Fail that and "open source" just means the code is uploaded.

## Inputs

1. Code that runs, plus a path that gets it running from zero on someone else's machine (not "it works on mine"), and a dependency list (`package-lock.json` / `pyproject.toml` / `Cargo.lock` / `go.sum`).
2. The license decision — the one made at step 0, or make it in Action 1 — plus platform permissions (edit repo metadata, set branch protection, push tags, create releases) and permission to search the repo history for secrets, which is a class of action you do by hand.
3. The maintenance rhythm you intend to keep: how often you look at issues, how many things run at once.

## Actions

1. **Pass the legal and security gates first** (8.1)
   - **Pick a license** — answer one question: do you want the widest possible use, or do you want derivatives to stay open? **MIT**: widest use, including closed-source products, but no patent grant. **Apache-2.0**: equally permissive plus an explicit patent grant, and it requires noting which files you changed. **GPL-3.0**: derivatives stay open — viral, and corporate policy often bans it outright. **AGPL-3.0**: network use counts too, so it covers SaaS and is the most likely to be blocked by policy. Libraries lean permissive (MIT / Apache-2.0), where more users is better; self-hosted applications can be stricter. Once outside contributors exist, changing the license needs every contributor's consent (unless a CLA or DCO was agreed from the start) — which is why step 0 settles it.
   - **Land it in three places, all saying the same thing** (follow `templates/license-todo.txt`): the full LICENSE at the repo root; the `license` field in package metadata (`package.json` / `pyproject.toml` / `Cargo.toml`) using the standard SPDX id; a license line at the end of the README. The platform should show the license name, not "Unknown"; disagreeing places, or hedging like "MIT OR Apache", means nothing was decided.
   - **Dependency and third-party license compatibility**: sweep direct and transitive licenses (`npm ls --all` with license-checker; `pip-licenses` for Python) and look at GPL / AGPL and "unknown" separately — one GPL / AGPL dependency contaminates your whole license, so put this check in CI rather than in your memory. Don't bring in code, images or datasets you have no rights to; attribution and licensing rules for AI-generated content differ across jurisdictions — **do not outsource this judgment to an agent**, confirm it yourself and ask a person when needed.
   - **Secrets and privacy**: confirm no secret sits in the repo history. **Rotate the key and clean the history — don't just delete the file**; a pushed secret is leaked by default. No real credentials in example config (`templates/env.example`). Collect no user data; if you collect it, ship a privacy note and a deletion path.
2. **Build the façade** (8.2) — seven README sections, structure from `templates/readme.md`, don't change it: 1) one-line positioning (what it is, who it's for); 2) why use it (how it differs from comparable projects, tradeoffs spelled out, no "faster, stronger"); 3) 30-second start (install, run, see something — **three commands or fewer**); 4) usage examples (copy-pasteable and genuinely working); 5) limits and non-goals (written down; this turns away half the useless issues); 6) status and roadmap (production-ready or not, what the next version does, maintenance rhythm); 7) license and contribution entry points (LICENSE link, CONTRIBUTING link, issue link).
   - **Repo metadata** drives discovery and trust too: a one-line `description`, `topics` keywords, a homepage link, a `license` field matching the LICENSE file. **Wear only badges you actually maintain** — CI status, latest version, license; **a red CI badge hurts more than no badge.**
3. **Fill in the community files** (8.3) — each file answers one stranger's question, and **the first three must exist: LICENSE, README, SECURITY** (without a license, nobody dares use the repo). Then: `CONTRIBUTING.md` (how do I take part: environment setup, test commands, commit conventions, PR expectations; `templates/contributing.md`), `CODE_OF_CONDUCT.md` (how do we treat people here: Contributor Covenant plus contact; `templates/code-of-conduct.md`), `SECURITY.md` (who do I tell about a vulnerability: private channel + response window + supported scope; `templates/security.md`), issue templates (how do I report: bug = repro steps/version/environment, feature = scenario/alternatives; `templates/issue-bug.md`, `templates/issue-feature.md`), a PR template (what should a PR say: what changed / why / how verified / risk; `templates/pr.md`), `CODEOWNERS` (who must take a look: maintainers and the directories they own; `templates/CODEOWNERS`), and a label scheme (how do I find work: `good first issue` / `help wanted` / `bug` / `enhancement` — at least these four; `templates/triage-labels.md`). Full content requirements per file: `references/community-files.md`.
4. **Set up CI and quality gates** (8.4; skeletons `templates/ci.yml`, `templates/release.yml`, `templates/dependabot.yml`)
   - **Minimal pipeline**: install dependencies → lint → typecheck → test → build artifacts, with the matrix kept to **the two versions you truly support** — every extra one burns your time.
   - **Branch protection**: main requires CI to pass, at least one review, no force push, no direct pushes. **The rules live on the platform, not in a document.**
   - **Dependency and security scanning, and the release pipeline**: Dependabot for upgrades and vulnerability alerts, CodeQL or similar for code scanning, Scorecard for a one-off repo security checkup; a tag triggers build and publish, and artifacts carry a checksum or signature so downloaders can verify provenance. Criterion: **someone opens a PR, CI runs by itself, and a failure blocks the merge** — miss either half and you don't have CI. Details (CI skeleton, the four branch-protection rules, dependency upgrades, the retreat when there's no CI platform): `references/ci-and-release.md`.
5. **Decide versions and the changelog** (8.5; skeleton `templates/changelog.md`)
   - **Semantic versioning in three sentences**: major = breaking change, minor = backwards-compatible feature, patch = backwards-compatible fix. **Three questions for "is this breaking?"**: does anyone depend on the current behaviour, will old calls error, did the data format change? Any "yes" → major. **CHANGELOG in Keep a Changelog's six sections**: Added / Changed / Deprecated / Removed / Fixed / Security — it faces users and is not a transcription of commits, so **three commits for one feature are one line here**, and **every release has a tag, notes and its matching changelog section**; shipping 0.x and saying the interface will still change beats forcing 1.0 and breaking it later.
6. **Set the operating rhythm** (8.6)
   - **Triage issues through a state machine**: new issue → reproduce/confirm → priority → owner → close or turn into a ticket. Unmanaged issues tell newcomers the project is dead. (Label mapping: `templates/triage-labels.md`; local tracker: `templates/issue-tracker.md`; use an external `triage` skill if installed, otherwise walk the state machine by hand.)
   - **Response rhythm**: promise no SLA, but publish "roughly how often I look" in the README or CONTRIBUTING. **Dependency cadence**: a minor upgrade monthly, security alerts immediately, and every upgrade passes CI — an upgrade whose log nobody read didn't happen. **Deprecation and archiving**: announce deprecation with a time window; when archiving, put the status and a replacement at the top of the README. **Time budget**: a solo project needs a cap on how many things run at once — a sustainability question, not a technical one; more projects die because the maintainer vanished than because the code was bad.
7. **Run the stranger-in-30-minutes test** (the skill's only criterion) — three conditions, none negotiable: **a clean directory** (no leftovers from your dev environment), **README only** (no reading code, no asking the author), **working within three commands** (install, run, see something). Read in this order; every step must land on a real file, and leave a trace — write down which minute you got stuck and why, fix it, walk it again. **Don't play the stranger yourself**: if you already know the answers, find someone who hasn't seen the repo, or switch machine and directory.

   | Minutes | Looking for | Lands in | Stuck here means |
   |---|---|---|---|
   | 0–3 | What is this, who is it for, worth reading on | README first paragraph + "why use it" | README lacks the one-line positioning, or buried it in adjectives |
   | 3–6 | Install it and run it once | README "30-second start" | The quickstart isn't real, or exceeds three commands |
   | 6–10 | Do I understand the vocabulary here | `CONTEXT.md` (glossary template `templates/CONTEXT.md`) | No `CONTEXT.md`, or an empty glossary |
   | 10–14 | What does the structure look like, which file do I change | `docs/architecture.md` (seam list) | No architecture doc or seam list (step 4, before `ticket-plan`) |
   | 14–18 | Why was it decided this way | `docs/decisions.md` + `docs/adr/` | No ledger or ADRs (go back to `decision-ledger`) |
   | 18–22 | What happens next, which ticket can start | ticket frontier (`.scratch/<feature>/issues/`) | No startable ticket, or no `good first issue` |
   | 22–26 | How do I take part, who gets a vulnerability report | `CONTRIBUTING.md` + `SECURITY.md` | CONTRIBUTING / SECURITY missing |
   | 26–30 | Open a PR and watch CI run by itself | the platform's PR page + branch protection | No CI or branch protection (rules not configured on the platform) |

## Outputs

- `LICENSE` full text + the package metadata `license` field + a README license section (all three consistent); `README.md` in seven sections + repo metadata (description / topics / homepage / license).
- Community files (`CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, issue templates, PR template, `CODEOWNERS`, label scheme); CI config + branch protection rules on the platform + release pipeline + dependency alerts; `CHANGELOG.md` and a first release with a tag and notes; a stranger-in-30-minutes test record (where you got stuck, what you changed, the result of the second run).

## Done criteria

- [ ] The stranger-in-30-minutes test passes: in a clean directory, README only, it installs and runs once, and I know which file to change to take part.
- [ ] LICENSE, README and SECURITY all exist; LICENSE / package metadata / README agree exactly on the license (the platform shows something other than "Unknown").
- [ ] The dependency license list has no unhandled GPL / AGPL / unknown-license dependency, and that check has a line in CI.
- [ ] No secret is findable in the repo history; example config holds placeholders only (`templates/env.example`); if a secret was ever pushed, it's rotated and the history is cleaned.
- [ ] I ran the three "30-second start" commands by hand in a clean directory and wrote down what I saw.
- [ ] Only badges I maintain are worn (CI / version / license), and the CI badge is green.
- [ ] Branch protection is on for main: CI passes + at least one review + no force push.
- [ ] Verified with a test PR: CI runs by itself and a failure blocks the merge.
- [ ] The first release has a tag, notes and its matching CHANGELOG section; the six-section CHANGELOG structure is in place.
- [ ] CONTRIBUTING states the response rhythm ("roughly how often I look") and the commands to run locally.
- [ ] I used the stranger's viewpoint once (different directory / machine / person) and kept a record of where I got stuck.

## Manual fallback

- **No CI platform**: at minimum write the local commands into `CONTRIBUTING.md` and **say there is no automated check** — honesty beats pretending, and claiming a quality gate you don't have damages trust more than admitting there isn't one. **Can't configure branch protection** (personal account / self-hosted platform): make "CI must pass and someone must review before merging" an explicit rule in CONTRIBUTING and say it relies on discipline rather than a machine; the criterion degrades, so say so.
- **Community files can wait; LICENSE, README and SECURITY cannot.** Code of Conduct can be Contributor Covenant with your contact filled in. **No platform account** (purely local repo): write the seven README sections, add a LICENSE and a SECURITY (an email is enough) so the repo is ready to push, then upload and fill in metadata later.
- **Don't know which license to pick**: go back to the question — widest use, or derivatives stay open? If you can't answer, put the contents of `templates/license-todo.txt` in as a placeholder and **don't make the repo public before deciding** (no license means all rights reserved, and nobody dares use it). **License names you don't recognize**: look each one up in its official text and treat anything unfamiliar as "unknown license", not as fine. **The repo doesn't even run yet** (a stranger is guaranteed to stall at 3–6 minutes): go back to steps 5/6 and make the code real, then return to the façade — a README cannot hide code that doesn't run.

## Next step

→ call `project-brief` to start the next idea at step 0; if step 8 exposed a problem in the flow itself (a step that keeps reworking), → call `flow-tuning`.

## Anti-patterns

| Anti-pattern | Why it's wrong | Instead |
|---|---|---|
| Building the README façade first, letting the three license places disagree (or "MIT OR Apache"), or filling it with "faster, stronger" | A wrong license wastes the façade work, the platform shows Unknown, and a slogan gives a stranger nothing to judge | Pass the gates first, keep LICENSE + metadata + README consistent, and state how you differ from comparable projects |
| A red CI badge, or branch protection that exists only in a document | A red badge reads as "nobody maintains this", and documents don't stop anyone | Only wear badges you maintain; configure the rules on the platform and verify with a failing PR |
| Transcribing commits into the CHANGELOG, or forcing 1.0 and breaking it later | Users can't tell whether to upgrade, and breaking changes arrive unannounced | One feature = one line; ship 0.x and say the interface will change |
| Collecting user data with no privacy note or deletion path, or letting an agent confirm third-party / AI-generated attribution | Both are legal exposures: unrecoverable when they go wrong, and an agent's confidence isn't correlated with correctness | Collect nothing or document the notice and deletion route; confirm attribution yourself and ask a person when needed |
| Taking on a pile of issues / PRs at once | More projects die because the maintainer vanished than because the code was bad | Cap how many run at once and publish the response rhythm |
