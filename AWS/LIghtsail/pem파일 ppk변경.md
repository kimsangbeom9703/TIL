# [AWS/Lightsail] 기본키(pem) 파일 ppk변경하여 putty로 로그인

##  기본키 파일 다운로드

```
    라이트세일 -> 연결 -> 기본키파일 다운로드

    putty Key Generator 다운로드

        Load -> 기본키파일 열기 -> save pirvate key -> 저장
```

## 로그인

```
    putty 실행
        Host Name = 서버아이피입력
        Saved Sesstions = 저장할 명칭

        Connection 
            SSH
                AUTH
                    Private key file authentication = ppk 파일 로드
    
    save 후 실행

    기본아이디 - ec2-user
```
