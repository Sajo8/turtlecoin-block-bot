import discord
import asyncio
import time
import json
import logging
import turtlecoin

#discord stuff
"""token = open('tokenfile').read()
client = discord.Client()"""

#logging/debugging stuff. exxtra noise in console which i dont like
"""logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)"""

#discord stuff
"""@client.event
async def on_ready():
	print("connected")"""

tc = turtlecoin.TurtleCoind(host='public.turtlenode.io', port=11898)
bc = tc.getblockcount()
bcd = bc['count']
print("Blockcount:", bcd)

#discord stuff
"""@client.event
async def on_message(message):
	if message.content == "hi":
		await client.send_message(message.channel, "hi")

client.run(token)"""


