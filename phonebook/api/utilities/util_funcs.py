import re
from .valid_patterns import PHONE_PATTERNS, ALLOWED_CHARS_RE


def valid_phone_number(number: str) -> tuple[str, bool]:
    """
    Validates a phone number against predefined patterns.

    Args:
        number (str): The phone number to validate.

    Returns:
        tuple: A tuple containing the cleaned phone number and a boolean indicating validity.
    """
    cleaned_number = number.strip()

    if not cleaned_number:
        return "Phone number cannot be empty or whitespace.", False

    if '<' in cleaned_number or '>' in cleaned_number:
        return ("Invalid characters in phone number.", False)

    if re.search(r"\s{2,}", cleaned_number):
        # disallow double or more spaces
        return ("Invalid spacing in phone number.", False)

    if not ALLOWED_CHARS_RE.fullmatch(cleaned_number):
        return ("Invalid characters in phone number.", False)

    if re.fullmatch(r"\d{10}", cleaned_number):
        # raw 10 digits without separators not allowed
        return ("Invalid phone number format.", False)

    # Must match at least one accepted pattern
    if not any(p.fullmatch(cleaned_number) for p in PHONE_PATTERNS):
        return ("Invalid phone number format.", False)

    return (cleaned_number, True)
