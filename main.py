from os import environ

from discord import Client, Embed
import aiohttp

from synth import synth
from commands import commands, http_commands


class Uwu(Client):
    async def on_ready(self):
        # Async HTTP client
        self.http_session = aiohttp.ClientSession()
        print('Howler ready!')
    
    async def on_message(self, message):
        if message.author != self.user and message.content.startswith('!') and message.content.strip() != '!':
            command = message.content[1:].split()[0]

            if command in http_commands:
                await http_commands[command](message, self.http_session)
            elif command in commands:
                await commands[command](message)


uwu = Uwu()
uwu.run(environ['DISCORDTOKEN'])