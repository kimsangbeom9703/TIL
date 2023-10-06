# [NodeJS] express / express-generator 로 프로젝트 만들기

## 참고
<https://velog.io/@new_wisdom/Node.js-6-Express-Express-generator%EB%A1%9C-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%EB%A7%8C%EB%93%A4%EA%B8%B0>


```
    NodeJS로 개발을 진행할 때 Express 웹 프레임워크를 많이 사용한다.
    근데 express를 처음 사용하면 구조가 정해져 있지 않다.
    이게 어떻게 보면 장점이자 단점이 되는데 자유도가 높은 만큼 자신의 스타일대로 개발하기 쉽다는 게 있지만
    여러 사람과 개발할 때 문제점이 생길 수 있다. 이해를 시켜야 한다.
    쉽게 프로젝트 구조를 만들어주는 generator 이 있다.
    물론 이게 정답은 아니니 참고만 하길 바란다.
```

## 설치 및 실행
``` 
    npm install -g express-generator

    express 프로젝트 --view=ejs
    
    cd 프로젝트

    npm install

    npm run start
```

## 구조
```
    프로젝트:.
    ├─bin
    ├─public
    │  ├─images
    │  ├─javascripts
    │  └─stylesheets
    ├─routes
    └─views
```

### bin/www
```
    http 모듈에 express 모듈을 연결하고 포트 번호를 지정.
    서버 실행시킨다.
```

### public
```
    외부에서 접근이 가능한 파일들
    css,images,js
```

### routers
```
    라우터 즉 브라우저에서 왔을때 어디로 보낼지??
```

### views
```
    view = html 파일 위치
    ejs를 템플릿 엔진으로 설치했기 때문에 html 이 아닌 ejs가 된다.
```

### app.js
```
    메인 역할을 하고 미들웨어를 관리한다
```

## 확인?
```
    개발을 하다 보면 router 에서 요청 받은 후 서비스 로직을 다 처리하기 때문에 소스가 많이 지저분하다.
    그래서 service , model 등 나눠주는게 좋다.
    물론 개인 자유!
```
