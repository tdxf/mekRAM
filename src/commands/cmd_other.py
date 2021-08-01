"""
Various simple commands
"""


from .cmds import cmd


@cmd()
async def tob(_, arg: str, **_k) -> tuple:
    return ' '.join(['{0:b}'.format(ord(char)) for char in arg]),


@cmd()
async def fromb(_, arg: str, **_k) -> tuple:
    return ''.join([chr(int(num_str, 2)) for num_str in arg.split()]),
