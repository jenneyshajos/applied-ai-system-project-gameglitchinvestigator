from logic_utils import check_guess, parse_guess


examples = [
    ("40", 50),
    ("60", 50),
    ("50", 50),
]

if __name__ == "__main__":
    for raw_guess, secret in examples:
        valid, guess, error = parse_guess(raw_guess)
        if not valid:
            print(f"Guess {raw_guess}: {error}")
            continue
        outcome, hint = check_guess(guess, secret)
        print(f"Guess {guess}, secret {secret}: {outcome} - {hint}")
