import discord
import asyncio
import turtlecoin
import json
import sys
import time
import random

# discord stuff
client = None
tc = None
tclbh = None
token = open('tokenfile').read()

if token:
	if token == 'YOUR-TOKEN-HERE':
		token = None
	else:
		client = discord.Client()


def connect_to_turtlecoind():
	global tc
	global tclbh
	tc = turtlecoin.TurtleCoind(host='public.turtlenode.io', port=11898)
	tclbh = tc.get_last_block_header()['result']


def decode_tx_extra(tx_extra_hex):
	curr_index = 0
	custom_data_arr = []
	tx_extra_decoded = ''

	while(curr_index < len(tx_extra_hex)):
		# these are special cases. See https://cryptonote.org/cns/cns005.txt
		if tx_extra_hex.startswith('00', curr_index):  # padding
			# All zeroes from here. No need to report this. We're done!
			curr_index = len(tx_extra_hex)
		elif tx_extra_hex.startswith('01', curr_index):  # payment ID
			curr_index += 2
			payment_id = tx_extra_hex[curr_index:curr_index + 65]
			curr_index += 65
		elif tx_extra_hex.startswith('02', curr_index):  # extra nonce (custom data)
			# next byte will specify size
			subfield_size = int(tx_extra_hex[curr_index:curr_index + 2], 16)
			curr_index += 2
			data = tx_extra_hex[curr_index:curr_index + subfield_size]
			custom_data_arr.append(data)
			curr_index += subfield_size
		else:
			tx_extra_decoded += "Hm, something went wrong. I got an invalid subfield tag of {tag}\n".format(tag=tx_extra_hex[curr_index:])
			curr_index += 2

	tx_extra_decoded += "Payment ID: {}\n".format(payment_id)

	for hash in custom_data_arr:
		utf8_str = None
		tx_extra_decoded += "Custom Data Hex: {}\n".format(hash)
		# try decoding as utf-8 data as well
		try:
			utf8_str = bytearray.fromhex(hash).decode()
		except ValueError as err:
			pass

		if utf8_str:
			tx_extra_decoded += "Custom Data UTF-8: {}\n".format(utf8_str)

	return tx_extra_decoded


def getstats(height):
	tcgl = tc.get_last_block_header()['result']['block_header']

	# height of the latest block
	height = tcgl['height']
	# hash of latest block
	hash = tcgl['hash']
	# whether atest block is orphan or not
	orphan = tcgl['orphan_status']

	# reward of the latest block
	reward = tcgl['reward']
	breward = reward / 100

	# wheter the time the block took to make is acceptable or not
	timex = tcgl['timestamp']
	prevhash = tcgl['prev_hash']
	glb = tc.get_block(prevhash)
	time2 = glb['result']['block']['timestamp']
	timed = timex - time2
	rock = "388916188715155467"
	pingrock = "<@" + rock + ">"
	blocktime = ""
	if timed <= 4:
		blocktime += "Block was too fast, {timed} seconds".format(timed=timed)
		pingrock += ""
	elif timed >= 90:
		blocktime += 'Took too long, {timed} seconds.'.format(timed=timed)
		pingrock += ""
	else:
		blocktime += "Took {timed} seconds to make, pretty nice".format(timed=timed)
		pingrock = ""

	# size of the block
	bsize = tc.get_block(hash)
	bsizes = bsize['result']['block']['blockSize']

	# number of transaction hashes in the block
	txs = tc.get_block(hash)
	ntxs = len(txs['result']['block']['transactions'])

	# each tx hash in the block
	hashes = [x['hash'] for x in txs['result']['block']['transactions']]

	# size of each tx
	hahsizes = [z['size'] for z in txs['result']['block']['transactions']]

	# size of all the txs
	txsize = txs['result']['block']
	txsizes = txsize['transactionsCumulativeSize']

	for hash in hashes:
		# tx extra hash
		teta = tc.get_transaction(hash)['result']['tx']['extra']
		# Decoded version of tx_extra:
		deteta = decode_tx_extra(teta)

	# size of tx extra
	txes = bsizes - txsizes

	# % of txs in the block
	txp = txsizes / bsizes * 100

	# % of tx_extra in the block
	txep = txes / bsizes * 100

	return {'height': height, 'hash': hash, 'orphan': orphan, 'reward': breward, 'bsizes': bsizes, 'blocktime': blocktime, 'ntxs': ntxs, 'hashes': hashes, 'hahsizes': hahsizes, 'txsizes': txsizes, 'teta': teta, 'deteta': deteta, 'txes': txes, 'txp': txp, 'txep': txep, 'pingrock': pingrock}


def prettyPrintStats(blockstats):
	msg = "```WE FOUND A NEW BLOCK!\n"
	msg += "\nHeight: {} \n".format(blockstats['height'])
	msg += "Hash: {} \n".format(blockstats['hash'])
	msg += "Orphan: {} \n".format(blockstats['orphan'])
	msg += "Reward: {} \n".format(blockstats['reward'])
	msg += "Size: {} \n".format(blockstats['bsizes'])
	msg += "Time took to make: {} \n".format(blockstats['blocktime'])

	msg += " \nNo. of txs in the block: {} \n".format(blockstats['ntxs'])
	msg += "Tx hashes in the block: {} \n".format(blockstats['hashes'])
	msg += "Size of each tx: {} \n".format(blockstats['hahsizes'])
	msg += "Size of all the txs: {} \n \n".format(blockstats['txsizes'])

	msg += "tx_extra hash: {} \n".format(blockstats['teta'])
	msg += "Decoded version of tx_extra: {} \n".format(blockstats['deteta'])
	msg += "Size of tx_extra: {} \n \n".format(blockstats['txes'])

	msg += "Percentage of txs in the block: {} % \n".format(blockstats['txp'])
	msg += "Percentage of tx_extra in the block: {} % ```".format(blockstats['txep'])

	# msg += blockstats['pingrock']
	print(msg)

	return msg


class client_check(object):
	def __init__(self, client):
		self.client = client

	def __call__(self, func):
		if not self.client:
			print("Cannot connect to Discord without a valid token. bot will attempt to print to console.")
			# Return the function unchanged, not decorated with Discord API.
			return func
		return self.client.event(func)


@client_check(client)
async def on_ready():
	print("connected")
	height = tclbh['block_header']['height']
	while True:
		nheight = tc.get_block_count()['result']['count']
		if height != nheight:
			prettyPrintStats(getstats(nheight))
			if client:
				await client.send_message(discord.Object(id='459931714471460864'), prettyPrintStats(getstats(nheight)))
			print("val changed")
			print(nheight)
			print(height)
			height = nheight
			print(height)
		await asyncio.sleep(0.5)


def start_local_event_loop():
	print("*** Starting local event loop with TurtleCoind ***")
	loop = asyncio.get_event_loop()
	loop.run_until_complete(on_ready())
	loop.close()


if __name__ == '__main__':
	connect_to_turtlecoind()

	if client:
		client.run(token)
	else:
		try:
			start_local_event_loop()
		except KeyboardInterrupt as err:
			print("\nShutdown requested. Exiting...")
			sys.exit(0)
