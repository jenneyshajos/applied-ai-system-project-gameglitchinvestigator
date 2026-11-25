# Game Glitch Investigator

## Project title and summary

**Game Glitch Investigator** is a Streamlit number-guessing game that repairs and demonstrates common bugs in a small interactive application. A player chooses a difficulty, guesses the secret number, receives higher/lower feedback, and can track a score across limited attempts. Optional OpenAI-generated commentary adds a conversational response to each valid guess, while deterministic code remains responsible for the actual result and score.

## Original project (Modules 1-3)

The original project is the **AI 110 Modules 1-3 Game Glitch Investigator**, based on the Module 1 Game Glitch Investigator starter. Its original goal was to have students investigate an intentionally broken Streamlit number-guessing game, identify its logic and state bugs, and repair the game. The starter provided a difficulty selector, secret number, hints, attempts, score, and a developer debug panel, with logic intended to be refactored and tested.

## Architecture overview

The [system diagram](diagrams/system-architecture.mmd) shows player input flowing through the Streamlit interface to pure game-logic helpers, which determine the range, validate the guess, evaluate the result, and update the score. When enabled, a separate commentary component sends only the guess, difficulty, attempt number, and authoritative outcome to the OpenAI API; the secret number is not sent, and the model cannot change the game result. Pytest uses a mocked provider for repeatable integration checks, while the example runner and saved outputs provide additional evidence.

## Features and design decisions

- **Difficulty ranges:** Easy is 1-20, Normal is 1-100, and Hard is 1-50; each difficulty also has an attempt limit.
- **Session state:** Streamlit session state retains the secret and game progress across reruns. This avoids changing the secret during a game.
- **Pure game logic:** Parsing, comparisons, ranges, and scoring are separated into `logic_utils.py`, making them testable without launching the interface.
- **Input behavior:** Guesses must be whole numbers. Empty or invalid text gets a clear error instead of being counted as a numeric guess.
- **Developer debug panel:** The panel exposes the secret and game state to make local testing easier. It is for development and should not be treated as a player-facing feature.
- **Optional AI commentary:** Enable it in the sidebar to request a short OpenAI-generated reaction after a valid guess. The response is supplemental; the deterministic game result remains authoritative. It is disabled by default to avoid unexpected API calls and costs.

The main trade-off is that the project prioritizes readable, deterministic game logic and course-level testability over a production deployment. AI commentary requires internet access and an OpenAI API key, can vary or be inaccurate, and may incur API charges. The debug panel intentionally reveals the answer, and automated tests do not automate browser interactions.

## Setup instructions

Requires Python 3.10 or later.

1. Open a terminal in the repository and move into the application directory:

   ```bash
   cd applied-ai-system-final
   ```

2. Install the project dependencies:

   ```bash
   python3 -m pip install -r requirements.txt
   ```

3. (Optional) Configure OpenAI if you want to enable AI commentary:

   ```bash
   export OPENAI_API_KEY="your-api-key"
   ```

   The default model is `gpt-6.2-astra`. To use another model available to your API account, set `OPENAI_MODEL` before starting the app:

   ```bash
   export OPENAI_MODEL="your-model-name"
   ```

   Keep the key private; do not commit it to the repository. No key is required to play the game without AI commentary.

4. Start the Streamlit application:

   ```bash
   python3 -m streamlit run app.py
   ```

5. Open the local URL printed by Streamlit, usually `http://localhost:8501`. In the sidebar, enable **AI commentary** to use the configured OpenAI model.

To run the fixed-input, logic-only demo instead of the interface:

```bash
python3 demo.py
```

## Sample interactions

The game logic is deterministic for each example below; the examples use a secret of 50. When AI commentary is enabled, the application also displays one variable, model-generated sentence. That text is not part of the authoritative game result.
The checked-in output examples below show the deterministic game result. AI wording varies per request, and the automated suite mocks the API rather than recording a live response.

### Input: guess below the secret

```text
Secret: 50
Guess: 40
```

```text
Guess 40, secret 50: Too Low - Go higher.
```

### Input: guess above the secret

```text
Secret: 50
Guess: 60
```

```text
Guess 60, secret 50: Too High - Go lower.
```

### Input: correct guess

```text
Secret: 50
Guess: 50
```

```text
Guess 50, secret 50: Win - Correct!
```

## Testing summary

Run the test suite from `applied-ai-system-final/`:

```bash
python3 -m pytest -q
```

Latest run: **27 test cases passed, 0 failed**. Tests cover correct/high/low guesses, whole-number parsing (including blank, whitespace, `None`, nonnumeric, and decimal input), difficulty ranges, score updates, and the AI integration's key handling, model selection, empty-response, and provider-error behavior. The OpenAI client is mocked in tests, so the suite is repeatable and makes no live or billable API calls. The fixed-input demo produces the three expected game outcomes shown above. Re-run the command to reproduce; exact outputs are saved in [assets/test-output.txt](assets/test-output.txt) and [assets/demo-output.txt](assets/demo-output.txt).

What worked: isolating game logic made it possible to assert expected behavior on edge cases quickly and reliably, and mocking OpenAI lets tests verify integration behavior without credentials. What is not covered: the suite does not automate browser rendering, Streamlit button interactions, or live API behavior end to end. AI confidence scores are not requested or treated as reliability evidence; the model only generates supplemental commentary, and its text may still be inaccurate.

## Reflection

This project reinforced that debugging is a process of forming a concrete expectation, reproducing a mismatch, changing the smallest relevant part, and checking the result with tests. It also showed how separating interface code from game rules makes problems easier to reason about. Responsible-AI collaboration, suggestion review, bias, and system limitations are documented in [model_card.md](model_card.md).

## Project structure

```text
applied-ai-system-final/
  app.py                 Streamlit interface and session-state flow
  ai_commentary.py       Optional OpenAI commentary integration
  logic_utils.py         Pure game logic
  demo.py                Streamlit-independent example runner
  tests/test_game_logic.py
  README.md
  model_card.md          Responsible-AI reflections
  assets/                Reproducible command output
  diagrams/              Mermaid system diagram
```
