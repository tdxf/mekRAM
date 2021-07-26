"""
Module for communicating with the Text Synth API.
For GPT text completion.
"""


import json

import aiohttp


# API URL
url = 'https://bellard.org/textsynth/api/v1/engines/gptj_6B/completions'


def get_data(prompt: str) -> bytes:
    """Returns the "data" argument used in our post request to Text Synth"""
    dictionary = {
        "prompt": prompt.encode('utf-8')[-4095:].decode('utf-8', 'ignore'),
        "temperature": 0.9,
        "top_k": 15,
        "top_p": 0.85,
        "seed": 0,
    }

    return json.dumps(dictionary, ensure_ascii=False).encode('utf-8')


async def synth(session: aiohttp.ClientSession, prompt: str) -> str:
    """Uses TextSynth to complete the prompt"""
    # Preparing arguments
    data = get_data(prompt)
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'mekRAM'
    }

    while True:
        # Do the request
        async with session.post(url, data=data, headers=headers) as resp:
            # Make sure that the response was 200
            if resp.status == 200:
                # Try to get the text, if anything goes wrong, try again
                try:
                    txt = await resp.text()
                except Exception:
                    continue

                # If everything went right, break out of the infinite loop
                if not txt.strip(' \n\t') == "":
                    break

    # The text returned from Text Synth comes chopped in dictionaries, so we need to format it
    dictionaries: list[str] = [json.loads(line)['text'] for line in txt.splitlines() if line.strip() != ""]
    formatted: str = "".join(dictionaries)
    return formatted
