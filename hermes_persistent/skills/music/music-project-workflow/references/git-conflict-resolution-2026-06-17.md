# Git Conflict Resolution: Global Project Index

## Context
The `musicom-agent/music-projects` repository uses a **global `index.html`** at the root to list all projects. Each project folder also contains its own `index.html` for project-specific details. This creates an `add/add` conflict when:
- A new project is added locally with its own `index.html`.
- The remote `index.html` is updated with entries for other projects.

## Conflict Type
`CONFLICT (add/add): Merge conflict in index.html`

## Resolution Steps

1. **Identify the conflict**:
   ```bash
   git status
   ```
   Output will show:
   ```
   Unmerged paths:
     (use "git add <file>..." to mark resolution)
     both added:      index.html
   ```

2. **Open the conflicted file**:
   ```bash
   cat index.html
   ```
   Look for conflict markers:
   ```
   <<<<<<< HEAD
   (local version)
   =======
   (remote version)
   >>>>>>> <commit-hash>
   ```

3. **Resolve the conflict**:
   - Use the **remote version** as the base (it contains the global project list).
   - Add the **new project entry** from the local version to the global list.
   - Ensure the new project's section is formatted consistently with existing entries.
   - Remove all conflict markers.

4. **Example Resolution**:
   ```html
   <!-- Before -->
   <<<<<<< HEAD
   <title>025-bollo-koos-indian-cross</title>
   ... (project-specific dashboard)
   =======
   <title>Musicom Projects</title>
   ... (global project list)
   >>>>>>> 606e4fd

   <!-- After -->
   <title>Musicom Projects</title>
   ... (global project list with new project entry added)
   ```

5. **Commit the resolution**:
   ```bash
   git add index.html
   git commit -m "Resolve index.html conflict: merge global index with 025-bollo-koos-indian-cross project"
   ```

6. **Push the changes**:
   ```bash
   git push origin master
   ```

## Pitfalls

- **Overwriting the global index**: Never replace the global `index.html` with a project-specific version. Always merge the new project entry into the global list.
- **Unrelated histories**: If `git pull` fails with `fatal: refusing to merge unrelated histories`, use:
  ```bash
  git pull origin master --allow-unrelated-histories
  ```
- **Rebase conflicts**: If using `git pull --rebase`, conflicts may require `git rebase --continue` or `git rebase --abort`.
- **Detached HEAD**: If you end up in a detached HEAD state, create a new branch, resolve conflicts, then merge back into `master`.

## Verification

After resolving the conflict:
- Open `index.html` in a browser to verify all projects are listed.
- Check that the new project's section is present and correctly formatted.
- Ensure no conflict markers remain in the file.