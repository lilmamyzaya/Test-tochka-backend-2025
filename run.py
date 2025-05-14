import json
from datetime import datetime

def check_capacity(max_capacity: int, guests: list) -> bool:
    events = []

    for guest in guests:
        check_in = datetime.strptime(guest["check-in"], "%Y-%m-%d").date()
        check_out = datetime.strptime(guest["check-out"], "%Y-%m-%d").date()
        events.append((check_in, 1))    # заезд
        events.append((check_out, -1))  # выезд

    events.sort()
    current = 0

    for _, change in events:
        current += change
        if current > max_capacity:
            return False

    return True


def read_non_empty():
    while True:
        line = input()
        if line.strip():
            return line.strip()

if __name__ == "__main__":
    max_capacity = int(read_non_empty())
    n = int(read_non_empty())

    guests = []
    for _ in range(n):
        line = read_non_empty()
        guests.append(json.loads(line))

    print(check_capacity(max_capacity, guests))
