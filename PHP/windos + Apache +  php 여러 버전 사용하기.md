# [php] windows 환경에서 php 여러 버전 사용하기 (Apache24)

```
    현재 내 pc의 php는 7.3 , 8.2를 사용중이였다.
    근데 최신꺼는 8로 개발이 되어있어 나중에 로컬서버로 다운을 받아 개발을 진행하면 apache 설정에서 바꿔주고 또 7점대 수정이 필요하면
    다시 바꿔주는 식으로 개발을 했는데 이건 너무 비효율적이라고 생각해 내가 찾은 방법을 공유하겠습니다.
```

# php 설치

```
    http://windows.php.net/download/
    버전에 맞는 php 를 Thread Safe로 설치한다.
```

## 설정
```
    내 폴더 구조는 C:/apm/ 하위에 Apache24 , php , mysql 이 설치되어있다.
```

### apache 설정 파일 복사 및 변경
```
    C:\apm\Apache24\conf 안에 있는 httpd.conf 파일을 다른 이름으로 저장한다 
    ex) httpd.conf -> httpd-php8.2.conf
```

### 파일 수정 (httpd-php8.2.conf)
```
httpd.conf

    # --php 7.3
    LoadModule php7_module "C:\apm\php/php7apache2_4.dll"
    AddHandler application/x-httpd-php .php
    PHPIniDir "C:/apm/php/"
    # --php 8.2.11
    # LoadModule php_module "C:\apm\php8.2.11\php8apache2_4.dll"
    # AddHandler application/x-httpd-php .php
    # PHPIniDir "C:/apm/php8.2.11/"            

    원래는 이렇게 주석을 제거하고 하는 방식으로 사용..

httpd-php8.2.conf

    # --php 8.2.11
    LoadModule php_module "C:\apm\php8.2.11\php8apache2_4.dll"
    AddHandler application/x-httpd-php .php
    PHPIniDir "C:/apm/php8.2.11/"

### 주의!
```
    httpd.conf , httpd-php8.2.conf 의 포트는 겹치지 않도록 다른 파일에서 관리하자.
    ex) httpd.conf
            Listen 80
            Listen 48000        
    ex) httpd-php8.2.conf
            Listen 48001
            Listen 48002
            Listen 48003        

    #Include conf/extra/httpd-vhosts.conf
    Include conf/extra/httpd-php8-vhosts.conf
    
    conf별로 vhost 도 관리해주면 좋다!
```

### 설치
```
    httpd -k install -n "ApachePHP8" -f "c:\apm\apache24\conf\httpd-php8-vhosts.conf"
```
### 실행 / 재시작 / 중지
```
    httpd -k start -n "ApachePHP8" 
    httpd -k restart -n "ApachePHP8" 
    httpd -k stop -n "ApachePHP8" 
```