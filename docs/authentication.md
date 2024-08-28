Starlette는 인증과 권한을 처리하기 위한 간단하지만 강력한 인터페이스를 제공합니다.
적절한 인증 백엔드와 함께 `AuthenticationMiddleware`를 설치하면 엔드포인트에서
`request.user`와 `request.auth` 인터페이스를 사용할 수 있습니다.

```python
from starlette.applications import Starlette
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError, SimpleUser
)
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.responses import PlainTextResponse
from starlette.routing import Route
import base64
import binascii


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        if "Authorization" not in conn.headers:
            return

        auth = conn.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'basic':
                return
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            raise AuthenticationError('유효하지 않은 기본 인증 자격 증명')

        username, _, password = decoded.partition(":")
        # TODO: 여기서 사용자 이름과 비밀번호를 확인해야 합니다.
        return AuthCredentials(["authenticated"]), SimpleUser(username)


async def homepage(request):
    if request.user.is_authenticated:
        return PlainTextResponse('안녕하세요, ' + request.user.display_name)
    return PlainTextResponse('안녕하세요')

routes = [
    Route("/", endpoint=homepage)
]

middleware = [
    Middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
]

app = Starlette(routes=routes, middleware=middleware)
```

## 사용자

`AuthenticationMiddleware`가 설치되면 엔드포인트나 다른 미들웨어에서 `request.user` 인터페이스를
사용할 수 있습니다.

이 인터페이스는 `BaseUser`를 상속해야 하며, 다음 두 가지 속성과 함께 사용자 모델에 포함된
다른 정보를 제공합니다.

* `.is_authenticated`
* `.display_name`

Starlette는 두 가지 내장 사용자 구현을 제공합니다: `UnauthenticatedUser()`와
`SimpleUser(username)`.

## AuthCredentials

인증 자격 증명을 사용자와 별개의 개념으로 취급하는 것이 중요합니다. 인증 스키마는
사용자 신원과 독립적으로 특정 권한을 제한하거나 부여할 수 있어야 합니다.

`AuthCredentials` 클래스는 `request.auth`가 노출하는 기본 인터페이스를 제공합니다:

* `.scopes`

## 권한

권한은 들어오는 요청이 필요한 인증 범위를 포함하도록 강제하는 엔드포인트 데코레이터로 구현됩니다.

```python
from starlette.authentication import requires


@requires('authenticated')
async def dashboard(request):
    ...
```

하나 또는 여러 개의 필요한 범위를 포함할 수 있습니다:

```python
from starlette.authentication import requires


@requires(['authenticated', 'admin'])
async def dashboard(request):
    ...
```

기본적으로 권한이 부여되지 않았을 때 403 응답이 반환됩니다.
경우에 따라 이를 커스터마이즈하고 싶을 수 있습니다. 예를 들어, 인증되지 않은 사용자로부터 URL 레이아웃 정보를 숨기고 싶을 수 있습니다.

```python
from starlette.authentication import requires


@requires(['authenticated', 'admin'], status_code=404)
async def dashboard(request):
    ...
```

!!! note
    `status_code` 매개변수는 WebSocket에서는 지원되지 않습니다. WebSocket의 경우 항상 403 (Forbidden) 상태 코드가 사용됩니다.

또는 인증되지 않은 사용자를 다른 페이지로 리다이렉트하고 싶을 수 있습니다.

```python
from starlette.authentication import requires


async def homepage(request):
    ...


@requires('authenticated', redirect='homepage')
async def dashboard(request):
    ...
```

사용자를 리다이렉트할 때, 리다이렉트되는 페이지는 원래 요청한 URL을 `next` 쿼리 파라미터에 포함합니다:

```python
from starlette.authentication import requires
from starlette.responses import RedirectResponse


@requires('authenticated', redirect='login')
async def admin(request):
    ...


async def login(request):
    if request.method == "POST":
        # 사용자가 인증되면
        # 원래 요청한 목적지로 보낼 수 있습니다
        if request.user.is_authenticated:
            next_url = request.query_params.get("next")
            if next_url:
                return RedirectResponse(next_url)
            return RedirectResponse("/")
```

클래스 기반 엔드포인트의 경우, 클래스의 메서드에 데코레이터를 감싸야 합니다.

```python
from starlette.authentication import requires
from starlette.endpoints import HTTPEndpoint


class Dashboard(HTTPEndpoint):
    @requires("authenticated")
    async def get(self, request):
        ...
```

## 사용자 정의 인증 오류 응답

인증 백엔드에서 `AuthenticationError`가 발생했을 때 보내는 오류 응답을 사용자 정의할 수 있습니다:

```python
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


def on_auth_error(request: Request, exc: Exception):
    return JSONResponse({"error": str(exc)}, status_code=401)

app = Starlette(
    middleware=[
        Middleware(AuthenticationMiddleware, backend=BasicAuthBackend(), on_error=on_auth_error),
    ],
)
```
