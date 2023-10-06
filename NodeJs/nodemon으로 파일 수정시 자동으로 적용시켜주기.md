# [NodeJS] nodemon으로 파일 수정시 자동으로 적용시켜주기

## 참고
<https://velog.io/@chy0428/Node-JS-Nodemon-%EC%84%A4%EC%B9%98>


```
    node app.js 로 파일을 수정하면 views는 파일이 변경되면 적용이 되지만
    라우터 등이 수정되면 적용이 되지않는다. nodemon을 사용하면 바로 적용이 가능하다.
    watch기능이라고 보면 된다.
```

## 설치 및 사용
```
    npm install nodemon --save-dev
    //dev 옵션은 개발자모드 즉 local에서만 실행하겠다는 의미다.

    package.json

        script 부분에
            "dev" : "nodemon ./bin/www" // or app.js 등을 하면 된다.
```
