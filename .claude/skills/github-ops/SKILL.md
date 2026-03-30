---
name: github-ops
description: >
  GitHub operations for InvestipsHub repos: branches, PRs, issues, releases.
  Use when: creating PRs, closing/linking issues, pushing branches, managing
  labels, checking CI status. Triggers on: "create PR", "push branch",
  "close issue", "merge", "pull request", "github", "issues", "release".
---

# GitHub Operations

Handles all GitHub CLI (`gh`) operations for InvestipsHub repositories with
project-specific context baked in to avoid common pitfalls.

## Repository Map

| Project | GitHub Repo | Local Path | Notes |
|---------|-------------|------------|-------|
| Frontend (Next.js) | `InvestipsHub/signal-hub` | `signal-hub/` | Main app, deployed to Vercel |
| Backend (Azure Functions) | `InvestipsHub/InvestipsHubApi` | `azureApi/InvestipsHubApi/` | C# API, deployed to Azure |

## Critical: Remote URL

The repos were transferred from `cdcalderon/*` to `InvestipsHub/*`. GitHub redirects
pushes but **PR creation fails** with the old URL.

**Before any PR operation**, verify and fix the remote:

```bash
# Check current remote
git remote -v

# If it shows cdcalderon, fix it:
git remote set-url origin https://github.com/InvestipsHub/signal-hub.git
# or for backend:
git remote set-url origin https://github.com/InvestipsHub/InvestipsHubApi.git
```

Always use `--repo InvestipsHub/<repo-name>` with `gh` commands as a safety net.

## Branch Naming Convention

```
<type>/<issue-numbers>-<short-description>
```

**Examples:**
- `fix/34-35-37-42-gap-search-ticker-branding`
- `feat/55-rsi-divergence-signal`
- `fix/41-signal-detail-chart-not-loading`

When fixing multiple issues in one branch, include all issue numbers sorted ascending.

**Types:** `fix/`, `feat/`, `chore/`, `refactor/`, `docs/`

## Creating a Pull Request

### Pre-flight checklist
1. Verify remote URL points to `InvestipsHub` (not `cdcalderon`)
2. Ensure branch is pushed: `git push -u origin <branch>`
3. Verify TypeScript compiles: `npx tsc --noEmit`

### PR creation command

```bash
# Always specify --repo to avoid ambiguity
gh pr create \
  --repo InvestipsHub/signal-hub \
  --title "Fix: short description (#issue1 #issue2)" \
  --body "$(cat <<'EOF'
## Summary
- **#42**: What was fixed
- **#35**: What was fixed

## Test plan
- [x] Test item 1
- [x] Test item 2

Closes #42, closes #35

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### PR title format
- Keep under 70 characters
- Start with type: `Fix:`, `Feat:`, `Chore:`
- Include issue numbers: `(#34 #35 #37 #42)`
- Example: `Fix: branding, ticker display, search UX (#34 #35 #37 #42)`

### Linking issues
- Use `Closes #N` in the PR body (one per line or comma-separated)
- This auto-closes issues when the PR is merged
- **Do NOT manually close issues before the user confirms merge** — the issue stays
  open until the PR is merged and the user confirms it

## Closing Issues

**Important:** Only close issues after the user confirms the PR has been merged.
Do not close issues at PR creation time.

```bash
# Close with a comment linking to the PR (only after merge is confirmed)
gh issue close <number> --repo InvestipsHub/signal-hub --comment "Fixed in #<PR>"

# Batch close multiple issues
for n in 34 35 37 42; do
  gh issue close $n --repo InvestipsHub/signal-hub --comment "Fixed in #54"
done
```

## Viewing Issues

```bash
# List open issues
gh issue list --repo InvestipsHub/signal-hub

# View specific issue
gh issue view 42 --repo InvestipsHub/signal-hub

# List issues by label
gh issue list --repo InvestipsHub/signal-hub --label "bug"
```

## Checking CI / PR Status

```bash
# View PR checks
gh pr checks <PR-number> --repo InvestipsHub/signal-hub

# View PR status
gh pr view <PR-number> --repo InvestipsHub/signal-hub

# List open PRs
gh pr list --repo InvestipsHub/signal-hub
```

## Merging PRs

```bash
# Merge with squash (preferred for feature branches)
gh pr merge <PR-number> --repo InvestipsHub/signal-hub --squash --delete-branch

# Merge with merge commit (for release branches)
gh pr merge <PR-number> --repo InvestipsHub/signal-hub --merge
```

**Always confirm with the user before merging.**

## Commit Message Format

```
<type>: <short description>

<optional body explaining why>

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

**Types:** `fix`, `feat`, `chore`, `refactor`, `docs`, `test`

Use HEREDOC for multi-line messages:
```bash
git commit -m "$(cat <<'EOF'
fix: remove $ prefix from ticker display

Render-layer fix preserving data logic that depends on raw $ prefix.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| PR creation fails with "Head sha can't be blank" | Remote URL is wrong. Run `git remote set-url origin https://github.com/InvestipsHub/<repo>.git` |
| `gh` uses wrong repo | Always pass `--repo InvestipsHub/<repo>` |
| Push rejected | Branch may need rebase: `git pull --rebase origin main` |
| Issue not auto-closing on merge | Use exact syntax: `Closes #N` (capital C, space, hash, number) |
| Commit references wrong issue | Double check issue numbers before committing |

## Workflow: Fix Multiple Issues

1. **Create branch** with all issue numbers: `fix/<numbers>-<description>`
2. **Make changes** — commit logically grouped changes (one commit per issue or per logical change)
3. **Verify** — `npx tsc --noEmit` and browser test
4. **Fix remote** — ensure it points to `InvestipsHub`
5. **Push** — `git push -u origin <branch>`
6. **Create PR** — with `--repo InvestipsHub/<repo>`, list all issues in body with `Closes #N`
7. **Ask user to merge** — present PR URL, wait for confirmation
8. **Close issues** (after merge confirmed) — `gh issue close N --repo InvestipsHub/<repo> --comment "Fixed in #PR"`
9. **Clean up** — `git checkout main && git pull origin main && git branch -d <branch>`
