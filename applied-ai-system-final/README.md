# Game Glitch Investigator

## Base project

This project extends and repairs the **AI 110 Module 1 Game Glitch Investigator starter**. The starter is an intentionally faulty Streamlit number-guessing game. The final application keeps secret state in Streamlit session state, validates guesses, provides type-safe hints, applies scoring, supports difficulty levels, and allows the player to restart cleanly.

## Features

- Easy (1-20), Normal (1-100), and Hard (1-50) ranges
- Stable secret number during reruns
- Correct lower/higher/win hints
- Input parsing for empty and nonnumeric guesses
- Attempt limits and final win/loss state
- Score updates and reset behavior
- Developer debug panel for reproducible testing

## Setup and run

Requires Python 3.10+.

```bash
cd applied-ai-system-final
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
```

Open the local URL shown by Streamlit, normally `http://localhost:8501`.

## Logic-only demo

The demo runs without Streamlit:

```bash
python3 demo.py
```

## Example interactions

### Example 1: guess too low

Input:

```text
Secret: 50
Guess: 40
```

Output:

```text
Too Low - Go higher.
```

### Example 2: guess too high

Input:

```text
Secret: 50
Guess: 60
```

Output:

```text
Too High - Go lower.
```

### Example 3: winning guess

Input:

```text
Secret: 50
Guess: 50
```

Output:

```text
Win - Correct!
```

## Automated tests

Run:

```bash
cd applied-ai-system-final
python3 -m pytest -q
```

Reproducible command output is saved in [assets/test-output.txt](assets/test-output.txt).

## Reproducible interaction log

Additional command output is available in [assets/demo-output.txt](assets/demo-output.txt). The system architecture is defined in [diagrams/system-architecture.mmd](diagrams/system-architecture.mmd).

## Project structure

```text
applied-ai-system-final/
  app.py                 Streamlit interface and session-state flow
  logic_utils.py         Pure game logic
  demo.py                Streamlit-independent example runner
  tests/test_game_logic.py
  README.md
  model_card.md
  assets/
  diagrams/
```
