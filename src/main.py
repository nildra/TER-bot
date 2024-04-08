from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord import Intents, Client, Message
from discord.ext import commands
from response import get_response
import pandas as pd

CHANNEL_CHAT = 1212465738196062289
LIMIT = None
ASK_COMMAND = "!ask"
SCAN_COMMAND = "!scan"

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

    if message.channel.id == CHANNEL_CHAT:
        
        if (user_message.lower().startswith(ASK_COMMAND)):
           await get_response(username=username, user_input=user_message.replace("!ask", ""), message=message)
        elif (user_message.lower().startswith(SCAN_COMMAND)):
        
            messages_df = pd.DataFrame(columns=['auteur', 'contenu', 'heure_date', 'channel', 'mentions', 'user_respond'])

            async for hist_message in message.channel.history(limit=LIMIT):
                author = hist_message.author.name
                content = hist_message.content.replace("\n", " ")
                created_at = hist_message.created_at.strftime("%Y-%m-%d %H:%M:%S")
                channel = hist_message.channel.name
                mentions = "NONE" if len(hist_message.mentions) == 0 else "$".join("{username}".format(username=user.name) for user in hist_message.mentions) # $ separator
                replied_user = "NONE" if not isinstance(hist_message.reference, discord.message.MessageReference) else hist_message.reference.resolved.author.name
                messages_df.loc[len(messages_df)] = [author, content, created_at, channel, mentions, replied_user]

            messages_df.to_csv("scan_{ch}.csv".format(ch=message.channel.name))
            print("Csv crée avec succes !", "scan_{ch}.csv".format(ch=message.channel.name))
            
def main():
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
