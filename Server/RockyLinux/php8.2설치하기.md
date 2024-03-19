# [Server/RockyLinux] php8.2 설치하기

# 이유
```
    기본으로 php를 설치하려고 하니 8.0.30 버전을 지원한다.
    그래서 저장소를 설치한 후 버전을 8.2로 올려보자!!
    패키지 관리로는 dnf 를 사용할거고 저장소는 remi를 사용할 예정이다.
```

## 설치 방법
```
    1.  dnf install epel-release

    2.  dnf install http://rpms.remirepo.net/enterprise/remi-release-9.rpm

    3.  dnf install dnf-utils

    4.  dnf module reset php

    5.  dnf module install php:remi-8.2

    6.  dnf update

    7.  dnf install php php-mysqli php-intl php-curl php-ftp php-fileinfo php-mbstring php-openssl php-pdo_mysql

    8.  php -v

    9.  systemctl start php-fpm

    10. systemctl enable php-fpm

    11. systemctl status php-fpm

```