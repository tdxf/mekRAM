"""
Uses twint to fetch tweets.
"""


import random
import datetime

import twitter_scraper

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
    while True:
        # Get a random date between the start of 2017 and today
        until: str = datetime.date.fromtimestamp(epochs.get_random_epoch(min_date)).isoformat()

        # Mount the query
        query: str = f'{query} until:{until} min_faves:{min_likes} filter:links'

        # Get the tweets, checking if one of the tweets has an image
        for tweet in twitter_scraper.get_tweets(query):
            print(tweet)

            if tweet['entries']['photos']:
                return tweet
