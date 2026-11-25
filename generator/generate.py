import json
import secrets
from pathlib import Path

def load_participants(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        participants = json.load(f)
    return participants["participants"]

def validate_participants(participants):
    participants_cleaned = []
    if not isinstance(participants, list):
        raise ValueError("Needs to be a list")
    elif len(participants) < 3:
        raise ValueError("You need more friends")
    for p in participants:
        if not isinstance(p, str):
            raise ValueError("Your friend is not a number")
        p = p.strip()
        if p == "":
            raise ValueError("You have a friend without a name?")
        participants_cleaned.append(p)

    if len(participants_cleaned) != len({p.lower() for p in participants_cleaned}):
        raise ValueError("You had dupicate names. If you have friends with same names then use their surename.")
    return participants_cleaned

        






file = Path("examples/participants.example.json")

participants = load_participants(file)
print(isinstance(participants, list))
