from distutils.util import change_root
from email import message
from http import client
from pydoc import cli
from random import random, randrange
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import json
from fifteen_api import FifteenAPI

fDB = open('walterDB.json', encoding='utf-8')
f = open('token.txt', "r")
db = json.load(fDB)
TOKEN = f.read()

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=".", intents=intents)
tts_api = FifteenAPI(show_debug=True)


@client.event
async def on_ready():
    print(
        "LOGIN SUCCESSFUL : {0.user}\n-----------------------------".format(client))


@client.event
async def on_message(message):
    # username = str(message.author).split('#')[0]
    user_message = str(message.content)
    #channel = str(message.channel.name)
    #print(f'{username}: {user_message} ({channel})')

    if message.author == client.user:
        return

    current_message = user_message.lower()

    # --------------------------------------------------------------

    # if current_message == ".join":
    #     channel = client.get_channel('610548499192479748')
    #     await client.join_voice_channel(channel)
    #     print('Bot joined the channel.')
    #     return

    # --------------------------------------------------------------
    wordsMSG = current_message.split()
    keys = db["slavonijaSupremacyKeys"]

    for word in wordsMSG:
        if word in keys:
            await message.channel.send(slavonijaSupremacy())
            return

    await client.process_commands(message)


@client.command(pass_context=True)
async def say(ctx, arg1, arg2):
    user = ctx.message.author
    channel = user.voice.channel

    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if (ctx.author.voice and voice == None):
        voice = await channel.connect()
    elif (not ctx.author.voice):
        await ctx.send("Cigane moraš biti u voicu!")
        return

    if(arg1 == "" or arg2 == ""):
        ctx.send("Correct Syntax : .say <voice> <text>")
        return

    response = tts_api.save_to_file(arg1, arg2, "tts.wav")
    assert response["status"] == "OK"
    assert response["filename"] == "tts.wav"
    print(response)

    source = FFmpegPCMAudio("tts.wav")
    player = voice.play(source)


# @client.command(pass_context=True)
# async def play(ctx):
#     response = tts_api.save_to_file("Fluttershy", "One more test", "tts.wav")
#     assert response["status"] == "OK"
#     assert response["filename"] == "tts.wav"
#     print(response)
#     return


@client.command(pass_context=True)
async def fuckoff(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Aj ode ja crncu jedan!")
    else:
        await ctx.send("Alo ba! Ti si na kreku ako mislis da sam u voicechannelu!")


def slavonijaSupremacy():
    lines = db["slavonijaSupremacy"]
    chosenMSG = randrange(0, len(lines))
    return lines[chosenMSG]


client.run(TOKEN)
