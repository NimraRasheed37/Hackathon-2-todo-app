from typing import Optional

def get_non_empty_input(prompt: str, error_message: str) -> Optional[str]:
    """Prompts the user for input and ensures it's not empty."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        else:
            print(error_message)

def get_optional_input(prompt: str) -> Optional[str]:
    """Prompts the user for optional input."""
    value = input(prompt).strip()
    return value if value else None

def confirm_action(prompt: str) -> bool:
    """Prompts the user for yes/no confirmation."""
    while True:
        choice = input(prompt).strip().lower()
        if choice in ["yes", "y"]:
            return True
        elif choice in ["no", "n"]:
            return False
        else:
            print("Please answer 'yes' or 'no'.")
