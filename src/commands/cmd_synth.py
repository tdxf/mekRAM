"""
Commands for simulating chatting with the GPT AI.
"""


from typing import Optional

from .cmds import cmd, discord
from .synth import synth


# Keys are Discord text channels
# Values are the chat histories (strings)
chats: dict = {}

# Whether the bot is currently awaiting for a reply or not
is_replying: bool = False


def default_prompt(name: str) -> str:
    """ 
    Generates the default prompt, given the name.
    That is, the initial text, created when the bot receives a first message.
    """
    prompt: str = f'The following is an IRC conversation between {name} and the mekRAM artificial intelligence.\n'
    prompt += f"{name}: hello there!\nmekRAM: hi! i'm good!\n"

    return prompt


def filter_only_ai(txt: str) -> str:
    """
    Sometimes the AI tries to predict messages for others.
    Or tries to translate the text into another language.

    We only want the AI's replies, not any other text.

    This function tries to remove these irrelevant lines by filtering 'txt'
    to only include lines that start with "mekRAM: ".

    (Except the first line)
    
    It returns the filtered text.
    """
    txt = txt.splitlines(True)

    return "".join(
        # Always include the first line
        [txt[0]] + 
        # filter
        [line for line in txt if line.startswith('mekRAM: ')])


def assure_channel(channel: discord.TextChannel, prompt: str) -> bool:
    """
    If 'channel' is in the chats list, return False.
    If it isn't, add it, with the value being 'prompt', and return True.
    """
    if channel in chats:
        return False
    else:
        chats[channel] = prompt
        return True
        

@cmd()
async def s(message: discord.Message, content: Optional[str], **kwargs) -> tuple:
    """Command for simulating chatting with Text Synth."""
    global is_replying

    # If the bot is awaiting a response from Text Synth for another message
    if is_replying:
        # FIXME: Bad exception handling to mantain typing effect

        await message.reply('Already replying to another message!')

        # Go back to typing
        await message.channel.trigger_typing()

    elif not content:
        raise Exception('No content!')

    else:
        is_replying = True

        # If a message history for the channel doesn't exist, create one
        if assure_channel(message.channel, default_prompt(message.author.display_name)):
            txt: str = f'in #{message.channel.name}'

            # Use "with you" if it's a private message, else use the channel name
            if message.channel.type != discord.ChannelType.private:
                txt: str = 'with you'

            await message.reply(f'Started talking {txt}!')

        # Cool typing effect
        await message.channel.trigger_typing()

        # Add the new user message to the prompt
        prompt: str = chats[message.channel] + f"{message.author.display_name}: {content}\nmekRAM: "

        # Generate
        while True:
            # Use an AI to complete the prompt
            generated: str = filter_only_ai(await synth(kwargs['aiohttp_session'], prompt))

            # FIXME: limit it to 3 lines
            generated: str = '\n'.join(generated.splitlines()[:3])

            # The string we're going to reply in Discord with
            reply: str = generated.replace('mekRAM: ', '')

            # Make sure it's not empty
            if reply.strip(' \n\t'):
                break

        # Make sure it has a newline in the end
        newline: str = '\n' if generated[-1] != '\n' else ''

        # Update the chat history
        chats[message.channel] = prompt + generated + newline

        # Not replying anymore
        is_replying = False

        return reply,


@cmd()
async def sh(message: discord.Message, _, **_k) -> tuple:
    """
    Replies with the message history for the channel
    """
    if message.channel not in chats:
        raise Exception("This channel doesn't have a message history")

    # Create the embed
    embed = discord.Embed()

    history: str = chats[message.channel]

    # Because of the 1024 character limit, we need to split the text into several fields
    while True:
        # We do it by lines so it's prettier
        value: list = history[:1024].rsplit('\n', 1)

        if not value[0].strip():
            break

        history = history[len(value[0]):]

        print(value)
        print(history)

        embed.add_field(name='text', value=value[0])

    return None, embed


@cmd()
async def sr(message: discord.Message, _: str, **_k) -> tuple:
    """
    Clears the message history for message.channel.
    """

    if message.channel not in chats:
        raise Exception("Channel doesn't have a message history to be deleted")
    chats.pop(message.channel)
    return 'Message history for this channel has been reset',
