# [AWS/Lightsail] 아마존리눅스 2023 MariaDB 설치하기

## 설치
```
dnf install mariadb105-server

mysql --version

sudo systemctl start mariadb
sudo systemctl enable mariadb
sudo systemctl status mariadb

```

## 설정
```
sudo mysql_secure_installation

Switch to unix_socket authentication [Y/n]
    - n
    → 유닉스 소켓이라는 인증 방식으로 전환할 것인지 물어보는 질문이다. 자세한 건 링크 참고. https://www.nemonein.xyz/2019/07/2254/
Change the root password? [Y/n]
    - y
    →root password를 변경할 건지 물어보는 질문.
Remove anonymous users? [Y/n]
    - y
    → 익명 사용자를 제거할 건지 물어보는 질문. 만약 Y를 하면 mysql -u root 로 로그인 해야 된다.(-u)
    n를 하면 ‘mysql’로도 로그인 된다. 익명 사용자가 권한을 갖는 것이기 때문에 보안상 지워주는 게 좋다.
Disallow root login remotely [Y]
    - n
    → localhost의 ip가 아닌 곳에서 root로 로그인이 가능하게 할 지 물어본다. Y를 하면 원격 로그인이 안 된다. 공부 용도이며 장소를 옮긴다 하면 n를 권장. 로컬에서만 사용하면 y
Remove test database and access to it? [Y/n]
    - y
    → test 데이터베이스를 제거할지 물어본다. 쓸 일이 없으면 n
Reload privilege tables now? [Y/n]
    - y
    → 권한을 변경을 했다면 y
```
