"""
Uses twint to fetch tweets.
"""


import os
import random
import asyncio
import datetime

import nest_asyncio
import twint

from . import epochs


is_fetching: bool = False


async def search_random_image(query: str, min_date: str, min_likes: int = 40) -> list[str]:
    """
    Searches Twitter with 'query', returning a random image from the results.
    Limiting the results by likes and by date.
    Likes being limited with 'min_likes'.
    And date being limited with a random date between 'min_date' and today.

    :param query: What the search terms are to find the images.
    :param min_date: Will search tweets by date, such date being chosen randomly.
                     Range being 'min_date' and today.
    :param min_likes: Limit tweets to have at least this many likes.
    :return: List of image URLs.
    """
    global is_fetching

    if is_fetching:
        raise Exception('Already fetching for another user')

    is_fetching = True

    # Get a random date between the start of 2017 and today
    since: str = datetime.date.fromtimestamp(epochs.get_random_epoch(min_date)).isoformat()

    c = twint.Config()

    c.Images = True
    c.Limit = 20

    c.Search = query
    c.Since = since
    c.Min_likes = min_likes

    tweets: list = []
    c.Store_object = True
    c.Store_object_tweets_list = tweets

    url_list = asyncio.Future()

    def set_url_list(*_) -> None:
        """
        Called after twint finishes filling the tweet list.
        Sets the url_list's value to be the tweet list.
        """
        global is_fetching
        is_fetching = False

        url_list.set_result(tweets)

    nest_asyncio.apply()
    twint.run.Search(c, set_url_list)
    nest_asyncio.apply()

    return random.choice(await url_list).photos
