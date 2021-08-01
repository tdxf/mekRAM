"""
Commands that integrate Twitter into them in one way or another.
"""


from .cmds import cmd
from . import twitter


@cmd()
async def ygd(_, _0, **_k) -> tuple:
    """
    Result is (hopefully) a random Oneshot art post from Twitter.
    Tribute to YGamingDude, hence the name.
    """

    result: list[str] = await twitter.search_random_image('#oneshotgame', '2017')

    return result[0],


@cmd()
async def dynamyc(_, _0, **_k) -> tuple:
    """Result is (hopefully) a random Starry Flowers art post from Twitter."""
    result: list[str] = await twitter.search_random_image('#starryflowers', '2017')

    return result[0],
