#!/usr/bin/env bash
set -euo pipefail

# Push the current integrated crawler worktree to the remote wyy branch.
# This script intentionally does not install dependencies or run pytest.

REMOTE="${REMOTE:-origin}"
TARGET_BRANCH="${TARGET_BRANCH:-wyy}"
COMMIT_MESSAGE="${COMMIT_MESSAGE:-feat(crawler): integrate XBY production base with wyy Harbor handoff}"
HISTORY_MESSAGE="${HISTORY_MESSAGE:-merge: preserve wyy history after Harbor integration}"
DRY_RUN="${DRY_RUN:-0}"
STAGE_ALL="${STAGE_ALL:-0}"

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

if ! git remote get-url "$REMOTE" >/dev/null 2>&1; then
  echo "remote not found: $REMOTE" >&2
  exit 2
fi

if [ -n "$(git ls-files -u)" ]; then
  echo "merge conflicts are present; resolve them before pushing" >&2
  git status --short
  exit 2
fi

echo "Fetching $REMOTE/$TARGET_BRANCH..."
git fetch "$REMOTE" "refs/heads/$TARGET_BRANCH"
remote_commit="$(git rev-parse FETCH_HEAD)"

echo "Staging integration files..."
if [ "$STAGE_ALL" = "1" ]; then
  git add -A
else
  stage_paths=(
    "docs/wyy-xby-harbor-sample-integration-plan.md"
    "scripts/push_merged_to_wyy.sh"
    "src/alvance_github_crawler"
    "tests"
  )
  for path in "${stage_paths[@]}"; do
    if [ -e "$path" ]; then
      git add "$path"
    fi
  done
fi

if ! git diff --cached --quiet; then
  echo "Creating integration commit..."
  git commit -m "$COMMIT_MESSAGE"
else
  echo "No staged changes; using existing HEAD."
fi

if ! git diff --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
  echo "unstaged or untracked files remain after staging; refusing to push partial state" >&2
  git status --short
  echo "Set STAGE_ALL=1 to include every non-ignored change." >&2
  exit 2
fi

if git merge-base --is-ancestor "$remote_commit" HEAD; then
  echo "$REMOTE/$TARGET_BRANCH is already in HEAD history."
else
  echo "Recording $REMOTE/$TARGET_BRANCH as merged while keeping the integrated tree..."
  git merge --no-ff -s ours "$remote_commit" -m "$HISTORY_MESSAGE"
fi

if [ "$DRY_RUN" = "1" ]; then
  echo "Dry run: git push --dry-run $REMOTE HEAD:refs/heads/$TARGET_BRANCH"
  git push --dry-run "$REMOTE" "HEAD:refs/heads/$TARGET_BRANCH"
else
  echo "Pushing HEAD to $REMOTE/$TARGET_BRANCH..."
  git push "$REMOTE" "HEAD:refs/heads/$TARGET_BRANCH"
fi

echo "Done."
