# [Python] uv 사용하기

## uv란
```
    pip + venv 를 한 도구로 합친 패키지 / 가상환경 매니저다.

    예전에는 이렇게 했다.
        python -m venv .venv
        .venv\Scripts\activate
        pip install -r requirements.txt
        python ewg_report.py

    uv 는 활성화 없이
        uv sync
        uv run python ewg_report.py
    로 같은 일을 한다.

    의존성은 requirements.txt 대신
        pyproject.toml
        uv.lock
    에 적힌다.
```

## 사용하는 이유
```
    1.  빠르다.
        pip 보다 설치가 훨씬 빠르다.
        패키지 받을 때 기다리는 시간이 줄어든다.

    2.  venv 활성화를 안 해도 된다.
        Activate.ps1 깜빡하고 전역에 pip install 하는 실수를 줄인다.
        uv run 이 그 폴더 .venv 를 알아서 쓴다.

    3.  다른 PC 에 맞추기 쉽다.
        uv.lock 이 있으면 uv sync 한 줄로
        같은 버전으로 깔린다.

    4.  pip / venv 를 대체한다.
        가상환경 만드는 이유(충돌 방지 / 프로젝트별 독립)는 그대로다.
        도구만 uv 로 바꾼다.
```

## 설치
```
    Windows
        py -m pip install uv
        uv --version

    설치 확인이 되면 된다.
```

## 새 프로젝트 만들기
```
    mkdir myproject
    cd myproject

    uv 0.12 기준 스크립트(크롤러, 실행 파일)는 이렇게 만든다.
        uv init --app --no-package .
        uv run python main.py

        Hello 가 나오면 성공이다.

    uv init . 만 치면 라이브러리 구조(src/)가 되고
    main.py 가 안 생긴다.

    uv init --app . 만 치면 앱이지만 패키지를 설치해서
    Windows 한글 경로에서 .pth 오류가 날 수 있다.

    --force 옵션은 없다.
    다시 만들려면 .venv, pyproject.toml, uv.lock 지우고
        uv init --app --no-package .
    만 한다.
```

## 패키지 설치
```
    추가
        uv add selenium
        uv add pymysql python-dotenv
        uv add --dev pytest
            --dev 는 개발용 (테스트 등)
            운영에 안 넣어도 되는 패키지다.

    삭제
        uv remove selenium

    pyproject.toml 에 목록이 쌓이고
    uv.lock 에 정확한 버전이 고정된다.

    pip freeze > requirements.txt 대신 이 두 파일을 쓴다.
```

## 실행
```
    uv run python main.py
    uv run python ewg_report.py

    uv run main.py 는 쓰지 않는다.
        main.py 라는 실행 파일을 찾아서
        program not found 가 난다.

    Activate 는 필요 없다.
    uv run 이 .venv 를 붙인다.
```

## 다른 환경에서
```
    uv init 을 다시 하지 않는다.
    폴더를 복사하거나 git clone 한 뒤 sync 만 한다.

    가져갈 것
        pyproject.toml
        uv.lock
        소스
        .env.example

    안 가져갈 것
        .venv
        .env
        log/

    그 PC 에서
        uv sync
        copy .env.example .env
        uv run python 실행파일.py

    개발용 패키지 빼고 운영만 하면
        uv sync --no-dev
```

## 주의할 점
```
    1.  .venv 는 git 에 올리지 않는다.
        올리는 건 pyproject.toml 과 uv.lock 이다.

    2.  uv run python 파일.py
        uv run 파일.py 가 아니다.

    3.  Windows 한글 경로 + uv 0.12
        패키지로 init 하면
            UnicodeDecodeError: 'cp949' ... .pth
            Failed to import the site module
        PYTHONUTF8=1 로도 안 된다.
        --no-package 로 만들고
        pyproject.toml 에
            [tool.uv]
            package = false
        를 지우지 않는다.

        한 번 깨진 .venv 는 지우고 다시 만든다.
            Remove-Item -Recurse -Force .venv

    4.  hardlink 경고
            Failed to hardlink files; falling back to full copy
        설치가 실패한 게 아니다.
        복사로 넣는다는 뜻이라 조금 느릴 수만 있다.
        없애려면
            $env:UV_LINK_MODE = "copy"

    5.  Cursor / VSCode 인터프리터는 .venv 파이썬으로 잡는다.
            Python: Select Interpreter
            .venv\Scripts\python.exe
```

## 한줄 정리
```
    uv = pip + venv 를 대체하는 빠른 도구
    만드는 이유 = 속도 / 활성화 생략 / lock 으로 재현
    쓰는 순서 = uv init --app --no-package . -> uv add -> uv run python 파일.py
    다른 PC = uv sync -> .env 작성 -> uv run
```
