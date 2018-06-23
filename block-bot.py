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

#discord stuff
@client.event
async def on_ready():
	print("connected")

tc = turtlecoin.TurtleCoind(host='public.turtlenode.io', port=11898)

tcgl = tc.getlastblockheader()['block_header']

#height of the latest block, int
height = tcgl['height']

#hash of the latest block. str
hash = tcgl['hash']

#if latest block is orphan or not. bool(str) 
orphan = tcgl['orphan_status']

#reward of the latest block. int
reward = tcgl['reward']
breward = reward / 100


time = tcgl['timestamp']
prevhash = tcgl['prev_hash']
time2 = tc.getlastblockheaderbyhash(prevhash)['block_header']['timestamp']

timed = time - time2
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

#transaction hashes. str
txs = tc.getblock(hash)
ntxs = len(txs['block']['transactions'])

#hash of each tx in the block
hashes = [x['hash'] for x in txs['block']['transactions']]

#size of each tx
hahsizes = [z['size'] for z in txs['block']['transactions']]


#print("Total size of the transactions:")
txsize = txs['block']
txsizes = txsize['transactionsCumulativeSize']


for hash in hashes:
	#tx extra hash
	teta = tc.gettransaction(hash)['tx']['extra']

#	Decoded version of tx_extra:
	data = '{"jsonrpc":"2.0","id":"test","method":"f_transaction_json","params":{"hash":teta}}'
	response = requests.post('https://blocks.turtle.link/daemon/json_rpc', data=data)

	# idk how to hex decode mman 
	# hex decode the tx extras some how
	
#size of tx extra
txes =  bsizes-txsizes


#percentage of txs in block
txp = txsizes/bsizes * 100
#percentage of tx_extra in block
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
async def on_message(message):
	#if Channel.id != 459931714471460864:
	#	return
	while True:
		nheight = tcgl['height']
		if nheight != height:
			await client.send_message(discord.Object(id='459931714471460864'), printstats)
			print("printstats")
			sleep(5)
		else:
			print("nope")

client.run(token)