import discord
import asyncio
import logging
import turtlecoin
import json
import requests
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


#discord stuff
@client.event
async def on_ready():
	print("connected")
	"""last_height = 0
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

"""height = " "
hash = " "
orphan = " "
breward = " "
bsizes = " "
ntxs = " "
hashes = " "
hahsizes = " "
blocktime = " "
teta = " "
response = " "
txes = " "
txp = " "
txep = " "
txsizes = " " """

def getstats():
	#height of the latest block, int
	global height 
	height = tcgl['height']

	#hash of the latest block. str
	global hash 
	hash = tcgl['hash']

	#if latest block is orphan or not. bool(str) 
	global orphan 
	orphan = tcgl['orphan_status']

	#reward of the latest block. int
	reward = tcgl['reward']
	global breward 
	breward = reward / 100


	time = tcgl['timestamp']
	prevhash = tcgl['prev_hash']
	time2 = tc.getlastblockheaderbyhash(prevhash)['block_header']['timestamp']

	timed = time - time2
	rock = "235707623985512451"
	global blocktime 
	blocktime = "Time took to make: "

	if timed <= 10:
		blocktime += "Block was too fast, {timed} seconds <@{rock}>".format(timed=timed, rock=rock)
	elif timed >= 90:
		blocktime += "Took too long, {timed} seconds. <@{rock}>".format(timed=time, rock=rock)
	else:
		blocktime += "Took {timed} seconds to make, pretty nice".format(timed=timed)

	bsize = tc.getblock(hash)
	global bsizes
	bsizes = bsize['block']['blockSize']

	#transaction hashes. str
	txs = tc.getblock(hash)
	global ntxs
	ntxs = len(txs['block']['transactions'])

	#hash of each tx in the block
	global hashes
	hashes = [x['hash'] for x in txs['block']['transactions']]

	#size of each tx
	global hahsizes
	hahsizes = [z['size'] for z in txs['block']['transactions']]


	#print("Total size of the transactions:")
	txsize = txs['block']
	global txsizes
	txsizes = txsize['transactionsCumulativeSize']


	for hash in hashes:
		#tx extra hash
		global teta
		teta = tc.gettransaction(hash)['tx']['extra']

	#	Decoded version of tx_extra:
		data = '{"jsonrpc":"2.0","id":"test","method":"f_transaction_json","params":{"hash":teta}}'
		global response
		response = requests.post('https://blocks.turtle.link/daemon/json_rpc', data=data)

		# idk how to hex decode mman 
		# hex decode the tx extras some how
	
	#size of tx extra
	global txes
	txes =  bsizes-txsizes


	#percentage of txs in block
	global txp
	txp = txsizes/bsizes * 100
	#percentage of tx_extra in block
	global txep
	txep = txes/bsizes * 100


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
Decoded version of tx_extra: {response} (this is borken i need help)
Size of tx_extra: {txes} au

Percentage of txs in the block: {txp} %
Percentage of tx_extra in the block: {txep} %

""".format(height=height, hash=hash, orphan=orphan, reward=breward, bsizes=bsizes, ntxs=ntxs, hashes=hashes, hashsizes=hahsizes, blocktime=blocktime, teta=teta, response=response, txes=txes, txp=txp, txep=txep, txsizes=txsizes)

print(printstats)


@client.event
async def upheight():
	while True:
		nheight = tcgl['height']
		if nheight != height:
			getstats()
			await client.send_message(discord.Object(id='459931714471460864'), printstats)
			print("printstats")
			sleep(5)
		else:
			print("nope")
			sleep(5)

client.run(token)