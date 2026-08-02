# Git Secret Leak Remediation & History Purging

When GitGuardian or GitHub alerts you that a secret (SMTP password, API key, private key, token) has been committed to a repository, you must immediately take action to **purge the secret from git history** and **rotate the secret**.

## Step-by-Step Remediation Workflow

### 1. Identify the Leaked Secret and Commit
Find when and where the secret was introduced:
```bash
# Search commit messages or diffs for the secret (e.g. part of a password or API key)
git log -S "secret_substring" --oneline
```
Determine which files were committed and are currently being tracked.

### 2. Update .gitignore Immediately
Ensure the file containing the secret is explicitly ignored so it won't be accidentally re-added or tracked in future commits:
```bash
# Append the file to .gitignore
echo ".env.mail" >> .gitignore
echo "*.mail" >> .gitignore
echo ".gitconfig" >> .gitignore
```

### 3. Back Up Local Versions
If the local file is still needed for development (e.g., config file, `.env.mail`), back it up to a safe location outside the git repository (like `/tmp/`) before purging:
```bash
cp .env.mail /tmp/.env.mail.bak
```

### 4. Stash Any Uncommitted Local Changes
Git filter-branch/filter-repo requires a clean working directory:
```bash
git stash --include-untracked
```

### 5. Purge the Secret from Git History
Use `git filter-branch` (or `git-filter-repo` if installed) to remove the file from all commits across all branches. 
*Note: Set `FILTER_BRANCH_SQUELCH_WARNING=1` to bypass the deprecation warning delay.*

```bash
export FILTER_BRANCH_SQUELCH_WARNING=1

git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env.mail .gitconfig" \
  --prune-empty --tag-name-filter cat -- --all
```

### 6. Force-Push to Overwrite GitHub History
Once history is rewritten locally, force-push the updated branches and tags to overwrite the compromised history on GitHub:
```bash
git push origin --force --all
git push origin --force --tags
```

### 7. Restore the Backed-Up Local Files
Restore your configuration files back to the local repository folder. Since you updated `.gitignore`, they will now remain local and untracked:
```bash
cp /tmp/.env.mail.bak .env.mail
```

### 8. Pop Local Stash
Restore any other uncommitted modifications:
```bash
git stash pop
```

### 9. Rotate Compromised Credentials
**CRITICAL**: Rewriting git history removes the public evidence, but search engines, GitGuardian, or scraping bots may have already harvested the secret. **Always rotate the leaked credential immediately.**
- Change the email/IMAP/SMTP password.
- Revoke and recreate the leaked API token/key.
- Verify status with `git status --porcelain` to confirm the sensitive files are indeed untracked.
