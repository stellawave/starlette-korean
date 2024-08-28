Starlette 애플리케이션은 애플리케이션이 시작되기 전에 실행해야 하는 코드나 애플리케이션이 종료될 때 처리해야 하는 코드를 다루기 위해 수명 주기 핸들러를 등록할 수 있습니다.

```python
import contextlib

from starlette.applications import Starlette


@contextlib.asynccontextmanager
async def lifespan(app):
    async with some_async_resource():
        print("시작 시 실행!")
        yield
        print("종료 시 실행!")


routes = [
    ...
]

app = Starlette(routes=routes, lifespan=lifespan)
```

Starlette는 수명 주기가 실행될 때까지 들어오는 요청을 처리하지 않습니다.

수명 주기 정리는 모든 연결이 닫히고 진행 중인 백그라운드 작업이 완료된 후에 실행됩니다.

비동기 작업 관리를 위해 [`anyio.create_task_group()`](https://anyio.readthedocs.io/en/stable/tasks.html)의 사용을 고려해보세요.

## 수명 주기 상태

수명 주기에는 `state`라는 개념이 있습니다. 이는 수명 주기와 요청 사이에 객체를 공유하는 데 사용할 수 있는 딕셔너리입니다.

```python
import contextlib
from typing import AsyncIterator, TypedDict

import httpx
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route


class State(TypedDict):
    http_client: httpx.AsyncClient


@contextlib.asynccontextmanager
async def lifespan(app: Starlette) -> AsyncIterator[State]:
    async with httpx.AsyncClient() as client:
        yield {"http_client": client}


async def homepage(request: Request) -> PlainTextResponse:
    client = request.state.http_client
    response = await client.get("https://www.example.com")
    return PlainTextResponse(response.text)


app = Starlette(
    lifespan=lifespan,
    routes=[Route("/", homepage)]
)
```

요청에서 받는 `state`는 수명 주기 핸들러에서 받은 상태의 **얕은** 복사본입니다.

## Running lifespan in tests

테스트 과정에서 수명 주기가 호출되도록 하기 위해서는 `TestClient`를 컨텍스트 관리자로 사용해야 합니다.

```python
from example import app
from starlette.testclient import TestClient


def test_homepage():
    with TestClient(app) as client:
        # 블록에 진입할 때 애플리케이션의 수명 주기가 호출됩니다.
        response = client.get("/")
        assert response.status_code == 200

    # 그리고 블록을 빠져나올 때 수명 주기의 정리가 실행됩니다.
```
