# [NodeJS] express / express-generator 로 생성된 프로젝트 typescript 로 변환하기

## express 설치
```bash
    npm install -g express-generator

    express 프로젝트 --view=ejs
    
    cd 프로젝트

    npm install
```

## typescript 설정
```
    npm install -D @types/cookie-parser @types/cors @types/debug @types/ejs @types/express @types/morgan @types/node nodemon ts-node typescript

    npx tsc --init
```

## tsconfig.json 설정
```json
{
  "compilerOptions": {
    "target": "ES6",                         // TypeScript가 컴파일할 ECMAScript 버전 (이 경우 ES6).
    "module": "commonjs",                    // 컴파일된 코드에서 사용할 모듈 시스템. `commonjs`는 일반적으로 Node.js에서 사용됩니다.
    "strict": true,                          // 모든 엄격한 타입 검사 옵션을 활성화합니다 (예: 암시적인 `any` 사용 방지).
    "esModuleInterop": true,                 // 기본 내보내기(default export)가 없는 모듈에서 기본 임포트를 허용하여 CommonJS 모듈과의 호환성을 높입니다.
    "skipLibCheck": true,                    // 선언 파일(`.d.ts`)의 타입 검사를 생략하여 빌드 성능을 향상시킵니다.
    "forceConsistentCasingInFileNames": true, // 파일 이름의 대소문자가 일관되도록 강제합니다.
    "outDir": "./dist",                      // 컴파일된 JavaScript 파일을 저장할 출력 디렉토리입니다.
    "rootDir": "./src"                       // TypeScript 소스 파일이 위치한 루트 디렉토리입니다.
  },
  "include": ["src/**/*.ts"],                // `src` 디렉토리 및 하위 디렉토리의 모든 `.ts` 파일을 포함합니다.
  "exclude": ["node_modules"]                // `node_modules` 디렉토리는 컴파일에서 제외됩니다.
}
```

## 폴더 구조 변경
```
    my-app/
    ├── src/
    │   ├── bin/
    │   ├── routes/
    │   ├── controllers/
    │   ├── app.ts (혹은 index.ts)
    │   └── ...
    ├── views/
    │   └── index.ejs
    ├── public/
    │   ├── images/
    │   ├── styles/
    │   └── scripts/
    ├── .env
    ├── package.json
    ├── tsconfig.json
    └── ...
```
## js -> ts 변경

### app.ts
```ts
//app.ts
import 'dotenv/config'; // dotenv 설정
import createError from 'http-errors';
import express, {Request, Response, NextFunction} from 'express';
import cors from 'cors';
import path from 'path';
import cookieParser from 'cookie-parser';
import logger from 'morgan';

import indexRouter from './routes/index';
import usersRouter from './routes/users';

const app = express();

// view engine setup
app.set('views', path.join(__dirname, '../views'));
app.set('view engine', 'ejs');

app.use(cors());

// 로깅 레벨 설정
const loggingLevel = process.env.LOGGING_LEVEL || 'dev'; // 기본값은 'dev'
app.use(logger(loggingLevel));

// 미들웨어 설정
app.use(express.json());
app.use(express.urlencoded({extended: false}));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, '../public')));

// 라우터 설정
app.use('/', indexRouter);
app.use('/users', usersRouter);

// 404 처리 미들웨어
app.use(function (req: Request, res: Response, next: NextFunction) {
    next(createError(404));
});

// 에러 처리 미들웨어
app.use(function (err: any, req: Request, res: Response, next: NextFunction) {
    // 로컬 변수 설정 (개발 환경에서만 상세 에러 제공)
    res.locals.message = err.message;
    res.locals.error = req.app.get('env') === 'development' ? err : {};

    // 에러 페이지 렌더링
    res.status(err.status || 500);
    res.render('error');
});

export default app;
```

### /bin/www
```ts
#!/usr/bin/env node

import dotenv from 'dotenv';
import createError from 'http-errors';
import debug from 'debug';
import http from 'http';
import app from '../app';

const env: string = process.env.NODE_ENV || 'development';
dotenv.config({ path: `./.env.${env}` });
console.log(`Running in ${env} mode`);

// 포트 설정
const port = normalizePort(process.env.PORT || '3000');
app.set('port', port);

// HTTP 서버 생성
const server = http.createServer(app);

// 서버 실행
server.listen(port);
server.on('error', onError);
server.on('listening', onListening);

// 포트를 정상화하는 함수
function normalizePort(val: string): number | string | boolean {
  const port = parseInt(val, 10);

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

// HTTP 서버 에러 처리
function onError(error: any): void {
  if (error.syscall !== 'listen') {
    throw error;
  }

  const bind = typeof port === 'string'
      ? `Pipe ${port}`
      : `Port ${port}`;

  // 특정 listen 에러 처리
  switch (error.code) {
    case 'EACCES':
      console.error(`${bind} requires elevated privileges`);
      process.exit(1);
      break;
    case 'EADDRINUSE':
      console.error(`${bind} is already in use`);
      process.exit(1);
      break;
    default:
      throw error;
  }
}

// HTTP 서버가 리스닝 중일 때
function onListening() {
  const addr = server.address();
  if (addr) {
    const bind = typeof addr === 'string' ? 'pipe ' + addr : 'port ' + addr.port;
    debug('Listening on ' + bind);
  }
}

```

### /routes/index
```ts
import express, { Request, Response, NextFunction } from 'express';
const router = express.Router();

/* GET home page. */
router.get('/', (req: Request, res: Response, next: NextFunction) => {
  res.render('index', { title: 'Express' });
});

export default router;


```
