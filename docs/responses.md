Starlette는 `send` 채널에서 적절한 ASGI 메시지를 보내는 몇 가지 응답 클래스를 포함하고 있습니다.

### Response

서명: `Response(content, status_code=200, headers=None, media_type=None)`

* `content` - 문자열 또는 바이트 문자열입니다.
* `status_code` - 정수형 HTTP 상태 코드입니다.
* `headers` - 문자열로 이루어진 딕셔너리입니다.
* `media_type` - 미디어 타입을 나타내는 문자열입니다. 예: "text/html"

Starlette는 자동으로 Content-Length 헤더를 포함합니다. 또한 media_type을 기반으로 Content-Type 헤더를 포함하며, 텍스트 타입의 경우 charset을 추가합니다(단, `media_type`에 이미 charset이 지정되어 있지 않은 경우에 한합니다).

응답을 인스턴스화한 후에는 ASGI 애플리케이션 인스턴스로 호출하여 보낼 수 있습니다.

```python
from starlette.responses import Response


async def app(scope, receive, send):
    assert scope['type'] == 'http'
    response = Response('Hello, world!', media_type='text/plain')
    await response(scope, receive, send)
```

#### 쿠키 설정

Starlette는 응답 객체에 쿠키를 설정할 수 있도록 `set_cookie` 메서드를 제공합니다.

서명: `Response.set_cookie(key, value, max_age=None, expires=None, path="/", domain=None, secure=False, httponly=False, samesite="lax")`

* `key` - 쿠키의 키가 될 문자열입니다.
* `value` - 쿠키의 값이 될 문자열입니다.
* `max_age` - 쿠키의 수명을 초 단위로 정의하는 정수입니다. 음수 또는 0 값은 쿠키를 즉시 삭제합니다. `선택사항`
* `expires` - 쿠키가 만료될 때까지의 초를 정의하는 정수 또는 datetime 객체입니다. `선택사항`
* `path` - 쿠키가 적용될 경로의 하위 집합을 지정하는 문자열입니다. `선택사항`
* `domain` - 쿠키가 유효한 도메인을 지정하는 문자열입니다. `선택사항`
* `secure` - SSL과 HTTPS 프로토콜을 사용하여 요청이 이루어진 경우에만 쿠키를 서버로 전송할지 여부를 나타내는 부울 값입니다. `선택사항`
* `httponly` - `Document.cookie` 속성, `XMLHttpRequest` 또는 `Request` API를 통해 JavaScript로 쿠키에 접근할 수 없음을 나타내는 부울 값입니다. `선택사항`
* `samesite` - 쿠키의 samesite 전략을 지정하는 문자열입니다. 유효한 값은 `'lax'`, `'strict'`, `'none'`입니다. 기본값은 `'lax'`입니다. `선택사항`

#### 쿠키 삭제

마찬가지로, Starlette는 설정된 쿠키를 수동으로 만료시키기 위한 `delete_cookie` 메서드도 제공합니다.

서명: `Response.delete_cookie(key, path='/', domain=None)`


### HTMLResponse

텍스트나 바이트를 받아 HTML 응답을 반환합니다.

```python
from starlette.responses import HTMLResponse


async def app(scope, receive, send):
    assert scope['type'] == 'http'
    response = HTMLResponse('<html><body><h1>Hello, world!</h1></body></html>')
    await response(scope, receive, send)
```

### PlainTextResponse

텍스트나 바이트를 받아 일반 텍스트 응답을 반환합니다.

```python
from starlette.responses import PlainTextResponse


async def app(scope, receive, send):
    assert scope['type'] == 'http'
    response = PlainTextResponse('Hello, world!')
    await response(scope, receive, send)
```

### JSONResponse

데이터를 받아 `application/json` 인코딩된 응답을 반환합니다.

```python
from starlette.responses import JSONResponse


async def app(scope, receive, send):
    assert scope['type'] == 'http'
    response = JSONResponse({'hello': 'world'})
    await response(scope, receive, send)
```

#### 사용자 정의 JSON 직렬화

JSON 직렬화에 대한 세밀한 제어가 필요한 경우, `JSONResponse`를 상속받아 `render` 메서드를 오버라이드할 수 있습니다.

예를 들어, [orjson](https://pypi.org/project/orjson/)과 같은 서드파티 JSON 라이브러리를 사용하고 싶다면:

```python
from typing import Any

import orjson
from starlette.responses import JSONResponse


class OrjsonResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return orjson.dumps(content)
```

일반적으로 특정 엔드포인트를 미세 최적화하거나 비표준 객체 타입을 직렬화해야 하는 경우가 아니라면 기본적으로 `JSONResponse`를 사용하는 것이 *아마도* 좋을 것입니다.

### RedirectResponse

HTTP 리다이렉트를 반환합니다. 기본적으로 307 상태 코드를 사용합니다.

```python
from starlette.responses import PlainTextResponse, RedirectResponse


async def app(scope, receive, send):
    assert scope['type'] == 'http'
    if scope['path'] != '/':
        response = RedirectResponse(url='/')
    else:
        response = PlainTextResponse('안녕하세요, 세상!')
    await response(scope, receive, send)
```

### StreamingResponse

비동기 제너레이터나 일반 제너레이터/이터레이터를 받아 응답 본문을 스트리밍합니다.

```python
from starlette.responses import StreamingResponse
import asyncio


async def slow_numbers(minimum, maximum):
    yield '<html><body><ul>'
    for number in range(minimum, maximum + 1):
        yield '<li>%d</li>' % number
        await asyncio.sleep(0.5)
    yield '</ul></body></html>'


async def app(scope, receive, send):
    assert scope['type'] == 'http'
    generator = slow_numbers(1, 10)
    response = StreamingResponse(generator, media_type='text/html')
    await response(scope, receive, send)
```

`open()`으로 생성된 <a href="https://docs.python.org/3/glossary.html#term-file-like-object" target="_blank">파일 유사 객체</a>는 일반 이터레이터라는 점을 염두에 두세요. 따라서 `StreamingResponse`에서 직접 반환할 수 있습니다.

### FileResponse

파일을 비동기적으로 스트리밍하여 응답합니다.

다른 응답 유형과 다른 인수 세트로 인스턴스화됩니다:

* `path` - 스트리밍할 파일의 파일 경로.
* `headers` - 포함할 사용자 정의 헤더(딕셔너리 형태).
* `media_type` - 미디어 타입을 나타내는 문자열. 설정되지 않은 경우, 파일 이름이나 경로를 사용하여 미디어 타입을 추론합니다.
* `filename` - 설정된 경우, 응답의 `Content-Disposition`에 포함됩니다.
* `content_disposition_type` - 응답의 `Content-Disposition`에 포함됩니다. "attachment"(기본값) 또는 "inline"으로 설정할 수 있습니다.

파일 응답에는 적절한 `Content-Length`, `Last-Modified`, `ETag` 헤더가 포함됩니다.

```python
from starlette.responses import FileResponse


async def app(scope, receive, send):
    assert scope['type'] == 'http'
    response = FileResponse('statics/favicon.ico')
    await response(scope, receive, send)
```

## 서드파티 응답

#### [EventSourceResponse](https://github.com/sysid/sse-starlette)

[서버-전송 이벤트](https://html.spec.whatwg.org/multipage/server-sent-events.html)를 구현하는 응답 클래스입니다. 웹소켓의 복잡성 없이 서버에서 클라이언트로 이벤트 스트리밍을 가능하게 합니다.

#### [baize.asgi.FileResponse](https://baize.aber.sh/asgi#fileresponse)

Starlette의 [`FileResponse`](https://www.starlette.io/responses/#fileresponse)를 원활하게 대체할 수 있으며, [Head 메서드](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/HEAD)와 [Range 요청](https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests)을 자동으로 처리합니다.
