# [FastApi] Nginx + Gunicorn 연동

## 참고
<https://wikidocs.net/177269>

## Gunicorn 이란
```
    uvicorn 를 백그라운드에서 실행 가능하게 한다
    nodejs 의 forever 라고 생각하면 된다.
```

## Gunicorn 설치
```
    pip install gunicorn
```

## 확인
```
    gunicorn --bind 0:8000 main:app --worker-class uvicorn.workers.UvicornWorker
```

## 서비스 파일 생성
```
/etc/systemd/system/gunicorn.service 파일 생성

[Unit]
Description=Gunicorn daemon for FastAPI app
After=network.target

[Service]
User=nginx
Group=nginx
WorkingDirectory=/home/webmaster/api_weather/app
ExecStart=/home/webmaster/api_weather/venv/bin/gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target

```

## 서비스 등록 및 시작 & 확인
```
    sudo systemctl enable gunicorn.service  # 서비스 등록
    sudo systemctl start gunicorn.service   # 서비스 시작
    sudo systemctl status gunicorn # 서비스 확인
```

## Nginx 설정
```
server {
        listen 80;
        server_name {서버IP주소 또는 도메인 주소};
        
        location /similarity {
                proxy_pass http://localhost:8000;
                proxy_redirect off;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
}
```

## 소스 수정 후 적용
```
    소스 수정 후 재시작 하지 않으면 적용되지않는다.
    systemctl restart gunicorn
```