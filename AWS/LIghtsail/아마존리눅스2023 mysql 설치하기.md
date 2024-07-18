# [AWS/Lightsail] 아마존리눅스 2023 MySQL 설치하기

## 기존방식
```
$ wget dev.mysql.com/get/mysql80-commuity-release-e17-5.noarch.rpm

$ rpm -ivh mysql-community-release-e17.5.noarch.rpm
```

## 변경방식
```
$ sudo dnf install https://dev.mysql.com/get/mysql80-community-release-el9-1.noarch.rpm

$ sudo dnf install mysql-community-server
```