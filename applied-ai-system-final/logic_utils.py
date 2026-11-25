def get_range_for_difficulty(difficulty: str):
    """Return the inclusive number range for a difficulty name."""
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 100),
        "Hard": (1, 50),
    }
    return ranges.get(difficulty, (1, 100))


def parse_guess(raw: str):
    """Parse a text guess, returning (valid, integer, error)."""
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    try:
        return True, int(raw.strip()), None
    except (TypeError, ValueError):
        return False, None, "That is not a whole number."


def check_guess(guess, secret):
    """Compare a guess to a secret and return (outcome, hint)."""
    if guess == secret:
        return "Win", "Correct!"
    if guess > secret:
        return "Too High", "Go lower."
    return "Too Low", "Go higher."


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Return the updated score for a guess outcome."""
    if outcome == "Win":
        points = max(10, 100 - 10 * (attempt_number + 1))
        return current_score + points
    if outcome == "Too High" and attempt_number % 2 == 0:
        return current_score + 5
    if outcome in {"Too High", "Too Low"}:
        return current_score - 5
    return current_score
