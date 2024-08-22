# [PHP] IonCube 사용하여 php 소스코드 암호화 하기 #1

## 사용이유
```
    로컬 환경에 APM을 설치해서 나가야 되는 경우가 있을 때 소스 보호를 위해 사용하게 되었다.
```

## 정보
```
    https://www.ioncube.com/
    https://www.ioncube.com/main.php?c=account

    사용 버전

        Product  : PHP Encoder Cerberus Edition 12 for Win32
        Version  : 12.0.2
        Upgrade  : None Available
        Licenses : Allocated 0 of 1    
```

## loader 설치
```bash
    이온큐브로 암호화 한 소스를 읽으려면 loader을 설치해야 한다

    cd /usr/local

    wget https://downloads.ioncube.com/loader_downloads/ioncube_loaders_lin_x86-64.tar.gz

    tar xzf ioncube_loaders_lin_x86-64.tar.gz

    cd ioncube

    php -i | grep extension_dir

    cp -R ioncube_loader_lin_8.1* /usr/lib64/php/modules/
```

## php 설정 
```
    vi /etc/php.ini

    하단에

    zend_extension="/usr/lib64/php/modules/ioncube_loader_lin_8.1.so"

    추가

    php 재시작

    php -v 확인
```