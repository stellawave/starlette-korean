Starlette는 HTTP 메서드 디스패칭과 WebSocket 세션을 처리하기 위한 클래스 기반 뷰 패턴을 제공하는 `HTTPEndpoint`와 `WebSocketEndpoint` 클래스를 포함합니다.

### HTTPEndpoint

`HTTPEndpoint` 클래스는 ASGI 애플리케이션으로 사용될 수 있습니다:

```python
from starlette.responses import PlainTextResponse
from starlette.endpoints import HTTPEndpoint


class App(HTTPEndpoint):
    async def get(self, request):
        return PlainTextResponse(f"안녕하세요, 세상!")
```

Starlette 애플리케이션 인스턴스를 사용하여 라우팅을 처리하는 경우, `HTTPEndpoint` 클래스로 디스패치할 수 있습니다. 클래스의 인스턴스가 아닌 클래스 자체로 디스패치해야 합니다:

```python
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.endpoints import HTTPEndpoint
from starlette.routing import Route


class Homepage(HTTPEndpoint):
    async def get(self, request):
        return PlainTextResponse(f"안녕하세요, 세상!")


class User(HTTPEndpoint):
    async def get(self, request):
        username = request.path_params['username']
        return PlainTextResponse(f"안녕하세요, {username}")

routes = [
    Route("/", Homepage),
    Route("/{username}", User)
]

app = Starlette(routes=routes)
```

HTTP 엔드포인트 클래스는 해당 핸들러에 매핑되지 않는 요청 메서드에 대해 "405 Method not allowed" 응답을 반환합니다.

### WebSocketEndpoint

`WebSocketEndpoint` 클래스는 `WebSocket` 인스턴스의 기능을 감싸는 ASGI 애플리케이션입니다.

ASGI 연결 스코프는 엔드포인트 인스턴스의 `.scope`를 통해 접근할 수 있으며, `on_receive` 메서드에서 예상되는 웹소켓 데이터를 검증하기 위해 선택적으로 설정할 수 있는 `encoding` 속성을 가지고 있습니다.

인코딩 유형은 다음과 같습니다:

* `'json'`
* `'bytes'`
* `'text'`

특정 ASGI 웹소켓 메시지 유형을 처리하기 위해 재정의할 수 있는 세 가지 메서드가 있습니다:

* `async def on_connect(websocket, **kwargs)`
* `async def on_receive(websocket, data)`
* `async def on_disconnect(websocket, close_code)`

```python
from starlette.endpoints import WebSocketEndpoint


class App(WebSocketEndpoint):
    encoding = 'bytes'

    async def on_connect(self, websocket):
        await websocket.accept()

    async def on_receive(self, websocket, data):
        await websocket.send_bytes(b"Message: " + data)

    async def on_disconnect(self, websocket, close_code):
        pass
```

`WebSocketEndpoint`는 `Starlette` 애플리케이션 클래스와 함께 사용할 수도 있습니다:

```python
import uvicorn
from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint, HTTPEndpoint
from starlette.responses import HTMLResponse
from starlette.routing import Route, WebSocketRoute


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

class Homepage(HTTPEndpoint):
    async def get(self, request):
        return HTMLResponse(html)

class Echo(WebSocketEndpoint):
    encoding = "text"

    async def on_receive(self, websocket, data):
        await websocket.send_text(f"Message text was: {data}")

routes = [
    Route("/", Homepage),
    WebSocketRoute("/ws", Echo)
]

app = Starlette(routes=routes)
```
