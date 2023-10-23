# [AWS/Lightsail] Nginx 설치 및 php연동

##  Nginx 설치
```
    설치 될 nginx 확인
        yum info nginx
    설치
        yum install nginx
    재부팅시 자동 활성화
        systemctl enable nginx
    상태 확인
        systemctl start nginx
```

## Nginx 설정

```
    설정 위치

    cd /etc/nginx

    nginx 를 수정하려면 /etc/nginx/nginx.conf 기본파일을 수정하면 되지만
    나는 virtual host를 적용하여 하나의 서버에 여러 프로젝트를 관리하려고 한다.

    nginx.conf파일을 보면

    include /etc/nginx/conf.d/*.conf;
        
    중간에 저런 내용이 있을텐데 밑에 
    
    include /etc/nginx/conf.d/*/*.conf;

    를 추가한다. 이유는 폴더로 관리할 것이다.

```

##


## php 연동

### Apache 연동 (Windows) 
```
    <VirtualHost *:48147>
        DocumentRoot "test\public"
        ServerName 127.0.0.1
        ServerAlias 118.130.196.46
        ErrorLog "logs/Work/test.error.log"
        CustomLog "logs/Work/test.access.log" common
        
        Alias /uploads "test\writable\uploads"

        <Directory "test\writable\uploads">
            Options Indexes FollowSymLinks
            AllowOverride All
            Require all granted
        </Directory>
    </VirtualHost>
```

### Nginx 연동 
```
    /home/webmaster/test 를 생성

    chmod -R 755 /home/webmaster/test

    server {
        listen       48001;
        server_name  127.0.0.1;
        root         /home/webmaster/test;

        access_log /var/log/nginx/test.access;
        error_log /var/log/nginx/test.error error;

        location / {
            root /home/webmaster/test;
            index index.php index.html;
        }
    
        #root /path/to/test/public;

        #location /uploads {
        #   alias /path/to/test/writable/uploads;
        #}

        location ~ \.php$ {
              fastcgi_pass   unix:/run/php-fpm/www.sock;
              fastcgi_index  index.php;
              fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
              include        fastcgi_params;
        }
    }


```