# [FastApi] MySQL 연동시 주의 점.

## 문제
```py
   DATABASE_URL = f"{DB_TYPE}://{DB_USERNAME}:{escaped_password}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

   로컬환경에서 .env 파일의 값을 불러와서 연동을 잘하고 있었는데 리눅스환경에서 오류가 발생하는 것이다.
   뭐지 뭐지 고민하다 찾은것은 password의 특수문자가 문제였다.
```

## 해결
```py
    from urllib.parse import quote_plus

    # 비밀번호에 특수 문자가 포함된 경우 이스케이프 처리
    escaped_password = quote_plus(DB_PASSWORD)

    # 연결 문자열 작성
    DATABASE_URL = f"{DB_TYPE}://{DB_USERNAME}:{escaped_password}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
```
