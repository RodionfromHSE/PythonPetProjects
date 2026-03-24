# StudyBot — Leitner System

A terminal-based spaced repetition tool using the Leitner box algorithm.

## Setup

```bash
# install dependencies
cd StudyBot && uv sync

# update db path in config.yaml
```

## Usage

```bash
# run directly
uv run python main.py

# or via launch script (can be symlinked to /usr/local/bin)
./launch_scripts/leitner.sh

# symlink example
ln -s "$(pwd)/launch_scripts/leitner.sh" /usr/local/bin/leitner
```

## Commands

| Command | Example | Description |
|---------|---------|-------------|
| `addPlus` | `addPlus: A + B + C` | Add items with yesterday's date appended |
| `add` | `add: A + B: 15.03` | Add items with explicit date (optional) |
| `getToday` | `getToday` | Show today's cards |
| `get` | `get: 15.03` | Show cards for a date |
| `getAll` | `getAll` | Unrepeated cards (last 31 days) |
| `makeShifts` | `makeShifts` | Shift today's cards to next level |
| `makeShiftsFrom` | `makeShiftsFrom: 01.03` | Shift from a specific date |
| `makeShiftsAll` | `makeShiftsAll` | Shift all unrepeated |
| `view` | `view` | View all levels |
| `remove` | `remove: name` | Remove card by name |
| `freeze` / `unfreeze` | `freeze` | Pause/resume scheduling |
| `close` | `close` | Exit |
