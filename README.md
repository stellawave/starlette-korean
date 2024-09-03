<p align="center">
  <a href="https://www.starlette.io/"><img width="420px" src="https://raw.githubusercontent.com/encode/starlette/master/docs/img/starlette.png" alt='starlette'></a>
</p>
<p align="center">
    <em>✨ The little ASGI framework that shines. ✨</em>
</p>

---

[![Build Status](https://github.com/encode/starlette/workflows/Test%20Suite/badge.svg)](https://github.com/encode/starlette/actions)
[![Package version](https://badge.fury.io/py/starlette.svg)](https://pypi.python.org/pypi/starlette)
[![Supported Python Version](https://img.shields.io/pypi/pyversions/starlette.svg?color=%2334D058)](https://pypi.org/project/starlette)

**Documentation**: [https://www.starlette.io/](https://www.starlette.io/) 또는 [비공식 한국어 웹페이지](https://starlette.pinstella.com/)

---

# Starlette

Starlette는 가벼운 [ASGI][asgi] 프레임워크/툴킷으로, Python에서 비동기 웹 서비스를 구축하는 데 이상적입니다.

프로덕션 환경에서 사용할 준비가 되어 있으며, 다음과 같은 기능을 제공합니다:

* 가볍고 복잡도가 낮은 HTTP 웹 프레임워크
* WebSocket 지원
* 프로세스 내 백그라운드 작업
* 시작 및 종료 이벤트
* `httpx`를 기반으로 한 테스트 클라이언트
* CORS, GZip, 정적 파일, 스트리밍 응답
* 세션 및 쿠키 지원
* 100% 테스트 커버리지
* 100% 타입 어노테이션이 된 코드베이스
* 적은 수의 핵심 의존성
* `asyncio` 및 `trio` 백엔드와 호환
* [독립적인 벤치마크][techempower]에 대해 전반적으로 우수한 성능

## 요구사항

Python 3.8+

## 설치

```shell
$ pip3 install starlette
```

또한 [uvicorn](https://www.uvicorn.org/), [daphne](https://github.com/django/daphne/), 또는 [hypercorn](https://hypercorn.readthedocs.io/en/latest/)과 같은 ASGI 서버를 설치해야 합니다.

```shell
$ pip3 install uvicorn
```

## 예제

**example.py**:

```python
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


async def homepage(request):
    return JSONResponse({'hello': 'world'})

routes = [
    Route("/", endpoint=homepage)
]

app = Starlette(debug=True, routes=routes)
```

그런 다음 Uvicorn을 사용하여 애플리케이션을 실행합니다:

```shell
$ uvicorn example:app
```

더 완전한 예제는 [encode/starlette-example](https://github.com/encode/starlette-example)을 참조하세요.

## 의존성

Starlette는 `anyio`만 필요하며, 다음은 선택사항입니다:

* [`httpx`][httpx] - `TestClient`를 사용하려면 필요합니다.
* [`jinja2`][jinja2] - `Jinja2Templates`를 사용하려면 필요합니다.
* [`python-multipart`][python-multipart] - `request.form()`으로 폼 파싱을 지원하려면 필요합니다.
* [`itsdangerous`][itsdangerous] - `SessionMiddleware` 지원에 필요합니다.
* [`pyyaml`][pyyaml] - `SchemaGenerator` 지원에 필요합니다.

`pip3 install starlette[full]`로 이 모든 것을 설치할 수 있습니다.

## 프레임워크 또는 툴킷

Starlette는 완전한 프레임워크로 사용되거나 ASGI 툴킷으로 사용되도록 설계되었습니다. 모든 구성 요소를 독립적으로 사용할 수 있습니다.

```python
from starlette.responses import PlainTextResponse


async def app(scope, receive, send):
    assert scope['type'] == 'http'
    response = PlainTextResponse('Hello, world!')
    await response(scope, receive, send)
```

`example.py`의 `app` 애플리케이션을 실행합니다:

```shell
$ uvicorn example:app
INFO: Started server process [11509]
INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

코드 변경 시 자동 재로딩을 활성화하려면 `--reload`와 함께 uvicorn을 실행하세요.

## 모듈성

Starlette가 설계된 모듈성은 모든 ASGI 프레임워크 간에 공유할 수 있는 재사용 가능한 구성 요소를 구축하도록 촉진합니다. 이를 통해 공유 미들웨어와 마운트 가능한 애플리케이션의 생태계를 구축할 수 있습니다.

깔끔한 API 분리는 각 구성 요소를 개별적으로 이해하기 쉽게 만듭니다.

# 한국어 번역

**이 페이지의 번역 과정은 90% 이상 AI가 진행하였습니다.**
자세한 내용은 [블로그](https://jason-in-cosmos.blogspot.com/2024/08/1-with-claude-api.html)를 참고하세요.

일부 오역이나, 과도한 음역이 포함되어 있을 수 있습니다.

---

<p align="center"><i>Starlette는 <a href="https://github.com/encode/starlette/blob/master/LICENSE.md">BSD 라이선스</a> 코드입니다.<br/>세심하게 설계되고 제작되었습니다.</i></br>&mdash; ⭐️ &mdash;</p>

[asgi]: https://asgi.readthedocs.io/en/latest/
[httpx]: https://www.python-httpx.org/
[jinja2]: https://jinja.palletsprojects.com/
[python-multipart]: https://andrew-d.github.io/python-multipart/
[itsdangerous]: https://itsdangerous.palletsprojects.com/
[sqlalchemy]: https://www.sqlalchemy.org
[pyyaml]: https://pyyaml.org/wiki/PyYAMLDocumentation
[techempower]: https://www.techempower.com/benchmarks/#hw=ph&test=fortune&l=zijzen-sf
