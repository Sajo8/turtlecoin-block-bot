import discord
import asyncio
import time
import json


token = open('tokenfile').read()
client = discord.Client()


@client.event
async def on_ready():
    print("connected")

@client.event
async def on_message(message):
	if message.content == "hi":
		await client.send_message(message.channel, ":cookie:")

client.run(token)


