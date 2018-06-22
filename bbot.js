const TurtleCoind = require('turtlecoin-rpc').TurtleCoind;

var daemon = new TurtleCoind({
  host: 'public.turtlenode.io',
  port: 11898,
});


console.log("A new block was found!!!");

lbh = daemon.getLastBlockHeader();

lbh.then(result => console.log("Height: " + result.height), result => console.log("Could not retrieve the height"));
lbh.then(result => console.log("Hash: " + result.hash), result => console.log("Could not retrieve the hash"));
lbh.then(result => console.log("Orphan: " + result.orphan_status), result => console.log("Could not retrieve orphan status"));
lbh.then(result => console.log("Reward: " + result.reward + " TRTL"), result => console.log("Could not retrieve reward"));
console.log("Tx's in the block: 1 trillion	");

var result1
var result2

lbh.then(function (result) {
  console.log("Height: " + result.height)
  return daemon.getBlock({
  	hash: result.hash
  }) 
}).then(function (result2) {  
  console.log(result2.transactions[2].hash)
  return daemon.getTransaction({
  	hash: result2.transactions[2].hash
  })
}).then(function (result3) {
  console.log(result3.tx[0].extra)
}).catch(console.log('idk man'))

/*lbh.then(someFunc, console.log("Could not retrieve the hash"));

someFunc(result) {
  daemon.getBlock(result.hash).t hen(result => console.log("txs: "result.transactions), result => console.log("coudnt get the txs"));
}*/

var result1
var result2

someFunc().then(function (res) {
  result1 = res
  return someOtherFunc(result1.blah)
}).then(function (res) {
  result2 = res
  return someOtherSajoNeedsToRead(result1.blah, result2.blah)
}).then(function (res) {
  console.log('Go read a book' + result1.blah + result2.blah + res.blah)
}).catch(function (err) {
  console.log('errrrrrr ' + err)
})






