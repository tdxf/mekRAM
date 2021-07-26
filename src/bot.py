"""
Creates the discord Client object.
"""


from typing import Any, Callable
import traceback

import aiohttp
import discord


from commands import commands_list, cmds, cmd_emojicode


class Uwu(discord.Client):
    """
    Discord's client, supporting mekRAM's commands.
    """

    async def on_ready(self) -> Any:
        # Async HTTP client
        self.http_session = aiohttp.ClientSession()
        print('mekRAM ready!')
        print(commands_list.commands)

    async def on_message(self, message) -> Any:
        if message.author != self.user and message.content and message.content.strip() != '!':
            try:
                if message.content[0] == '!':
                    # Get the command name
                    command: str = message.content[1:].split()[0]

                    # If the command exists, run it
                    if command in commands_list.commands:
                        # Running

                        # Get the command object
                        command: cmds.Command = commands_list.commands[command]

                        # Run the command
                        result: tuple = await command.run(message, self.http_session)

                        # Replying

                        # Get the function we should use to reply
                        reply_function: Callable = command.get_reply_function(message)

                        # Call it
                        await reply_function(result[0],
                                             embed=result[1] if len(result) > 1 else None)

                # For comands called through direct messages
                # (only d and e for now)
                elif message.channel.type == discord.ChannelType.private and message.content[0] in ['e', 'd']:
                    await message.reply(cmd_emojicode.dm(message, message.content[0] == 'd'))

            except Exception as error:
                traceback.print_exc()
                await message.reply(
                    embed=discord.Embed(title='ERROR.',
                                        color=discord.Color.red(), description=str(error)))
