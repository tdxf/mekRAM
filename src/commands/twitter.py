"""
Uses twint to fetch tweets.
"""


import os
import random
import asyncio
import datetime

import twint

import epochs


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
    # Make sure that the tweet selected has at least one image in it
    # Get a random date between the start of 2017 and today
    until: str = datetime.date.fromtimestamp(epochs.get_random_epoch(min_date)).isoformat()

    c = twint.Config()

    c.Images = True
    c.Limit = 10

    c.Search = query
    c.Until = until
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
        url_list.set_result(tweets)

    twint.run.Search(c, set_url_list)

    return random.choice(await url_list).photos
