# [AWS/Lightsail] MySQL 설치 및 설정

##  설치
```
    sudo dnf install https://dev.mysql.com/get/mysql80-community-release-el9-1.noarch.rpm
    sudo dnf install mysql-community-server

    systemctl start mysqld
    systemctl status mysqld
```

## 설정
```
-   계정정보 변경
    -   임시비밀번호 확인
        -   cat /var/log/mysqld.log | grep 'temporary password'
    -   mysql -u root -p 
    -   비밀번호 변경
        -   alter user 'root'@'localhost' identified with mysql_native_password by '비밀번호';
    -   계정 생성 (내부접속가능)
        -   CREATE USER 'test_manager'@'localhost' IDENTIFIED BY '비밀번호';
    -   계정 생성 (외부접속가능)
        -   CREATE USER 'test_manager'@'%' IDENTIFIED BY '비밀번호';
-   Databases 생성  
    -   CREATE DATABASE db_test_svr_real
    -   권한 부여
        -   create user 'test'@'%' identified by '비밀번호';
        -   GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
        -   GRANT ALL PRIVILEGES ON db_test_svr_real.* TO 'test_manager'@'%' WITH GRANT OPTION;
    -   flush privileges;

-   라이트세일 홈페이지
    -   3306 port 추가 
```



