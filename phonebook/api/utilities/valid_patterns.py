import re

# Accept only these characters up-front (rejects slashes/XSS/etc.)
ALLOWED_CHARS_RE = re.compile(r"^[0-9()+.\- ]+$")

# Union of accepted phone formats
PHONE_PATTERNS = [
    # 1) Internal 5-digit extension: 12345
    re.compile(r"^\d{5}$"),
    # 2) NA local subscriber only: 123-1234
    re.compile(r"^\d{3}-\d{4}$"),
    # 3) NA with parentheses area code, optional country code 1 or +1:
    #    (703)111-2121, 1(670)123-4567, +1 (703) 123-1234
    re.compile(r"^(?:\+?1[ .-]?)?\(\d{3}\)[ ]?\d{3}-\d{4}$"),
    # 4) NA with separators (hyphen, space, dot), optional country code 1 or +1:
    #    670-123-4567, 670 123 4567, 670.123.4567, 1-670-123-4567, 1 670 123 4567, 1.670.123.4567
    re.compile(r"^(?:\+?1[ .-]?)?\d{3}-\d{3}-\d{4}$"),
    re.compile(r"^(?:\+?1[ .-]?)?\d{3} \d{3} \d{4}$"),
    re.compile(r"^(?:\+?1[ .-]?)?\d{3}\.\d{3}\.\d{4}$"),
    # 5) International with +CC and area code in parens:
    #    +32 (21) 212-2324
    re.compile(r"^\+\d{1,3} \(\d{1,3}\) \d{2,4}[- ]\d{3,4}$"),
    # 6) International with 011 prefix:
    #    011 701 111 1234, 011 1 703 111 1234
    re.compile(r"^011(?: [0-9]{1,4}){3,4}$"),
    # 7) Danish 8-digit formats, spaces or dots, optional +45/45:
    #    12 34 56 78, 1234 5678, 12.34.56.78, 1234.5678, +45 12 34 56 78
    re.compile(r"^(?:\+?45[ .]?)?(?:\d{2}(?:[ .]\d{2}){3}|\d{4}[ .]\d{4})$"),
    # 8) Ten digits as two groups of five separated by space or dot:
    #    12345 12345, 12345.12345
    re.compile(r"^\d{5}[ .]\d{5}$"),
]

ATTACKER_REGEX = re.compile(
    r"\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|EXEC|UNION)\b|--|;",
    re.IGNORECASE,
)
