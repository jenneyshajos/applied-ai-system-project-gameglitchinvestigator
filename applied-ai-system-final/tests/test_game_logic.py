from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score


def test_winning_guess():
    assert check_guess(50, 50) == ("Win", "Correct!")


def test_guess_too_high():
    assert check_guess(60, 50) == ("Too High", "Go lower.")


def test_guess_too_low():
    assert check_guess(40, 50) == ("Too Low", "Go higher.")


def test_parse_guess_accepts_integer():
    assert parse_guess("42") == (True, 42, None)


def test_parse_guess_rejects_empty_and_nonnumeric():
    assert parse_guess("") == (False, None, "Enter a guess.")
    assert parse_guess("hello") == (False, None, "That is not a whole number.")


def test_difficulty_ranges():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Hard") == (1, 50)
    assert get_range_for_difficulty("Unknown") == (1, 100)


def test_win_score_is_bounded_and_added():
    assert update_score(20, "Win", 1) == 100
    assert update_score(20, "Win", 20) == 30
