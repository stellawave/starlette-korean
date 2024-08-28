Starlette는 특정 템플릿 엔진과 엄격하게 결합되어 있지 않지만, Jinja2는 훌륭한 선택입니다.

### Jinja2Templates

서명: `Jinja2Templates(directory, context_processors=None, **env_options)`

* `directory` - 디렉토리 경로를 나타내는 문자열, [os.Pathlike][pathlike] 또는 문자열이나 [os.Pathlike][pathlike]의 리스트입니다.
* `context_processors` - 템플릿 컨텍스트에 추가할 딕셔너리를 반환하는 함수들의 리스트입니다.
* `**env_options` - Jinja2 환경에 전달할 추가 키워드 인자입니다.

Starlette는 `jinja2`를 구성하는 간단한 방법을 제공합니다. 이것이 기본적으로 사용하고 싶은 방법일 것입니다.

```python
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles


templates = Jinja2Templates(directory='templates')

async def homepage(request):
    return templates.TemplateResponse(request, 'index.html')

routes = [
    Route('/', endpoint=homepage),
    Mount('/static', StaticFiles(directory='static'), name='static')
]

app = Starlette(debug=True, routes=routes)
```

들어오는 `request` 인스턴스가 템플릿 컨텍스트의 일부로 포함되어야 함에 주의하세요.

Jinja2 템플릿 컨텍스트는 자동으로 `url_for` 함수를 포함하므로, 애플리케이션 내의 다른 페이지로 올바르게 하이퍼링크를 걸 수 있습니다.

예를 들어, HTML 템플릿 내에서 정적 파일에 링크할 수 있습니다:

```html
<link href="{{ url_for('static', path='/css/bootstrap.min.css') }}" rel="stylesheet" />
```

[사용자 정의 필터][jinja2]를 사용하려면 `Jinja2Templates`의 `env` 속성을 업데이트해야 합니다:

```python
from commonmark import commonmark
from starlette.templating import Jinja2Templates

def marked_filter(text):
    return commonmark(text)

templates = Jinja2Templates(directory='templates')
templates.env.filters['marked'] = marked_filter
```

## 사용자 정의 jinja2.Environment 인스턴스 사용하기

Starlette는 미리 구성된 [`jinja2.Environment`](https://jinja.palletsprojects.com/en/3.0.x/api/#api) 인스턴스도 받아들입니다.

```python
import jinja2
from starlette.templating import Jinja2Templates

env = jinja2.Environment(...)
templates = Jinja2Templates(env=env)
```

## 컨텍스트 프로세서

컨텍스트 프로세서는 템플릿 컨텍스트에 병합될 딕셔너리를 반환하는 함수입니다.
모든 함수는 `request` 인자 하나만 받으며 컨텍스트에 추가할 딕셔너리를 반환해야 합니다.

템플릿 프로세서의 일반적인 사용 사례는 공유 변수로 템플릿 컨텍스트를 확장하는 것입니다.

```python
import typing
from starlette.requests import Request

def app_context(request: Request) -> typing.Dict[str, typing.Any]:
    return {'app': request.app}
```

### 컨텍스트 템플릿 등록하기

`Jinja2Templates` 클래스의 `context_processors` 인자에 컨텍스트 프로세서를 전달하세요.

```python
import typing

from starlette.requests import Request
from starlette.templating import Jinja2Templates

def app_context(request: Request) -> typing.Dict[str, typing.Any]:
    return {'app': request.app}

templates = Jinja2Templates(
    directory='templates', context_processors=[app_context]
)
```

!!! info
    컨텍스트 프로세서로 비동기 함수는 지원되지 않습니다.

## 템플릿 응답 테스트하기

테스트 클라이언트를 사용할 때, 템플릿 응답에는 `.template`과 `.context` 속성이 포함됩니다.

```python
from starlette.testclient import TestClient


def test_homepage():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.template.name == 'index.html'
    assert "request" in response.context
```

## Jinja2 환경 커스터마이징

`Jinja2Templates`는 Jinja2 `Environment`가 지원하는 모든 옵션을 받습니다.
이를 통해 Starlette가 생성한 `Environment` 인스턴스를 더 세밀하게 제어할 수 있습니다.

`Environment`에서 사용 가능한 옵션 목록은 [여기](https://jinja.palletsprojects.com/en/3.0.x/api/#jinja2.Environment)에서 Jinja2 문서를 확인할 수 있습니다.

```python
from starlette.templating import Jinja2Templates


templates = Jinja2Templates(directory='templates', autoescape=False, auto_reload=True)
```

## 비동기 템플릿 렌더링

Jinja2는 비동기 템플릿 렌더링을 지원하지만, 일반적으로 템플릿에 데이터베이스 조회나 
다른 I/O 작업을 수행하는 로직을 포함하지 않는 것이 좋습니다.

대신 엔드포인트에서 모든 I/O를 수행하도록 하는 것을 권장합니다.
예를 들어, 뷰 내에서 모든 데이터베이스 쿼리를 엄격하게 평가하고
최종 결과를 컨텍스트에 포함시키는 것입니다.

[jinja2]: https://jinja.palletsprojects.com/en/3.0.x/api/?highlight=environment#writing-filters
[pathlike]: https://docs.python.org/3/library/os.html#os.PathLike
