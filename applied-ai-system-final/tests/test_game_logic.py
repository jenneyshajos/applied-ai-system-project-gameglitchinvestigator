import pytest

from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score


@pytest.mark.parametrize(
    ("guess", "secret", "expected"),
    [
        (50, 50, ("Win", "Correct!")),
        (60, 50, ("Too High", "Go lower.")),
        (40, 50, ("Too Low", "Go higher.")),
        (-1, 1, ("Too Low", "Go higher.")),
    ],
)
def test_check_guess_outcome_and_hint(guess, secret, expected):
    assert check_guess(guess, secret) == expected


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("42", (True, 42, None)),
        (" 42 ", (True, 42, None)),
        ("0", (True, 0, None)),
        ("", (False, None, "Enter a guess.")),
        ("   ", (False, None, "Enter a guess.")),
        (None, (False, None, "Enter a guess.")),
        ("hello", (False, None, "That is not a whole number.")),
        ("4.5", (False, None, "That is not a whole number.")),
    ],
)
def test_parse_guess(raw, expected):
    assert parse_guess(raw) == expected


@pytest.mark.parametrize(
    ("difficulty", "expected"),
    [
        ("Easy", (1, 20)),
        ("Normal", (1, 100)),
        ("Hard", (1, 50)),
        ("Unknown", (1, 100)),
    ],
)
def test_difficulty_ranges(difficulty, expected):
    assert get_range_for_difficulty(difficulty) == expected


@pytest.mark.parametrize(
    ("starting_score", "outcome", "attempt", "expected"),
    [
        (20, "Win", 1, 100),
        (20, "Win", 20, 30),
        (25, "Too High", 2, 30),
        (25, "Too High", 1, 20),
        (25, "Too Low", 4, 20),
        (25, "Invalid", 1, 25),
    ],
)
def test_update_score(starting_score, outcome, attempt, expected):
    assert update_score(starting_score, outcome, attempt) == expected
