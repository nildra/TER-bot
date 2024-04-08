
import google.generativeai as genai
import os
from IPython.display import Markdown
from dotenv import load_dotenv
from typing import Final
from discord import Message

import replicate

load_dotenv()
#https://replicate.com/account/api-tokens
llama_2_api_key: Final[str] = os.getenv('LLAMA_2')

async def get_response(username, user_input, message: Message):
    print("on recupere la reponse")
    userToCHat = "Message de " + username + ": " + user_input
    output = replicate.run("meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        input={
            "prompt": userToCHat
        }
    )

    # The meta/llama-2-70b-chat model can stream output as it's running.
    # The predict method returns an iterator, and you can iterate over that output.
    reponse = ""
    for item in output:
        # https://replicate.com/meta/llama-2-70b-chat/api#output-schema
        print(item, end="")
        reponse += item
    print("reponse reçu", reponse)

    await sendMessage(message, reponse)


async def sendMessage(message: Message, reponse):
    print("envoie dans le channel")
    await message.channel.send(reponse)