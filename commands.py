from time import gmtime

from pytz import timezone
from discord import Embed

from synth import synth


commands = {}
http_commands = {}


def command(func):
    def inner(message):
        split = message.content.split()
        arguments = split[1:] if len(split) > 1 else []

        return func(message, arguments)
    commands[func.__name__] = func
    return inner


def httpcommand(func):
    def inner(message, http_session):
        return func(message, http_session)
    http_commands[func.__name__] = func
    return inner


########
# HELP #
########

help_embed = Embed()
help_embed.add_field(name='AI Chat', value='!s <message> - Chat\n!sm - Message History\n!sr - Restart')
help_embed.add_field(name='Other', value='!time <person> - Show local time for <person>')

@command
async def help(m, a):
    await m.reply(embed=help_embed)


###########
# AI CHAT #
###########

s_channels = {}
s_replying = False

def s_get_default_prompt(author):
    """ helper """
    return author.name + ': hi!\nAI: hi :D\n'

def s_filter_text(txt):
    """
    Helper function

    Sometimes the AI tries to predict messages for other
    or tries to translate the text into another language

    We only want the AI's replies, not any other text

    This function tries to remove these irrelevant lines by filtering 'txt'
    to only include lines that start with "AI: "

    (Except the first one)
    """
    txt = txt.splitlines(True)

    return "".join([txt[0]] + [line for line in txt if line.startswith('AI: ')])

@httpcommand
async def s(m, session):
    """
    Chat with an AI!
    """

    global s_replying

    if s_replying:
        await m.reply('Already replying to another message!')
        await m.channel.trigger_typing()

    else:
        s_replying = True

        # If a message history for the channel doesn't exist, create one
        if not m.channel in s_channels:
            s_channels[m.channel] = s_get_default_prompt(m.author)

            await m.reply(f'Started talking in #{m.channel.name}!')

        # Cool typing effect
        await m.channel.trigger_typing()

        #
        # Prepare the prompt
        #

        # Gets the message content without the !s
        content = m.content[3:]

        # Structure the prompt like a chatroom 
        prompt = s_channels[m.channel] + f'{m.author.name}: {content}\nAI: '

        #
        # Generate
        #
    
        # Use an AI to complete the prompt
        # It only returns the new generated text, it doesn't include the prompt
        gen = await synth(session, prompt)

        #
        # Remove irrelevant lines
        #

        # Split the text into lines and check if each line starts with "AI:"
        gen = s_filter_text(gen)
        print(gen)

        #
        # Reply!
        #

        await m.reply(gen.replace('AI: ', ''))

        #
        # Update the channel message history
        #
        s_channels[m.channel] = prompt + gen

        s_replying = False


@command
async def sm(m, a):
    """
    Replies with the message history for the channel
    """
    if not m.channel in s_channels:
        await m.reply("This channel doesn't have a message history")
    else:
        embed = Embed()
        history = s_channels[m.channel]

        # Because of the 1024 character limit, we need to split the embed
        while history != '\n':
            # We do it by lines so it's prettier
            value = history[:1024].rsplit('\n', 1)[0]
            history = history[len(value):]

            print(history)

            # Embed name is invisible
            embed.add_field(name='\u200b', value=value)

        await m.reply(embed=embed)


@command
async def sr(m, a):
    if not m.channel in s_channels:
        await m.reply("This channel doesn't have a message history to be deleted")
    else:
        s_channels.pop(m.channel)
        await m.reply('Message history for this channel has been reset')


#########
# Other #
#########

t_people = {
    'aky': ['America/Sao_Paulo', 'the southeast of Brazil'],
    'annas': ['Asia/Jakarta', 'Java, Indonesia'],
    'jack': ['America/Los_Angeles', 'west coast USA'],
    'kamii': ['Asia/Manila', 'the Philippines'],
    'kosai': ['America/Santiago', 'Chile'],
    'trigo': ['Asia/Istanbul', 'Turkey'],
    'wai': ['Europe/Sofia', 'Bulgaria']
}

@command
async def time(m, a):
    person = a[0] if a else None

    if not person in t_people:
        await m.reply("Person isn't in the list")
    else:
        await m.reply(f"It is {timezone(t_people[person][0]).strftime('%Y-%m-%d %H:%M')} in {t_people[person][1]}")