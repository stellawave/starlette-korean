Starlette는 오류나 처리된 예외가 발생했을 때 응답을 반환하는 방식을 처리하기 위해 사용자 정의 예외 처리기를 설치할 수 있도록 합니다.

```python
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse


HTML_404_PAGE = ...
HTML_500_PAGE = ...


async def not_found(request: Request, exc: HTTPException):
    return HTMLResponse(content=HTML_404_PAGE, status_code=exc.status_code)

async def server_error(request: Request, exc: HTTPException):
    return HTMLResponse(content=HTML_500_PAGE, status_code=exc.status_code)


exception_handlers = {
    404: not_found,
    500: server_error
}

app = Starlette(routes=routes, exception_handlers=exception_handlers)
```

`debug`가 활성화되어 있고 오류가 발생하면, Starlette는 설치된 500 핸들러를 사용하는 대신 트레이스백 응답을 반환합니다.

```python
app = Starlette(debug=True, routes=routes, exception_handlers=exception_handlers)
```

특정 상태 코드에 대한 핸들러를 등록하는 것 외에도, 예외 클래스에 대한 핸들러를 등록할 수 있습니다.

특히 내장된 `HTTPException` 클래스의 처리 방식을 재정의하고 싶을 수 있습니다. 예를 들어, JSON 스타일의 응답을 사용하려면:

```python
async def http_exception(request: Request, exc: HTTPException):
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)

exception_handlers = {
    HTTPException: http_exception
}
```

`HTTPException`은 `headers` 인자도 갖추고 있습니다. 이를 통해 헤더를 응답 클래스로 전파할 수 있습니다:

```python
async def http_exception(request: Request, exc: HTTPException):
    return JSONResponse(
        {"detail": exc.detail},
        status_code=exc.status_code,
        headers=exc.headers
    )
```

`WebSocketException`의 처리 방식을 재정의하고 싶을 수도 있습니다:

```python
async def websocket_exception(websocket: WebSocket, exc: WebSocketException):
    await websocket.close(code=1008)

exception_handlers = {
    WebSocketException: websocket_exception
}
```

## 오류 및 처리된 예외

처리된 예외와 오류를 구분하는 것이 중요합니다.

처리된 예외는 오류 상황을 나타내지 않습니다. 이들은 적절한 HTTP 응답으로 변환되어 표준 미들웨어 스택을 통해 전송됩니다. 기본적으로 `HTTPException` 클래스가 처리된 예외를 관리하는 데 사용됩니다.

오류는 애플리케이션 내에서 발생하는 다른 모든 예외입니다. 이러한 경우는 전체 미들웨어 스택을 통해 예외로 버블링되어야 합니다. 오류 로깅 미들웨어는 예외를 서버까지 다시 발생시키도록 해야 합니다.

실제로 사용되는 오류 처리기는 `exception_handler[500]` 또는 `exception_handler[Exception]`입니다. `500`과 `Exception` 키 모두 사용할 수 있습니다. 아래를 참조하세요:

```python
async def handle_error(request: Request, exc: HTTPException):
    # 일부 로직 수행
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)

exception_handlers = {
    Exception: handle_error  # 또는 "500: handle_error"
}
```

[`BackgroundTask`](https://www.starlette.io/background/)가 예외를 발생시키는 경우, `handle_error` 함수에 의해 처리되지만 그 시점에서 응답이 이미 전송되었음을 주의해야 합니다. 다시 말해, `handle_error`에 의해 생성된 응답은 무시됩니다. 응답이 전송되기 전에 오류가 발생한 경우에는 응답 객체를 사용합니다 - 위의 예에서는 반환된 `JSONResponse`를 사용합니다.

이러한 동작을 올바르게 처리하기 위해 `Starlette` 애플리케이션의 미들웨어 스택은 다음과 같이 구성됩니다:

* `ServerErrorMiddleware` - 서버 오류 발생 시 500 응답을 반환합니다.
* 설치된 미들웨어
* `ExceptionMiddleware` - 처리된 예외를 다루고 응답을 반환합니다.
* 라우터
* 엔드포인트

## HTTPException

`HTTPException` 클래스는 처리된 예외에 사용할 수 있는 기본 클래스를 제공합니다. `ExceptionMiddleware` 구현은 기본적으로 모든 `HTTPException`에 대해 일반 텍스트 HTTP 응답을 반환합니다.

* `HTTPException(status_code, detail=None, headers=None)`

`HTTPException`은 라우팅이나 엔드포인트 내에서만 발생시켜야 합니다. 미들웨어 클래스는 대신 적절한 응답을 직접 반환해야 합니다.

## WebSocketException

WebSocket 엔드포인트 내에서 오류를 발생시키기 위해 `WebSocketException` 클래스를 사용할 수 있습니다.

* `WebSocketException(code=1008, reason=None)`

[사양에 정의된](https://tools.ietf.org/html/rfc6455#section-7.4.1) 유효한 코드를 설정할 수 있습니다.
