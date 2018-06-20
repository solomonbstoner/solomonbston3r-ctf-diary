const cryptonight = require('node-cryptonight').hash
var data = new Buffer("00000000000000000000000000000000000000000000000000000000000000000000000000000000000000", "hex");
var hash = cryptonight(data, 1).toString("hex")
console.log(hash)

sol = "b5a7f63abb94d07d1a6445c36c07c7e8327fe61b1647e391b4c7edae5de57a3d"
if (hash == sol) {
    console.log('Correct');
} else {
    console.log('Incorrect');
}
