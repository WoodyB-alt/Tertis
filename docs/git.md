# Git

## Common Git commands

### git clone

Use to initially clone a remote repository to your local machine. Automatically sets up
the `master` or `main` branch with matching upstream branches.

### git status

Shows the high level status of the content in your repositorie's local files.
Shows files that have changes as well as untracked and deleted content.

### git diff

Shows deatiled differences between 2 content objects or trees.
Without any further arguments, shows all unstaged differences in detail.

### git add

Add a local change to the set of staged changes.

### git commit

Commit all staged changes. Essentially snapshots the staged changes into your repositorie's
history. Allows you to attach a commit message to describe the changes.

### git rebase

Replay a set of commits on top of a specific base.

### git remote

Show all remotes known to this repository.

### git push

Upload the current history to a remote. Without any further arguments, uploads the
history of the checked out branch to the configured upstream branch.

### git pull

Download and merge history from a remote into the current barnch. Without any
further arguments, downloads and merges the latest history of the configured upstream branch.

### git merge

…

### git stash

Stash away changes in the current local tree. Useful when needing to change branches
but not wanting to actually commit uncommitted local changes.

## Cookbook

### Change my previous commit

To add code changes, use `git add ...` followed by `git commit --amend --no-edit`.
To reword the latest commit message, use `git commit --amend`.

### Integrate changes from source branch to facilitate merging

Use rebase to pull in all changes from the target branch before merging.

```
# Create a throwaway branch to do the rebasing.
# Useful to not screw up your feature branch when something goes haywire.

# Checkout the current feature branch
git checkout feature-branch

# Create and switch to the feature-branch for rebasing
git switch -c feature-branch-rebase

# Rebase the feature branch for rebasing on the target branch
git rebase target

# If everything was successful, (re)set the feature branch to the HEAD of the
# rebased branch and continue your work or push for pull request
git checkout feature-branch
git reset feature-branch-rebase

# If the rebase was unsuccessful, discard the feature-branch-rebase
git checkout feature branch
git branch -d feature-branch-rebase
```

### Stage only related changes in the same file

If you want to add changes you made to one file to multiple commits so that they are
logically grouped, use `git add --interactive` or `git add --patch` for an interactive
way to do so.
