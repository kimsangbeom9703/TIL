# [PHP] php 8.2.11 버전 설치하기.

## 설치 
<http://windows.php.net/download/>
```
    버전에 맞는 Thread Safe 파일 다운로드
    압축해제는 C:\apm or C:\
```

## 설정
```
    php.ini-development -> php.ini 
    extension_dir = 설치경로\ext        //  ex) C:\php-8.2.11\ext

```

## extension 설정
```
나는 보통

extension=curl
;extension=ffi
extension=ftp
extension=fileinfo
;extension=gd
;extension=gettext
;extension=gmp
extension=intl
;extension=imap
extension=mbstring
;extension=exif      ; Must be after mbstring as it depends on it
extension=mysqli
;extension=oci8_12c  ; Use with Oracle Database 12c Instant Client
;extension=oci8_19  ; Use with Oracle Database 19 Instant Client
;extension=odbc
extension=openssl
;extension=pdo_firebird
extension=pdo_mysql
;extension=pdo_oci
;extension=pdo_odbc
;extension=pdo_pgsql
;extension=pdo_sqlite
;extension=pgsql
;extension=shmop

; The MIBS data available in the PHP distribution must be installed.
; See https://www.php.net/manual/en/snmp.installation.php
;extension=snmp

;extension=soap
;extension=sockets
;extension=sodium
extension=sqlite3
;extension=tidy
;extension=xsl
;extension=zip

```

## Apache24 연동
```
    httpd.conf

        LoadModule php_module "C:\php-8.2.11\php8apache2_4.dll"
        AddHandler application/x-httpd-php .php
        PHPIniDir "C:\php-8.2.11"
```

## 환경 변수 등록
```
    path 등록
        C:\php8.2.11
        C:\php8.2.11\ext
```

## 재시작
```
    cmd 관리자 모드 실행

        httpd -k restart
        
```
