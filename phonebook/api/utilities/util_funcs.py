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


def valid_name(name: str) -> tuple[str, bool]:
    """
    Validates a contact name:
        - Only letters, spaces, apostrophes (’ or '), hyphens, commas, dots
        - No empty/whitespace-only
        - No double spaces
        - Apostrophes and hyphens must be between letters
        - Optional comma in “Last, First [Middle|Initial.]” form
        - Dots allowed only for initials (e.g., “F.”)
        - At most one hyphen in the whole name (reject multi-hyphen chains)
        - Max 3 tokens (reject overly long token counts)
    """
    cleaned = name.strip()
    NAME_ALLOWED_CHARS_RE = re.compile(r"^[A-Za-z\u00C0-\u024F ’'\-.,]+$")

    if not cleaned:
        return "Name cannot be empty or whitespace.", False

    # Basic character allow-list (blocks digits, <, >, *, ;, etc.)
    if not NAME_ALLOWED_CHARS_RE.fullmatch(cleaned):
        return "Invalid characters in name.", False

    # No double spaces
    if re.search(r"\s{2,}", cleaned):
        return "Invalid name.", False

    # Apostrophes and hyphens must be surrounded by letters
    letter = r"[A-Za-z\u00C0-\u024F]"
    if re.search(fr"(?<!{letter})[’']|[’'](?!{letter})", cleaned):
        return "Invalid Name.", False
    if re.search(fr"(?<!{letter})-|-(?!{letter})", cleaned):
        return "Invalid Name.", False

    # If there is a comma, enforce “Last, First …”
    if "," in cleaned:
        if cleaned.count(",") != 1:
            return "Invalid Name.", False
        # Must be "something, space something"
        if not re.fullmatch(fr"{letter}[A-Za-z\u00C0-\u024F ’'\-]*, {letter}[A-Za-z\u00C0-\u024F ’'\-\.]*", cleaned):
            return "Invalid Name.", False

    # Dots must be used only for initials (single letter followed by dot, then end or space)
    for m in re.finditer(r"\.", cleaned):
        i = m.start()
        # Dot must follow a single letter; preceding char must be a letter and the char before that must be start or space/comma
        if i == 0 or not cleaned[i - 1].isalpha():
            return "Invalid Name.", False
        # After dot must be end or a space
        if i + 1 < len(cleaned) and cleaned[i + 1] != " ":
            return "Invalid Name.", False

    # Reject multi-hyphen chains (allow at most one hyphen total)
    if cleaned.count("-") > 1:
        return "Invalid name.", False

    # Reject overly long token counts (max 3 tokens after removing commas)
    token_str = cleaned.replace(",", "")
    tokens = [t for t in token_str.split(" ") if t]
    if len(tokens) > 3:
        return "Invalid name.", False

    return cleaned, True
