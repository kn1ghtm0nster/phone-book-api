import pytest

from phonebook.api.utilities import valid_phone_number

INVALID_NUMBERS = [
    '123',
    '1/703/123/1234',
    'NR 102-123-1234',
    '<script>alert("xss")</script>',
    '7031231234',
    '+1234  (201)  123-1234',
    '(001)  123-1234',
    '+01  (703)  123-1234',
    '(703)  123-1234 ext 204',
]

VALID_NUMBERS = [
    '12345',
    '(703)111-2121',
    '123-1234',
    '+1 (703)111-2121',
    '+32 (21) 212-2324',
    '1(703)123-1234',
    '011 701 111 1234',
    '12345.12345',
    '011 1 703 111 1234'
]


def test_valid_phone_number():
    num = '703-123-4567'
    assert valid_phone_number(num) == ('703-123-4567', True)


def test_valid_phone_number_empty_string():
    num = ''
    assert valid_phone_number(num) == (
        "Phone number cannot be empty or whitespace.", False)


def test_valid_phone_number_xss_attempt():
    num = '<script>alert("xss")</script>'
    assert valid_phone_number(num) == (
        "Invalid characters in phone number.", False)


def test_valid_phone_number_double_spaces():
    num = '703  123  4567'
    assert valid_phone_number(num) == (
        "Invalid spacing in phone number.", False)


def test_valid_phone_number_no_separators():
    num = '7031234567'
    assert valid_phone_number(num) == (
        "Invalid phone number format.", False)


def test_valid_phone_number_invalid_values():
    for num in INVALID_NUMBERS:
        assert valid_phone_number(num)[1] is False


def test_valid_phone_number_valid_values():
    for num in VALID_NUMBERS:
        assert valid_phone_number(num)[1] is True
