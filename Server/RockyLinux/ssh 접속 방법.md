# [Server/RockyLinux] ssh 접속 허용하기

# 허용방법

```
    1. vi /etc/ssh/sshd_config
        -   port 22 주석 해제
    
    2. systemctl start sshd.service

    3. systemctl status sshd.service
    
    4. firewall-cmd --zone=public --add-port=22/tcp --permanent

    5. firewall-cmd --reload
```
