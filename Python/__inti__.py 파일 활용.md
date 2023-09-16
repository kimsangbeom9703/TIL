# [Python] __init__.py 활용하기

```
    패키지를 생성하면 __init__.py 파일은 필수 아닌 필수이다. 
    fastApi 에서 routers 폴더를 만들어 router을 나눠서 저장하고 있었다.
    main router에 불러오려고 하니 나중에 router이 많아지면 되게 import 하는 부분이 지저분할 거라고 생각했다.
    방법이 없나 여러 테스트를 해봤는데 좋은 방법을 찾았다.

    routers / __init__.py 파일에 미리 정의를 하는 것이다.
```
```py
# routers / __init__.py
    from .users import users_router
    from .items import items_router
```

```py
# main.py
    from fastapi import FastAPI

    import routers as rt

    app = FastAPI()
    app.include_router(rt.users_router)
    app.include_router(rt.items_router)

```