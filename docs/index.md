<p align="center">
  <img width="420px" src="/img/starlette.png" alt='starlette'>
</p>
<p align="center">
    <em>✨ 빛나는 작은 ASGI 프레임워크. ✨(비공식 한국어 번역)</em>
</p>
<p align="center">
<a href="https://github.com/encode/starlette/actions">
    <img src="https://github.com/encode/starlette/workflows/Test%20Suite/badge.svg" alt="Build Status">
</a>
<a href="https://pypi.org/project/starlette/">
    <img src="https://badge.fury.io/py/starlette.svg" alt="Package version">
</a>
</p>

---

# 소개

Starlette는 경량 [ASGI][asgi] 프레임워크/툴킷으로, Python에서 비동기 웹 서비스를 구축하는 데 이상적입니다.

프로덕션 환경에서 사용할 준비가 되어 있으며 다음과 같은 기능을 제공합니다:

* 경량의 낮은 복잡도를 가진 HTTP 웹 프레임워크
* WebSocket 지원
* 프로세스 내 백그라운드 작업
* 시작 및 종료 이벤트
* `httpx`를 기반으로 한 테스트 클라이언트
* CORS, GZip, 정적 파일, 스트리밍 응답
* 세션 및 쿠키 지원
* 100% 테스트 커버리지
* 100% 타입 어노테이션이 된 코드베이스
* 적은 수의 필수 의존성
* `asyncio` 및 `trio` 백엔드와 호환
* 독립적인 벤치마크에서 [우수한 전반적인 성능][techempower]

## 요구 사항

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


app = Starlette(debug=True, routes=[
    Route('/', homepage),
])
```

그런 다음 애플리케이션을 실행하세요...

```shell
$ uvicorn example:app
```

더 완전한 예제는 [여기를 참조하세요](https://github.com/encode/starlette-example).

## 의존성

Starlette는 `anyio`만 필요로 하며, 다음 의존성은 선택적입니다:

* [`httpx`][httpx] - `TestClient`를 사용하려면 필요합니다.
* [`jinja2`][jinja2] - `Jinja2Templates`를 사용하려면 필요합니다.
* [`python-multipart`][python-multipart] - `request.form()`으로 폼 파싱을 지원하려면 필요합니다.
* [`itsdangerous`][itsdangerous] - `SessionMiddleware` 지원에 필요합니다.
* [`pyyaml`][pyyaml] - `SchemaGenerator` 지원에 필요합니다.

`pip3 install starlette[full]`로 이 모든 것을 설치할 수 있습니다.

## 프레임워크 또는 툴킷

Starlette는 완전한 프레임워크로 사용하거나 ASGI 툴킷으로 사용할 수 있도록 설계되었습니다. 모든 구성 요소를 독립적으로 사용할 수 있습니다.

```python
from starlette.responses import PlainTextResponse


async def app(scope, receive, send):
    assert scope['type'] == 'http'
    response = PlainTextResponse('안녕하세요, 세상!')
    await response(scope, receive, send)
```

`example.py`에서 `app` 애플리케이션을 실행합니다:

```shell
$ uvicorn example:app
INFO: Started server process [11509]
INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

코드 변경 시 자동 재로딩을 활성화하려면 `--reload`와 함께 uvicorn을 실행하세요.

## 모듈성

Starlette가 설계된 모듈성은 모든 ASGI 프레임워크 간에 공유할 수 있는 재사용 가능한 컴포넌트를 구축하는 것을 촉진합니다. 이는 공유 미들웨어와 마운트 가능한 애플리케이션의 생태계를 가능하게 합니다.

깔끔한 API 분리는 각 컴포넌트를 개별적으로 이해하기 쉽게 만듭니다.

---

<p align="center"><i>Starlette는 <a href="https://github.com/encode/starlette/blob/master/LICENSE.md">BSD 라이선스</a> 코드입니다.<br/>세심하게 설계 및 제작되었습니다.</i></br>&mdash; ⭐️ &mdash;</p>

[asgi]: https://asgi.readthedocs.io/en/latest/
[httpx]: https://www.python-httpx.org/
[jinja2]: https://jinja.palletsprojects.com/
[python-multipart]: https://andrew-d.github.io/python-multipart/
[itsdangerous]: https://itsdangerous.palletsprojects.com/
[sqlalchemy]: https://www.sqlalchemy.org
[pyyaml]: https://pyyaml.org/wiki/PyYAMLDocumentation
[techempower]: https://www.techempower.com/benchmarks/#hw=ph&test=fortune&l=zijzen-sf
