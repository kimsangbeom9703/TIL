# [ETC] [mkcert] localhost https 적용하기

## 참고
<https://mungkhs1.tistory.com/64>
<https://github.com/FiloSottile/mkcert/releases> <br/>

##  적용이유 

```
    요즘 브라우저에서 http인 경우 차단하는 경우가 많다.
    로컬도 https를 적용해보자.
```

## 설치 주소 : <https://github.com/FiloSottile/mkcert/releases>

```
    Releases => 최신 Releases의 mkcert-v1.x.x-windows-amd64.exe 다운로드

    예) mkcert-v1.4.4-windows-amd64.exe
```

## 설치방법

```bash
    코딩 작업 중인 프로젝트 폴더에 cert 폴더 생성
    mkcert-v1.4.4-windows-amd64.exe -> mkcert.exe // rename
    
    cd cert
    ./mkcert -install

    ./mkcert -key-file localhost-key.pem -cert-file localhost-cert.pem localhost 127.0.0.1 ::1
```

## nodeJS (express) 적용방법
```bash
    npm install https fs
```
```js
#!/usr/bin/env node

/**
 * Module dependencies.
 */

var app = require('../app');
var debug = require('debug')('test:server');
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
  key: fs.readFileSync("./cert/localhost-key.pem",'utf-8'),
  cert: fs.readFileSync("./cert/localhost-cert.pem",'utf-8'),
};


var httpsServer = https.createServer(httpsOptions, app);

/**
 * Listen on provided port, on all network interfaces.
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

## 문제점
```
vmware 에서 테스트를 진행하였는데
HTTPS 적용 테스트를 진행한 결과, 해당 서버 장비에서는 로컬 인증서 설치 시 정상적으로 HTTPS 접속이 가능한 것으로 확인되었습니다.  
다만, 다른 PC에서 서버 ip 접속 시 “주의 요함”이라는 브라우저 보안 경고 메시지가 표시되는 현상이 발생하였습니다.
이는 사용된 인증서가 현재 장비에서만 신뢰되도록 설정되어 있고,  
타 PC에서는 해당 인증서를 신뢰하지 않기 때문에 발생하는 문제로 판단됩니다.  
```
