Starlette는 HTTP 요청과 유사한 역할을 수행하지만 웹소켓을 통해 데이터를 송수신할 수 있는 `WebSocket` 클래스를 포함하고 있습니다.

### WebSocket

시그니처: `WebSocket(scope, receive=None, send=None)`

```python
from starlette.websockets import WebSocket


async def app(scope, receive, send):
    websocket = WebSocket(scope=scope, receive=receive, send=send)
    await websocket.accept()
    await websocket.send_text('Hello, world!')
    await websocket.close()
```

WebSocket은 매핑 인터페이스를 제공하므로 `scope`와 동일한 방식으로 사용할 수 있습니다.

예를 들어: `websocket['path']`는 ASGI 경로를 반환합니다.

#### URL

웹소켓 URL은 `websocket.url`로 접근합니다.

이 속성은 실제로 `str`의 하위 클래스이며, URL에서 파싱할 수 있는 모든 구성 요소도 노출합니다.

예: `websocket.url.path`, `websocket.url.port`, `websocket.url.scheme`.

#### 헤더

헤더는 불변의, 대소문자를 구분하지 않는 멀티 딕셔너리로 노출됩니다.

예: `websocket.headers['sec-websocket-version']`

#### 쿼리 파라미터

쿼리 파라미터는 불변의 멀티 딕셔너리로 노출됩니다.

예: `websocket.query_params['search']`

#### 경로 파라미터

라우터 경로 파라미터는 딕셔너리 인터페이스로 노출됩니다.

예: `websocket.path_params['username']`

### 연결 수락

* `await websocket.accept(subprotocol=None, headers=None)`

### 데이터 전송

* `await websocket.send_text(data)`
* `await websocket.send_bytes(data)`
* `await websocket.send_json(data)`

JSON 메시지는 기본적으로 버전 0.10.0부터 텍스트 데이터 프레임을 통해 전송됩니다.
바이너리 데이터 프레임을 통해 JSON을 전송하려면 `websocket.send_json(data, mode="binary")`를 사용하세요.

### 데이터 수신

* `await websocket.receive_text()`
* `await websocket.receive_bytes()`
* `await websocket.receive_json()`

`starlette.websockets.WebSocketDisconnect()`를 발생시킬 수 있습니다.

JSON 메시지는 기본적으로 버전 0.10.0부터 텍스트 데이터 프레임을 통해 수신됩니다.
바이너리 데이터 프레임을 통해 JSON을 수신하려면 `websocket.receive_json(data, mode="binary")`를 사용하세요.

### 데이터 반복

* `websocket.iter_text()`
* `websocket.iter_bytes()`
* `websocket.iter_json()`

`receive_text`, `receive_bytes`, `receive_json`와 유사하지만 비동기 이터레이터를 반환합니다.

```python hl_lines="7-8"
from starlette.websockets import WebSocket


async def app(scope, receive, send):
    websocket = WebSocket(scope=scope, receive=receive, send=send)
    await websocket.accept()
    async for message in websocket.iter_text():
        await websocket.send_text(f"Message text was: {message}")
    await websocket.close()
```

`starlette.websockets.WebSocketDisconnect`가 발생하면 이터레이터가 종료됩니다.

### 연결 종료

* `await websocket.close(code=1000, reason=None)`

### 메시지 송수신

원시 ASGI 메시지를 송수신해야 하는 경우, 원시 `send`와 `receive` 콜러블 대신 `websocket.send()`와 `websocket.receive()`를 사용해야 합니다. 이렇게 하면 웹소켓의 상태가 올바르게 업데이트됩니다.

* `await websocket.send(message)`
* `await websocket.receive()`

### 거부 응답 전송

`websocket.accept()`를 호출하기 전에 `websocket.close()`를 호출하면 서버는 자동으로 HTTP 403 에러를 클라이언트에 전송합니다.

다른 에러 응답을 보내고 싶다면 `websocket.send_denial_response()` 메서드를 사용할 수 있습니다. 이 메서드는 응답을 보내고 연결을 종료합니다.

* `await websocket.send_denial_response(response)`

이를 위해서는 ASGI 서버가 WebSocket Denial Response 확장을 지원해야 합니다. 지원되지 않는 경우 `RuntimeError`가 발생합니다.
