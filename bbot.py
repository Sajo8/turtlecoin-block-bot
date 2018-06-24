import discord
import asyncio
import logging
import turtlecoin
import json
import time

#discord stuff
token = open('tokenfile').read()
client = discord.Client()

"""'def prettyPrintDict(dict):
	try:
		print (json.dumps(dict, indent=4, sort_keys=True))
	except Exception as e:
		print('{}, Error: {}'.format('Failed to decode dict as json', e))"""

tc = turtlecoin.TurtleCoind(host='public.turtlenode.io', port=11898)

tcgl = tc.getlastblockheader()['block_header']

"""def hi():
	last_height = 0
	height = 0

	while True:
		height = tcgl['height']
		if height != last_height:
			last_height = height
			info = getDaemonInfo()
			msg = prettyPrintInfo(info)
			client.send_message(channel, msg)
		time.sleep(5)

async def getDaemonInfo():
	hash = tcgl['hash']
	return {'hash': hash}

async def prettyPrintInfo(blockInfo):
	msg = ""
	msg += f"Hash: {blockInfo['hash']}"
	return msg"""


height = tcgl['height']
hash = tcgl['hash']
orphan = tcgl['orphan_status']

reward = tcgl['reward']
breward = reward / 100

timex = tcgl['timestamp']
prevhash = tcgl['prev_hash']
glb = tc.getblock(prevhash)
time2 = glb['block']['timestamp']
timed = timex - time2
rock = "235707623985512451"
blocktime = "Time took to make: "
if timed <= 10:
	blocktime += "Block was too fast, {timed} seconds <@{rock}>".format(timed=timed, rock=rock)
elif timed >= 90:
	blocktime += "Took too long, {timed} seconds. <@{rock}>".format(timed=time, rock=rock)
else:
	blocktime += "Took {timed} seconds to make, pretty nice".format(timed=timed)

bsize = tc.getblock(hash)
bsizes = bsize['block']['blockSize']

txs = tc.getblock(hash)
ntxs = len(txs['block']['transactions'])

hashes = [x['hash'] for x in txs['block']['transactions']]

hahsizes = [z['size'] for z in txs['block']['transactions']]

txsize = txs['block']
txsizes = txsize['transactionsCumulativeSize']

for hash in hashes:
	#tx extra hash
	teta = tc.gettransaction(hash)['tx']['extra']
#	Decoded version of tx_extra:
	try:
		deteta = bytes.fromhex(teta[66:]).decode('utf-8')
	except UnicodeDecodeError:
		deteta = "unable to decode, probably nothing in there"

	#hex decode tx extra somehow

txes =  bsizes-txsizes

txp = txsizes/bsizes * 100

txep = txes/bsizes * 100

def getstats():
	#height of the latest block, int
	height
	#hash of the latest block. str
	hash 
	#if latest block is orphan or not. bool(str) 
	orphan 
	#reward of the latest block. int
	breward
	#if time block took to make is acceptable
	blocktime
	# size of block
	bsizes
	#transaction hashes. str
	ntxs
	#hash of each tx in the block
	hashes
	#size of each tx
	hahsizes
	#print("Total size of the transactions:")
	txsizes
	#print out the tx_Extra hash and its decoded version
	teta
	deteta
	#size of tx extra
	txes
	#percentage of txs in block
	txp
	#percentage of tx_extra in block
	txep

getstats()

printstats = """We just found a block!

Height: {height}
Hash: {hash}
Orphan: {orphan}
Reward: {reward}
Block size: {bsizes}
{blocktime}

No. of txs in the block: {ntxs}
Tx hashes in the block: {hashes}
Size of each tx: {hashsizes}
Size of all the txs: {txsizes}

tx_extra hash: {teta}
Decoded version of tx_extra: {deteta}
Size of tx_extra: {txes} au

Percentage of txs in the block: {txp} %
Percentage of tx_extra in the block: {txep} %

-----------------------------------------------
""".format(height=height, hash=hash, orphan=orphan, reward=breward, bsizes=bsizes, ntxs=ntxs, hashes=hashes, hashsizes=hahsizes, blocktime=blocktime, teta=teta, deteta=deteta, txes=txes, txp=txp, txep=txep, txsizes=txsizes)

while True:
	getstats()


@client.event
async def on_ready():
	print("connected")
	await client.send_message(discord.Object(id='459931714471460864'), printstats)
	while True:
		nheight = tc.getblockcount()['count']
		if nheight != height:
			print(nheight)
			print(height)
			print(printstats)
			await client.send_message(discord.Object(id='459931714471460864'), printstats)
			time.sleep(0.4)
		else:
			print("nope")
			print(neight)
			print(height)
			time.sleep(0.4)



client.run(token)