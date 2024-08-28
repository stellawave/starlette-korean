Starlette는 전체 애플리케이션에 적용되는 동작을 추가하기 위한 여러 미들웨어 클래스를 포함하고 있습니다. 이들은 모두 표준 ASGI 미들웨어 클래스로 구현되어 있으며, Starlette나 다른 ASGI 애플리케이션에 적용할 수 있습니다.

## Using middleware

Starlette 애플리케이션 클래스를 사용하면 예외 핸들러로 감싸진 상태를 유지하면서 ASGI 미들웨어를 포함할 수 있습니다.

```python
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

routes = ...

# 모든 요청에 'example.com' 또는 '*.example.com' 호스트 헤더가 포함되도록 하고,
# https-only 접근을 엄격하게 강제합니다.
middleware = [
    Middleware(
        TrustedHostMiddleware,
        allowed_hosts=['example.com', '*.example.com'],
    ),
    Middleware(HTTPSRedirectMiddleware)
]

app = Starlette(routes=routes, middleware=middleware)
```

모든 Starlette 애플리케이션은 기본적으로 두 가지 미들웨어를 자동으로 포함합니다:

* `ServerErrorMiddleware` - 애플리케이션 예외가 사용자 정의 500 페이지를 반환하거나 DEBUG 모드에서 애플리케이션 트레이스백을 표시할 수 있도록 합니다. 이는 *항상* 가장 바깥쪽 미들웨어 계층입니다.
* `ExceptionMiddleware` - 예외 핸들러를 추가하여 특정 유형의 예상된 예외 케이스를 핸들러 함수와 연결할 수 있게 합니다. 예를 들어, 엔드포인트 내에서 `HTTPException(status_code=404)`를 발생시키면 사용자 정의 404 페이지가 렌더링됩니다.

미들웨어는 위에서 아래로 평가되므로, 예제 애플리케이션의 실행 흐름은 다음과 같습니다:

* 미들웨어
    * `ServerErrorMiddleware`
    * `TrustedHostMiddleware`
    * `HTTPSRedirectMiddleware`
    * `ExceptionMiddleware`
* 라우팅
* 엔드포인트

Starlette 패키지에서 사용 가능한 미들웨어 구현은 다음과 같습니다:

## CORSMiddleware

브라우저에서의 교차 출처 요청을 허용하기 위해 나가는 응답에 적절한 [CORS 헤더](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)를 추가합니다.

CORSMiddleware 구현에서 사용되는 기본 매개변수는 기본적으로 제한적이므로, 브라우저가 교차 도메인 컨텍스트에서 특정 출처, 메서드 또는 헤더를 사용할 수 있도록 허용하려면 명시적으로 활성화해야 합니다.

```python
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

routes = ...

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'])
]

app = Starlette(routes=routes, middleware=middleware)
```

다음 인자들이 지원됩니다:

* `allow_origins` - 교차 출처 요청을 허용해야 하는 출처 목록입니다. 예: `['https://example.org', 'https://www.example.org']`. `['*']`를 사용하여 모든 출처를 허용할 수 있습니다.
* `allow_origin_regex` - 교차 출처 요청을 허용해야 하는 출처와 일치시킬 정규식 문자열입니다. 예: `'https://.*\.example\.org'`.
* `allow_methods` - 교차 출처 요청에 대해 허용되어야 하는 HTTP 메서드 목록입니다. 기본값은 `['GET']`입니다. `['*']`를 사용하여 모든 표준 메서드를 허용할 수 있습니다.
* `allow_headers` - 교차 출처 요청에 대해 지원되어야 하는 HTTP 요청 헤더 목록입니다. 기본값은 `[]`입니다. `['*']`를 사용하여 모든 헤더를 허용할 수 있습니다. `Accept`, `Accept-Language`, `Content-Language`, `Content-Type` 헤더는 CORS 요청에 대해 항상 허용됩니다.
* `allow_credentials` - 교차 출처 요청에 대해 쿠키를 지원해야 함을 나타냅니다. 기본값은 `False`입니다. 또한 자격 증명을 허용하려면 `allow_origins`, `allow_methods`, `allow_headers`를 `['*']`로 설정할 수 없으며, 모두 명시적으로 지정해야 합니다.
* `expose_headers` - 브라우저에서 접근 가능해야 하는 응답 헤더를 나타냅니다. 기본값은 `[]`입니다.
* `max_age` - 브라우저가 CORS 응답을 캐시하는 최대 시간(초)을 설정합니다. 기본값은 `600`입니다.

미들웨어는 두 가지 특정 유형의 HTTP 요청에 응답합니다...

#### CORS 프리플라이트 요청

`Origin`과 `Access-Control-Request-Method` 헤더가 있는 모든 `OPTIONS` 요청입니다. 이 경우 미들웨어는 들어오는 요청을 가로채고 적절한 CORS 헤더와 함께 정보 제공을 위해 200 또는 400 응답을 반환합니다.

#### 단순 요청

`Origin` 헤더가 있는 모든 요청입니다. 이 경우 미들웨어는 요청을 정상적으로 통과시키지만, 응답에 적절한 CORS 헤더를 포함시킵니다.

## SessionMiddleware

서명된 쿠키 기반 HTTP 세션을 추가합니다. 세션 정보는 읽을 수 있지만 수정할 수는 없습니다.

`request.session` 딕셔너리 인터페이스를 사용하여 세션 데이터에 접근하거나 수정합니다.

다음 인자들이 지원됩니다:

* `secret_key` - 무작위 문자열이어야 합니다.
* `session_cookie` - 기본값은 "session"입니다.
* `max_age` - 세션 만료 시간(초)입니다. 기본값은 2주입니다. `None`으로 설정하면 쿠키가 브라우저 세션 동안 유지됩니다.
* `same_site` - SameSite 플래그는 브라우저가 교차 사이트 요청과 함께 세션 쿠키를 보내는 것을 방지합니다. 기본값은 `'lax'`입니다.
* `path` - 세션 쿠키에 설정된 경로입니다. 기본값은 `'/'`입니다.
* `https_only` - Secure 플래그를 설정해야 함을 나타냅니다(HTTPS에서만 사용 가능). 기본값은 `False`입니다.
* `domain` - 서브도메인 간 또는 교차 도메인 간 쿠키를 공유하는 데 사용되는 쿠키의 도메인입니다. 브라우저는 기본적으로 도메인을 쿠키를 설정한 동일한 호스트로 설정하며, 서브도메인은 제외합니다([참조](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies#domain_attribute)).

```python
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

routes = ...

middleware = [
    Middleware(SessionMiddleware, secret_key=..., https_only=True)
]

app = Starlette(routes=routes, middleware=middleware)
```

## HTTPSRedirectMiddleware

모든 들어오는 요청이 `https` 또는 `wss`여야 함을 강제합니다. `http` 또는 `ws`로 들어오는 모든 요청은 대신 보안 스키마로 리다이렉트됩니다.

```python
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

routes = ...

middleware = [
    Middleware(HTTPSRedirectMiddleware)
]

app = Starlette(routes=routes, middleware=middleware)
```

이 미들웨어 클래스에는 구성 옵션이 없습니다.

## TrustedHostMiddleware

HTTP 호스트 헤더 공격을 방지하기 위해 모든 들어오는 요청에 `Host` 헤더가 올바르게 설정되어 있는지 강제합니다.

```python
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

routes = ...

middleware = [
    Middleware(TrustedHostMiddleware, allowed_hosts=['example.com', '*.example.com'])
]

app = Starlette(routes=routes, middleware=middleware)
```

다음 인수가 지원됩니다:

* `allowed_hosts` - 호스트 이름으로 허용되어야 하는 도메인 이름 목록입니다. `*.example.com`과 같은 와일드카드 도메인이 서브도메인 매칭을 위해 지원됩니다. 모든 호스트 이름을 허용하려면 `allowed_hosts=["*"]`를 사용하거나 미들웨어를 생략하세요.
* `www_redirect` - True로 설정하면 허용된 호스트의 non-www 버전에 대한 요청이 www 버전으로 리다이렉트됩니다. 기본값은 `True`입니다.

들어오는 요청이 올바르게 검증되지 않으면 400 응답이 전송됩니다.

## GZipMiddleware

`Accept-Encoding` 헤더에 `"gzip"`이 포함된 모든 요청에 대해 GZip 응답을 처리합니다.

이 미들웨어는 표준 응답과 스트리밍 응답을 모두 처리합니다.

```python
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware


routes = ...

middleware = [
    Middleware(GZipMiddleware, minimum_size=1000, compresslevel=9)
]

app = Starlette(routes=routes, middleware=middleware)
```

다음 인수가 지원됩니다:

* `minimum_size` - 이 최소 크기(바이트)보다 작은 응답은 GZip 압축하지 않습니다. 기본값은 `500`입니다.
* `compresslevel` - GZip 압축 중 사용됩니다. 1에서 9 사이의 정수입니다. 기본값은 `9`입니다. 낮은 값은 더 빠른 압축을 제공하지만 파일 크기가 더 크고, 높은 값은 더 느린 압축을 제공하지만 파일 크기가 더 작습니다.

이 미들웨어는 이미 `Content-Encoding`이 설정된 응답은 두 번 인코딩되는 것을 방지하기 위해 GZip 압축하지 않습니다.

## BaseHTTPMiddleware

요청/응답 인터페이스에 대해 ASGI 미들웨어를 작성할 수 있게 해주는 추상 클래스입니다.

### 사용법

`BaseHTTPMiddleware`를 사용하여 미들웨어 클래스를 구현하려면 `async def dispatch(request, call_next)` 메서드를 오버라이드해야 합니다.

```python
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware


class CustomHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers['Custom'] = 'Example'
        return response

routes = ...

middleware = [
    Middleware(CustomHeaderMiddleware)
]

app = Starlette(routes=routes, middleware=middleware)
```

미들웨어 클래스에 설정 옵션을 제공하려면 `__init__` 메서드를 오버라이드해야 합니다. 첫 번째 인수가 `app`이고 나머지 인수는 선택적 키워드 인수여야 합니다. 이렇게 할 경우 인스턴스에 `app` 속성을 설정해야 합니다.

```python
class CustomHeaderMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, header_value='Example'):
        super().__init__(app)
        self.header_value = header_value

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers['Custom'] = self.header_value
        return response


middleware = [
    Middleware(CustomHeaderMiddleware, header_value='Customized')
]

app = Starlette(routes=routes, middleware=middleware)
```

미들웨어 클래스는 `__init__` 메서드 외부에서 상태를 수정하지 않아야 합니다. 대신 상태를 `dispatch` 메서드 내에서 로컬로 유지하거나 명시적으로 전달해야 하며, 미들웨어 인스턴스를 변경해서는 안 됩니다.

### Limitations

현재 `BaseHTTPMiddleware`에는 몇 가지 알려진 한계가 있습니다:

- `BaseHTTPMiddleware`를 사용하면 [`contextlib.ContextVar`](https://docs.python.org/3/library/contextvars.html#contextvars.ContextVar)의 변경 사항이 상위로 전파되지 않습니다. 즉, 엔드포인트에서 `ContextVar`의 값을 설정하고 미들웨어에서 읽으려고 하면 엔드포인트에서 설정한 값과 동일하지 않다는 것을 발견하게 됩니다 (이 동작의 예시는 [이 테스트](https://github.com/encode/starlette/blob/621abc747a6604825190b93467918a0ec6456a24/tests/middleware/test_base.py#L192-L223)를 참조하세요).

이러한 한계를 극복하려면 아래에 설명된 [순수 ASGI 미들웨어](#pure-asgi-middleware)를 사용하세요.

## pure asgi middleware

[ASGI 스펙](https://asgi.readthedocs.io/en/latest/)은 ASGI 인터페이스를 직접 사용하여 ASGI 미들웨어를 구현할 수 있게 합니다. 이는 다음 ASGI 애플리케이션을 호출하는 ASGI 애플리케이션 체인으로 구현됩니다. 실제로 Starlette에 포함된 미들웨어 클래스들이 이렇게 구현되어 있습니다.

이 저수준 접근 방식은 동작에 대한 더 큰 제어권과 프레임워크 및 서버 간의 향상된 상호 운용성을 제공합니다. 또한 [`BaseHTTPMiddleware`의 한계](#limitations)를 극복합니다.

### 순수 ASGI 미들웨어 작성하기

ASGI 미들웨어를 만드는 가장 일반적인 방법은 클래스를 사용하는 것입니다.

```python
class ASGIMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        await self.app(scope, receive, send)
```

위의 미들웨어는 가장 기본적인 ASGI 미들웨어입니다. 생성자 인수로 부모 ASGI 애플리케이션을 받고, 그 부모 애플리케이션을 호출하는 `async __call__` 메서드를 구현합니다.

[`asgi-cors`](https://github.com/simonw/asgi-cors/blob/10ef64bfcc6cd8d16f3014077f20a0fb8544ec39/asgi_cors.py)와 같은 일부 구현은 함수를 사용하는 대안적 스타일을 사용합니다:

```python
import functools

def asgi_middleware():
    def asgi_decorator(app):

        @functools.wraps(app)
        async def wrapped_app(scope, receive, send):
            await app(scope, receive, send)

        return wrapped_app

    return asgi_decorator
```

어떤 경우든, ASGI 미들웨어는 `scope`, `receive`, `send` 세 가지 인수를 받는 호출 가능한 객체여야 합니다.

* `scope`는 연결에 대한 정보를 담고 있는 딕셔너리입니다. `scope["type"]`은 다음 중 하나일 수 있습니다:
    * [`"http"`](https://asgi.readthedocs.io/en/latest/specs/www.html#http-connection-scope): HTTP 요청의 경우.
    * [`"websocket"`](https://asgi.readthedocs.io/en/latest/specs/www.html#websocket-connection-scope): WebSocket 연결의 경우.
    * [`"lifespan"`](https://asgi.readthedocs.io/en/latest/specs/lifespan.html#scope): ASGI 라이프스팬 메시지의 경우.
* `receive`와 `send`는 ASGI 서버와 ASGI 이벤트 메시지를 교환하는 데 사용할 수 있습니다 - 이에 대해서는 아래에서 더 자세히 설명합니다. 이 메시지의 유형과 내용은 스코프 유형에 따라 다릅니다. 자세한 내용은 [ASGI 명세](https://asgi.readthedocs.io/en/latest/specs/index.html)를 참조하세요.

### 순수 ASGI 미들웨어 사용하기

순수 ASGI 미들웨어는 다른 미들웨어와 마찬가지로 사용할 수 있습니다:

```python
from starlette.applications import Starlette
from starlette.middleware import Middleware

from .middleware import ASGIMiddleware

routes = ...

middleware = [
    Middleware(ASGIMiddleware),
]

app = Starlette(..., middleware=middleware)
```

[미들웨어 사용하기](#using-middleware)도 참조하세요.

### 타입 어노테이션

미들웨어에 어노테이션을 추가하는 방법에는 Starlette 자체를 사용하는 방법과 [`asgiref`](https://github.com/django/asgiref)를 사용하는 방법 두 가지가 있습니다.

* Starlette 사용: 가장 일반적인 사용 사례에 적합합니다.

```python
from starlette.types import ASGIApp, Message, Scope, Receive, Send


class ASGIMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def send_wrapper(message: Message) -> None:
            # ... 무언가를 수행
            await send(message)

        await self.app(scope, receive, send_wrapper)
```

* [`asgiref`](https://github.com/django/asgiref) 사용: 더 엄격한 타입 힌팅을 위해 사용합니다.

```python
from asgiref.typing import ASGI3Application, ASGIReceiveCallable, ASGISendCallable, Scope
from asgiref.typing import ASGIReceiveEvent, ASGISendEvent


class ASGIMiddleware:
    def __init__(self, app: ASGI3Application) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def send_wrapper(message: ASGISendEvent) -> None:
            # ... 무언가를 수행
            await send(message)

        return await self.app(scope, receive, send_wrapper)
```

### 일반적인 패턴

#### 특정 요청만 처리하기

ASGI 미들웨어는 `scope`의 내용에 따라 특정 동작을 적용할 수 있습니다.

예를 들어, HTTP 요청만 처리하려면 다음과 같이 작성하세요...

```python
class ASGIMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        ...  # 여기서 무언가를 수행하세요!

        await self.app(scope, receive, send)
```

마찬가지로, WebSocket 전용 미들웨어는 `scope["type"] != "websocket"`으로 검사합니다.

미들웨어는 요청 메서드, URL, 헤더 등에 따라 다르게 동작할 수도 있습니다.

#### Starlette 컴포넌트 재사용하기

Starlette는 ASGI `scope`, `receive` 및/또는 `send` 인자를 받아들이는 여러 데이터 구조를 제공하여 더 높은 수준의 추상화로 작업할 수 있게 합니다. 이러한 데이터 구조에는 [`Request`](requests.md#request), [`Headers`](requests.md#headers), [`QueryParams`](requests.md#query-parameters), [`URL`](requests.md#url) 등이 포함됩니다.

예를 들어, `Request`를 인스턴스화하여 HTTP 요청을 더 쉽게 검사할 수 있습니다:

```python
from starlette.requests import Request

class ASGIMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope)
            ... # `request.method`, `request.url`, `request.headers` 등을 사용

        await self.app(scope, receive, send)
```

또한 [responses](responses.md)를 재사용할 수 있습니다. 이들도 ASGI 애플리케이션입니다.

#### 즉시 응답 보내기

연결 `scope`를 검사하면 조건에 따라 다른 ASGI 앱을 호출할 수 있습니다. 한 가지 사용 사례는 앱을 호출하지 않고 응답을 보내는 것입니다.

예를 들어, 이 미들웨어는 요청된 경로를 기반으로 영구 리다이렉트를 수행하기 위해 딕셔너리를 사용합니다. 이는 라우트 URL 패턴을 리팩토링해야 할 경우 레거시 URL에 대한 지속적인 지원을 구현하는 데 사용될 수 있습니다.

```python
from starlette.datastructures import URL
from starlette.responses import RedirectResponse

class RedirectsMiddleware:
    def __init__(self, app, path_mapping: dict):
        self.app = app
        self.path_mapping = path_mapping

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        url = URL(scope=scope)

        if url.path in self.path_mapping:
            url = url.replace(path=self.path_mapping[url.path])
            response = RedirectResponse(url, status_code=301)
            await response(scope, receive, send)
            return

        await self.app(scope, receive, send)
```

사용 예시는 다음과 같습니다:

```python
from starlette.applications import Starlette
from starlette.middleware import Middleware

routes = ...

redirections = {
    "/v1/resource/": "/v2/resource/",
    # ...
}

middleware = [
    Middleware(RedirectsMiddleware, path_mapping=redirections),
]

app = Starlette(routes=routes, middleware=middleware)
```

#### 요청 검사 또는 수정

요청 정보는 `scope`를 조작하여 액세스하거나 변경할 수 있습니다. 이 패턴의 완전한 예시는 Uvicorn의 [`ProxyHeadersMiddleware`](https://github.com/encode/uvicorn/blob/fd4386fefb8fe8a4568831a7d8b2930d5fb61455/uvicorn/middleware/proxy_headers.py)를 참조하세요. 이는 프론트엔드 프록시 뒤에서 서비스할 때 `scope`를 검사하고 조정합니다.

또한, `receive` ASGI 호출 가능 객체를 래핑하면 [`http.request`](https://asgi.readthedocs.io/en/latest/specs/www.html#request-receive-event) ASGI 이벤트 메시지를 조작하여 HTTP 요청 본문에 액세스하거나 수정할 수 있습니다.

예를 들어, 이 미들웨어는 들어오는 요청 본문의 크기를 계산하고 기록합니다...

```python
class LoggedRequestBodySizeMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        body_size = 0

        async def receive_logging_request_body_size():
            nonlocal body_size

            message = await receive()
            assert message["type"] == "http.request"

            body_size += len(message.get("body", b""))

            if not message.get("more_body", False):
                print(f"요청 본문의 크기: {body_size} 바이트")

            return message

        await self.app(scope, receive_logging_request_body_size, send)
```

마찬가지로, WebSocket 미들웨어는 [`websocket.receive`](https://asgi.readthedocs.io/en/latest/specs/www.html#receive-receive-event) ASGI 이벤트 메시지를 조작하여 들어오는 WebSocket 데이터를 검사하거나 변경할 수 있습니다.

HTTP 요청 본문을 변경하는 예시는 [`msgpack-asgi`](https://github.com/florimondmanca/msgpack-asgi)를 참조하세요.

#### 응답 검사 또는 수정

`send` ASGI 호출 가능 객체를 래핑하면 기본 애플리케이션이 보내는 HTTP 응답을 검사하거나 수정할 수 있습니다. 이를 위해 [`http.response.start`](https://asgi.readthedocs.io/en/latest/specs/www.html#response-start-send-event) 또는 [`http.response.body`](https://asgi.readthedocs.io/en/latest/specs/www.html#response-body-send-event) ASGI 이벤트 메시지에 반응하세요.

예를 들어, 이 미들웨어는 고정된 추가 응답 헤더를 추가합니다:

```python
from starlette.datastructures import MutableHeaders

class ExtraResponseHeadersMiddleware:
    def __init__(self, app, headers):
        self.app = app
        self.headers = headers

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def send_with_extra_headers(message):
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                for key, value in self.headers:
                    headers.append(key, value)

            await send(message)

        await self.app(scope, receive, send_with_extra_headers)
```

HTTP 응답을 검사하고 구성 가능한 HTTP 액세스 로그 라인을 기록하는 예시는 [`asgi-logger`](https://github.com/Kludex/asgi-logger/blob/main/asgi_logger/middleware.py)를 참조하세요.

마찬가지로, WebSocket 미들웨어는 [`websocket.send`](https://asgi.readthedocs.io/en/latest/specs/www.html#send-send-event) ASGI 이벤트 메시지를 조작하여 나가는 WebSocket 데이터를 검사하거나 변경할 수 있습니다.

응답 본문을 변경하는 경우 응답 `Content-Length` 헤더를 새 응답 본문 길이와 일치하도록 업데이트해야 합니다. 완전한 예시는 [`brotli-asgi`](https://github.com/fullonic/brotli-asgi)를 참조하세요.

#### 엔드포인트에 정보 전달

기본 앱이나 엔드포인트와 정보를 공유해야 하는 경우 `scope` 사전에 저장할 수 있습니다. 이는 규약이라는 점에 유의하세요 - 예를 들어, Starlette는 이를 사용하여 라우팅 정보를 엔드포인트와 공유합니다 - 하지만 ASGI 사양의 일부는 아닙니다. 이를 수행하는 경우 다른 미들웨어나 애플리케이션에서 사용할 가능성이 낮은 키를 사용하여 충돌을 피해야 합니다.

예를 들어, 아래 미들웨어를 포함하면 엔드포인트에서 `request.scope["asgi_transaction_id"]`에 액세스할 수 있습니다.

```python
import uuid

class TransactionIDMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        scope["asgi_transaction_id"] = uuid.uuid4()
        await self.app(scope, receive, send)
```

#### 정리 및 오류 처리

애플리케이션을 `try/except/finally` 블록이나 컨텍스트 관리자로 감싸서 정리 작업을 수행하거나 오류 처리를 할 수 있습니다.

예를 들어, 다음 미들웨어는 메트릭을 수집하고 애플리케이션 예외를 처리할 수 있습니다...

```python
import time

class MonitoringMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        start = time.time()
        try:
            await self.app(scope, receive, send)
        except Exception as exc:
            ...  # 예외 처리
            raise
        finally:
            end = time.time()
            elapsed = end - start
            ...  # `elapsed`를 메트릭으로 모니터링 백엔드에 제출
```

이 패턴의 전체 예시는 [`timing-asgi`](https://github.com/steinnes/timing-asgi)를 참조하세요.

### 주의사항

#### ASGI 미들웨어는 상태를 가지지 않아야 합니다

ASGI는 동시 요청을 처리하도록 설계되었기 때문에, 연결별 상태는 `__call__` 구현 내에서 범위가 지정되어야 합니다. 그렇지 않으면 일반적으로 요청 간에 변수 읽기/쓰기가 충돌하고 버그가 발생할 가능성이 높습니다.

예를 들어, 응답에 `X-Mock` 헤더가 있는 경우 조건부로 응답 본문을 대체하는 방법은 다음과 같습니다...

=== "✅ 이렇게 하세요"

    ```python
    from starlette.datastructures import Headers

    class MockResponseBodyMiddleware:
        def __init__(self, app, content):
            self.app = app
            self.content = content

        async def __call__(self, scope, receive, send):
            if scope["type"] != "http":
                await self.app(scope, receive, send)
                return

            # HTTP 응답에 'X-Mock' 헤더가 있으면 
            # `True`로 설정할 플래그입니다.
            # ✅: 이 함수에 범위가 지정되어 있습니다.
            should_mock = False

            async def maybe_send_with_mock_content(message):
                nonlocal should_mock

                if message["type"] == "http.response.start":
                    headers = Headers(raw=message["headers"])
                    should_mock = headers.get("X-Mock") == "1"
                    await send(message)

                elif message["type"] == "http.response.body":
                    if should_mock:
                        message = {"type": "http.response.body", "body": self.content}
                    await send(message)

            await self.app(scope, receive, maybe_send_with_mock_content)
    ```

=== "❌ 이렇게 하지 마세요"

    ```python hl_lines="7-8"
    from starlette.datastructures import Headers

    class MockResponseBodyMiddleware:
        def __init__(self, app, content):
            self.app = app
            self.content = content
            # ❌: 이 변수는 요청 간에 읽고 쓰여질 것입니다!
            self.should_mock = False

        async def __call__(self, scope, receive, send):
            if scope["type"] != "http":
                await self.app(scope, receive, send)
                return

            async def maybe_send_with_mock_content(message):
                if message["type"] == "http.response.start":
                    headers = Headers(raw=message["headers"])
                    self.should_mock = headers.get("X-Mock") == "1"
                    await send(message)

                elif message["type"] == "http.response.body":
                    if self.should_mock:
                        message = {"type": "http.response.body", "body": self.content}
                    await send(message)

            await self.app(scope, receive, maybe_send_with_mock_content)
    ```

이 잠재적인 문제를 해결하는 전체 구현 예제는 [`GZipMiddleware`](https://github.com/encode/starlette/blob/9ef1b91c9c043197da6c3f38aa153fd874b95527/starlette/middleware/gzip.py)를 참조하세요.

### 추가 읽을거리

이 문서만으로도 ASGI 미들웨어를 만드는 방법에 대한 좋은 기초를 가질 수 있을 것입니다.

그럼에도 불구하고 이 주제에 대한 훌륭한 글들이 있습니다:

- [ASGI 소개: 비동기 Python 웹 생태계의 출현](https://florimond.dev/en/posts/2019/08/introduction-to-asgi-async-python-web/)
- [ASGI 미들웨어를 작성하는 방법](https://pgjones.dev/blog/how-to-write-asgi-middleware-2021/)

## 다른 프레임워크에서 미들웨어 사용하기

다른 ASGI 애플리케이션에 ASGI 미들웨어를 래핑하려면 애플리케이션 인스턴스를 래핑하는 더 일반적인 패턴을 사용해야 합니다:

```python
app = TrustedHostMiddleware(app, allowed_hosts=['example.com'])
```

Starlette 애플리케이션 인스턴스에서도 이렇게 할 수 있지만, `middleware=<미들웨어 인스턴스 목록>` 스타일을 사용하는 것이 좋습니다. 이렇게 하면:

* 모든 것이 단일 최외곽 `ServerErrorMiddleware`로 래핑된 상태로 유지됩니다.
* 최상위 `app` 인스턴스를 유지합니다.

## 라우트 그룹에 미들웨어 적용하기

미들웨어는 `Mount` 인스턴스에도 추가할 수 있어, 라우트 그룹이나 서브 애플리케이션에 미들웨어를 적용할 수 있습니다:

```python
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.routing import Mount, Route


routes = [
    Mount(
        "/",
        routes=[
            Route(
                "/example",
                endpoint=...,
            )
        ],
        middleware=[Middleware(GZipMiddleware)]
    )
]

app = Starlette(routes=routes)
```

이런 방식으로 사용된 미들웨어는 `Starlette` 애플리케이션에 적용된 미들웨어처럼 예외 처리 미들웨어로 감싸지지 않는다는 점에 주의하세요.
이는 보통 `Response`를 검사하거나 수정하는 미들웨어에만 해당되며, 대부분의 경우 오류 응답에 이 로직을 적용하고 싶지 않을 것입니다.
만약 일부 라우트에서만 오류 응답에 미들웨어 로직을 적용하고 싶다면 몇 가지 방법이 있습니다:

* `Mount`에 `ExceptionMiddleware`를 추가합니다
* 미들웨어에 `try/except` 블록을 추가하고 거기서 오류 응답을 반환합니다
* 표시와 처리를 두 개의 미들웨어로 분리합니다. 하나는 `Mount`에 넣어 응답이 처리가 필요하다고 표시하고(예: `scope["log-response"] = True`로 설정), 다른 하나는 `Starlette` 애플리케이션에 적용하여 실제 작업을 수행합니다.

`Route`/`WebSocket` 클래스도 `middleware` 인자를 받아 단일 라우트에 미들웨어를 적용할 수 있습니다:

```python
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.routing import Route


routes = [
    Route(
        "/example",
        endpoint=...,
        middleware=[Middleware(GZipMiddleware)]
    )
]

app = Starlette(routes=routes)
```

또한 `Router` 클래스에도 미들웨어를 적용할 수 있어, 라우트 그룹에 미들웨어를 적용할 수 있습니다:

```python
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.routing import Route, Router


routes = [
    Route("/example", endpoint=...),
    Route("/another", endpoint=...),
]

router = Router(routes=routes, middleware=[Middleware(GZipMiddleware)])
```

## 서드파티 미들웨어

#### [asgi-auth-github](https://github.com/simonw/asgi-auth-github)

이 미들웨어는 모든 ASGI 애플리케이션에 인증을 추가하여, 사용자가 GitHub 계정으로 로그인하도록 요구합니다([OAuth](https://developer.github.com/apps/building-oauth-apps/authorizing-oauth-apps/)를 통해).
접근은 특정 사용자나 특정 GitHub 조직 또는 팀의 멤버로 제한할 수 있습니다.

#### [asgi-csrf](https://github.com/simonw/asgi-csrf)

CSRF 공격을 방지하기 위한 미들웨어입니다. 이 미들웨어는 Double Submit Cookie 패턴을 구현합니다. 쿠키가 설정되고, 이후 숨겨진 폼 필드의 csrftoken이나 `x-csrftoken` HTTP 헤더와 비교됩니다.

#### [AuthlibMiddleware](https://github.com/aogier/starlette-authlib)

Starlette 세션 미들웨어를 대체할 수 있는 미들웨어로, [authlib의 jwt](https://docs.authlib.org/en/latest/jose/jwt.html) 모듈을 사용합니다.

#### [BugsnagMiddleware](https://github.com/ashinabraham/starlette-bugsnag)

예외를 [Bugsnag](https://www.bugsnag.com/)에 로깅하기 위한 미들웨어 클래스입니다.

#### [CSRFMiddleware](https://github.com/frankie567/starlette-csrf)

CSRF 공격을 방지하기 위한 미들웨어입니다. 이 미들웨어는 Double Submit Cookie 패턴을 구현합니다. 쿠키가 설정되고, 이후 `x-csrftoken` HTTP 헤더와 비교됩니다.

#### [EarlyDataMiddleware](https://github.com/HarrySky/starlette-early-data)

[TLSv1.3 early data](https://tools.ietf.org/html/rfc8470) 요청을 감지하고 거부하기 위한 미들웨어와 데코레이터입니다.

#### [PrometheusMiddleware](https://github.com/perdy/starlette-prometheus)

진행 중인 요청을 포함하여 요청 및 응답과 관련된 Prometheus 메트릭을 캡처하기 위한 미들웨어 클래스입니다.

#### [ProxyHeadersMiddleware](https://github.com/encode/uvicorn/blob/master/uvicorn/middleware/proxy_headers.py)

Uvicorn은 프록시 서버가 사용될 때 `X-Forwarded-Proto`와 `X-Forwarded-For` 헤더를 기반으로 클라이언트 IP 주소를 결정하는 미들웨어 클래스를 포함하고 있습니다. 더 복잡한 프록시 구성의 경우, 이 미들웨어를 수정해야 할 수 있습니다.

#### [RateLimitMiddleware](https://github.com/abersheeran/asgi-ratelimit)

속도 제한 미들웨어입니다. 정규 표현식으로 URL을 매칭하고, 유연한 규칙과 높은 커스터마이징이 가능합니다. 사용하기 매우 쉽습니다.

#### [RequestIdMiddleware](https://github.com/snok/asgi-correlation-id)

요청 ID를 읽고 생성하여 애플리케이션 로그에 첨부하는 미들웨어 클래스입니다.

#### [RollbarMiddleware](https://docs.rollbar.com/docs/starlette)

예외, 오류 및 로그 메시지를 [Rollbar](https://www.rollbar.com)에 로깅하기 위한 미들웨어 클래스입니다.

#### [StarletteOpentracing](https://github.com/acidjunk/starlette-opentracing)

[OpenTracing.io](https://opentracing.io/) 호환 트레이서에 트레이싱 정보를 내보내는 미들웨어 클래스로,
분산 애플리케이션의 프로파일링과 모니터링에 사용할 수 있습니다.

#### [SecureCookiesMiddleware](https://github.com/thearchitector/starlette-securecookies)

Starlette 애플리케이션에 자동 쿠키 암호화 및 복호화를 추가하는 커스터마이즈 가능한 미들웨어로,
기존 쿠키 기반 미들웨어에 대한 추가 지원도 제공합니다.

#### [TimingMiddleware](https://github.com/steinnes/timing-asgi)

각 요청에 대한 타이밍 정보(CPU 및 월 시간)를 내보내는 미들웨어 클래스입니다.
이러한 타이밍을 statsd 메트릭으로 내보내는 방법에 대한 예제도 포함하고 있습니다.

#### [WSGIMiddleware](https://github.com/abersheeran/a2wsgi)

WSGI 애플리케이션을 ASGI 애플리케이션으로 변환하는 미들웨어 클래스입니다.
