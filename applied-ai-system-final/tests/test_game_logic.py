import pytest

from ai_commentary import (
    CommentaryGenerationError,
    DEFAULT_MODEL,
    generate_commentary,
)
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


def test_generate_commentary_uses_configured_openai_model(monkeypatch):
    import ai_commentary

    captured = {}

    class FakeResponses:
        def create(self, **kwargs):
            captured.update(kwargs)
            return type("Response", (), {"output_text": "  Nice guess!  "})()

    class FakeClient:
        def __init__(self, api_key):
            captured["api_key"] = api_key
            self.responses = FakeResponses()

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "test-model")
    monkeypatch.setattr(ai_commentary, "OpenAI", FakeClient)

    result = generate_commentary(40, "Too Low", 1, "Normal")

    assert result == "Nice guess!"
    assert captured["api_key"] == "test-key"
    assert captured["model"] == "test-model"
    assert "Authoritative outcome: Too Low" in captured["input"]
    assert "secret" not in captured["input"].lower()


def test_generate_commentary_requires_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(CommentaryGenerationError, match="OPENAI_API_KEY"):
        generate_commentary(40, "Too Low", 1, "Normal")


def test_generate_commentary_uses_default_model(monkeypatch):
    import ai_commentary

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    captured = {}

    class FakeResponses:
        def create(self, **kwargs):
            captured.update(kwargs)
            return type("Response", (), {"output_text": "Good try!"})()

    class FakeClient:
        def __init__(self, api_key):
            self.responses = FakeResponses()

    monkeypatch.setattr(ai_commentary, "OpenAI", FakeClient)

    assert generate_commentary(60, "Too High", 2, "Normal") == "Good try!"
    assert captured["model"] == DEFAULT_MODEL


def test_generate_commentary_rejects_empty_response(monkeypatch):
    import ai_commentary

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    class FakeResponses:
        def create(self, **kwargs):
            return type("Response", (), {"output_text": "  "})()

    class FakeClient:
        def __init__(self, api_key):
            self.responses = FakeResponses()

    monkeypatch.setattr(ai_commentary, "OpenAI", FakeClient)

    with pytest.raises(CommentaryGenerationError, match="empty commentary"):
        generate_commentary(60, "Too High", 2, "Normal")


def test_generate_commentary_reports_openai_errors(monkeypatch):
    import ai_commentary
    from openai import OpenAIError

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    class FakeResponses:
        def create(self, **kwargs):
            raise OpenAIError("simulated provider failure")

    class FakeClient:
        def __init__(self, api_key):
            self.responses = FakeResponses()

    monkeypatch.setattr(ai_commentary, "OpenAI", FakeClient)

    with pytest.raises(CommentaryGenerationError, match="simulated provider failure"):
        generate_commentary(60, "Too High", 2, "Normal")
