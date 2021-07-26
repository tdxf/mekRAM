"""
Function for generating a random epoch time.
Used for getting random posts in Twitter and, in the future, Reddit.
"""


import time
import datetime
import random


def get_random_epoch(min_date: str) -> int:
    """
    Returns a random epoch timestamp, ranging from 'min_date' to the current time.
    'min_date' may be in ISO format or only specify the year.
    """

    # Allow 'min_date' to only specify a year
    if len(min_date) == 4:
        min_date += '-01-01'

    # Get the epochs
    min_epoch: int = int(datetime.datetime.fromisoformat(min_date).timestamp())
    epoch_now: int = int(time.time())

    # Exception for if the minimum time is illogical
    if min_epoch > epoch_now:
        raise Exception('Minimum time bigger than current time')

    # Return the random epoch
    return random.randint(min_epoch, epoch_now)
