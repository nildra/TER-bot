from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from response import get_response

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

ints = Intents.default()
ints.message_content = True
client = Client(intents=ints)

@client.event
async def on_ready():
    print(client.user, " is running")

@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return
    
    username = str(message.author)
    user_message = str(message.content)
    print(username, user_message, "#")

    if message.channel.id == 1212465738196062289:
        await get_response(username=username, user_input=user_message, message=message)

def main():
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
