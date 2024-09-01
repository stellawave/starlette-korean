from __future__ import annotations

import sys
import typing
import warnings

if sys.version_info >= (3, 10):  # pragma: no cover
    from typing import ParamSpec
else:  # pragma: no cover
    from typing_extensions import ParamSpec

from starlette.datastructures import State, URLPath
from starlette.middleware import Middleware, _MiddlewareClass
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.middleware.exceptions import ExceptionMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import BaseRoute, Router
from starlette.types import ASGIApp, ExceptionHandler, Lifespan, Receive, Scope, Send
from starlette.websockets import WebSocket

AppType = typing.TypeVar("AppType", bound="Starlette")
P = ParamSpec("P")


class Starlette:
    """
    애플리케이션 인스턴스를 생성합니다.

    **매개변수:**

    * **debug** - 오류 발생 시 디버그 트레이스백을 반환할지 여부를 나타내는 부울 값.
    * **routes** - 들어오는 HTTP 및 WebSocket 요청을 처리할 라우트 목록.
    * **middleware** - 모든 요청에 대해 실행될 미들웨어 목록. Starlette 애플리케이션은 항상 자동으로 두 개의 미들웨어 클래스를 포함합니다.
      `ServerErrorMiddleware`는 전체 스택의 가장 바깥쪽에서 추가되어 어디서든 발생할 수 있는 잡히지 않은 오류를 처리합니다.
      `ExceptionMiddleware`는 라우팅 또는 엔드포인트에서 발생하는 처리된 예외 케이스를 처리하기 위해 가장 안쪽에서 추가됩니다.
    * **exception_handlers** - 정수 상태 코드 또는 예외 클래스 유형을 호출 가능한 예외 처리기와 매핑한 것. 예외 처리기는 `handler(request, exc) -> response` 형식이어야 하며, 일반 함수 또는 비동기 함수일 수 있습니다.
    * **on_startup** - 애플리케이션 시작 시 실행할 호출 가능한 항목 목록. 시작 핸들러는 인수를 받지 않으며, 일반 함수 또는 비동기 함수일 수 있습니다.
    * **on_shutdown** - 애플리케이션 종료 시 실행할 호출 가능한 항목 목록. 종료 핸들러는 인수를 받지 않으며, 일반 함수 또는 비동기 함수일 수 있습니다.
    * **lifespan** - 시작 및 종료 작업을 수행할 수 있는 lifespan 컨텍스트 함수. 이는 `on_startup` 및 `on_shutdown` 핸들러를 대체하는 새로운 스타일로, 둘 중 하나만 사용해야 합니다.
    """

    def __init__(
        self: AppType,
        debug: bool = False,
        routes: typing.Sequence[BaseRoute] | None = None,
        middleware: typing.Sequence[Middleware] | None = None,
        exception_handlers: typing.Mapping[typing.Any, ExceptionHandler] | None = None,
        on_startup: typing.Sequence[typing.Callable[[], typing.Any]] | None = None,
        on_shutdown: typing.Sequence[typing.Callable[[], typing.Any]] | None = None,
        lifespan: Lifespan[AppType] | None = None,
    ) -> None:
        # The lifespan context function is a newer style that replaces
        # on_startup / on_shutdown handlers. Use one or the other, not both.
        assert lifespan is None or (
            on_startup is None and on_shutdown is None
        ), "Use either 'lifespan' or 'on_startup'/'on_shutdown', not both."

        self.debug = debug
        self.state = State()
        self.router = Router(
            routes, on_startup=on_startup, on_shutdown=on_shutdown, lifespan=lifespan
        )
        self.exception_handlers = (
            {} if exception_handlers is None else dict(exception_handlers)
        )
        self.user_middleware = [] if middleware is None else list(middleware)
        self.middleware_stack: ASGIApp | None = None

    def build_middleware_stack(self) -> ASGIApp:
        debug = self.debug
        error_handler = None
        exception_handlers: dict[
            typing.Any, typing.Callable[[Request, Exception], Response]
        ] = {}

        for key, value in self.exception_handlers.items():
            if key in (500, Exception):
                error_handler = value
            else:
                exception_handlers[key] = value

        middleware = (
            [Middleware(ServerErrorMiddleware, handler=error_handler, debug=debug)]
            + self.user_middleware
            + [
                Middleware(
                    ExceptionMiddleware, handlers=exception_handlers, debug=debug
                )
            ]
        )

        app = self.router
        for cls, args, kwargs in reversed(middleware):
            app = cls(app=app, *args, **kwargs)
        return app

    @property
    def routes(self) -> list[BaseRoute]:
        return self.router.routes

    def url_path_for(self, name: str, /, **path_params: typing.Any) -> URLPath:
        return self.router.url_path_for(name, **path_params)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        scope["app"] = self
        if self.middleware_stack is None:
            self.middleware_stack = self.build_middleware_stack()
        await self.middleware_stack(scope, receive, send)

    def on_event(self, event_type: str) -> typing.Callable:  # type: ignore[type-arg]
        return self.router.on_event(event_type)  # pragma: nocover

    def mount(self, path: str, app: ASGIApp, name: str | None = None) -> None:
        self.router.mount(path, app=app, name=name)  # pragma: no cover

    def host(self, host: str, app: ASGIApp, name: str | None = None) -> None:
        self.router.host(host, app=app, name=name)  # pragma: no cover

    def add_middleware(
        self,
        middleware_class: type[_MiddlewareClass[P]],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> None:
        if self.middleware_stack is not None:  # pragma: no cover
            raise RuntimeError("Cannot add middleware after an application has started")
        self.user_middleware.insert(0, Middleware(middleware_class, *args, **kwargs))

    def add_exception_handler(
        self,
        exc_class_or_status_code: int | type[Exception],
        handler: ExceptionHandler,
    ) -> None:  # pragma: no cover
        self.exception_handlers[exc_class_or_status_code] = handler

    def add_event_handler(
        self,
        event_type: str,
        func: typing.Callable,  # type: ignore[type-arg]
    ) -> None:  # pragma: no cover
        self.router.add_event_handler(event_type, func)

    def add_route(
        self,
        path: str,
        route: typing.Callable[[Request], typing.Awaitable[Response] | Response],
        methods: list[str] | None = None,
        name: str | None = None,
        include_in_schema: bool = True,
    ) -> None:  # pragma: no cover
        self.router.add_route(
            path, route, methods=methods, name=name, include_in_schema=include_in_schema
        )

    def add_websocket_route(
        self,
        path: str,
        route: typing.Callable[[WebSocket], typing.Awaitable[None]],
        name: str | None = None,
    ) -> None:  # pragma: no cover
        self.router.add_websocket_route(path, route, name=name)

    def exception_handler(
        self, exc_class_or_status_code: int | type[Exception]
    ) -> typing.Callable:  # type: ignore[type-arg]
        warnings.warn(
            "The `exception_handler` decorator is deprecated, and will be removed in version 1.0.0. "  # noqa: E501
            "Refer to https://www.starlette.io/exceptions/ for the recommended approach.",  # noqa: E501
            DeprecationWarning,
        )

        def decorator(func: typing.Callable) -> typing.Callable:  # type: ignore[type-arg]  # noqa: E501
            self.add_exception_handler(exc_class_or_status_code, func)
            return func

        return decorator

    def route(
        self,
        path: str,
        methods: list[str] | None = None,
        name: str | None = None,
        include_in_schema: bool = True,
    ) -> typing.Callable:  # type: ignore[type-arg]
        """
        We no longer document this decorator style API, and its usage is discouraged.
        Instead you should use the following approach:

        >>> routes = [Route(path, endpoint=...), ...]
        >>> app = Starlette(routes=routes)
        """
        warnings.warn(
            "The `route` decorator is deprecated, and will be removed in version 1.0.0. "  # noqa: E501
            "Refer to https://www.starlette.io/routing/ for the recommended approach.",  # noqa: E501
            DeprecationWarning,
        )

        def decorator(func: typing.Callable) -> typing.Callable:  # type: ignore[type-arg]  # noqa: E501
            self.router.add_route(
                path,
                func,
                methods=methods,
                name=name,
                include_in_schema=include_in_schema,
            )
            return func

        return decorator

    def websocket_route(self, path: str, name: str | None = None) -> typing.Callable:  # type: ignore[type-arg]
        """
        We no longer document this decorator style API, and its usage is discouraged.
        Instead you should use the following approach:

        >>> routes = [WebSocketRoute(path, endpoint=...), ...]
        >>> app = Starlette(routes=routes)
        """
        warnings.warn(
            "The `websocket_route` decorator is deprecated, and will be removed in version 1.0.0. "  # noqa: E501
            "Refer to https://www.starlette.io/routing/#websocket-routing for the recommended approach.",  # noqa: E501
            DeprecationWarning,
        )

        def decorator(func: typing.Callable) -> typing.Callable:  # type: ignore[type-arg]  # noqa: E501
            self.router.add_websocket_route(path, func, name=name)
            return func

        return decorator

    def middleware(self, middleware_type: str) -> typing.Callable:  # type: ignore[type-arg]  # noqa: E501
        """
        We no longer document this decorator style API, and its usage is discouraged.
        Instead you should use the following approach:

        >>> middleware = [Middleware(...), ...]
        >>> app = Starlette(middleware=middleware)
        """
        warnings.warn(
            "The `middleware` decorator is deprecated, and will be removed in version 1.0.0. "  # noqa: E501
            "Refer to https://www.starlette.io/middleware/#using-middleware for recommended approach.",  # noqa: E501
            DeprecationWarning,
        )
        assert (
            middleware_type == "http"
        ), 'Currently only middleware("http") is supported.'

        def decorator(func: typing.Callable) -> typing.Callable:  # type: ignore[type-arg]  # noqa: E501
            self.add_middleware(BaseHTTPMiddleware, dispatch=func)
            return func

        return decorator
