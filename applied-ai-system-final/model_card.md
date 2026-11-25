# Model Card: Game Glitch Investigator

## Intended use

This application is a small educational number-guessing game. It demonstrates input validation, state management, comparison logic, scoring, and test-driven debugging. An optional OpenAI model generates short commentary about valid guesses; deterministic code, not the model, decides game outcomes and scores. It is intended for course demonstrations and local practice, not for real-world prediction or high-stakes decision-making.

## Live AI component

The optional commentary client uses the OpenAI Responses API. Its model is configurable with `OPENAI_MODEL` and defaults to `gpt-6.2-astra`. It receives the player's guess, difficulty, attempt number, and already-determined outcome; the secret number is not included in the request. The API key is read from `OPENAI_API_KEY`, not stored in code. The app displays API errors and keeps deterministic game behavior available when commentary fails.

AI-generated commentary may be inaccurate or inappropriate despite instructions to follow the game result. It is presentation only and must not be used to determine hints, win/loss, or scoring. Enabling commentary transmits the listed game facts to OpenAI and may incur API charges. Do not enter personal or sensitive information as a guess.

## Limitations and biases

The game does not use demographic data or make decisions about people, so it has no direct demographic classification bias. It does have accessibility and representation limitations: the interface is English-only, hints assume players understand "higher" and "lower," and the fixed difficulty ranges and attempt limits will not suit every player. The developer debug panel reveals the secret and must not be enabled in a public player-facing deployment.

The OpenAI commentary can vary between runs and may be inaccurate, confusing, or inappropriate despite the prompt instructions. It is not authoritative: deterministic code alone decides the hint, win/loss state, and score. Only a small amount of game context is sent, and the secret is excluded, but requests still go to an external provider and can incur charges.

## Potential misuse and safeguards

The API could be misused by repeatedly triggering requests to consume the owner's API quota, or by exposing the game publicly without controlling who can use it. The model might also produce misleading commentary or text unsuitable for a player. The current safeguards are to make AI opt-in and disabled by default, call it only for valid guesses, cap the response at 60 output tokens, send no secret or free-form user prompt, and keep it out of the game decision path. Keep the API key private and use provider spending limits. Before public deployment, add authentication and request rate limits, and review or moderate generated text; the current local educational app does not provide those deployment controls.

## Reliability testing reflection

The latest automated run passed 27 tests, including deterministic game logic and mocked OpenAI success, missing-key, empty-response, and provider-error cases. One surprising result during the original testing was that the starter tests compared `check_guess` to a string even though the helper returns an `(outcome, message)` tuple; the test expectation itself needed correction. I also learned that a mocked API test proves the request/response handling, not the live model's quality. The live API and browser flow are not covered by automated tests, so I cannot claim the model commentary has been evaluated for accuracy or safety.

## AI collaboration reflection

AI was used as a debugging and implementation teammate; the starter reflection records Claude-assisted exploration, and later project changes used Copilot assistance. Suggestions were treated as hypotheses and checked against the code, tests, and reproducible demo.

### Suggestion accepted

I accepted the suggestion to keep the secret number in Streamlit `session_state` across reruns. This addresses the root state-reset bug instead of recreating the target on each click. I also followed the suggestion to parse guesses as integers and compare integer values consistently. I verified the related behavior through the deterministic game logic and tests.

### Suggestion rejected or revised

I rejected the workaround that converted the secret to a string on alternating attempts. It was harder to reason about and introduced inconsistent types instead of fixing the comparison path. I kept the guess and secret numeric, and made outcome evaluation remain deterministic. For the later request to add a live model, I limited AI to optional commentary rather than letting it control the result or score; this avoids allowing a variable model response to break game correctness.

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
