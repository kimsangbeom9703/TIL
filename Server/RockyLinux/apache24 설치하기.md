# [Server/RockyLinux] apache24 설치하기

# 설치하기
```
    1.  yum install httpd // 아파치 설치
    2.  systemctl enable httpd // 아파치 서비스 적용
    3.  systemctl start httpd   //  아파치 실행
    4.  firewall-cmd --zone=public --permanent --add-port=80/tcp    //포트 열기
    5.  firewall-cmd --reload   //포트 재시작
    6.  firewall-cmd --zone=public --list-all   //포트 리스트 확인
```