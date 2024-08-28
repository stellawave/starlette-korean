Starlette는 다른 모든 기능을 잘 연결하는 `Starlette`라는 애플리케이션 클래스를 포함하고 있습니다.

```python
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles


def homepage(request):
    return PlainTextResponse('안녕하세요, 세계!')

def user_me(request):
    username = "John Doe"
    return PlainTextResponse('안녕하세요, %s님!' % username)

def user(request):
    username = request.path_params['username']
    return PlainTextResponse('안녕하세요, %s님!' % username)

async def websocket_endpoint(websocket):
    await websocket.accept()
    await websocket.send_text('안녕하세요, 웹소켓!')
    await websocket.close()

def startup():
    print('준비 완료')


routes = [
    Route('/', homepage),
    Route('/user/me', user_me),
    Route('/user/{username}', user),
    WebSocketRoute('/ws', websocket_endpoint),
    Mount('/static', StaticFiles(directory="static")),
]

app = Starlette(debug=True, routes=routes, on_startup=[startup])
```

### 애플리케이션 인스턴스화

::: starlette.applications.Starlette
    :docstring:

### 앱 인스턴스에 상태 저장하기

제네릭 `app.state` 속성을 사용하여 애플리케이션 인스턴스에 임의의 추가 상태를 저장할 수 있습니다.

예를 들어:

```python
app.state.ADMIN_EMAIL = 'admin@example.org'
```

### 앱 인스턴스에 접근하기

`request`가 사용 가능한 곳(즉, 엔드포인트와 미들웨어)에서는 `request.app`을 통해 앱에 접근할 수 있습니다.
