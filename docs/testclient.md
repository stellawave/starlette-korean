테스트 클라이언트를 사용하면 `httpx` 라이브러리를 사용하여 ASGI 애플리케이션에 대한 요청을 만들 수 있습니다.

```python
from starlette.responses import HTMLResponse
from starlette.testclient import TestClient


async def app(scope, receive, send):
    assert scope['type'] == 'http'
    response = HTMLResponse('<html><body>안녕하세요, 세계!</body></html>')
    await response(scope, receive, send)


def test_app():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == 200
```

테스트 클라이언트는 다른 `httpx` 세션과 동일한 인터페이스를 제공합니다.
특히 요청을 만들기 위한 호출은 단순한 표준 함수 호출이며, 비동기 함수가 아닙니다.

인증, 세션 쿠키 처리 또는 파일 업로드와 같은 `httpx`의 표준 API를 사용할 수 있습니다.

예를 들어, TestClient에서 헤더를 설정하려면 다음과 같이 할 수 있습니다:

```python
client = TestClient(app)

# 향후 요청을 위해 클라이언트에 헤더 설정
client.headers = {"Authorization": "..."}
response = client.get("/")

# 각 요청마다 별도로 헤더 설정
response = client.get("/", headers={"Authorization": "..."})
```

그리고 예를 들어 TestClient로 파일을 보내려면:

```python
client = TestClient(app)

# 단일 파일 보내기
with open("example.txt", "rb") as f:
    response = client.post("/form", files={"file": f})

# 여러 파일 보내기
with open("example.txt", "rb") as f1:
    with open("example.png", "rb") as f2:
        files = {"file1": f1, "file2": ("filename", f2, "image/png")}
        response = client.post("/form", files=files)
```

더 자세한 정보는 `httpx` [문서](https://www.python-httpx.org/advanced/)를 확인할 수 있습니다.

기본적으로 `TestClient`는 애플리케이션에서 발생하는 모든 예외를 발생시킵니다. 때때로 서버 예외를 발생시키는 대신 500 오류 응답의 내용을 테스트하고 싶을 수 있습니다. 이 경우 `client = TestClient(app, raise_server_exceptions=False)`를 사용해야 합니다.

!!! 주의

    `TestClient`가 `lifespan` 핸들러를 실행하도록 하려면,
    `TestClient`를 컨텍스트 매니저로 사용해야 합니다. `TestClient`가 
    인스턴스화될 때는 트리거되지 않습니다. 이에 대해 
    [여기](lifespan.md#running-lifespan-in-tests)에서 더 자세히 알아볼 수 있습니다.

### 비동기 백엔드 선택

`TestClient`는 `backend` (문자열)와 `backend_options` (딕셔너리) 인자를 받습니다.
이 옵션들은 `anyio.start_blocking_portal()`에 전달됩니다. 허용되는 백엔드 옵션에 대한 
자세한 정보는 [anyio 문서](https://anyio.readthedocs.io/en/stable/basics.html#backend-options)를 
참조하세요.
기본적으로 `asyncio`가 기본 옵션과 함께 사용됩니다.

`Trio`를 실행하려면 `backend="trio"`를 전달하세요. 예를 들어:

```python
def test_app()
    with TestClient(app, backend="trio") as client:
       ...
```

`uvloop`과 함께 `asyncio`를 실행하려면 `backend_options={"use_uvloop": True}`를 전달하세요. 예를 들어:

```python
def test_app()
    with TestClient(app, backend_options={"use_uvloop": True}) as client:
       ...
```

### WebSocket 세션 테스트하기

테스트 클라이언트를 사용하여 웹소켓 세션도 테스트할 수 있습니다.

초기 핸드셰이크를 구축하기 위해 `httpx` 라이브러리가 사용되므로, HTTP와 웹소켓 테스트 간에 동일한 인증 옵션과 기타 헤더를 사용할 수 있습니다.

```python
from starlette.testclient import TestClient
from starlette.websockets import WebSocket


async def app(scope, receive, send):
    assert scope['type'] == 'websocket'
    websocket = WebSocket(scope, receive=receive, send=send)
    await websocket.accept()
    await websocket.send_text('Hello, world!')
    await websocket.close()


def test_app():
    client = TestClient(app)
    with client.websocket_connect('/') as websocket:
        data = websocket.receive_text()
        assert data == 'Hello, world!'
```

세션의 작업들은 표준 함수 호출이며, await 가능한 것이 아닙니다.

세션을 컨텍스트 관리 `with` 블록 내에서 사용하는 것이 중요합니다. 이는 ASGI 애플리케이션이 실행되는 백그라운드 스레드가 적절히 종료되고, 애플리케이션 내에서 발생하는 모든 예외가 항상 테스트 클라이언트에 의해 발생되도록 보장합니다.

#### 테스트 세션 설정하기

* `.websocket_connect(url, subprotocols=None, **options)` - `httpx.get()`와 동일한 인자 집합을 받습니다.

애플리케이션이 웹소켓 연결을 수락하지 않으면 `starlette.websockets.WebSocketDisconnect`를 발생시킬 수 있습니다.

`websocket_connect()`는 반드시 컨텍스트 관리자(`with` 블록)로 사용되어야 합니다.

!!! note
    `params` 인자는 `websocket_connect`에서 지원되지 않습니다. 쿼리 인자를 전달해야 하는 경우, URL에 직접 하드코딩하세요.

    ```python
    with client.websocket_connect('/path?foo=bar') as websocket:
        ...
    ```

#### 데이터 보내기

* `.send_text(data)` - 주어진 텍스트를 애플리케이션에 보냅니다.
* `.send_bytes(data)` - 주어진 바이트를 애플리케이션에 보냅니다.
* `.send_json(data, mode="text")` - 주어진 데이터를 애플리케이션에 보냅니다. 바이너리 데이터 프레임을 통해 JSON을 보내려면 `mode="binary"`를 사용하세요.

#### 데이터 받기

* `.receive_text()` - 애플리케이션이 보낸 들어오는 텍스트를 기다리고 반환합니다.
* `.receive_bytes()` - 애플리케이션이 보낸 들어오는 바이트 문자열을 기다리고 반환합니다.
* `.receive_json(mode="text")` - 애플리케이션이 보낸 들어오는 json 데이터를 기다리고 반환합니다. 바이너리 데이터 프레임을 통해 JSON을 받으려면 `mode="binary"`를 사용하세요.

`starlette.websockets.WebSocketDisconnect`를 발생시킬 수 있습니다.

#### 연결 닫기

* `.close(code=1000)` - 웹소켓 연결의 클라이언트 측 종료를 수행합니다.

### 비동기 테스트

때로는 애플리케이션 외부에서 비동기 작업을 수행해야 할 수 있습니다.
예를 들어, 기존의 비동기 데이터베이스 클라이언트/인프라를 사용하여 앱을 호출한 후 데이터베이스 상태를 확인하고 싶을 수 있습니다.

이러한 상황에서는 `TestClient`를 사용하기 어렵습니다. 왜냐하면 `TestClient`는 자체 이벤트 루프를 생성하고, 데이터베이스 연결과 같은 비동기 리소스는 종종 이벤트 루프 간에 공유될 수 없기 때문입니다.
이를 해결하는 가장 간단한 방법은 전체 테스트를 비동기로 만들고 [httpx.AsyncClient]와 같은 비동기 클라이언트를 사용하는 것입니다.

다음은 그러한 테스트의 예시입니다:

```python
from httpx import AsyncClient
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import PlainTextResponse


def hello(request: Request) -> PlainTextResponse:
    return PlainTextResponse("Hello World!")


app = Starlette(routes=[Route("/", hello)])


# pytest를 사용하는 경우, 다음과 같은 비동기 마커를 추가해야 합니다:
# @pytest.mark.anyio  # https://github.com/agronholm/anyio 사용
# 또는 pytest-asyncio를 설치하고 구성하세요 (https://github.com/pytest-dev/pytest-asyncio)
async def test_app() -> None:
    # 주의: "/" 같은 상대 URL이 작동하려면 반드시 `base_url`을 설정해야 합니다
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        r = await client.get("/")
        assert r.status_code == 200
        assert r.text == "Hello World!"
```

[httpx.AsyncClient]: https://www.python-httpx.org/advanced/#calling-into-python-web-apps
