# [NodeJS] .env 구동 환경마다 다른 환경 변수 파일 설정하기

## 
```
  .env.local >>> .env.development, .env.production, .env.test >>> .env

  .env.local
    여기에 등록된 변수는 모든 환경에서 최우선순위로 적용되며, 다른 환경에 같은 변수가 있다면 덮어쓴다.

  .env.development
    개발환경 (process.env.NODE_ENV === "development")에서 사용할 환경 변수를 정의한다. .env에 같은 환경 변수가 있다면 덮어쓴다.

  .env.production
    배포환경 (process.env.NODE_ENV === "production")에서 사용할 환경 변수를 정의한다. .env에 같은 환경 변수가 있다면 덮어쓴다.

  .env.test
    테스트 환경(process.env.NODE_ENV === "test")에서 사용할 환경 변수를 정의한다.

  .env
    가장 우선 순위가 낮다. 보통, 모든 환경에서 공통으로 사용할 변수를 등록한다.  
```

