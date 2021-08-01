"""
A command for "reading" the text in an image.
"""


import io

from PIL import Image
import pytesseract

from .cmds import cmd, discord


@cmd()
async def read(message: discord.Message, _, **_k) -> tuple:
    """Tries to read the image attached to 'message'."""

    if not message.attachments or not message.attachments[0].content_type.startswith('image'):
        raise Exception("No images provided")

    stream = io.BytesIO(await message.attachments[0].read())

    image: Image = Image.open(stream)

    txt: str = pytesseract.image_to_string(image)

    if txt == '': txt = 'No text found'

    return txt,
