Starlette는 [12팩터 패턴][twelve-factor]을 따라 구성과 코드를 엄격히 분리하도록 권장합니다.

구성은 환경 변수에 저장하거나 소스 제어에 커밋되지 않는 `.env` 파일에 저장해야 합니다.

```python title="main.py"
from sqlalchemy import create_engine
from starlette.applications import Starlette
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

# 구성은 환경 변수 및/또는 ".env" 파일에서 읽힙니다.
config = Config(".env")

DEBUG = config('DEBUG', cast=bool, default=False)
DATABASE_URL = config('DATABASE_URL')
SECRET_KEY = config('SECRET_KEY', cast=Secret)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=CommaSeparatedStrings)

app = Starlette(debug=DEBUG)
engine = create_engine(DATABASE_URL)
...
```

```shell title=".env"
# 이 파일을 소스 제어에 커밋하지 마세요.
# 예: `.gitignore` 파일에 ".env"를 포함시키세요.
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/database
SECRET_KEY=43n080musdfjt54t-09sdgr
ALLOWED_HOSTS=127.0.0.1, localhost
```

## 구성 우선순위

구성 값이 읽히는 순서는 다음과 같습니다:

* 환경 변수에서.
* `.env` 파일에서.
* `config`에 주어진 기본값.

위의 어느 것도 일치하지 않으면 `config(...)`는 오류를 발생시킵니다.

## 비밀

민감한 키의 경우, `Secret` 클래스가 유용합니다. 이는 해당 값이 트레이스백이나 다른 코드 내부 검사에 노출될 수 있는 경우를 최소화하는 데 도움이 됩니다.

`Secret` 인스턴스의 값을 얻으려면 명시적으로 문자열로 캐스팅해야 합니다. 이는 값이 사용되는 시점에서만 수행해야 합니다.

```python
>>> from myproject import settings
>>> settings.SECRET_KEY
Secret('**********')
>>> str(settings.SECRET_KEY)
'98n349$%8b8-7yjn0n8y93T$23r'
```

!!! tip

    데이터베이스 URL을 저장하고 로그에 노출되는 것을 방지하기 위해 `databases` 패키지의 `DatabaseURL`을 [여기](https://github.com/encode/databases/blob/ab5eb718a78a27afe18775754e9c0fa2ad9cd211/databases/core.py#L420)에서 사용할 수 있습니다.

## CommaSeparatedStrings

단일 구성 키 내에 여러 값을 저장하기 위해 `CommaSeparatedStrings` 타입이 유용합니다.

```python
>>> from myproject import settings
>>> print(settings.ALLOWED_HOSTS)
CommaSeparatedStrings(['127.0.0.1', 'localhost'])
>>> print(list(settings.ALLOWED_HOSTS))
['127.0.0.1', 'localhost']
>>> print(len(settings.ALLOWED_HOSTS))
2
>>> print(settings.ALLOWED_HOSTS[0])
'127.0.0.1'
```

## 환경 읽기 또는 수정하기

경우에 따라 프로그래밍 방식으로 환경 변수를 읽거나 수정하고 싶을 수 있습니다. 이는 특히 테스트에서 유용하며, 환경의 특정 키를 재정의하고 싶을 수 있습니다.

`os.environ`에서 직접 읽거나 쓰는 대신, Starlette의 `environ` 인스턴스를 사용해야 합니다. 이 인스턴스는 표준 `os.environ`에 대한 매핑이며, 추가로 구성에 의해 이미 읽힌 후에 환경 변수가 설정되는 경우 오류를 발생시켜 보호합니다.

`pytest`를 사용하는 경우, `tests/conftest.py`에서 초기 환경을 설정할 수 있습니다.

```python title="tests/conftest.py"
from starlette.config import environ

environ['DEBUG'] = 'TRUE'
```

## 접두사가 붙은 환경 변수 읽기

`env_prefix` 인자를 설정하여 환경 변수에 네임스페이스를 지정할 수 있습니다.

```python title="myproject/settings.py"
import os

from starlette.config import Config

os.environ['APP_DEBUG'] = 'yes'
os.environ['ENVIRONMENT'] = 'dev'

config = Config(env_prefix='APP_')

DEBUG = config('DEBUG') # APP_DEBUG를 조회하고, "yes"를 반환합니다
ENVIRONMENT = config('ENVIRONMENT') # APP_ENVIRONMENT를 조회하지만, 변수가 정의되지 않아 KeyError를 발생시킵니다
```

## 전체 예제

대규모 애플리케이션을 구조화하는 것은 복잡할 수 있습니다. 설정과 코드의 적절한 분리, 테스트 중 데이터베이스 격리, 테스트와 프로덕션 데이터베이스 분리 등이 필요합니다.

여기서는 애플리케이션 구조화를 시작할 수 있는 방법을 보여주는 완전한 예제를 살펴보겠습니다.

먼저, 설정, 데이터베이스 테이블 정의, 애플리케이션 로직을 분리해 보겠습니다:

```python title="myproject/settings.py"
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

DEBUG = config('DEBUG', cast=bool, default=False)
SECRET_KEY = config('SECRET_KEY', cast=Secret)

DATABASE_URL = config('DATABASE_URL')
```

```python title="myproject/tables.py"
import sqlalchemy

# 데이터베이스 테이블 정의
metadata = sqlalchemy.MetaData()

organisations = sqlalchemy.Table(
    ...
)
```

```python title="myproject/app.py"
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.routing import Route

from myproject import settings


async def homepage(request):
    ...

routes = [
    Route("/", endpoint=homepage)
]

middleware = [
    Middleware(
        SessionMiddleware,
        secret_key=settings.SECRET_KEY,
    )
]

app = Starlette(debug=settings.DEBUG, routes=routes, middleware=middleware)
```

이제 테스트 구성을 다뤄보겠습니다.
테스트 스위트가 실행될 때마다 새로운 테스트 데이터베이스를 생성하고, 테스트가 완료되면 삭제하고 싶습니다. 또한 다음을 확인하고 싶습니다.

```python title="tests/conftest.py"
from starlette.config import environ
from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

# 이 줄은 'settings'가 import된 후에 사용하면 오류가 발생합니다.
environ['DEBUG'] = 'TRUE'

from myproject import settings
from myproject.app import app
from myproject.tables import metadata


@pytest.fixture(autouse=True, scope="session")
def setup_test_database():
    """
    테스트가 실행될 때마다 깨끗한 테스트 데이터베이스를 생성합니다.
    """
    url = settings.DATABASE_URL
    engine = create_engine(url)
    assert not database_exists(url), '테스트 데이터베이스가 이미 존재합니다. 테스트를 중단합니다.'
    create_database(url)             # 테스트 데이터베이스를 생성합니다.
    metadata.create_all(engine)      # 테이블을 생성합니다.
    yield                            # 테스트를 실행합니다.
    drop_database(url)               # 테스트 데이터베이스를 삭제합니다.


@pytest.fixture()
def client():
    """
    테스트 케이스에서 사용할 수 있는 'client' 픽스처를 만듭니다.
    """
    # 우리의 픽스처는 컨텍스트 매니저 내에서 생성됩니다. 이는 모든 테스트 케이스에 대해
    # 애플리케이션 수명 주기가 실행되도록 보장합니다.
    with TestClient(app) as test_client:
        yield test_client
```

[twelve-factor]: https://12factor.net/config
