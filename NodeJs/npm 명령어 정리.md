# [NPM] npm 명령어 정리

```txt
    npm은 패키지 매니저이고 nodejs의 단짝으로 보면되고 필요한 모듈을 설치하고 관리하기 용이하다.
```

## 참고
<https://ahnsisters.tistory.com/16>
```
    npm@5 부터 --save 옵션을 기본 옵션으로 저장한다.
```
## 시작하기
```bash
    npm init
    
    package.json 파일 생성
```

## npm install
```
    npm install  // 패키지 설치
```

## npm install -g 
```
    npm install -g test // 패키지 전역 설치 (내 PC 어디서든 사용 가능)
```

## npm install  / npm install --save
```
    npm install --save test // package.json의 dependencies에 추가
```

## npm install -D / npm install --save-dev
```
    npm install --save test // package.json의 dependencies에 추가
```

## 버전 지정 후 설치
```
    npm install test@1.0.1
```

## 버전 정보의 구성
```
    1) 메이저 버전 번호 : 하위 호환이 되지 않는 변경 사항
    2) 마이너 버전 번호 : 하위 호환이 되는 변경 사항
    3) 패치 버전 번호 : 간단한 버그 수정
```

## 버전 정보 표기 방법
```
    version
    명시된 version과 일치


    >version
    명시된 version보다 높은 버전


    >=version
    명시된 version과 같거나 높은 버전


    <version
    명시된 version보다 낮은 버전


    <=version
    명시된 version과 같거나 낮은 버전


    ~version
    명시된 version과 근사한 버전


    ^version
    명시된 version과 호횐되는 버전



     ~(틸트)와 ^(캐럿)의 차이
    1) ~(틸트)• 틸트는 패치 버전 범위 내에서 업데이트 한다.
        ex)- ~0.0.1 : 0.0.1 <= version < 0.1.0- ~0.1.1 : 0.1.1 <= version < 0.2.0
    2) ^(캐럿)• 캐럿은 마이너 버전 범위 내에서 업데이트 한다.
        ex)- ^1.0.2 : 1.0.2 <= version < 2.0
```
