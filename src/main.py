"""
Aky's cool Discord bot!
"""


from os import environ

from bot import Uwu


uwu = Uwu()
uwu.run(environ['DISCORDTOKEN'])
