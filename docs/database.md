Starlette는 특정 데이터베이스 구현에 엄격하게 묶여있지 않습니다.

[GINO](https://python-gino.org/)와 같은 비동기 ORM을 사용하거나, 일반적인 비동기 엔드포인트를 사용하여 [SQLAlchemy](https://www.sqlalchemy.org/)와 통합할 수 있습니다.

이 문서에서는 다양한 데이터베이스 드라이버에 대해 SQLAlchemy 코어 지원을 제공하는 [databases 패키지](https://github.com/encode/databases)와의 통합 방법을 보여드리겠습니다.

다음은 테이블 정의, `database.Database` 인스턴스 구성, 그리고 데이터베이스와 상호작용하는 몇 가지 엔드포인트를 포함한 완전한 예제입니다.

**.env**

```ini
DATABASE_URL=sqlite:///test.db
```

**app.py**

```python
import contextlib

import databases
import sqlalchemy
from starlette.applications import Starlette
from starlette.config import Config
from starlette.responses import JSONResponse
from starlette.routing import Route


# 환경 변수 또는 '.env' 파일에서 설정을 가져옵니다.
config = Config('.env')
DATABASE_URL = config('DATABASE_URL')


# 데이터베이스 테이블 정의
metadata = sqlalchemy.MetaData()

notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean),
)

database = databases.Database(DATABASE_URL)

@contextlib.asynccontextmanager
async def lifespan(app):
    await database.connect()
    yield
    await database.disconnect()

# 메인 애플리케이션 코드
async def list_notes(request):
    query = notes.select()
    results = await database.fetch_all(query)
    content = [
        {
            "text": result["text"],
            "completed": result["completed"]
        }
        for result in results
    ]
    return JSONResponse(content)

async def add_note(request):
    data = await request.json()
    query = notes.insert().values(
       text=data["text"],
       completed=data["completed"]
    )
    await database.execute(query)
    return JSONResponse({
        "text": data["text"],
        "completed": data["completed"]
    })

routes = [
    Route("/notes", endpoint=list_notes, methods=["GET"]),
    Route("/notes", endpoint=add_note, methods=["POST"]),
]

app = Starlette(
    routes=routes,
    lifespan=lifespan,
)
```

마지막으로, 데이터베이스 테이블을 생성해야 합니다. Alembic을 사용하는 것이 권장되며, 이에 대해서는 [마이그레이션](#migrations) 섹션에서 간단히 다룹니다.

## 쿼리

쿼리는 [SQLAlchemy Core 쿼리][sqlalchemy-core]로 작성할 수 있습니다.

다음과 같은 메서드가 지원됩니다:

* `rows = await database.fetch_all(query)`
* `row = await database.fetch_one(query)`
* `async for row in database.iterate(query)`
* `await database.execute(query)`
* `await database.execute_many(query)`

## 트랜잭션

데이터베이스 트랜잭션은 데코레이터, 컨텍스트 매니저 또는 로우 레벨 API로 사용할 수 있습니다.

엔드포인트에 데코레이터 사용:

```python
@database.transaction()
async def populate_note(request):
    # 이 데이터베이스 삽입은 트랜잭션 내에서 발생합니다.
    # `RuntimeError`에 의해 롤백됩니다.
    query = notes.insert().values(text="you won't see me", completed=True)
    await database.execute(query)
    raise RuntimeError()
```

컨텍스트 매니저 사용:

```python
async def populate_note(request):
    async with database.transaction():
        # 이 데이터베이스 삽입은 트랜잭션 내에서 발생합니다.
        # `RuntimeError`에 의해 롤백됩니다.
        query = notes.insert().values(text="you won't see me", completed=True)
        await request.database.execute(query)
        raise RuntimeError()
```

로우 레벨 API 사용:

```python
async def populate_note(request):
    transaction = await database.transaction()
    try:
        # 이 데이터베이스 삽입은 트랜잭션 내에서 발생합니다.
        # `RuntimeError`에 의해 롤백됩니다.
        query = notes.insert().values(text="you won't see me", completed=True)
        await database.execute(query)
        raise RuntimeError()
    except:
        await transaction.rollback()
        raise
    else:
        await transaction.commit()
```

## 테스트 격리

데이터베이스를 사용하는 서비스에 대해 테스트를 실행할 때 확인하고자 하는 몇 가지 사항이 있습니다. 우리의 요구사항은 다음과 같아야 합니다:

* 테스트용 별도의 데이터베이스 사용.
* 테스트를 실행할 때마다 새로운 테스트 데이터베이스 생성.
* 각 테스트 케이스 간 데이터베이스 상태 격리 보장.

이러한 요구사항을 충족하기 위해 애플리케이션과 테스트를 어떻게 구조화해야 하는지 아래와 같습니다:

```python
from starlette.applications import Starlette
from starlette.config import Config
import databases

config = Config(".env")

TESTING = config('TESTING', cast=bool, default=False)
DATABASE_URL = config('DATABASE_URL', cast=databases.DatabaseURL)
TEST_DATABASE_URL = DATABASE_URL.replace(database='test_' + DATABASE_URL.database)

# 테스트 중에는 'force_rollback'을 사용하여 각 테스트 케이스 간에
# 데이터베이스 변경사항이 유지되지 않도록 합니다.
if TESTING:
    database = databases.Database(TEST_DATABASE_URL, force_rollback=True)
else:
    database = databases.Database(DATABASE_URL)
```

테스트 실행 중에 `TESTING`을 설정하고 테스트 데이터베이스를 설정해야 합니다.
`py.test`를 사용한다고 가정하면, `conftest.py`는 다음과 같을 수 있습니다:

```python
import pytest
from starlette.config import environ
from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

# 이는 `os.environ`을 설정하지만 추가적인 보호를 제공합니다.
# 애플리케이션 import 아래에 이를 배치하면 'TESTING'이 이미 환경에서
# 읽혔다는 오류를 발생시킵니다.
environ['TESTING'] = 'True'

import app


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    """
    모든 테스트 케이스에서 깨끗한 데이터베이스를 생성합니다.
    안전을 위해 데이터베이스가 이미 존재하는 경우 중단해야 합니다.

    여기서는 `sqlalchemy_utils` 패키지를 사용하여 데이터베이스를 일관되게
    생성하고 삭제하는 데 도움이 되는 몇 가지 헬퍼를 사용합니다.
    """
    url = str(app.TEST_DATABASE_URL)
    engine = create_engine(url)
    assert not database_exists(url), '테스트 데이터베이스가 이미 존재합니다. 테스트를 중단합니다.'
    create_database(url)             # 테스트 데이터베이스를 생성합니다.
    metadata.create_all(engine)      # 테이블을 생성합니다.
    yield                            # 테스트를 실행합니다.
    drop_database(url)               # 테스트 데이터베이스를 삭제합니다.


@pytest.fixture()
def client():
    """
    테스트 케이스에서 'client' fixture를 사용할 때, 테스트 케이스 간에
    완전한 데이터베이스 롤백이 이루어집니다:

    def test_homepage(client):
        url = app.url_path_for('homepage')
        response = client.get(url)
        assert response.status_code == 200
    """
    with TestClient(app) as client:
        yield client
```

## Migrations

데이터베이스의 점진적인 변경사항을 관리하기 위해 데이터베이스 마이그레이션을 사용해야 할 것입니다. 이를 위해 SQLAlchemy 작성자가 만든 [Alembic][alembic]을 강력히 추천합니다.

```shell
$ pip install alembic
$ alembic init migrations
```

이제 Alembic이 설정된 DATABASE_URL을 참조하고 테이블 메타데이터를 사용하도록 설정해야 합니다.

`alembic.ini`에서 다음 줄을 제거하세요:

```shell
sqlalchemy.url = driver://user:pass@localhost/dbname
```

`migrations/env.py`에서 `'sqlalchemy.url'` 설정 키와 `target_metadata` 변수를 설정해야 합니다. 다음과 같이 작성하세요:

```python
# Alembic Config 객체
config = context.config

# Alembic이 우리의 DATABASE_URL과 테이블 정의를 사용하도록 구성...
import app
config.set_main_option('sqlalchemy.url', str(app.DATABASE_URL))
target_metadata = app.metadata

...
```

그런 다음 위의 notes 예제를 사용하여 초기 리비전을 생성하세요:

```shell
alembic revision -m "Create notes table"
```

그리고 새로 생성된 파일(`migrations/versions` 내)에 필요한 지시사항을 채우세요:

```python
def upgrade():
    op.create_table(
      'notes',
      sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
      sqlalchemy.Column("text", sqlalchemy.String),
      sqlalchemy.Column("completed", sqlalchemy.Boolean),
    )

def downgrade():
    op.drop_table('notes')
```

첫 번째 마이그레이션을 실행하세요. 이제 notes 앱을 실행할 수 있습니다!

```shell
alembic upgrade head
```

**테스트 중 마이그레이션 실행**

테스트 데이터베이스를 생성할 때마다 테스트 스위트가 데이터베이스 마이그레이션을 실행하도록 하는 것이 좋습니다. 이는 마이그레이션 스크립트의 문제를 잡는 데 도움이 되며, 테스트가 실제 데이터베이스와 일관된 상태의 데이터베이스에서 실행되도록 보장하는 데 도움이 됩니다.

`create_test_database` 픽스처를 약간 수정할 수 있습니다:

```python
from alembic import command
from alembic.config import Config
import app

...

@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    url = str(app.DATABASE_URL)
    engine = create_engine(url)
    assert not database_exists(url), '테스트 데이터베이스가 이미 존재합니다. 테스트를 중단합니다.'
    create_database(url)             # 테스트 데이터베이스 생성
    config = Config("alembic.ini")   # 마이그레이션 실행
    command.upgrade(config, "head")
    yield                            # 테스트 실행
    drop_database(url)               # 테스트 데이터베이스 삭제
```

[sqlalchemy-core]: https://docs.sqlalchemy.org/en/latest/core/
[alembic]: https://alembic.sqlalchemy.org/en/latest/
