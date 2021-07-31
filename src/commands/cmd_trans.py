"""
Commands that use Google Translate.
"""


import googletrans

from cmds import cmd, discord


translator = googletrans.Translator()


@cmd()
async def tra(_: discord.Message, argument: str, **_k) -> tuple:
    """
    Translates the string passed to the command.
    Arguments:
        If the single string argument's first character is a ":",
        assume that the first word in the argument is the desired destination languaged.
        If there isn't a ":", use English as the default destination language.
    """

    if not argument:
        raise Exception('Not enough arguments for !tra')

    # Get the destination language
    split_arg: list[str] = argument.split()
    first_arg: str = split_arg[0]

    if first_arg[0] == ':' and len(split_arg) > 1:
        lang: str = first_arg[1:]

        # Override the argument variable,
        # as it will be used later on as the text sent to translater
        argument: str = ' '.join(split_arg[1:])

    # If it wasn't passed, assume english
    else:
        lang: str = 'en'

    # If the language code isn't available, raise an exception
    if lang not in googletrans.LANGUAGES.keys():
        raise Exception("Language doesn't exist! Use !h tra for a list.")

    # Translate the text
    translation = translator.translate(argument, lang)

    # Make a cute embed

    # Get the capitalized language names
    src: str = googletrans.LANGUAGES[translation.src].capitalize()
    dest: str = googletrans.LANGUAGES[translation.dest].capitalize()

    # The embed's title shows the languages
    embed_title: str = f'{src} -> {dest}'

    # Create the embed
    embed = discord.Embed(title=embed_title,
                          description=translation.text,
                          color=discord.Color.teal())

    return None, embed
