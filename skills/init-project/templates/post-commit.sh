#!/bin/bash
# ==============================================================================
# Universal Post-Commit Context Archival Hook
# Automatically archives .vault-notes.md and appends commit diffs to pending log.
# ==============================================================================

REPO_NAME=$(basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)")
PENDING_FILE="${VAULT_PENDING_FILE:-$HOME/.vault/.pending-commits.jsonl}"

# If .vault-notes.md exists and has content, archive it
if [ -f ".vault-notes.md" ] && [ -s ".vault-notes.md" ]; then
    ARCHIVE_DIR=".vault-notes-archive"
    mkdir -p "$ARCHIVE_DIR"
    TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
    mv ".vault-notes.md" "$ARCHIVE_DIR/notes_$TIMESTAMP.md"
    touch ".vault-notes.md"
fi

# Append commit metadata to pending sync log if configured
if [ -d "$(dirname "$PENDING_FILE")" ]; then
    LAST_COMMIT_HASH=$(git log -1 --format="%h" 2>/dev/null)
    LAST_COMMIT_MSG=$(git log -1 --format="%s" 2>/dev/null)
    DIFF_STAT=$(git diff HEAD~1 HEAD --stat 2>/dev/null | tail -n 1 | sed 's/^[ \t]*//')
    CHANGED_FILES=$(git diff-tree --no-commit-id --name-only -r HEAD 2>/dev/null | tr '\n' '|' | sed 's/|$//')

    if [ -n "$LAST_COMMIT_HASH" ]; then
        JSON_ENTRY=$(python3 -c "
import json, sys
data = {
    'repo': sys.argv[1],
    'commit': sys.argv[2],
    'message': sys.argv[3],
    'files': sys.argv[4],
    'diff_stat': sys.argv[5],
    'timestamp': '$(date -u +"%Y-%m-%dT%H:%M:%SZ")'
}
print(json.dumps(data))
" "$REPO_NAME" "$LAST_COMMIT_HASH" "$LAST_COMMIT_MSG" "$CHANGED_FILES" "$DIFF_STAT" 2>/dev/null)

        if [ -n "$JSON_ENTRY" ]; then
            echo "$JSON_ENTRY" >> "$PENDING_FILE"
        fi
    fi
fi

exit 0
