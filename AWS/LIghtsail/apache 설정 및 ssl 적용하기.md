# [AWS/Lightsail] 아파치 설정 및 SSL 적용하기 (Apache)

##  아파치 설정 및 SSL 적용하기

```txt
    현재 적용한 서버는 EC2 = Amazon Linux 2 AMI 이다
```

## 아파치 설치
```bash
    yum install httpd
    systemctl enable httpd
    systemctl start httpd
```

## 아파치 설치 경로
```
    cd /etc/httpd/
```

## 기본 설정
```
    설정파일 : cd/etc/httpd/conf/httpd.conf
```

## 추가 
```
    mkdir conf.vhosts

    vi /etc/httpd/conf/httpd.conf

    IncludeOptional conf.d/*.conf
    IncludeOptional conf.vhosts/*/*.conf
    
    하단에 추가
```

## 버츄얼호스트 등록
```
    cd /etc/httpd/conf.vhosts

    mkdir 서비스명

    vi 서비스명.conf


    <VirtualHost *:80>
        ServerName 도메인
        #ServerAdmin root@localhost

        DocumentRoot /home/webmaster/서비스명/public
        DirectoryIndex index.php index.htm index.html

        ErrorLog "logs/서비스명_error.log"
        CustomLog "logs/서비스명_access.log" combined

        <Directory /home/webmaster/서비스명/public>
            Options Indexes FollowSymLinks MultiViews
            AllowOverride All
            Require all granted
            RewriteEngine On
            RewriteBase /
            RewriteRule ^index\.html$ - [L]
            RewriteCond %{REQUEST_FILENAME} !-f
            RewriteCond %{REQUEST_FILENAME} !-d
            RewriteRule . /index.html [L]
        </Directory>

    #RewriteCond %{SERVER_NAME} =도메인 
    #RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
    </VirtualHost>

```
## ssl 설치
```
    systemctl is-enabled httpd
    systemctl start httpd && sudo systemctl enable httpd
    yum update -y
    yum install -y mod_ssl

    yum install -y certbot python2-certbot-apache

    sudo certbot --apache

                => mod_ssl 설치 전 실행시 오류 발생

                Saving debug log to /var/log/letsencrypt/letsencrypt.log
                Could not find ssl_module; not disabling session tickets.
                Enter email address (used for urgent renewal and security notices)
                 (Enter 'c' to cancel): 이메일 입력

                - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                Please read the Terms of Service at
                https://letsencrypt.org/documents/LE-SA-v1.2-November-15-2017.pdf. You must
                agree in order to register with the ACME server. Do you agree?
                - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                (Y)es/(N)o: y

                - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                Would you be willing, once your first certificate is successfully issued, to
                share your email address with the Electronic Frontier Foundation, a founding
                partner of the Let's Encrypt project and the non-profit organization that
                develops Certbot? We'd like to send you email about our work encrypting the web,
                EFF news, campaigns, and ways to support digital freedom.
                - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                (Y)es/(N)o: n
                Account registered.

                Which names would you like to activate HTTPS for?
                - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                1: 버츄얼 등록한 도메인
                - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                Select the appropriate numbers separated by commas and/or spaces, or leave input
                blank to select all options shown (Enter 'c' to cancel):
                Requesting a certificate for 버츄얼 등록한 도메인

                Successfully received certificate.
                Certificate is saved at: /etc/letsencrypt/live/버츄얼 등록한 도메인/fullchain.pem
                Key is saved at:         /etc/letsencrypt/live/버츄얼 등록한 도메인/privkey.pem
                This certificate expires on 2022-10-04.
                These files will be updated when the certificate renews.
                Certbot has set up a scheduled task to automatically renew this certificate in the background.

                Deploying certificate
                Could not install certificate

                NEXT STEPS:

                - The certificate was saved, but could not be installed (installer: apache). After fixing the error shown below, try installing it again by running:

                    certbot install --cert-name 버츄얼 등록한 도메인

                Could not find ssl_module; not installing certificate.
                Ask for help or search for solutions at https://community.letsencrypt.org. See the logfile /var/log/letsencrypt/letsencrypt.log or re-run Certbot with -v for more details.

                => mod_ssl 설치 후 후속 명령 다시 실행

                $ sudo certbot install --cert-name 버츄얼 등록한 도메인

                Saving debug log to /var/log/letsencrypt/letsencrypt.log
                Deploying certificate
                Successfully deployed certificate for 버츄얼 등록한 도메인 to /etc/httpd/conf.vhosts/서비스명-le-ssl.conf

            
    인증서 갱신
        테스트
            -   certbot renew --dry-run
        만료일 확인
            -   certbot certificates
            
            0 3 * * * /usr/bin/certbot renew --renew-hook="systemctl restart httpd" >> /var/log/서비스/crontab/ssl_renew`date +\%Y\%m\%d\%H\%M`.log 2>&1

```