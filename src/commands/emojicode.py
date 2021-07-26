"""
Emoji encryption!

=======
| WHY |
=======

indeed.

========
| KEYS |
========

Keys are encoded using Ascii85.
When decoded, they return a mapping list.

In this list, each item's index links it to the string.printable character of same index.
While each item's integer value links it to the emoji_list's character with that number index.
"""

import string
import random
from base64 import a85encode, a85decode


printables: list = list(string.printable)
emojis: list = list(
    '😇😚🤨😢😪👽🤭😃😊😽😜🧐😮😒😲😣😗😞😝🤗👾💨👺😥🤫🤑🥸😳😦🤒😷🤥🤯🤠🙄😁😩🤔😶😰😔🥶💀🥵😙🤢🤕😐😵🤮😸👿😹😍😾🤧🤬😟😴🤤🥴😕😏🤪😀😯😎💫🥰😆😠🥱🤐😓😋😨🙀💩😅😈😑😻😧🤩😂😡😫🙁🤣😖😭😄👻😱👹😘😛😉🥳🙃😼😿🥲😤🤖😌🤡😬🙂🤓🥺'
)


def generate_key() -> bytes:
    """Generates a random key."""
    # A list of emoji indexes in the emoji list
    list_of_indexes: list[int] = list(range(len(emojis)))

    # Randomly get 'length of the list of printable characters' indexes
    sample: list = random.sample(list_of_indexes, k=len(printables))

    # Encode the key in Ascii85 so it's shorter
    return a85encode(bytes(sample))


def key_string(key: bytes) -> str:
    """Converts the 'key' bytes into printable ascii text"""
    return key.decode('ascii')


def ensure_key_valid(key: bytes) -> None:
    """Raises an exception if key is invalid."""
    try:
        if not len(a85decode(key)) == len(printables):
            raise Exception("Key doesn't have the right number of elements")
    except Exception as exception:
        raise Exception(f'INVALID KEY: {str(exception)}')


def key_to_dict(key: bytes) -> dict:
    """Returns a dictionary that maps emojis to printable characters"""
    ensure_key_valid(key)

    # Decode the key to get the list of indexes for the emojis list
    emoji_indexes: list = list(a85decode(key))

    # Makes the mapping in the emoji_indexes list more explicit
    # by turning it into a dictionary
    # Read this module's docstring's key section for an explanation
    map_dict: dict = {}

    for printables_index, emojis_index in enumerate(emoji_indexes):
        map_dict[printables[printables_index]] = emojis[emojis_index]

    return map_dict


def encrypt_text(txt: str, key: bytes) -> str:
    """
    Encrypt 'txt' with 'key'.
    Returns the encrypted text.
    """

    # Encode the text with Ascii85 first
    txt: str = a85encode(txt.encode('ascii')).decode('ascii')

    # Get the mapping dictionary
    key: dict = key_to_dict(key)
    return ''.join([key[c] for c in txt])


def decrypt_text(encrypted_txt: str, key: bytes) -> str:
    """
    Decrypts 'encrypted_txt' with 'key'.
    Returns the decrypted text.
    """

    # Get the mapping dictionary, and invert it
    map_dict: dict = key_to_dict(key)
    map_dict: dict = {map_dict[k]: k for k in map_dict}

    # Unemojify the text
    txt: str = ''.join([map_dict[char] for char in encrypted_txt])

    # Decode the text using Ascii64
    txt: bytes = bytes(txt, 'ascii')
    txt: str = a85decode(txt).decode('ascii')

    return txt


# Just for testing
if __name__ == '__main__':
    my_key: bytes = generate_key()
    print(f"key: {key_string(my_key)}")

    encoded_text: str = encrypt_text('quick brown fox', my_key)
    print(f"encoded text: {encoded_text}")

    decoded_text: str = decrypt_text(encoded_text, my_key)
    print(f"decoded text: {decoded_text}")
