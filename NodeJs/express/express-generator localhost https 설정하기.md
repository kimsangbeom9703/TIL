# [NodeJS] express / express-generator 로 만든 프로젝트 localhost https 적용하기

## 참고

<https://charming-kyu.tistory.com/46>

## express 설치
```bash
    npm install -g express-generator

    express 프로젝트 --view=ejs
    
    cd 프로젝트

    npm install
```

## mkcert 설치
```bash
    npm install -g mkcert
    
    mkdir config

    mkcert create-ca

    mkcert create-cert
```

## 필요 모듈 설치
```bash
    npm install --save https fs
```

## ./bin/www 수정
```js
#!/usr/bin/env node

/**
 * Module dependencies.
 */

var app = require('../app');
var debug = require('debug')('localhosthttps:server');
var http = require('http');
var https = require('https');
var fs = require('fs');

/**
 * Get port from environment and store in Express.
 */

var port = normalizePort(process.env.PORT || '3000');
app.set('port', port);

/**
 * Create HTTP server.
 */

var server = http.createServer(app);

/**
 * Create HTTPS server with SSL certificates.
 */

var httpsOptions = {
    key: fs.readFileSync("./config/cert.key"),
    cert: fs.readFileSync("./config/cert.crt"),
};

var httpsServer = https.createServer(httpsOptions, app);

/**
 * Listen on provided ports, on all network interfaces.
 */

server.listen(port);
server.on('error', onError);
server.on('listening', onListening);

httpsServer.listen(443); // HTTPS default port
httpsServer.on('error', onError);
httpsServer.on('listening', onListening);

/**
 * Normalize a port into a number, string, or false.
 */

function normalizePort(val) {
    var port = parseInt(val, 10);

    if (isNaN(port)) {
        // named pipe
        return val;
    }

    if (port >= 0) {
        // port number
        return port;
    }

    return false;
}

/**
 * Event listener for server "error" event.
 */

function onError(error) {
    if (error.syscall !== 'listen') {
        throw error;
    }

    var bind = typeof port === 'string' ? 'Pipe ' + port : 'Port ' + port;

    // handle specific listen errors with friendly messages
    switch (error.code) {
        case 'EACCES':
            console.error(bind + ' requires elevated privileges');
            process.exit(1);
            break;
        case 'EADDRINUSE':
            console.error(bind + ' is already in use');
            process.exit(1);
            break;
        default:
            throw error;
    }
}

/**
 * Event listener for server "listening" event.
 */

function onListening() {
    var addr = server.address();
    var bind = typeof addr === 'string' ? 'pipe ' + addr : 'port ' + addr.port;
    debug('HTTP Listening on ' + bind);

    var httpsAddr = httpsServer.address();
    var httpsBind = typeof httpsAddr === 'string' ? 'pipe ' + httpsAddr : 'port ' + httpsAddr.port;
    debug('HTTPS Listening on ' + httpsBind);
}


```

## 확인
```bash
    npm run start
```