import random

import streamlit as st

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


ATTEMPT_LIMITS = {"Easy": 6, "Normal": 8, "Hard": 5}


def start_new_game(difficulty):
    low, high = get_range_for_difficulty(difficulty)
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []


st.set_page_config(page_title="Game Glitch Investigator", page_icon="🎮")
st.title("🎮 Game Glitch Investigator")
st.caption("Find the secret number and repair the investigation.")

st.sidebar.header("Settings")
difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Normal", "Hard"], index=1)
attempt_limit = ATTEMPT_LIMITS[difficulty]
low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty
if st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    start_new_game(difficulty)

if "secret" not in st.session_state:
    start_new_game(difficulty)

st.info(
    f"Guess a whole number between {low} and {high}. "
    f"Attempts left: {max(0, attempt_limit - st.session_state.attempts)}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input("Enter your guess:", key="guess_input")

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess")
with col2:
    new_game = st.button("New Game")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    start_new_game(difficulty)
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    valid, guess, error = parse_guess(raw_guess)
    if not valid:
        st.session_state.history.append(raw_guess)
        st.error(error)
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess)
        outcome, message = check_guess(guess, st.session_state.secret)

        if show_hint:
            st.info(message)

        st.session_state.score = update_score(
            st.session_state.score,
            outcome,
            st.session_state.attempts,
        )

        if outcome == "Win":
            st.session_state.status = "won"
            st.balloons()
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            st.error(
                f"Out of attempts! The secret was {st.session_state.secret}. "
                f"Score: {st.session_state.score}"
            )
