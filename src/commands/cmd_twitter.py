"""
Commands that integrate Twitter into them in one way or another.
"""


from cmds import cmd
import twitter


@cmd()
async def ygd(_, _0, **_k) -> tuple:
    """
    Result is a random Oneshot art post from Twitter.
    Tribute to YGamingDude, hence the name.
    """

    result: list[str] = await twitter.search_random_image('#oneshotgame', '2017')

    return result[0],
