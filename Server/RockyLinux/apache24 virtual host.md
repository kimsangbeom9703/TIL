# [Server/RockyLinux] virtual host 설정하기

##  세팅이유
```
    개발을 하다보면 하나의 서버에서 여러 서비스를 돌려야 되는 상황이 발생한다.
    그 경우 포트 또는 도메인을 연결해서 서비스를 매칭시킬 수 있다.

    지금은 도메인은 세팅이 안되어있으니 포트로 나누는걸 해보자
```

## 설정 방법
```
    1. cd /etc/httpd/

    2. mkdir conf.vhosts

    3. cd conf.vhosts
    
    4. mkdir 서비스명

    5. vi 서비스명.cnf

        <VirtualHost *:8080>
                ServerName 127.0.0.1
                ServerAlias 10.20.40.58
                DocumentRoot /home/webmaster/서비스폴더
                #DocumentRoot /var/www/html/test
                DirectoryIndex index.php index.htm index.html

                ErrorLog "logs/Service/서비스폴더/ervice.error.log"
                CustomLog "logs/Service/서비스폴더/service.access.log" common
        </VirtualHost>
    
    6. /etc/httpd/conf/httpd.conf 수정

    최하단에
    IncludeOptional conf.vhosts/*/*.conf 추가

    상단에
    Listen 8080
    추가

    7. systemctl restart httpd

    8. firewall-cmd --list-all

    9. firewall-cmd --permanent --zone=public --add-port=8080/tcp

    10. firewall-cmd --reload

    11. chmod +x /home/webmaster // 안해도될듯?

    12.  chcon -R -t httpd_sys_content_t /home

```