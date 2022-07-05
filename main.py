from distutils.util import change_root
from email import message
from http import client
from pydoc import cli
from random import random, randrange
import discord
import json

TOKEN = 0
f = open('walterDB.json', encoding='utf-8')
db = json.load(f)

client = discord.Client()


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    if message.author == client.user:
        return

    current_message = user_message.lower()

    if current_message == "amogus":
        await message.channel.send(f"Hello {username}!")
        return

    wordsMSG = current_message.split()
    keys = db["slavonijaSupremacyKeys"]

    for word in wordsMSG:
        if word in keys:
            await message.channel.send(slavonijaSupremacy())
            return


def slavonijaSupremacy():
    lines = db["slavonijaSupremacy"]
    chosenMSG = randrange(0, len(lines))
    return lines[chosenMSG]


@client.event
async def on_ready():
    print("LOGIN SUCCESSFUL : {0.user}".format(client))

client.run(TOKEN)
