const fs = require('fs');
fs.readFile('input.txt', function read(err, data) {
    if (err) {
        throw err;
    }
    console.log(data.toString());
});