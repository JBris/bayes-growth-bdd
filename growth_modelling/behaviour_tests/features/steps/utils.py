######################################
# Imports
######################################

# External
from parse_type import TypeBuilder

######################################
# Functions
######################################

def snake_case_string(text: str) -> str:
    """
    Apply some processing to convert a string to snakecase.

    Args:
        text (str):
            The input text.

    Returns:
        str: The snakecase string.
    """
    snake_string = (
        text
        .strip()
        .replace(" ", "_")
        .replace(".", "_")
        .replace("-", "_")
        .lower()
    )
    return snake_string

def parse_comma_list(text: str) -> list:
    """
    Parse a comma-delimited string into a list.

    Args:
        text (str):
            The input text.

    Returns:
        list: The parsed list.
    """
    word_list: list[str] = (
        text
        .replace(", and", ",")
        .replace(" ", "")
        .split(",")
    )

    return word_list

######################################
# Types
######################################

parse_enabled_disabled = TypeBuilder.make_enum({"enabled": True, "disabled": False})
parse_male_female = TypeBuilder.make_enum({"male": "m", "female": "f"})
