"""
Command list in an embed.
"""


from .cmds import cmd, discord


help_embed = discord.Embed(title='Commands List. ? means optional')

help_embed.add_field(name='AI Chat',
                     value='!s <message> - Chat\n!sh - Chat History\n!sr - Restart')
help_embed.add_field(name='Other',
                     value='''!time <person?> - Show local time for <person>.
Shows a table containing all the times if no argument is supplied''')


@cmd()
async def mekhelp(_, _0, **_k) -> tuple:
    """
    Displays the help Embed.
    """

    return None, help_embed
