#!/bin/bash

# resolve symlinks so this works from /usr/local/bin too
SOURCE="$0"
while [ -L "$SOURCE" ]; do
    DIR="$(cd "$(dirname "$SOURCE")" && pwd)"
    SOURCE="$(readlink "$SOURCE")"
    [[ "$SOURCE" != /* ]] && SOURCE="$DIR/$SOURCE"
done
STUDY_BOT_DIR="$(cd "$(dirname "$SOURCE")/.." && pwd)"

echo "Starting Leitner System..."
cd "$STUDY_BOT_DIR" && uv run python main.py
echo "Leitner System Finished."
