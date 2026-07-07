# Personal Access Token Scope Pitfall: Create vs Write

## Problem

A GitHub PAT with `public_repo` scope can **create** new repositories via the API
but **cannot**:
- Push to repos via `git push`
- Write files via the **Contents API** (`PUT /repos/:owner/:repo/contents/:path`)
- Manage existing repos (update, delete files)

This manifests as **HTTP 403 "Write access to repository not granted"** even though the
token successfully created the repo moments earlier.

## Root Cause

`public_repo` = read access to public repos + create new public repos.
`repo` = full control of repositories (read, write, push, admin).

These are different scope levels. A token with only `public_repo` is like
having a key that can build a house but not enter it.

## Fix

1. Go to **GitHub → Settings → Developer Settings → Personal Access Tokens**
2. Edit the token (or generate a new one)
3. Ensure **`repo` (Full control of repositories)** is checked
4. Regenerate if needed (old token is invalidated)

## Diagnostic Pattern

```
Can create repo via API?     YES  → token has public_repo scope
Can push to that repo?       NO   → token lacks repo scope
Contents API writes work?    NO   → token lacks repo scope
```