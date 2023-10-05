# [AWS/Lightsail] 아마존리눅스2023 SSL 적용하기 (Nginx)

##  아마존리눅스2023 SSL 적용하기 (Nginx)

```
    아마존 리눅스에서 ssl 을 적용하려니 쉽지않다..
    패키지를 지원하지 않는 경우도 많다.
    epel-release 가 amazon linux 2023 에는 설치가 안된다.
    파이썬 가상환경을 사용하여 진행해보자.
```

## certbot 설치
```
    sudo dnf install -y python3 augeas-libs pip

    sudo python3 -m venv /opt/certbot/

    sudo /opt/certbot/bin/pip install --upgrade pip

    sudo /opt/certbot/bin/pip install certbot

    sudo ln -s /opt/certbot/bin/certbot /usr/bin/certbot

```
## Nginx 중지
```
    service stop nginx
```

## 인증서 생성
```
    certbot certonly --standalone

    EMAIL 입력

    Y

    N

    인증받을 도메인 입력.
```

## SSL 인증서 적용
```
    /etc/nginx/conf.d/ssl.conf 생성

    server {
        listen 443;
        server_name 도메인;

        location = /favicon.ico { access_log off; log_not_found off; }

        ssl on;
        ssl_certificate      /etc/letsencrypt/live/도메인/fullchain.pem;
        ssl_certificate_key  /etc/letsencrypt/live/도메인/privkey.pem;
        ssl_prefer_server_ciphers on;

        location / {
            proxy_pass         http://127.0.0.1:8000;
            proxy_redirect     off;
            proxy_set_header   Host $host;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        }
}


```

