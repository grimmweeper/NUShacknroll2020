require('babel-register')({
    presets: ['env']
});

module.exports = require('./test.mjs/index.js')