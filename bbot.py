import discord
import asyncio
import logging
import turtlecoin
import json
import time
import random

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

def getstats(height):

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
	blocktime = ""
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
			deteta = bytes.fromhex(hash).decode('utf-8')
		except UnicodeDecodeError:
			deteta = "unable to decode, probably nothing in there"

	txes =  bsizes-txsizes

	txp = txsizes/bsizes * 100

	txep = txes/bsizes * 100

	return {'height': height, 'hash': hash, 'orphan': orphan, 'reward': breward, 'bsizes': bsizes, 'blocktime': blocktime, 'ntxs': ntxs, 'hashes': hashes, 'hahsizes': hahsizes, 'txsizes': txsizes, 'teta': teta, 'deteta': deteta, 'txes': txes, 'txp': txp, 'txep': txep}

	#height of the latest block, int
	#height
	#hash of the latest block. str
	#hash 
	#if latest block is orphan or not. bool(str) 
	#orphan 
	#reward of the latest block. int
	#breward
	#if time block took to make is acceptable
	#blocktime
	# size of block
	#bsizes
	#transaction hashes. str
	#ntxs
	#hash of each tx in the block
	#hashes
	#size of each tx
	#hahsizes
	#print("Total size of the transactions:")
	#txsizes
	#print out the tx_Extra hash and its decoded version
	#teta
	#deteta
	#size of tx extra
	#txes
	#percentage of txs in block
	#txp
	#percentage of tx_extra in block
	#txep

def prettyPrintStats(blockstats):
	msg = "BLOCK STATS:\n"
	msg += "Height: {} \n".format(blockstats['height'])
	msg += "Hash: {} \n".format(blockstats['hash'])
	msg += "Orphan: {} \n".format(blockstats['orphan'])
	msg += "Reward {} \n".format(blockstats['reward'])
	msg += "Size: {} \n".format(blockstats['bsizes'])
	msg += "Time took to make: {}".format(blockstats['blocktime'])

	msg += " \nNo. of txs in the block: {} \n".format(blockstats['ntxs'])
	msg += "Tx hashes in the block: {} \n".format(blockstats['hashes'])
	msg += "Size of each tx: {} \n".format(blockstats['hahsizes'])
	msg += "Size of all the txs: {} \n".format(blockstats['txsizes'])

	msg += "tx_extra hash: {} \n".format(blockstats['teta'])
	msg += "Decoded version of tx_extra: {} \n".format(blockstats['deteta'])
	msg += "Size of tx_extra: {} \n".format(blockstats['txes'])

	msg += "Percentage of txs in the block: {} % \n".format(blockstats['txp'])
	msg += "Percentage of tx_extra in the block: {} % \n".format(blockstats['txep'])

	msg += "------------------"

	return msg


@client.event
async def on_ready():
	print("connected")
	height = tcgl['height']
	while True:
		#prettyPrintStats(getstats(nheight))	
		nheight = tc.getblockcount()['count']
		if height != nheight:
			prettyPrintStats(getStats(nheight))
			await client.send_message(discord.Object(id='459931714471460864'), prettyPrintStats(getstats(nheight)))
			print("val changed")
			print(nheight)
			print(height)
			height = nheight
			print(height)
			await asyncio.sleep(0.4)

	

	"""await client.send_message(discord.Object(id='459931714471460864'), printstats)
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
			time.sleep(0.4)"""


"""printstats = We just found a block!

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
.format(height=height, hash=hash, orphan=orphan, reward=breward, bsizes=bsizes, ntxs=ntxs, hashes=hashes, hashsizes=hahsizes, blocktime=blocktime, teta=teta, deteta=deteta, txes=txes, txp=txp, txep=txep, txsizes=txsizes)"""



client.run(token)