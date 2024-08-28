Starlette는 널리 사용되는 [OpenAPI 명세][openapi]와 같은 API 스키마 생성을 지원합니다. (이전에는 "Swagger"로 알려져 있었습니다.)

스키마 생성은 `app.routes`를 통해 애플리케이션의 라우트를 검사하고, 엔드포인트의 독스트링이나 다른 속성들을 사용하여 완전한 API 스키마를 결정합니다.

Starlette는 특정 스키마 생성 또는 검증 도구에 묶여있지 않지만, 독스트링을 기반으로 OpenAPI 스키마를 생성하는 간단한 구현을 포함하고 있습니다.

```python
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.schemas import SchemaGenerator


schemas = SchemaGenerator(
    {"openapi": "3.0.0", "info": {"title": "Example API", "version": "1.0"}}
)

def list_users(request):
    """
    responses:
      200:
        description: 사용자 목록.
        examples:
          [{"username": "tom"}, {"username": "lucy"}]
    """
    raise NotImplementedError()


def create_user(request):
    """
    responses:
      200:
        description: 사용자.
        examples:
          {"username": "tom"}
    """
    raise NotImplementedError()


def openapi_schema(request):
    return schemas.OpenAPIResponse(request=request)


routes = [
    Route("/users", endpoint=list_users, methods=["GET"]),
    Route("/users", endpoint=create_user, methods=["POST"]),
    Route("/schema", endpoint=openapi_schema, include_in_schema=False)
]

app = Starlette(routes=routes)
```

이제 "/schema" 엔드포인트에서 OpenAPI 스키마에 접근할 수 있습니다.

`.get_schema(routes)`를 사용하여 API 스키마를 직접 생성할 수 있습니다:

```python
schema = schemas.get_schema(routes=app.routes)
assert schema == {
    "openapi": "3.0.0",
    "info": {"title": "Example API", "version": "1.0"},
    "paths": {
        "/users": {
            "get": {
                "responses": {
                    200: {
                        "description": "사용자 목록.",
                        "examples": [{"username": "tom"}, {"username": "lucy"}],
                    }
                }
            },
            "post": {
                "responses": {
                    200: {"description": "사용자.", "examples": {"username": "tom"}}
                }
            },
        },
    },
}
```

API 문서 생성과 같은 도구를 사용할 수 있도록 API 스키마를 출력하고 싶을 수도 있습니다.

```python
if __name__ == '__main__':
    assert sys.argv[-1] in ("run", "schema"), "사용법: example.py [run|schema]"

    if sys.argv[-1] == "run":
        uvicorn.run("example:app", host='0.0.0.0', port=8000)
    elif sys.argv[-1] == "schema":
        schema = schemas.get_schema(routes=app.routes)
        print(yaml.dump(schema, default_flow_style=False))
```

### 서드파티 패키지

#### [starlette-apispec][starlette-apispec]

Starlette를 위한 간편한 APISpec 통합으로, 일부 객체 직렬화 라이브러리를 지원합니다.

[openapi]: https://github.com/OAI/OpenAPI-Specification
[starlette-apispec]: https://github.com/Woile/starlette-apispec
