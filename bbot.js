const TurtleCoind = require('turtlecoin-rpc').TurtleCoind;

var daemon = new TurtleCoind({
  host: 'public.turtlenode.io',
  port: 11898,
});


console.log("A new block was found!!!");

lbh = daemon.getLastBlockHeader();

lbh.then(result => console.log("Height: " + result.height), result => console.log("Could not retrieve the height"));
let hash = lbh.then(result => console.log("Hash: " + result.hash), result => console.log("Could not retrieve the hash"));
hash.daemon.getBlock(hash.hash).then(result => console.log("Transactions: " + result.transactions), result => console.log("Couldnt retrieve the transactions"));
lbh.then(result => console.log("Orphan: " + result.orphan_status), result => console.log("Could not retrieve orphan status"));
lbh.then(result => console.log("Reward: " + result.reward + " TRTL"), result => console.log("Could not retrieve reward"));
console.log("Tx's in the block:")





