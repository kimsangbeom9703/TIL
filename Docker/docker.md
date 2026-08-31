# Docker 공부

## 도커를 사용하는 이유

로컬에서는 잘 되는데, 서버에 올리면 안 되는 경우가 있다.

원인은 대부분 **환경이 다르기 때문**이다.

- Node.js / Python 버전이 다름
- 설치된 라이브러리(의존성)가 다름
- OS, 환경변수, 설정이 다름

도커는 **앱 + 실행에 필요한 환경**을 하나로 묶어서 이미지로 만든다.  
그 이미지를 어디서 실행하든(내 PC, 서버, 클라우드) 같은 환경이 되므로, “내 컴퓨터에선 됐는데” 문제가 줄어든다.

---

## 핵심 개념

| 용어 | 한 줄 설명 | 비유 |
| --- | --- | --- |
| **이미지 (Image)** | 실행 파일 + 환경을 담은 읽기 전용 템플릿 | 클래스, 또는 설치 파일 |
| **컨테이너 (Container)** | 이미지를 실행한 인스턴스. 실제로 돌아가는 프로세스 | 객체, 또는 설치된 프로그램이 실행 중인 상태 |
| **Dockerfile** | 이미지를 만드는 레시피(스크립트) | 요리 레시피 |
| **레지스트리 (Registry)** | 이미지를 올려두고 받아오는 저장소 (예: Docker Hub) | GitHub, npm 저장소 |

관계:

```
Dockerfile  --(build)-->  이미지  --(run)-->  컨테이너
                              ↑
                         레지스트리 (push / pull)
```

같은 이미지로 컨테이너를 여러 개 띄울 수 있다.  
컨테이너를 지워도 이미지는 남아 있다. 이미지만 있으면 언제든 다시 실행할 수 있다.

---

## 예제: Express 앱을 도커로 실행하기

실습 폴더: `docker-test`

### 1. 테스트 폴더 만들기

```bash
mkdir docker-test
cd docker-test
```

### 2. Express 앱 만들기

```bash
npm init -y
npm install express
```

`app.js`

```js
const express = require('express');
const app = express();
const PORT = 3000;

app.get('/', (req, res) => {
  res.send('안녕하세요! 도커 컨테이너에서 실행 중입니다.\n');
});

app.listen(PORT, () => {
  console.log(`서버가 ${PORT}번 포트에서 실행 중입니다.`);
});
```

이 시점에서는 아직 도커가 아니다. 그냥 Node.js 웹서버다.  
로컬에서 `node app.js`로 실행하면 `http://localhost:3000` 에서 확인할 수 있다.

이제 이 앱을 **컨테이너 안에서도 똑같이** 돌리기 위해 Dockerfile을 만든다.

### 3. Dockerfile 만들기

파일 이름은 반드시 `Dockerfile` (확장자 없음).  
`docker-test` 폴더 안에 둔다.

```dockerfile
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["node", "app.js"]
```

#### 각 명령어 의미

| 명령어 | 하는 일 |
| --- | --- |
| `FROM node:18` | Node.js 18이 깔린 리눅스를 베이스 이미지로 사용. 맨 위에서 시작점을 정한다. |
| `WORKDIR /app` | 컨테이너 안 작업 폴더를 `/app`으로 지정. 이후 `COPY`, `RUN`, `CMD`는 이 폴더 기준이다. |
| `COPY package*.json ./` | 내 PC의 `package.json`, `package-lock.json`을 컨테이너 `/app`으로 복사. |
| `RUN npm install` | 컨테이너 안에서 패키지 설치. 이미지에 `node_modules`가 포함된다. |
| `COPY . .` | 나머지 소스(`app.js` 등)를 `/app`으로 복사. |
| `EXPOSE 3000` | 이 컨테이너가 3000번 포트를 쓴다고 **문서화**하는 것. 실제로 포트를 열어주지는 않는다. 포트 연결은 `docker run -p`가 한다. |
| `CMD ["node", "app.js"]` | 컨테이너가 시작될 때 실행할 명령. 이미지 안의 기본 실행 명령이다. |

#### `package.json`을 먼저 복사하는 이유

`COPY package*.json` → `RUN npm install` → `COPY . .` 순서가 중요하다.

도커는 **레이어** 단위로 이미지를 만들고, 안 바뀐 레이어는 캐시를 재사용한다.

- `app.js`만 수정하면 `npm install` 레이어는 그대로 재사용된다. 빌드가 빨라진다.
- 처음부터 `COPY . .`를 하면 소스 한 줄만 바꿔도 `npm install`을 다시 한다.

### 4. 이미지 빌드하기

`docker-test` 폴더에서:

```bash
docker build -t my-first-app .
```

| 부분 | 의미 |
| --- | --- |
| `docker build` | Dockerfile을 읽어서 이미지를 만들어라 |
| `-t my-first-app` | 이미지에 `my-first-app`이라는 이름(태그)을 붙여라 |
| `.` | 빌드 컨텍스트. **현재 폴더**의 Dockerfile과 파일들을 사용하라는 뜻. 빠뜨리면 에러 난다. |

빌드가 끝나면 로컬에 `my-first-app` 이미지가 생긴다.  
이 이미지는 “Node 18 + express + app.js”가 들어 있는 실행 템플릿이다.

### 5. 빌드된 이미지 확인하기

```bash
docker images
```

`REPOSITORY`에 `my-first-app`이 보이면 빌드 성공이다.

### 6. 컨테이너 실행하기

```bash
docker run -p 3000:3000 my-first-app
```

| 부분 | 의미 |
| --- | --- |
| `docker run` | 이미지로부터 컨테이너를 만들어 실행 |
| `-p 3000:3000` | 포트 연결. **호스트:컨테이너** 순서 |
| `my-first-app` | 사용할 이미지 이름 |

`-p 3000:3000`을 풀면:

- 왼쪽 `3000` → 내 컴퓨터(호스트)의 3000번 포트
- 오른쪽 `3000` → 컨테이너 안의 3000번 포트 (`app.js`의 `PORT`)

브라우저에서 `http://localhost:3000` 으로 접속하면, 내 PC 3000번으로 들어온 요청이 컨테이너 3000번으로 전달된다.

이 명령은 **포그라운드(attached)** 실행이다.

- 터미널이 컨테이너에 붙고, 서버 로그가 계속 출력된다.
- Ctrl+C를 누르면 컨테이너도 같이 멈춘다.

---

## 백그라운드 실행 / 목록 / 끄기

매번 터미널을 붙잡고 있을 수는 없으니, 뒤에서 돌리고 필요할 때 끄면 된다.

### 백그라운드로 실행 (`-d`)

```bash
docker run -d -p 3000:3000 my-first-app
```

- `-d` (detached): 컨테이너는 뒤에서 돌고, 터미널은 바로 돌아온다.
- 성공하면 긴 컨테이너 ID가 출력된다.

이름을 붙여 두면 나중에 다루기 쉽다.

```bash
docker run -d -p 3000:3000 --name my-app my-first-app
```

같은 이름(`my-app`)은 한 번에 하나만 쓸 수 있다.  
이미 있으면 지우거나, 다른 이름을 써야 한다.

### 실행 중인 컨테이너 보기

```bash
docker ps
```

지금 돌아가는 컨테이너만 나온다.

중지된 것까지 보려면:

```bash
docker ps -a
```

자주 보는 컬럼:

- `CONTAINER ID` — ID. 앞 몇 글자만 써도 된다.
- `IMAGE` — 어떤 이미지로 떴는지
- `STATUS` — Up / Exited
- `PORTS` — `0.0.0.0:3000->3000/tcp` 이면 호스트 3000이 컨테이너 3000에 연결된 것
- `NAMES` — `--name`으로 준 이름. 안 주면 도커가 임의 이름을 붙인다.

### 컨테이너 끄기 / 삭제

```bash
docker stop my-app
```

이름 대신 ID 앞부분을 써도 된다.

```bash
docker stop 28c3fea0ad7e
```

- `docker stop` — 종료 신호를 주고 잠시 기다린다. 일반적으로 이걸 쓴다.
- `docker kill` — 바로 강제 종료.
- `docker rm my-app` — 이미 중지된 컨테이너를 목록에서 삭제.
- `docker rm -f my-app` — 실행 중이어도 강제 종료 후 삭제.

컨테이너를 지워도 **이미지는 남아 있다.**  
다시 실행하려면 `docker run`만 하면 된다.

참고: `-p`의 왼쪽은 **내 PC 포트**, 오른쪽은 **컨테이너 포트**다.  
컨테이너 앱은 계속 3000을 쓰는데, 내 PC 3000이 이미 쓰 중이면 이렇게 바꿀 수 있다.

```bash
docker run -d -p 4000:3000 --name my-app my-first-app
```

이 경우 브라우저는 `http://localhost:4000` 으로 접속한다.  
컨테이너 안 `app.js`의 `PORT = 3000`은 그대로다.

---

## 로그 보기 (`docker logs`)

`-d`로 백그라운드 실행하면 터미널에 로그가 안 보인다.  
그럴 때 컨테이너가 남긴 출력을 보는 명령이 `docker logs`다.

`app.js`의 `console.log(...)` 같은 내용이 여기로 온다.

먼저 이름으로 실행해 둔다. (`docker-test`가 아니라, 이미지가 있는 어디서든 실행 가능)

```bash
docker run -d -p 3000:3000 --name my-app my-first-app
```

### 지금까지 나온 로그 전부 보기

```bash
docker logs my-app
```

이름 대신 컨테이너 ID 앞부분도 된다.

정상적으로 떴다면 이런 한 줄이 보인다.

```
서버가 3000번 포트에서 실행 중입니다.
```

### 실시간으로 따라가기 (`-f`)

```bash
docker logs -f my-app
```

`-f`는 follow. 새 로그가 나올 때마다 계속 보여 준다.  
포그라운드 `docker run`처럼 보이지만, **컨테이너는 끄지 않는다.**  
보는 것만 그만두려면 Ctrl+C.

### 자주 쓰는 옵션

```bash
docker logs --tail 50 my-app      # 마지막 50줄만
docker logs --since 10m my-app    # 최근 10분만
docker logs -f --tail 50 my-app   # 최근 50줄부터 실시간
```

에러가 났을 때 가장 먼저 보는 곳이 여기다.  
컨테이너가 바로 꺼져도 `docker ps -a`로 이름을 찾은 뒤 `docker logs`로 이유를 확인할 수 있다.

---

## 컨테이너 안으로 들어가기 (`docker exec`)

실행 중인 컨테이너는 작은 리눅스처럼 들어갔다 나올 수 있다.  
파일이 어디 있는지, 패키지가 설치됐는지 확인할 때 쓴다.

```bash
docker exec -it my-app sh
```

| 부분 | 의미 |
| --- | --- |
| `docker exec` | 이미 돌아가는 컨테이너 안에서 명령을 실행 |
| `-i` | 입력을 컨테이너로 보낸다 (interactive) |
| `-t` | 터미널처럼 보이게 한다 (tty) |
| `my-app` | 대상 컨테이너 |
| `sh` | 그 안에서 실행할 프로그램. 여기서는 셸 |

`-it`는 거의 항상 같이 쓴다. 셸에 들어가려면 둘 다 필요하다.

프롬프트가 바뀌면 성공이다. 이제 컨테이너 안이다.

```bash
pwd          # /app  (WORKDIR)
ls           # package.json, app.js, node_modules ...
cat app.js
exit         # 나온다. 컨테이너는 계속 돌아간다
```

`exit` 또는 Ctrl+D로 나온다.  
**나오는 것과 끄는 것은 다르다.**  
`exec`로 나왔다고 서버가 멈추지 않는다. 끄려면 따로 `docker stop my-app`.

한 줄만 실행하고 바로 나오기:

```bash
docker exec my-app ls /app
docker exec my-app node -v
```

이 경우는 `-it`가 필요 없다. 결과를 보고 끝이기 때문이다.

`docker run`과 `docker exec` 차이:

- `run` — 이미지를 **새로** 컨테이너로 만들어 실행
- `exec` — **이미 실행 중인** 컨테이너 안에 명령을 보냄

꺼져 있는 컨테이너에는 `exec`가 안 된다. 먼저 `docker start my-app`으로 다시 켜야 한다.

```bash
docker start my-app    # 중지했던 컨테이너를 다시 실행 (새로 만들지 않음)
docker stop my-app     # 끄기
```

`run`은 매번 새 컨테이너를 만든다. 같은 이름으로 다시 `run`하려면 먼저 `docker rm`을 해야 한다.  
이미 있는 걸 다시 켤 때는 `start`를 쓴다.

---

## `.dockerignore`

Dockerfile에 `COPY . .`가 있으면, 현재 폴더 파일이 이미지로 들어간다.  
이 때 `node_modules`까지 넣으면:

- 이미지가 필요 없이 커진다
- 내 PC에서 설치한 모듈이 리눅스 컨테이너로 들어가서 문제가 날 수 있다
- 빌드가 느려진다

컨테이너용 패키지는 이미 `RUN npm install`이 설치한다.  
내 PC의 `node_modules`는 복사할 필요가 없다.

`.gitignore`와 같은 역할이다.  
`docker-test` 폴더에 `.dockerignore` 파일을 만든다.

```
node_modules
npm-debug.log
.git
.gitignore
*.md
```

이 파일에 적힌 것은 `COPY . .` 때 빠진다.  
`package.json`은 빼면 안 된다. `RUN npm install`이 그 파일을 보고 설치한다.

적용하려면 이미지를 **다시 빌드**해야 한다.

```bash
cd docker-test
docker build -t my-first-app .
```

같은 태그(`my-first-app`)로 다시 빌드하면, 그 이름이 새 이미지를 가리킨다.

---

## 이미지 삭제 / 정리

컨테이너 삭제(`docker rm`)와 이미지 삭제(`docker rmi`)는 다르다.

```bash
docker rm my-app              # 컨테이너만 삭제. 이미지는 남음
docker rmi my-first-app       # 이미지 삭제
```

이미지가 “컨테이너가 사용 중”이라며 안 지워지면, 그 이미지로 만든 컨테이너를 먼저 지운다.

```bash
docker rm -f my-app
docker rmi my-first-app
```

지금은 `docker system prune`은 몰라도 된다.  
안 쓰는 것을 한꺼번에 지우는 명령이라, 실수로 필요한 것까지 지울 수 있다.

---

## 볼륨 — 컨테이너를 지워도 남는 데이터

컨테이너 안의 파일은 **그 컨테이너가 살아있는 동안만** 있다.  
`docker rm` 하면 안에서 만든 파일도 같이 사라진다.

그래서 DB 데이터, 업로드 파일처럼 **남기고 싶은 것**은 컨테이너 밖 저장소에 둔다. 그게 볼륨이다.

`-v`는 `docker run` 할 때 붙인다. 이미 만들어 둔 컨테이너에 나중에 추가할 수는 없다.  
지금은 `my-app`이 꺼져 있으니, 볼륨 실습 전에 지우고 새로 띄운다.

```bash
docker rm my-app
```

볼륨은 쓰임이 다른 **두 종류**를 알면 된다.

| 종류 | 무엇이 붙나 | 언제 쓰나 |
| --- | --- | --- |
| **명명 볼륨 (named volume)** | 도커가 관리하는 저장소 | DB, 로그, 업로드처럼 “앱 데이터” |
| **바인드 마운트 (bind mount)** | 내 PC의 폴더/파일 | 개발할 때 코드를 바로 반영하고 싶을 때 |

형식은 둘 다 `-v 왼쪽:오른쪽` 이다.

- 왼쪽 = 호스트(내 PC 또는 도커가 만든 볼륨)
- 오른쪽 = 컨테이너 안 경로

포트 `-p 호스트:컨테이너` 와 같은 방향이다.

---

### 1) 볼륨 없이 지우면 파일이 사라지는지 확인

```bash
docker run -d -p 3000:3000 --name my-app my-first-app
docker exec my-app sh -c "echo hello > /app/memo.txt"
docker exec my-app cat /app/memo.txt
```

`hello`가 보이면 컨테이너 안에 파일이 생긴 것이다. 이제 지우고 같은 이름으로 다시 띄운다.

```bash
docker rm -f my-app
docker run -d -p 3000:3000 --name my-app my-first-app
docker exec my-app cat /app/memo.txt
```

`No such file` 이 나와야 정상이다.  
새 컨테이너는 이미지에서 다시 시작된 것이라, 아까 만든 `memo.txt`는 없다.

---

### 2) 명명 볼륨 — 도커가 보관하는 저장소

볼륨 이름을 정해서 컨테이너 폴더에 붙인다.

```bash
docker rm -f my-app
docker run -d -p 3000:3000 -v my-data:/app/data --name my-app my-first-app
```

- `my-data` — 볼륨 이름. 없으면 도커가 새로 만든다.
- `/app/data` — 컨테이너 안에서 그 볼륨이 보이는 경로.

파일을 볼륨 쪽에 쓴다. (`/app/memo.txt`가 아니라 `/app/data/memo.txt`)

```bash
docker exec my-app sh -c "echo hello > /app/data/memo.txt"
docker exec my-app cat /app/data/memo.txt
```

컨테이너를 지우고, **같은 볼륨 이름**으로 다시 띄운다.

```bash
docker rm -f my-app
docker run -d -p 3000:3000 -v my-data:/app/data --name my-app my-first-app
docker exec my-app cat /app/data/memo.txt
```

이번엔 `hello`가 남아 있다. 컨테이너는 새것인데, `my-data` 볼륨은 그대로이기 때문이다.

볼륨 목록:

```bash
docker volume ls
```

`my-data`가 보이면 된다. 삭제는 컨테이너를 먼저 지운 뒤:

```bash
docker volume rm my-data
```

명명 볼륨은 **MariaDB, Redis 같은 DB**에 가장 많이 쓴다.  
DB 컨테이너를 지워도 볼륨만 있으면 데이터는 남는다.

---

### 3) 바인드 마운트 — 내 PC 폴더를 그대로 붙이기

컨테이너 안에서 `vi app.js`를 치다 막힌 이유:

- 이미지에 `vi`, 메모장이 없는 경우가 많다.
- 안에서 고치면 그 컨테이너에만 남고, `rm` 하면 사라진다.
- 고치고 싶은 파일은 **내 PC에서 편집**하는 편이 맞다.

바인드 마운트는 내 PC의 파일을 컨테이너 경로에 겹쳐 붙인다.  
`docker-test` 폴더에서:

```bash
docker rm -f my-app
docker run -d -p 3000:3000 -v ${PWD}/app.js:/app/app.js --name my-app my-first-app
```

PowerShell에서 `${PWD}`는 현재 폴더 경로다.  
왼쪽이 내 PC의 `app.js`, 오른쪽이 컨테이너의 `/app/app.js`.

이제 Cursor에서 `app.js` 문구를 바꾸고 저장한 뒤, 컨테이너를 한 번 재시작한다.

```bash
docker restart my-app
```

`node app.js`는 파일 변경을 자동으로 다시 읽지 않는다.  
그래서 저장만 해서는 브라우저에 바로 안 바뀐다. `restart`가 필요하다. (나중에 nodemon을 쓰면 자동 재시작이 된다.)

확인:

```bash
docker logs my-app
```

브라우저 `http://localhost:3000` 도 다시 보면 된다.

#### 폴더 전체를 붙일 때 주의

```bash
-v ${PWD}:/app
```

이렇게 하면 내 PC의 `docker-test`가 컨테이너 `/app`을 **통째로 덮어쓴다.**  
윈도우에서 설치한 `node_modules`가 리눅스 컨테이너를 덮어서 앱이 깨질 수 있다.

지금은 **파일 하나만** (`app.js`) 붙이는 쪽을 권한다.

---

### 두 종류의 차이 한 줄

- **명명 볼륨**: 도커가 보관. 위치는 몰라도 된다. 데이터가 목적인 경우.
- **바인드 마운트**: 내 PC 경로를 지정. 코드를 고치는 게 목적인 경우.

실무에서는 DB는 명명 볼륨, 개발 중인 소스만 바인드 마운트를 쓰는 경우가 많다.

---

## Docker Compose — 여러 컨테이너를 파일로 한 번에

지금까지는 명령을 하나씩 쳤다.

```bash
docker build -t my-first-app .
docker run -d -p 3000:3000 --name my-app my-first-app
```

앱과 Redis를 같이 띄우려면 `docker run`을 두 번 하고, 네트워크도 직접 만들어야 한다.  
그걸 한 파일에 적어 두고, 한 명령으로 올리고 내리는 게 **Compose**다.

실습 파일: `docker-test/docker-compose.yml`

지금 쓰는 명령은 `docker-compose`가 아니라 **`docker compose`** (띄어쓰기)다. Docker Desktop에 들어 있는 최신 방식이다.

### `docker run`이 파일로 옮겨진 모습

```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      PORT: "3000"
      REDIS_URL: redis://redis:6379
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data

volumes:
  redis-data:
```

| compose | 예전에 친 명령 |
| --- | --- |
| `services:` | 띄울 컨테이너들을 나열 |
| `build: .` | `docker build .` — 이 폴더 Dockerfile로 이미지 만들기 |
| `ports: "3000:3000"` | `-p 3000:3000` |
| `environment:` | `-e PORT=3000` 같은 환경변수 |
| `depends_on: redis` | redis를 먼저 시작하라. (준비가 끝날 때까지 기다리진 않음) |
| `image: redis:7-alpine` | Dockerfile 없이 Docker Hub 이미지를 그대로 사용 |
| `volumes: redis-data:/data` | `-v redis-data:/data` 명명 볼륨 |

Redis에 `ports:`가 없는 이유: 브라우저는 앱(3000)만 보면 된다.  
Redis 6379는 **compose 네트워크 안**에서만 쓴다. 내 PC 포트와 안 겹친다.

`REDIS_URL: redis://redis:6379` 의 `redis`는 컨테이너 이름이 아니라 **서비스 이름**이다.  
같은 `docker-compose.yml` 안 서비스끼리는 그 이름으로 서로를 찾는다.

`app.js`는 그 값을 읽는다.

```js
const PORT = Number(process.env.PORT) || 3000;
const REDIS_URL = process.env.REDIS_URL || 'redis://127.0.0.1:6379';
```

컨테이너 안에서는 `redis://redis:6379` 로 붙고,  
PC에서 그냥 `node app.js`를 치면 `127.0.0.1:6379` 로 붙는다.

참고: `redis` npm 패키지 6은 Node 20 이상이 필요하다.  
그래서 Dockerfile 베이스를 `node:18` → `node:20` 으로 바꿔 두었다.

### 올리고 / 내리고 / 보기

`docker-test` 폴더에서:

```bash
docker compose up --build -d
```

| 부분 | 의미 |
| --- | --- |
| `docker compose up` | yml에 적힌 서비스를 전부 실행 |
| `--build` | 앱 이미지를 다시 빌드 (app.js, package.json이 바뀌었으니 필요) |
| `-d` | 백그라운드. `docker run -d` 와 같다 |

확인:

```bash
docker compose ps
docker compose logs
docker compose logs -f app
```

브라우저는 전과 같다. `http://localhost:3000`  
정상이면 인사말과 함께 `Redis에서도 안녕` 이 보인다.

컨테이너 안으로 들어가기 (서비스 이름 사용):

```bash
docker compose exec app sh
```

끄기:

```bash
docker compose down
```


컨테이너와 네트워크를 지운다. **볼륨 `redis-data`는 남는다.**  
볼륨까지 지우려면:

```bash
docker compose down -v
```

지금은 `-v` 없이 `down`만 쓰는 걸 권한다.

`docker ps`로도 보이지만, 이름이 `docker-test-app-1`, `docker-test-redis-1` 처럼 붙는다.  
폴더 이름 + 서비스 이름 + 번호다.

포트 3000이 이미 쓰 중이면 왼쪽만 바꾸면 된다.

```yaml
ports:
  - "3001:3000"
```

브라우저는 `http://localhost:3001` . 컨테이너 안 앱은 여전히 3000이다.

---

### `app.js`를 고쳤는데 반영이 안 되는 이유

컨테이너가 실행하는 건 **지금 PC의 `app.js`가 아니라, 이미지 안에 복사된 `app.js`**다.

이미지는 빌드 순간의 스냅샷이다. Cursor에서 저장해도 이미지 속 파일은 그대로다.

`docker compose up` 은 이미 만들어 둔 이미지를 재사용한다.  
그래서 코드만 고치고 `up`만 치면 예전 내용이 그대로 나온다.

반영하는 방법은 두 가지다.

#### 방법 1: 이미지를 다시 빌드 (기본)

```bash
docker compose up --build -d
```

`--build`가 Dockerfile의 `COPY . .`를 다시 실행해서, 지금 `app.js`를 이미지에 넣는다.  
배포할 때, 또는 의존성(`package.json`)이 바뀌었을 때 이 방식이다.

`up`만 치는 것과 `--build`를 붙이는 것의 차이:

| 명령 | 하는 일 |
| --- | --- |
| `docker compose up -d` | 있는 이미지로 컨테이너만 다시 띄움. 코드 변경 없음 |
| `docker compose up --build -d` | 이미지부터 다시 만들고 띄움. `app.js` 반영됨 |

#### 방법 2: 바인드 마운트 (개발할 때)

매번 빌드하기 싫으면, PC의 `app.js`를 컨테이너 경로에 붙인다.  
`docker-compose.yml`의 `app` 서비스에 `volumes`를 추가한다.

```yaml
  app:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - ./app.js:/app/app.js
    environment:
      PORT: "3000"
      REDIS_URL: redis://redis:6379
    depends_on:
      - redis
```

`./app.js` = 지금 폴더의 파일  
`/app/app.js` = 컨테이너 안 파일

이러면 이미지 속 파일을 PC 파일이 덮는다. `--build` 없이 저장한 내용이 컨테이너에 보인다.

다만 `node app.js`는 파일 변경을 자동으로 다시 읽지 않는다.  
저장한 뒤 앱 프로세스만 재시작한다.

```bash
docker compose restart app
```

Redis는 그대로 두고 `app`만 재시작한다.

폴더 전체 `./:/app` 는 쓰지 않는다. 윈도우 `node_modules`가 리눅스 `/app`을 덮을 수 있다.

정리:

- **배포 / 의존성 변경** → `docker compose up --build -d`
- **개발 중 코드만 수정** → 바인드 마운트 + `docker compose restart app`

---

### Postgres 서비스와 앱 연동

MySQL보다 환경변수가 단순해서 DB는 Postgres로 둔다. Redis는 그대로 두고 `db` 서비스만 추가한다.

```yaml
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: mydb
    ports:
      - "5432:5432"
    volumes:
      - db_data:/var/lib/postgresql/data
```

| 항목 | 의미 |
| --- | --- |
| `POSTGRES_USER` / `PASSWORD` / `DB` | 컨테이너가 처음 뜰 때 계정과 DB를 만들어 줌 |
| `5432:5432` | PC에서 DBeaver 등으로 붙일 때. 앱끼리만 쓰면 없어도 됨 |
| `db_data:/var/lib/postgresql/data` | 명명 볼륨. 컨테이너를 지워도 DB 데이터는 남음 |

앱은 서비스 이름 **`db`** 로 접속한다. `127.0.0.1`이 아니다.

```yaml
POSTGRES_HOST: db
POSTGRES_USER: myuser
POSTGRES_PASSWORD: mypassword
POSTGRES_DB: mydb
```

`app.js`는 `pg`로 `SELECT NOW()` 한 번 실행해서 연결을 확인한다.

```bash
docker compose up --build -d
```

`package.json`에 `pg`가 추가됐으므로 `--build`가 필요하다.  
`http://localhost:3000` 에 Redis 메시지와 `Postgres 연결됨: (시간)` 이 같이 보이면 성공이다.

PC에서 DB툴로 볼 때는 `localhost:5432`, 계정 `myuser` / `mypassword`, DB `mydb`.  
5432가 이미 쓰 중이면 왼쪽만 바꾼다. 예: `"5433:5432"`

---

## 지금까지의 흐름 정리

```
1. 앱 작성 (app.js)
2. Dockerfile 작성
3. .dockerignore 작성
4. docker build / docker run        ← 컨테이너 하나
5. docker logs / docker exec
6. docker stop / docker rm
7. -v 명명 볼륨 / 바인드 마운트
8. docker-compose.yml               ← 앱 + Redis + Postgres
9. docker compose up --build -d     ← 코드/패키지 반영하려면 --build
10. localhost:3000 에서 Redis, Postgres 값 확인
11. docker compose down
```
