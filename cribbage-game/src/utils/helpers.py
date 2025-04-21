def validate_input(user_input, valid_options):
    if user_input not in valid_options:
        raise ValueError(f"Invalid input: {user_input}. Valid options are: {valid_options}")

def format_score(score):
    return f"Score: {score}"

def display_message(message):
    print(message)