## HTTP Routing

Starlette는 간단하지만 강력한 요청 라우팅 시스템을 가지고 있습니다. 라우팅 테이블은 라우트 목록으로 정의되며, 애플리케이션을 인스턴스화할 때 전달됩니다.

```python
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route


async def homepage(request):
    return PlainTextResponse("홈페이지")

async def about(request):
    return PlainTextResponse("소개")


routes = [
    Route("/", endpoint=homepage),
    Route("/about", endpoint=about),
]

app = Starlette(routes=routes)
```

`endpoint` 인자는 다음 중 하나일 수 있습니다:

* 단일 `request` 인자를 받고 응답을 반환해야 하는 일반 함수 또는 비동기 함수.
* Starlette의 [HTTPEndpoint](endpoints.md#httpendpoint)와 같이 ASGI 인터페이스를 구현하는 클래스.

## 경로 매개변수

경로는 URI 템플릿 스타일을 사용하여 경로 구성 요소를 캡처할 수 있습니다.

```python
Route('/users/{username}', user)
```
기본적으로 이는 경로 끝 또는 다음 `/`까지의 문자를 캡처합니다.

컨버터를 사용하여 캡처되는 내용을 수정할 수 있습니다. 사용 가능한 컨버터는 다음과 같습니다:

* `str`은 문자열을 반환하며, 기본값입니다.
* `int`는 Python 정수를 반환합니다.
* `float`는 Python 부동 소수점 숫자를 반환합니다.
* `uuid`는 Python `uuid.UUID` 인스턴스를 반환합니다.
* `path`는 추가적인 `/` 문자를 포함한 나머지 경로를 반환합니다.

컨버터는 다음과 같이 콜론을 앞에 붙여 사용합니다:

```python
Route('/users/{user_id:int}', user)
Route('/floating-point/{number:float}', floating_point)
Route('/uploaded/{rest_of_path:path}', uploaded)
```

정의되지 않은 다른 컨버터가 필요한 경우 직접 만들 수 있습니다.
아래는 `datetime` 컨버터를 만들고 등록하는 방법의 예시입니다:

```python
from datetime import datetime

from starlette.convertors import Convertor, register_url_convertor


class DateTimeConvertor(Convertor):
    regex = "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(.[0-9]+)?"

    def convert(self, value: str) -> datetime:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")

    def to_string(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%dT%H:%M:%S")

register_url_convertor("datetime", DateTimeConvertor())
```

등록 후에는 다음과 같이 사용할 수 있습니다:

```python
Route('/history/{date:datetime}', history)
```

경로 매개변수는 `request.path_params` 사전에서 사용할 수 있습니다.

```python
async def user(request):
    user_id = request.path_params['user_id']
    ...
```

## HTTP 메서드 처리

라우트는 엔드포인트가 처리하는 HTTP 메서드도 지정할 수 있습니다:

```python
Route('/users/{user_id:int}', user, methods=["GET", "POST"])
```

기본적으로 함수 엔드포인트는 지정하지 않는 한 `GET` 요청만 허용합니다.

## 경로 서브마운팅

대규모 애플리케이션에서는 공통 경로 접두사를 기반으로 라우팅 테이블의 일부를 분리하고 싶을 수 있습니다.

```python
routes = [
    Route('/', homepage),
    Mount('/users', routes=[
        Route('/', users, methods=['GET', 'POST']),
        Route('/{username}', user),
    ])
]
```

이 스타일을 사용하면 프로젝트의 다른 부분에서 라우팅 테이블의 다른 하위 집합을 정의할 수 있습니다.

```python
from myproject import users, auth

routes = [
    Route('/', homepage),
    Mount('/users', routes=users.routes),
    Mount('/auth', routes=auth.routes),
]
```

마운팅을 사용하여 Starlette 애플리케이션 내에 하위 애플리케이션을 포함할 수도 있습니다. 예를 들어...

```python
# 이것은 독립형 정적 파일 서버입니다:
app = StaticFiles(directory="static")

# 이것은 Starlette 애플리케이션 내에서 "/static" 경로 아래에 마운트된 
# 정적 파일 서버입니다.
routes = [
    ...
    Mount("/static", app=StaticFiles(directory="static"), name="static")
]

app = Starlette(routes=routes)
```

## URL 역방향 조회

특히 리다이렉트 응답을 반환해야 하는 경우와 같이 특정 경로의 URL을 생성해야 할 때가 자주 있습니다.

* 시그니처: `url_for(name, **path_params) -> URL`

```python
routes = [
    Route("/", homepage, name="homepage")
]

# 다음을 사용하여 URL을 반환할 수 있습니다...
url = request.url_for("homepage")
```

URL 조회에는 경로 매개변수가 포함될 수 있습니다...

```python
routes = [
    Route("/users/{username}", user, name="user_detail")
]

# 다음을 사용하여 URL을 반환할 수 있습니다...
url = request.url_for("user_detail", username=...)
```

`Mount`에 `name`이 포함된 경우, 하위 마운트는 역방향 URL 조회를 위해 `{prefix}:{name}` 스타일을 사용해야 합니다.

```python
routes = [
    Mount("/users", name="users", routes=[
        Route("/", user, name="user_list"),
        Route("/{username}", user, name="user_detail")
    ])
]

# 다음을 사용하여 URL을 반환할 수 있습니다...
url = request.url_for("users:user_list")
url = request.url_for("users:user_detail", username=...)
```

마운트된 애플리케이션에는 `path=...` 매개변수가 포함될 수 있습니다.

```python
routes = [
    ...
    Mount("/static", app=StaticFiles(directory="static"), name="static")
]

# 다음을 사용하여 URL을 반환할 수 있습니다...
url = request.url_for("static", path="/css/base.css")
```

`request` 인스턴스가 없는 경우, 애플리케이션에 대해 역방향 조회를 수행할 수 있지만 이는 URL 경로만 반환합니다.

```python
url = app.url_path_for("user_detail", username=...)
```

## 호스트 기반 라우팅

`Host` 헤더를 기반으로 동일한 경로에 대해 다른 라우트를 사용하려는 경우입니다.

매칭 시 `Host` 헤더에서 포트가 제거된다는 점에 유의하세요.
예를 들어, `Host (host='example.org:3600', ...)`는 
`Host` 헤더에 `3600` 이외의 포트가 포함되어 있거나 포트가 없는 경우에도
(`example.org:5600`, `example.org`) 처리됩니다.
따라서 `url_for`에서 사용하기 위해 필요한 경우 포트를 지정할 수 있습니다.

호스트 기반 라우트를 애플리케이션에 연결하는 여러 가지 방법이 있습니다.

```python
site = Router()  # 예: `@site.route()`를 사용하여 구성합니다.
api = Router()   # 예: `@api.route()`를 사용하여 구성합니다.
news = Router()  # 예: `@news.route()`를 사용하여 구성합니다.

routes = [
    Host('api.example.org', api, name="site_api")
]

app = Starlette(routes=routes)

app.host('www.example.org', site, name="main_site")

news_host = Host('news.example.org', news)
app.router.routes.append(news_host)
```

URL 조회는 경로 매개변수와 마찬가지로 호스트 매개변수를 포함할 수 있습니다.

```python
routes = [
    Host("{subdomain}.example.org", name="sub", app=Router(routes=[
        Mount("/users", name="users", routes=[
            Route("/", user, name="user_list"),
            Route("/{username}", user, name="user_detail")
        ])
    ]))
]
...
url = request.url_for("sub:users:user_detail", username=..., subdomain=...)
url = request.url_for("sub:users:user_list", subdomain=...)
```

## 라우트 우선순위

들어오는 경로는 각 `Route`에 대해 순서대로 매칭됩니다.

하나 이상의 라우트가 들어오는 경로와 일치할 수 있는 경우, 
더 구체적인 라우트가 일반적인 경우보다 먼저 나열되도록 주의해야 합니다.

예를 들어:

```python
# 이렇게 하지 마세요: `/users/me`는 절대 들어오는 요청과 일치하지 않습니다.
routes = [
    Route('/users/{username}', user),
    Route('/users/me', current_user),
]

# 이렇게 하세요: `/users/me`가 먼저 테스트됩니다.
routes = [
    Route('/users/me', current_user),
    Route('/users/{username}', user),
]
```

## Router 인스턴스 작업

저수준에서 작업하는 경우 `Starlette` 애플리케이션을 생성하는 대신 
일반 `Router` 인스턴스를 사용하고 싶을 수 있습니다. 
이렇게 하면 미들웨어로 래핑하지 않고 애플리케이션 라우팅만 제공하는 
경량 ASGI 애플리케이션을 얻을 수 있습니다.

```python
app = Router(routes=[
    Route('/', homepage),
    Mount('/users', routes=[
        Route('/', users, methods=['GET', 'POST']),
        Route('/{username}', user),
    ])
])
```

## WebSocket 라우팅

WebSocket 엔드포인트로 작업할 때는 일반적인 `Route` 대신 `WebSocketRoute`를 
사용해야 합니다.

`WebSocketRoute`의 경로 매개변수와 역방향 URL 조회는 
위의 HTTP [Route](#http-routing) 섹션에서 찾을 수 있는 HTTP `Route`와 동일하게 작동합니다.

```python
from starlette.applications import Starlette
from starlette.routing import WebSocketRoute


async def websocket_index(websocket):
    await websocket.accept()
    await websocket.send_text("Hello, websocket!")
    await websocket.close()


async def websocket_user(websocket):
    name = websocket.path_params["name"]
    await websocket.accept()
    await websocket.send_text(f"Hello, {name}")
    await websocket.close()


routes = [
    WebSocketRoute("/", endpoint=websocket_index),
    WebSocketRoute("/{name}", endpoint=websocket_user),
]

app = Starlette(routes=routes)
```

`endpoint` 인수는 다음 중 하나일 수 있습니다:

* 단일 `websocket` 인수를 받는 비동기 함수.
* Starlette의 [WebSocketEndpoint](endpoints.md#websocketendpoint)와 같이 ASGI 인터페이스를 구현하는 클래스.
