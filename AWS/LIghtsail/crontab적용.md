# [AWS/Lightsail] crontab 스케쥴러 설치 및 적용

##  설치
```
    sudo yum install -y cronie

    sudo systemctl start crond
    sudo systemctl enable crond
```

## 설정
```
    다른계정에게 권한생성 
    chown -R webmaster:webmaster crontab
```

## 사용법
```
*　　　　　　*　　　　　　*　　　　　　*　　　　　　*
분(0-59)　　시간(0-23)　　일(1-31)　　월(1-12)　　　요일(0-7)


ex)
0 3 * * * /usr/bin/certbot renew --renew-hook="systemctl restart nginx" >> /var/log/sysmate/crontab/ssl_renew_`date +\%Y\%m\%d\%H\%M`.log 2

```






