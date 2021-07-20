import json
import asyncio

import aiohttp


# API URL
url = 'https://bellard.org/textsynth/api/v1/engines/gptj_6B/completions'


def get_data(prompt):
    """
    Returns the "data" argument used in the TextSynth post request
    """

    dictionary =  {
        "prompt": prompt.encode('utf-8')[-4095:].decode('utf-8', 'ignore'),
        "temperature": 0.9,
        "top_k": 40,
        "top_p": 0.9,
        "seed": 0,
    }

    return json.dumps(dictionary, ensure_ascii=False).encode('utf-8')


async def synth(session, prompt):
    """
    Uses TextSynth to complete the prompt
    """

    #
    # Getting the completion
    #

    while True:
        # Preparing arguments
        data = get_data(prompt)
        headers = { 'Content-Type': 'application/json', 'User-Agent': 'HowlerBot'}

        # Do the request
        async with session.post(url, data=data, headers=headers) as resp:
            if resp.status == 200:
                txt = await resp.text()
                if txt.strip():
                    break

    #
    # Formatting the result appropriately and returning
    #
    
    # The text returned from TextSynth comes chopped in dictionaries, so we need to format it
    return "".join([json.loads(line)['text'] for line in txt.splitlines() if line.strip() != ""])
