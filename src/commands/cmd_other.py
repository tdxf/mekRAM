"""
Various simple commands
"""


from base64 import b64encode, b64decode

from .cmds import cmd


@cmd()
async def tob(_, arg: str, **_k) -> tuple:
    return ' '.join(['{0:b}'.format(ord(char)) for char in arg]),


@cmd()
async def fromb(_, arg: str, **_k) -> tuple:
    return ''.join([chr(int(num_str, 2)) for num_str in arg.split()]),


@cmd()
async def to64(_, arg: str, **_k) -> tuple:
    return b64encode(bytes(arg, 'UTF-8')).decode(),


@cmd()
async def from64(_, arg: str, **_k) -> tuple:
    return b64decode(arg).decode(),
