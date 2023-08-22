

#   파이썬을 공부하려는 이유
```
1.  새로운 언어에 도전해보기.
2.  실력향상.
3.  좋은곳으로 이직.?ㅎㅎㅎ
```


#   파이썬 설치

    -   윈도우 

        https://www.python.org/downloads/ 최신버전 다운로드 진행
        
        python.exe 실행 후 python -v
        

    -   리눅스

        yum install python3
        yum install python3-pip.noarch  // pip 패키지 매니저 설치.
        python3 --version // 버전 확인.
        
        alias python=python3 // python3라고 치기 귀찮으니 python 으로 별칭 등록
        

##  파이썬 가상환경 설치하기
```
    파이썬은 가상 환경을 구성할 수 있다.
    이유는 예를들어 개발을 진행 할 때 파이썬 버전을 다르게 필요로 하는 경우가 있는데 그럴 경우 환경을 나눠서 개발할 수 있게 도와준다.

    파이썬의 기본 플로우 ex) 가상환경 구성 -> 프로젝트 구성 -> 앱 구성 / 프론트 서버 / 백앤드 서버 구동
    virtualenv or venv  가 있는데 venv 는 느리고 확장성이 떨어지는 이슈 , 파이썬 버전을 달리 할 수 없는 문제로 virtualenv 사용.

    
    1.  pip install virtualenv

    
```


