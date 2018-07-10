import discord
import asyncio
import turtlecoin
import json
import time
import random

#discord stuff
token = open('tokenfile').read()
client = discord.Client()


tc = turtlecoin.TurtleCoind(host='public.turtlenode.io', port=11898)

tclbh = tc.get_last_block_header()['result']

def getstats(height):

	tcgl = tc.get_last_block_header()['result']['block_header']

	#height of the latest block
	height = tcgl['height']
	#hash of latest block
	hash = tcgl['hash']
	# whether atest block is orphan or not
	orphan = tcgl['orphan_status']

	#reward of the latest block
	reward = tcgl['reward']
	breward = reward / 100

	#wheter the time the block took to make is acceptable or not
	timex = tcgl['timestamp']
	prevhash = tcgl['prev_hash']
	glb = tc.get_block(prevhash)
	time2 = glb['block']['timestamp']
	timed = timex - time2
	rock = "388916188715155467"
	pingrock = "<@" + rock + ">"
	blocktime = ""
	if timed <= 4:
		blocktime += f"Block was too fast, {timed} seconds"
		pingrock += ""
	elif timed >= 90:
		blocktime += f'Took too long, {timed} seconds.'
		pingrock += ""
	else:
		blocktime += f"Took {timed} seconds to make, pretty nice"
		pingrock = ""

	#size of the block
	bsize = tc.get_block(hash)
	bsizes = bsize['block']['blockSize']

	# number of transaction hashes in the block
	txs = tc.get_block(hash)
	ntxs = len(txs['block']['transactions'])

	#each tx hash in the block
	hashes = [x['hash'] for x in txs['block']['transactions']]

	# size of each tx
	hahsizes = [z['size'] for z in txs['block']['transactions']]

	#size of all the txs
	txsize = txs['block']
	txsizes = txsize['transactionsCumulativeSize']


	for hash in hashes:
		#tx extra hash
		teta = tc.get_transaction(hash)['tx']['extra']
		#Decoded version of tx_extra:
		try:
			deteta = bytes.fromhex(teta).decode('utf-8')
		except UnicodeDecodeError:
			print("deta oops")
			#deteta = "unable to decode, probably nothing in there"

	#size of tx extra		
	txes =  bsizes-txsizes

	# % of txs in the block
	txp = txsizes/bsizes * 100

	# % of tx_extra in the block
	txep = txes/bsizes * 100

	return {'height': height, 'hash': hash, 'orphan': orphan, 'reward': breward, 'bsizes': bsizes, 'blocktime': blocktime, 'ntxs': ntxs, 'hashes': hashes, 'hahsizes': hahsizes, 'txsizes': txsizes, 'teta': teta, 'deteta': deteta, 'txes': txes, 'txp': txp, 'txep': txep, 'pingrock': pingrock}


def prettyPrintStats(blockstats):
	msg = "```WE FOUND A NEW BLOCK!\n"
	msg += f"\nHeight: {blockstats['height']} \n"
	msg += f"Hash: {blockstats['hash']} \n"
	msg += f"Orphan: {blockstats['orphan']} \n"
	msg += f"Reward: {blockstats['reward']} \n"
	msg += f"Size: {blockstats['bsizes']} \n"
	msg += f"Time took to make: {blockstats['blocktime']} \n"

	msg += f" \nNo. of txs in the block: {blockstats['ntxs']} \n"
	msg += f"Tx hashes in the block: {blockstats['hashes']} \n"
	msg += f"Size of each tx: {blockstats['hahsizes']} \n"
	msg += f"Size of all the txs: {blockstats['txsizes']} \n \n"

	msg += f"tx_extra hash: {blockstats['teta']} \n"
	msg += f"Decoded version of tx_extra: {blockstats['deteta']} \n"
	msg += f"Size of tx_extra: {blockstats['txes']} \n \n"

	msg += f"Percentage of txs in the block: {blockstats['txp']} % \n"
	msg += f"Percentage of tx_extra in the block: {blockstats['txep']} % ```"

	#msg += blockstats['pingrock']

	return msg
	print(msg)


@client.event
async def on_ready():
	print("connected")
	height = tclbh['height']
	while True:
		#prettyPrintStats(getstats(nheight))	
		nheight = tc.getblockcount()['count']
		if height != nheight:
			prettyPrintStats(getstats(nheight))
			await client.send_message(discord.Object(id='459931714471460864'), prettyPrintStats(getstats(nheight)))
			print("val changed")
			print(nheight)
			print(height)
			height = nheight
			print(height)
		await asyncio.sleep(0.5)


client.run(token)