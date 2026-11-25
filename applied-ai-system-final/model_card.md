# Model Card: Game Glitch Investigator

## Intended use

This application is a small educational number-guessing game. It demonstrates input validation, state management, comparison logic, scoring, and test-driven debugging. An optional OpenAI model generates short commentary about valid guesses; deterministic code, not the model, decides game outcomes and scores. It is intended for course demonstrations and local practice, not for real-world prediction or high-stakes decision-making.

## Live AI component

The optional commentary client uses the OpenAI Responses API. Its model is configurable with `OPENAI_MODEL` and defaults to `gpt-6.2-astra`. It receives the player's guess, difficulty, attempt number, and already-determined outcome; the secret number is not included in the request. The API key is read from `OPENAI_API_KEY`, not stored in code. The app displays API errors and keeps deterministic game behavior available when commentary fails.

AI-generated commentary may be inaccurate or inappropriate despite instructions to follow the game result. It is presentation only and must not be used to determine hints, win/loss, or scoring. Enabling commentary transmits the listed game facts to OpenAI and may incur API charges. Do not enter personal or sensitive information as a guess.

## AI collaboration

AI assistance was used as a coding teammate during debugging. The starter reflection records Claude-assisted exploration, while the final implementation and documentation were reviewed by a human. AI suggestions identified likely root causes, but final correctness came from source review, the demo runner, and pytest.

### AI-suggested changes verified and accepted

- Keep the secret number in Streamlit `session_state` instead of recreating it on every rerun.
- Compare integer values consistently rather than alternating secret values between `int` and `str`.
- Route parsing and comparison through `logic_utils.py`.
- Generate a new secret after a difficulty change or New Game button.

### AI suggestions accepted with changes

The base app contained duplicated and misleading logic. I normalized it and added explicit range mappings through pure helper functions rather than relying on UI-only rules. I also reorganized tests so they assert complete `(outcome, message)` results instead of comparing a tuple to a string.

### AI suggestions not accepted

The original game fix did not need an external model, so I kept game evaluation deterministic. In response to the later request for live AI, I added an optional API for commentary only rather than letting an LLM decide the result. AI was not treated as an authority: generated fixes were tested locally. I also rejected the original workaround that converted the secret to a string on alternating turns because that intentionally created inconsistent types and hid the real bug.

## Bias and fairness reflections

The system has no demographic data and makes no decisions about people. Its main bias risks are representational and usability biases:

- Hints assume the player understands "higher" and "lower."
- Range and attempt settings give experienced players more or fewer challenges but do not unfairly target a protected group.
- English-only interface text may exclude users who do not read English.
- The debug panel reveals the secret and should be used only for development.

Future versions could add localization, adjustable text size, and accessible labels.

## Testing results

Testing uses `pytest` with pure functions for deterministic coverage:

- Winning guesses return `"Win"` and the success message.
- Too-high guesses return `"Too High"` and direct the player lower.
- Too-low guesses return `"Too Low"` and direct the player higher.
- Empty and nonnumeric input is rejected with useful errors.
- Easy, Normal, Hard, and unknown difficulty ranges are checked.
- Score updates add win points and bounded minimum win points.
- Negative guesses, whitespace, decimal input, `None`, and unknown difficulty names are covered.
- `Too High` and `Too Low` scoring and invalid-outcome score preservation are tested.
- AI helper tests verify configured/default model selection, secret omission from request input, missing API key, empty response, and provider-error reporting.

### Testing limitations

The current suite does not automate browser rendering or Streamlit rerun timing. It does not use randomized property tests or verify every possible secret number. OpenAI integration tests mock the client and do not verify live model quality, availability, or provider billing. These limits reduce confidence in UI and live-service behavior compared with confidence in pure game logic. Browser automation and an opt-in live smoke test can be added after Streamlit behavior is stable.

Run `python3 -m pytest -q` to reproduce. Exact output is in [assets/test-output.txt](assets/test-output.txt). The logic-only demo output is in [assets/demo-output.txt](assets/demo-output.txt). The latest suite passed 27 cases and covers mocked API success, missing-key and empty-response errors, plus provider-error reporting. This does not calculate AI confidence scores or verify live response quality.

## Reflection prompts

### 1. What was broken when you started?

The initial application had hints whose labels and directions were not consistent. The secret could be recreated during reruns, changing the target unpredictably. New Game did not fully reset the game, and difficulty changes could produce an invalid range or leave old state behind. Core logic was also embedded in the UI rather than isolated for testing.

### 2. How did AI help and how did you verify it?

AI was useful for proposing likely root causes and candidate refactors, especially session state and type mismatches. I did not trust those suggestions without evidence. I reviewed the resulting code, ran pure-logic demos, and ran focused pytest cases that cover win, high, low, invalid input, ranges, and score behavior.

### 3. Debugging and testing

I reproduced behavior by entering values around a known secret and running `demo.py` with 40, 60, and 50 against secret 50. I considered a bug fixed only after deterministic tests passed and after the Streamlit flow was refactored to retain state consistently. The original test file also needed correction because it expected a string while `check_guess` intentionally returns an outcome-and-message tuple.

### 4. What did you learn about Streamlit and state?

Streamlit reruns the script after interactions. Variables initialized locally can disappear or reset, so durable values belong in `st.session_state`. A New Game action must explicitly reset attempts, history, status, score, and secret. Difficulty changes also need to reset state so a new range does not accidentally use an old secret.

### 5. Looking ahead

Future work should retain small, pure functions near the UI, run tests after each behavioral change, and treat AI-generated code as a draft requiring human review. I would write regression tests before fixes, preserve a clear commit history, and add UI automation only after the logic suite is stable.
