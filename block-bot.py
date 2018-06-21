import discord
import asyncio
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

wd = turtlecoin.Walletd(password='test')

tcgl = tc.getlastblockheader()['block_header']

#height of the latest block, int
height = tcgl['height']
print("Height:", height)

#hash of the latest block. str
hash = tcgl['hash']
print("Hash:", hash)

#if latest block is orphan or not. bool(str) 
orphan = tcgl['orphan_status']
print("Orphan:", orphan)

#reward of the latest block. int
reward = tcgl['reward']
print("Block reward:", reward, "TRTL")


#transaction hashes. str
txs = wd.get_transaction_hashes(addresses=["TRTLuwiaLFrdZtpApXbf5WT6VtpQrBaPnjQgpgLpjD6sdnz3uwKXxRnamo3SEs7TLpDQwmXTxuppsScAAbpGe7CX8Kdsdrgmz6d"], block_hash="748d6ad93d0d64fe6c5bad40975a09e269f92feb4655bd5c4bab3a6074206939", block_count=1, payment_id='')

print("No. of txs in the block:", len(txs))
print("Transaction hashes:")
print(txs)



#discord stuff
"""@client.event
async def on_message(message):
	if message.content == "hi":
		await client.send_message(message.channel, "hi")

client.run(token)"""


