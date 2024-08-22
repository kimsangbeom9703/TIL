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
    service nginx stop
```
http://daedeok-school.svr.kr/
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

### 발급된 인증서 목록 조회
```
    $   certbot certificates
```

### ssl 인증서 재갱신
```
    crontab -e 등록
   
    0 3 * * * /usr/bin/certbot renew --renew-hook="systemctl restart nginx" >> /var/log/sysmate/crontab/ssl_renew_`date +\%Y\%m\%d\%H\%M`.log 2>&1

```

### 2024-01-04 인증서 재갱신
```
    위에 인증서 갱신 방법을 쓰면 .. nginx가 80포트를 사용하고 있기 때문에 오류가 발생한다.
    certbot 은 80 포트를 이용하여 검증용 웹 서버를 띄워 발급하기 때문이다.
```
### 오류내용
```
    Saving debug log to /var/log/letsencrypt/letsencrypt.log

    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    Processing /etc/letsencrypt/renewal/https.test.net.conf
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    Renewing an existing certificate for https.test.net
    Failed to renew certificate https.test.net with error: Could not bind TCP port 80 because it is already in use by another process on this system (such as a web server). Please stop the program in question and then try again.

    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    All renewals failed. The following certificates could not be renewed:
    /etc/letsencrypt/live/https.test.net/fullchain.pem (failure)
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    1 renew failure(s), 0 parse failure(s)
    Ask for help or search for solutions at https://community.letsencrypt.org. See the logfile /var/log/letsencrypt/letsencrypt.log or re-run Certbot with -v for more details.
```

### 해결방안
```
    mkdir ssl-renew
    cd ssl-renew
    vi ssl-renew.sh
```
### ssl-renew.sh
```sh
    #!/bin/sh
    # weather.sysmate.net ssl renew
    #
    #
    systemctl stop nginx

    /usr/bin/certbot renew --renew-hook="systemctl restart nginx" >> /var/log/sysmate/crontab/ssl_renew_`date +\%Y\%m\%d\%H\%M`.log 2>&1

    systemctl start nginx
```

### crontab 수정
```
    crontab -e 등록
    
    0 3 * * * /data/ssl-renew/ssl-renew.sh

    # crond 재실행
    systemctl restart crond
```