# [NodeJS] Module 만들기

```
    모듈을 npm으로 다운받아서 사용해봤지 직접 만들어 보자!!
```

## 모듈만들기
```js
    //  test/createModule/index.js
    console.log('createModule실행');
    module.exports = {
        test : (a) => a
    }
```
```bash
    cd ..
    mkdir readModule
    cd readModule
    npm install ../createModule // ..readmodule 밖에 있기 때문.
```

## 모듈 불러오기
```js
    // test/readModule/index.js
    const createModule = require("createModule");
    console.log(createModule('성공'));
```
