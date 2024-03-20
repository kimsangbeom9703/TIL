# [Server/RockyLinux] MySQL 설치 및 설정

### 참고
<https://docs.3rdeyesys.com/database/ncloud-database-mysql-8-latest-version-install-on-rocky-linux.html#mysql-%EB%8D%B0%EB%AA%AC-%EC%8B%9C%EC%9E%91>

##  버전 확인
```
    https://dev.mysql.com/downloads/repo/yum/
```
##  설치
```
    dnf install https://dev.mysql.com/get/mysql80-community-release-el9-5.noarch.rpm
    dnf install mysql-community-server

    systemctl start mysqld
    systemctl status mysqld
```

## 설정
```
    임시비밀번호 확인
        
        cat /var/log/mysqld.log | grep 'temporary password'

    MySQL 보안 설정
        
        mysqld --initialize-insecure --user=mysql

        mysql_secure_installation

        임시비밀번호 입력

        새로운 패스워드 입력

        Remove anonymous users?  y

        Disallow root login remotely? (Press y|Y for Yes, any other key for No) : y
        
        Remove test database and access to it? (Press y|Y for Yes, any other key for No) : y

        Reload privilege tables now? (Press y|Y for Yes, any other key for No) : y

```

## 사용자 생성
```
    CREATE USER 'id'@'%' IDENTIFIED BY '비밀번호';
    flush privileges;
```

## 포트 변경 및 열기
```
    포트 확인 하기
        mysql -u root -p
        show global variables like "PORT";

    포트 변경하기
        1.  systemctl stop mysqld
        2.  vi /etc/my.cnf
                port=13306  추가

        3.  Selinux 보안 정책 조정

            3-1. semanage port -a -t mysqld_port_t -p tcp 13306
            3-2. restorecon -Rv /etc/my.cnf

        4.  systemctl start mysqld        


        5.  sudo firewall-cmd --permanent --add-port=13306/tcp
        
        6.  sudo firewall-cmd --reload

        7.  netstat -ntap | grep LISTEN
                tcp6       0      0 :::13306                :::*                    LISTEN      2092/mysqld
                tcp6       0      0 :::33060                :::*                    LISTEN      2092/mysqld 
        
            포트를 보면 나는 13306을 열었는데 33060이 같이 열려있는 경우를 확인할 수 있다.

            MySQL X Protocol은 표준프로토콜과 병행하여 사용할 수 있고 mysql 서버 간의 통신을 위해 새로운 기능및 프로토콜을 제공한다.

            해당기능을 현재는 사용하지 않으므로 비활성화하자.
        
        8.  vi /etc/my.cnf
                mysqlx=OFF  추가
```

## DB 생성 및 권한 부여
```
    1. mysql -u root -p 

    2. CREATE DATABASE <디비명>

    3. GRANT ALL PRIVILEGES ON <디비명>.* TO '<사용자>'@'%' WITH GRANT OPTION;

    4. flush privileges;
```
