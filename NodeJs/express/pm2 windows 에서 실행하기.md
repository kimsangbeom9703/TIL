# [NodeJS] pm2 윈도우즈 부팅시 자동실행(윈도우 서비스 사용)

## 환경변수 설정
```
환경변수 -> 시스템 변수 -> 새로만들기
PM2_HOME = c:\etc\.pm2
```
## PM2 설치
```bash
    npm i -g pm2 pm2-windows-service npm-check-updates pm2-windows-startup
    pm2-startup install 
    pm2-service-install
    Y
```

## PM2 저장

```bash
    pm2 start ./bin/www
    pm2 save
    pm2 resurrect
    pm2 ls
```

