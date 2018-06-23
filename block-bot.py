import discord
import asyncio
import logging
import turtlecoin
import json
import requests

#discord stuff
token = open('tokenfile').read()
client = discord.Client()

#logging/debugging stuff. exxtra noise in console which i dont like
"""logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)"""

#discord stuff
@client.event
async def on_ready():
	print("connected")

"""def prettyPrintDict(dict):
	try:
		print (json.dumps(dict, indent=4, sort_keys=True))
	except Exception as e:
		print('{}, Error: {}'.format('Failed to decode dict as json', e))"""

tc = turtlecoin.TurtleCoind(host='public.turtlenode.io', port=11898)

tcgl = tc.getlastblockheader()['block_header']

#height of the latest block, int
height = tcgl['height']
#print("Height:", height)

#hash of the latest block. str
hash = tcgl['hash']
#print("Hash:", hash)

#if latest block is orphan or not. bool(str) 
orphan = tcgl['orphan_status']
#print("Orphan:", orphan)

#reward of the latest block. int
reward = tcgl['reward']
#print("Block reward:", reward / 100, "TRTL")

time = tcgl['timestamp']
prevhash = tcgl['prev_hash']
time2 = tc.getlastblockheaderbyhash(prevhash)['block_header']['timestamp']

timed = time - time2
rock = "235707623985512451"
blocktime = "Time took to make:"

if timed <= 10:
	blocktime += "Block was too fast, {timed} seconds <@{rock}>".format(timed=timed, rock=rock)
elif timed >= 90:
	blocktime += "Took too long, {timed} seconds. <@{rock}>".format(timed=time, rock=rock)
else:
	blocktime += "Took {timed} seconds to make, pretty nice".format(timed=timed)


#times = "Block was too fast, {timed} seconds <@{rock}>".format(timed=timed, rock=rock) if timed <= 10 else "Took too long, {timed} seconds. <@{rock}>".format(timed=time, rock=rock) if timed >= 90 else "Took {timed} seconds to make, pretty nice".format(timed=timed)


bsize = tc.getblock(hash)
bsizes = bsize['block']['blockSize']
#print("Size of block:", bsizes, "a.u.")

#transaction hashes. str
txs = tc.getblock(hash)
ntxs = len(txs['block']['transactions'])

#print("No. of txs in the block:", ntxs) 
#print("Tx hashes in the block:")

"""for transaction in txs['block']['transactions']:
	print(transaction['hash'])"""

hashes = [x['hash'] for x in txs['block']['transactions']]
#prettyPrintDict(hashes)

#print("Size of each tx:")

hahsizes = [z['size'] for z in txs['block']['transactions']]
#prettyPrintDict(hahsizes)

#print("Total size of the transactions:")
txsize = txs['block']
txsizes = txsize['transactionsCumulativeSize']
#print(txsizes, "a.u.")


for hash in hashes:
	teta = tc.gettransaction(hash)['tx']['extra']
#	print("tx_extra hash:")
#	prettyPrintDict(teta)
#	print("Decoded version of tx_extra:")	
	data = '{"jsonrpc":"2.0","id":"test","method":"f_transaction_json","params":{"hash":teta}}'
	response = requests.post('https://blocks.turtle.link/daemon/json_rpc', data=data)
#	print(response)

	# idk how to hex decode mman 
	# hex decode the tx extras some how
	

txes =  bsizes-txsizes
#print("\nSize of tx_extra:", txes, "a.u.")


txp = txsizes/bsizes * 100
txep = txes/bsizes * 100

#print("Percentage of transactions in the block:", txp, "%")
#print("Percentage of tx_extra in the block:", txep, "%")

printstats = """We just found a block!

Height: {height}
Hash: {hash}
Orphan: {orphan}
Reward: {reward}
Block size: {bsizes}
Made on time: {times}

No. of txs in the block: {ntxs}
Tx hashes in the block: {hashes}
Size of each tx: {hashsizes}
Size of all the txs: {txsizes}

tx_extra hash: {teta}
Decoded version of tx_extra: {response} (this is borken i need help)
Size of tx_extra: {txes} au

Percentage of txs in the block: {txp} %
Percentage of tx_extra in the block: {txep} %

""".format(height=height, hash=hash, orphan=orphan, reward=reward, bsizes=bsizes, ntxs=ntxs, hashes=hashes, hashsizes=hahsizes, times=times, teta=teta, response=response, txes=txes, txp=txp, txep=txep, txsizes=txsizes)

print(printstats)

@client.event
async def on_message(message):
	#if Channel.id != 459931714471460864:
	#	return
	if message.content == "hi":
		await client.send_message(message.channel, printstats)
	else:
		print("nope")



client.run(token)