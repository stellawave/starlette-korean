Starlette는 주어진 디렉터리의 파일을 제공하기 위한 `StaticFiles` 클래스도 포함하고 있습니다:

### StaticFiles

서명: `StaticFiles(directory=None, packages=None, html=False, check_dir=True, follow_symlink=False)`

* `directory` - 디렉터리 경로를 나타내는 문자열 또는 [os.PathLike][pathlike] 객체.
* `packages` - 파이썬 패키지의 문자열 리스트 또는 문자열 튜플의 리스트.
* `html` - HTML 모드로 실행. 디렉터리에 `index.html` 파일이 존재하면 자동으로 로드합니다.
* `check_dir` - 인스턴스화 시 디렉터리가 존재하는지 확인합니다. 기본값은 `True`입니다.
* `follow_symlink` - 파일 및 디렉터리에 대한 심볼릭 링크를 따라갈지 여부를 나타내는 불리언 값입니다. 기본값은 `False`입니다.

이 ASGI 애플리케이션을 Starlette의 라우팅과 결합하여 종합적인 정적 파일 서비스를 제공할 수 있습니다.

```python
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles


routes = [
    ...
    Mount('/static', app=StaticFiles(directory='static'), name="static"),
]

app = Starlette(routes=routes)
```

정적 파일은 일치하지 않는 요청에 대해 "404 Not found" 또는 "405 Method not allowed" 응답을 반환합니다. HTML 모드에서 `404.html` 파일이 존재하면 404 응답으로 표시됩니다.

`packages` 옵션을 사용하여 파이썬 패키지 내에 포함된 "static" 디렉터리를 포함할 수 있습니다. 파이썬 "bootstrap4" 패키지가 이에 대한 예시입니다.

```python
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles


routes=[
    ...
    Mount('/static', app=StaticFiles(directory='static', packages=['bootstrap4']), name="static"),
]

app = Starlette(routes=routes)
```

기본적으로 `StaticFiles`는 각 패키지에서 `statics` 디렉터리를 찾지만, 문자열 튜플을 지정하여 기본 디렉터리를 변경할 수 있습니다.

```python
routes=[
    ...
    Mount('/static', app=StaticFiles(packages=[('bootstrap4', 'static')]), name="static"),
]
```

정적 파일을 파이썬 패키징을 사용하여 포함하는 대신 "static" 디렉터리에 직접 포함하는 것을 선호할 수 있지만, 재사용 가능한 컴포넌트를 번들링하는 데 유용할 수 있습니다.

[pathlike]: https://docs.python.org/3/library/os.html#os.PathLike
