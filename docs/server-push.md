Starlette는 HTTP/2 및 HTTP/3 서버 푸시를 지원하여 클라이언트에 리소스를 푸시하여 페이지 로드 시간을 단축할 수 있습니다.

### `Request.send_push_promise`

리소스에 대한 서버 푸시를 시작하는 데 사용됩니다. 서버 푸시를 사용할 수 없는 경우 이 메서드는 아무 작업도 수행하지 않습니다.

서명: `send_push_promise(path)`

* `path` - 리소스의 경로를 나타내는 문자열입니다.

```python
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles


async def homepage(request):
    """
    스타일시트를 전달하기 위해 서버 푸시를 사용하는 홈페이지입니다.
    """
    await request.send_push_promise("/static/style.css")
    return HTMLResponse(
        '<html><head><link rel="stylesheet" href="/static/style.css"/></head></html>'
    )

routes = [
    Route("/", endpoint=homepage),
    Mount("/static", StaticFiles(directory="static"), name="static")
]

app = Starlette(routes=routes)
```
