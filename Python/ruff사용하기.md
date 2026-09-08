# [Python] ruff 사용하기

## ruff란
```
    파이썬 코드를 검사하고 모양을 맞춰 주는 도구다.
    린트(문제 찾기) + 포맷(줄바꿈, 따옴표, 들여쓰기)을 한 프로그램이 한다.

    예전에는 이렇게 나눴다.
        Black       포맷만
        flake8      린트
        isort       import 정렬

    ruff 는 이 역할을 하나로 합친 것이고
    포맷 결과는 Black 이랑 거의 같다. (기본 줄 길이 88자)

    파일을 그 자리에서 고친다.
    별도 결과 파일이나 리포트 HTML 은 안 만든다.
```

## 사용하는 이유
```
    1.  빠르다.
        Rust 로 만들어서 Black / flake8 보다 훨씬 빠르다.
        파일 많아도 부담이 적다.

    2.  도구를 하나만 쓰면 된다.
        Black + flake8 + isort 를 따로 안 깔아도 된다.

    3.  코드 리뷰에서 줄바꿈 얘기를 안 해도 된다.
        저장하거나 format 한 번 돌리면 팀 스타일이 같아진다.

    4.  Black 을 틀린 걸로 만든 건 아니다.
        포맷 규칙의 원조는 여전히 Black 이다.
        지금 새로 짜는 쪽에서 ruff 를 쓰는 이유는
        속도랑 린트까지 같이 되기 때문이다.
```

## 설치
```
    uv 프로젝트 (이 방식이 편하다)
        uv add --dev ruff
            개발용으로만 넣는다.
            운영 서버 크롤링에 ruff 가 필수는 아니다.

    pip / venv
        pip install ruff

    확인
        uv run ruff --version
        또는
        ruff --version
```

## 포맷 (format)
```
    현재 폴더 전체
        uv run ruff format .

    파일 하나
        uv run ruff format ewg_search.py

    성공하면 이런 메시지가 나온다.
        2 files reformatted, 4 files left unchanged

        reformatted  = 고친 파일
        unchanged    = 이미 맞춰져서 그대로인 파일

    바뀐 내용은 그 .py 를 열면 보인다.
    긴 한 줄을 여러 줄로 나누는 게 대부분이다.

    미리 보기만 (파일은 안 고침)
        uv run ruff format --diff .

    git 에 아직 안 올린 파일이면 git diff 에 안 나온다.
    원본이랑 비교하려면
        git diff --no-index -- "../ewg/ewg_search.py" "ewg_search.py"
```

## 린트 (check)
```
    문제만 보여 주기
        uv run ruff check .

    자동으로 고칠 수 있는 것만 고치기
        uv run ruff check --fix .

        안 쓰는 import, 간단한 문법 같은 걸 고친다.
        로직까지 알아서 바꿔 주지는 않는다.

    포맷만 쓸 거면 check 는 나중에 해도 된다.
```

## Cursor 에서 저장 시 적용
```
    필수는 아니다. 터미널에서 format 만 돌려도 된다.

    1.  확장 설치
            Ruff    charliermarsh.ruff

    2.  이 프로젝트만 적용하려면
            .vscode/settings.json

            {
              "[python]": {
                "editor.defaultFormatter": "charliermarsh.ruff",
                "editor.formatOnSave": true
              }
            }

    전역 Cursor 설정에 넣으면
    다른 파이썬 프로젝트 저장할 때도 포맷이 바뀐다.
    연습 / 이 프로젝트만 할 거면 폴더 설정이 안전하다.

    예전 VS Code 설정은 쓰지 않는다.
        python.formatting.provider
        python.linting.*
            구버전 API 라 지금 Cursor 에서는 안 먹거나 경고만 난다.
```

## 다른 환경에서
```
    ruff 는 pyproject.toml 의 dev 의존성으로 들어가 있으면
        uv sync
    할 때 같이 깔린다.

    운영만 하면
        uv sync --no-dev
            ruff 없이 실행용 패키지만 설치된다.

    포맷은 개발할 때 돌리면 된다.
        uv run ruff format .
```

## 주의할 점
```
    1.  format 은 파일을 바로 덮어쓴다.
        커밋 전에 --diff 로 한 번 보는 게 좋다.

    2.  동작이 바뀌는 리팩터가 아니다.
        줄 나누기, 따옴표, 쉼표 같은 모양만 맞춘다.

    3.  uv 프로젝트에서는
            uv run ruff format .
        로 실행한다.
        전역 ruff 랑 .venv ruff 버전이 다를 수 있다.

    4.  check --fix 는 format 이랑 다르다.
        format  = 모양
        check   = 버그 / 스타일 경고
```

## 한줄 정리
```
    ruff = 파이썬 포맷 + 린트를 한 도구
    만드는 이유 = 속도 / Black 호환 포맷 / 도구 하나로 통일
    쓰는 순서 = uv add --dev ruff -> uv run ruff format . -> (선택) ruff check --fix .
    저장 시 적용 = Cursor Ruff 확장 + formatOnSave (프로젝트 설정 권장)
```
