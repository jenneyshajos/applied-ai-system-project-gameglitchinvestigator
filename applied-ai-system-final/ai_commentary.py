import os

from openai import OpenAI, OpenAIError


DEFAULT_MODEL = "gpt-6.2-astra"


class CommentaryGenerationError(Exception):
    """Raised when AI commentary cannot be generated."""


def generate_commentary(guess: int, outcome: str, attempt_number: int, difficulty: str):
    """Generate short commentary without delegating game logic to the model."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise CommentaryGenerationError(
            "Set OPENAI_API_KEY in your environment to enable AI commentary."
        )

    model = os.getenv("OPENAI_MODEL") or DEFAULT_MODEL
    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=model,
            instructions=(
                "You are a playful commentator for a number guessing game. "
                "Write one short sentence reacting to the supplied game facts. "
                "The outcome is authoritative: do not contradict it, invent a "
                "different hint, or reveal or guess the secret number."
            ),
            input=(
                f"Difficulty: {difficulty}. Guess: {guess}. "
                f"Authoritative outcome: {outcome}. Attempt: {attempt_number}."
            ),
            max_output_tokens=60,
        )
    except OpenAIError as error:
        raise CommentaryGenerationError(
            f"OpenAI request failed ({type(error).__name__}): {error}"
        ) from error

    commentary = response.output_text.strip()
    if not commentary:
        raise CommentaryGenerationError("OpenAI returned empty commentary.")
    return commentary
