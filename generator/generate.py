import json
import secrets
from pathlib import Path
from generator.encryption import encrypt_name

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

def draw_participants(participants):
    receivers = participants.copy()
    while True:
        secrets.SystemRandom().shuffle(receivers)
        if all(p != r for p, r in zip(participants, receivers)):
            break

    result = dict(zip(participants, receivers))
    return result

def generate_codes(assignments):
    codes = {}
    for giver, receiver in assignments.items():
        coded = encrypt_name(receiver)
        codes[giver] = coded
    return codes

def save_codes(codes, file_path):
    with open(file_path, "x", encoding="utf-8") as f:
        json.dump(codes, f, indent=4, ensure_ascii=False)

def main():
    try:
        input_file = Path("private/participants.json")
        output_file = Path("private/keys.json")

        participants = load_participants(input_file)
        validated = validate_participants(participants)

        assignments = draw_participants(validated)
        codes = generate_codes(assignments)
        save_codes(codes, output_file)
        print(f"Successfully generated {len(codes)} Secret Santa codes.")
        print(f"Codes saved to: {output_file}")
        return 0
    except FileNotFoundError:
        print("Error: Required file or directory not found.")

    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")

    except KeyError:
        print("Error: Missing 'participants' key in JSON file.")

    except FileExistsError:
        print("Error: Secret Santa codes already exist. Cannot overwrite.")

    except ValueError as e:
        print(f"Error: {e}")

    except TypeError:
        print("Error: Invalid data structure.")

    except OSError:
        print("Error: Unable to read or write the file.")

    return 1

if __name__ == "__main__":
    raise SystemExit(main())