# [NodeJS] pm2 사용하기

## PM2 설치
```

npm i -g pm2 pm2-windows-service npm-check-updates pm2-windows-startup

pm2-service-install
Y

pm2-startup install 

```

## PM2 사용

```
    pm2 ecosystem
```

### 기본파일
```js
    module.exports = {
    apps : [{
        script: 'index.js',
        watch: '.'
    }, {
        script: './service-worker/',
        watch: ['./service-worker']
    }],

    deploy : {
        production : {
        user : 'SSH_USERNAME',
        host : 'SSH_HOSTMACHINE',
        ref  : 'origin/master',
        repo : 'GIT_REPOSITORY',
        path : 'DESTINATION_PATH',
        'pre-deploy-local': '',
        'post-deploy' : 'npm install && pm2 reload ecosystem.config.js --env production',
        'pre-setup': ''
        }
    }
    };  
```
### 사용파일
```js
module.exports = {
  apps : [{
    name: 'dev',
    script: './bin/www',
    instances: 1,
    autorestart: true,
    watch: true,
    env: {
      PORT:4000,//Express PORT
      NODE_ENV: 'development',
      MariaDB_HOST: "localhost",
      MariaDB_PORT:3306,
      MariaDB_USER:"root",
      MariaDB_PASSWORD:"",
      MariaDB_NAME:"DB-Name",
      Redis_HOST: "localhost",
      Redis_PORT: 6379
    },
  },
  {
    name: 'service',
    script: './bin/www',
    instances: -1, // 클러스터 모드
    autorestart: true,
    watch: false,
    env: {
      PORT: 3000,
      NODE_ENV: 'production',
      MariaDB_HOST: "localhost",
      MariaDB_PORT:3306,
      MariaDB_USER:"root",
      MariaDB_PASSWORD:"",
      MariaDB_NAME:"DB-Name",
      Redis_HOST: "localhost",
      Redis_PORT: 6379
    },
  }]
};
```

## package.json
```json
  "scripts": {
    "dev": "pm2 start ecosystem.config.js --only dev --env development",
    "start": "pm2 start ecosystem.config.js --only service --env production",
    "del": "pm2 del all"
  },
  
    --only 옵션은 ecosystem.config.js 파일에서 name 값이 dev인 항목에 설정들을 실행시키주는 옵션입니다.  
    --env 옵션은 실행되는 항목에 env 설정들을 실행시켜주는 옵션입니다.
```

## 명령어
```bash
    시작
    pm2 start ecosystem.config.js
    재시작
    pm2 restart ecosystem.config.js
    삭제
    pm2 delete id
    전체삭제
    pm2 kill 
    중지
    pm2 stop id


    pm2 save
    pm2 resurrect    
```