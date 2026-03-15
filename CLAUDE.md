# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the game
python worder.py              # 5-letter word game (default)
python worder.py -l 6         # 6-letter word game
python worder.py -l 7         # 7-letter word game

# Lint
pylint worder.py
# or lint all Python files (as CI does):
pylint $(git ls-files '*.py')
```

CI runs pylint against Python 3.8, 3.9, and 3.10 on every push (`.github/workflows/pylint.yml`).

## Architecture

Single-file Python app (`worder.py`) — no external dependencies beyond the standard library.

**Classes:**
- `UiColors` — ANSI escape code constants for terminal styling
- `Tile` — A letter tile; holds a character and renders itself with color based on game state (correct / present / absent / unused)
- `WorderGame` — Orchestrates game flow: loads the secret word, accepts guesses, validates them, updates tile states, and prints the board and alphabet row

**Word dictionaries:** `word5`, `word6`, `word7` — plain-text files (one word per line) loaded at runtime relative to the working directory. `get_random_word()` picks the secret; `is_word_valid()` checks guesses against the same file.

**Game flow:** up to 6 guesses; each guess is validated against the dictionary, then tiles are colored green (correct position), yellow (wrong position), or dark (absent). Repeated-letter logic is handled by `blank_out_first_occurrence()`. The alphabet display below the board reflects cumulative state across guesses.
