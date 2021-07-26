"""
Command for telling time in different timezones.
"""

from typing import Any
from datetime import datetime

import pytz

from cmds import cmd


# The time table's head
head: str = '-------- TIME TABLE --------'

people: dict = {
    'aky': ['America/Sao_Paulo', 'the southeast of Brazil'],
    'annas': ['Asia/Jakarta', 'Java, Indonesia'],
    'jack': ['America/Los_Angeles', 'west coast USA'],
    'kamii': ['Asia/Manila', 'the Philippines'],
    'kosai': ['America/Santiago', 'Chile'],
    'trigo': ['Asia/Istanbul', 'Turkey'],
    'wai': ['Europe/Sofia', 'Bulgaria']
}


def get_formatted_time(person_key: str) -> str:
    """
    Gets people[person_key]'s time as a pretty string.
    """

    # Get the person's timezone object
    timezone: Any = pytz.timezone(people[person_key][0])

    # Get the current UTC time
    utc: datetime = datetime.utcnow().replace(tzinfo=pytz.utc)

    # Convert and format
    formatted_time: str = utc.astimezone(timezone).strftime('%I:%M%p %d of %b')

    return formatted_time


def get_time_table() -> str:
    """
    Creates a dynamic pretty time table and returns it.
    """

    time_table: str = '```\n' + head + '\n'

    # Align it

    person_longest_name: str = max(people.keys())
    time_align: int = len(person_longest_name) + 1  # Account for the ":"

    # Add people's times
    for person in people:
        # Define the line and add the border
        line: str = "| "

        # Add the spacing, aligning the names to the right
        line += ' ' * (time_align - len(person) + 1)  # Account for the ":" again

        # Add the person's formatted time
        line += f"{person}: " + f"{get_formatted_time(person)}"

        # Spacing added after the person's time
        right_padding: str = ' ' * (len(head) - len(line) - 1)

        # Add the line to the table
        time_table += line + right_padding + '|\n'

    # Close the table
    time_table += '-' * len(head) + '```'

    return time_table


@cmd()
async def tz(_, person: str, **_k) -> tuple:
    """Shows times in different timezones."""
    print(person)

    if not person:
        return get_time_table(),
    elif person in people.keys():
        return f"In {people[person][1]} it's {get_formatted_time(person)}",
    else:
        raise Exception("Person isn't in the list")
