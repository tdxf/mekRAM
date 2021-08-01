"""
Commands for the EmojiEncryptionThingTM
"""


from typing import Callable, Optional

import discord

from .cmds import cmd, ReplyType
from . import emojicode


# A dictionary mapping users to encryption keys
registered_keys: dict = {}


@cmd(ReplyType.PRIVATE)
async def gen(message: discord.Message, _, **_k) -> tuple:
    """
    Generates a new key for the user
    and registers it for them
    """

    # Generate a key
    key = emojicode.generate_key()

    # Register
    registered_keys[message.author] = key

    return (
        f'Registered\nSend me a message starting with "e" to encode text and with "d" to decode text',
        discord.Embed(title='key', description=f'```{emojicode.key_string(key)}```')
    )


@cmd(ReplyType.PRIVATEREPLY)
async def reg(message: discord.Message, key: Optional[str], **_k) -> tuple:
    """Adds the author of 'message' to the registered_keys dictionary. The value being 'key'"""
    emojicode.ensure_key_valid(key)
    registered_keys[message.author] = key
    return 'Registered key!',


@cmd(ReplyType.PRIVATE)
async def dec(message: discord.Message, _, **_k) -> tuple:
    """
    Decodes the message replied to by 'message'.
    """

    # If there's no message being replied to
    if not message.reference:
        raise Exception('You should only use !dec while replying')

    # If the user doesn't have a key registered
    if message.author not in registered_keys:
        raise Exception("You haven't registered a key yet")

    # Decode it
    try:
        # Get the message that was replied to by 'message'
        message_replied: discord.Message = await message.channel.fetch_message(message.reference.message_id)

        # Decrypt string
        decoded: str = emojicode.decrypt_text(message_replied.content, registered_keys[message.author])
    except Exception:
        raise Exception('Error while decoding')
    else:
        decoded: str = f'{message.author.display_name}: {decoded}'
        await message.delete()
        return decoded,


def dm(message: discord.Message, decode: bool) -> str:
    """
    Function for the d and e commands.
    'decode' is a bool, if it's True, we decode the message, if it's False we encode it.

    TEMPORARY
    """
    if message.author not in registered_keys:
        raise Exception("""You haven't registered a key yet, do it with !reg. 
        You could also generate a new one with !gen""")

    func: Callable = emojicode.decrypt_text if decode else emojicode.encrypt_text
    
    return func(message.content[2:], registered_keys[message.author])
