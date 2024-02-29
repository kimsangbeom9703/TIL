# [DB] MARIADB DB (마리아 디비) 설치하기

```
    지금까지는 MySQL을 사용하고있었는데 서비스 개발 중 라이센스가 살짝 애매해서 마리아 디비를 사용하기로 했다.
```

## 환경
```
    OS : windows 10 pro 64
    버전 : MariaDB Server 11.3.2 zip 형식
```
## 설치
```
    https://mariadb.org/download/?t=mariadb&p=mariadb&r=11.3.2

    11.3.2 zip 파일 다운로드

    설치 경로 : C:\apm\mariadb-11.3.2

    data 폴더 생성 - C:\apm\mariadb-11.3.2\data
```

## 환경변수 설정
```
    추가 : 
        변수 명 : MARIADB_HOME
        변수 값 : C:\apm\mariadb-11.3.2

        Path 에 C:\apm\mariadb-11.3.2\bin
```

## 윈도우 서비스 등록 및 DB 데이터 초기화
```
ex)
    %MARIADB_HOME%\bin\mysql_install_db.exe --datadir=%MARIADB_HOME%\data --service="mariaDB" --port=4306 --password=비밀번호
```

## 서비스 실행
```
    서비스 -> mariaDB 실행
```

## DB실행
```
    mariaDB -u root -p 

    비밀번호
```

## 마리아디비 mysqlworkbench 연동하기
```
    연동이 mysql 처럼 정보를 입력하면 되는데 문제가 동작을 하지 않는다.

    연결 시 Advanced 탭에서 Others:  useSSL=0 을 입력하자
```