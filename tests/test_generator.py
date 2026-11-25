import pytest

from generator.generate import (
    load_participants,
    validate_participants,
    draw_participants
)
from generator.encryption import(
    encrypt_name,
    decrypt_name
)

from pathlib import Path
from cryptography.exceptions import InvalidTag
import base64

def test_valid_participants():
    participants = ["Alice", "Bob", "Charlie"]

    validated = validate_participants(participants)

    assert validated == participants

@pytest.mark.parametrize("participants", [
    ["Alice", "Bob"],
    "Alice",
    ["Alice", 123, "Bob"],
    ["Alice", "", "Bob"],
    ["Alice", "   ", "Bob"],
    ["Alice", "Bob", "Alice"],
    ["Alice", "Bob", "ALICE"],
    ["Alice", "Bob", " Alice "]
])
def test_invalid_participants(participants):
    with pytest.raises(ValueError):
        validate_participants(participants)

def test_strip_whitespace():
    expected = ["Alice", "Bob", "Charlie"]
    participants = [" Alice ", "Bob", " Charlie "]

    validated = validate_participants(participants)

    assert validated == expected


@pytest.mark.parametrize("participants", [
    ["Alice", "Bob", "Charlie"],
    ["Alice", "Bob", "Charlie", "David"],
    ["Alice", "Bob", "Charlie", "David", "Albert"]
])
def test_no_self_assignment(participants):
    result = draw_participants(participants)

    for giver, receiver in result.items():
        assert giver != receiver

@pytest.mark.parametrize("participants", [
    ["Alice", "Bob", "Charlie"],
    ["Alice", "Bob", "Charlie", "David"],
    ["Alice", "Bob", "Charlie", "David", "Albert"]
])
def test_all_participants_are_givers(participants):
    result = draw_participants(participants)

    assert set(participants) == set(result.keys())

@pytest.mark.parametrize("participants", [
    ["Alice", "Bob", "Charlie"],
    ["Alice", "Bob", "Charlie", "David"],
    ["Alice", "Bob", "Charlie", "David", "Albert"]
])
def test_all_participants_are_receivers(participants):
    result = draw_participants(participants)

    assert set(participants) == set(result.values())

def test_original_list_unchanged():
    participants = ["Alice", "Bob", "Charlie", "David"]
    copy_participants = participants.copy()
    draw_participants(participants)
    assert participants == copy_participants


def test_repeated_draws():
    participants = ["Alice", "Bob", "Charlie", "David", "Albert"]

    for _ in range(1000):
        result = draw_participants(participants)

        assert set(participants) == set(result.keys())
        assert set(participants) == set(result.values())
        for giver, receiver in result.items():
            assert giver != receiver

def test_load_participants():
    expected = ["Alice", "Bob", "Charlie", "David"]
    file = Path("examples/participants.example.json")
    participants = load_participants(file)
    assert expected == participants

@pytest.mark.parametrize("name", [
    "Alberto",
    "Jüri",
    "Õnne",
    "Mari Tamm",
    "Émilie"
])
def test_encrypt_decrypt(name):
    en_name = encrypt_name(name)
    assert name == decrypt_name(en_name)


def test_unique_codes():
    name = "Alberto"

    en1 = encrypt_name(name)
    en2 = encrypt_name(name)

    assert en1 != en2

def test_invalid_code():
    code = "invalid_code"

    with pytest.raises(ValueError):
        decrypt_name(code)

def test_modified_code():
    name = "Alberto"
    code = encrypt_name(name)

    data = bytearray(base64.urlsafe_b64decode(code))

    data[-1] ^= 1

    modified_code = base64.urlsafe_b64encode(data).decode("utf-8")

    with pytest.raises(InvalidTag):
        decrypt_name(modified_code)