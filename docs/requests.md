Starlette는 ASGI 스코프와 수신 채널에 직접 접근하는 대신 들어오는 요청에 대해 더 나은 인터페이스를 제공하는 `Request` 클래스를 포함합니다.

### Request

시그니처: `Request(scope, receive=None)`

```python
from starlette.requests import Request
from starlette.responses import Response


async def app(scope, receive, send):
    assert scope['type'] == 'http'
    request = Request(scope, receive)
    content = '%s %s' % (request.method, request.url.path)
    response = Response(content, media_type='text/plain')
    await response(scope, receive, send)
```

Request는 매핑 인터페이스를 제공하므로 `scope`와 동일한 방식으로 사용할 수 있습니다.

예를 들어: `request['path']`는 ASGI 경로를 반환합니다.

요청 본문에 접근할 필요가 없다면 `receive`에 인수를 제공하지 않고 요청을 인스턴스화할 수 있습니다.

#### Method

요청 메서드는 `request.method`로 접근합니다.

#### URL

요청 URL은 `request.url`로 접근합니다.

이 속성은 URL에서 파싱할 수 있는 모든 구성 요소를 노출하는 문자열과 유사한 객체입니다.

예: `request.url.path`, `request.url.port`, `request.url.scheme`.

#### Headers

헤더는 변경할 수 없는, 대소문자를 구분하지 않는 멀티 딕셔너리로 노출됩니다.

예: `request.headers['content-type']`

#### Query Parameters

쿼리 매개변수는 변경할 수 없는 멀티 딕셔너리로 노출됩니다.

예: `request.query_params['search']`

#### Path Parameters

라우터 경로 매개변수는 딕셔너리 인터페이스로 노출됩니다.

예: `request.path_params['username']`

#### Client Address

클라이언트의 원격 주소는 명명된 2-튜플 `request.client`로 노출됩니다(또는 `None`).

호스트 이름 또는 IP 주소: `request.client.host`

클라이언트가 연결하는 포트 번호: `request.client.port`

#### Cookies

쿠키는 일반 딕셔너리 인터페이스로 노출됩니다.

예: `request.cookies.get('mycookie')`

유효하지 않은 쿠키의 경우 무시됩니다. (RFC2109)

#### Body

요청의 본문을 반환하는 몇 가지 다른 인터페이스가 있습니다:

바이트로 된 요청 본문: `await request.body()`

폼 데이터 또는 멀티파트로 파싱된 요청 본문: `async with request.form() as form:`

JSON으로 파싱된 요청 본문: `await request.json()`

`async for` 구문을 사용하여 스트림으로 요청 본문에 접근할 수도 있습니다:

```python
from starlette.requests import Request
from starlette.responses import Response


async def app(scope, receive, send):
    assert scope['type'] == 'http'
    request = Request(scope, receive)
    body = b''
    async for chunk in request.stream():
        body += chunk
    response = Response(body, media_type='text/plain')
    await response(scope, receive, send)
```

`.stream()`에 접근하면 전체 본문을 메모리에 저장하지 않고 바이트 청크가 제공됩니다. 이후 `.body()`, `.form()`, 또는 `.json()`을 호출하면 오류가 발생합니다.

롱 폴링이나 스트리밍 응답과 같은 일부 경우에는 클라이언트가 연결을 끊었는지 확인해야 할 수 있습니다. 이 상태는 `disconnected = await request.is_disconnected()`로 확인할 수 있습니다.

#### 요청 파일

요청 파일은 일반적으로 멀티파트 폼 데이터(`multipart/form-data`)로 전송됩니다.

서명: `request.form(max_files=1000, max_fields=1000)`

`max_files`와 `max_fields` 매개변수를 사용하여 최대 필드 또는 파일 수를 구성할 수 있습니다:

```python
async with request.form(max_files=1000, max_fields=1000):
    ...
```

!!! info
    이러한 제한은 보안상의 이유로 설정되며, 무제한의 필드나 파일을 허용하면 너무 많은 빈 필드를 파싱하는 데 CPU와 메모리를 많이 소비하여 서비스 거부 공격으로 이어질 수 있습니다.

`async with request.form() as form`을 호출하면 `starlette.datastructures.FormData`를 받게 되며, 이는 파일 업로드와 텍스트 입력을 모두 포함하는 불변 멀티딕트입니다. 파일 업로드 항목은 `starlette.datastructures.UploadFile` 인스턴스로 표현됩니다.

`UploadFile`은 다음과 같은 속성을 가집니다:

* `filename`: 업로드된 원본 파일 이름을 나타내는 `str` 또는 사용할 수 없는 경우 `None` (예: `myimage.jpg`).
* `content_type`: 콘텐츠 타입(MIME 타입 / 미디어 타입)을 나타내는 `str` 또는 사용할 수 없는 경우 `None` (예: `image/jpeg`).
* `file`: <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" target="_blank">`SpooledTemporaryFile`</a> (<a href="https://docs.python.org/3/glossary.html#term-file-like-object" target="_blank">파일과 유사한</a> 객체). 이는 "파일과 유사한" 객체를 기대하는 다른 함수나 라이브러리에 직접 전달할 수 있는 실제 Python 파일입니다.
* `headers`: `Headers` 객체. 대개 이는 `Content-Type` 헤더만 포함하지만, 멀티파트 필드에 추가 헤더가 포함된 경우 여기에 포함됩니다. 이 헤더들은 `Request.headers`의 헤더와 관련이 없음을 주의하세요.
* `size`: 업로드된 파일의 크기(바이트)를 나타내는 `int`. 이 값은 요청 내용에서 계산되므로 업로드된 파일의 크기를 찾는 데에는 `Content-Length` 헤더보다 더 나은 선택입니다. 설정되지 않은 경우 `None`입니다.

`UploadFile`은 다음과 같은 `async` 메서드를 가집니다. 이들은 모두 내부적으로 해당하는 파일 메서드를 호출합니다(내부 `SpooledTemporaryFile` 사용).

* `async write(data)`: `data`(`bytes`)를 파일에 씁니다.
* `async read(size)`: 파일에서 `size`(`int`) 바이트를 읽습니다.
* `async seek(offset)`: 파일에서 바이트 위치 `offset`(`int`)으로 이동합니다.
    * 예를 들어, `await myfile.seek(0)`은 파일의 시작 위치로 이동합니다.
* `async close()`: 파일을 닫습니다.

이 모든 메서드는 `async` 메서드이므로 "await"를 사용해야 합니다.

예를 들어, 파일 이름과 내용을 다음과 같이 얻을 수 있습니다:

```python
async with request.form() as form:
    filename = form["upload_file"].filename
    contents = await form["upload_file"].read()
```

!!! info
    [RFC-7578: 4.2](https://www.ietf.org/rfc/rfc7578.txt)에 명시된 대로, 파일을 포함하는 form-data 콘텐츠 부분은 
    `Content-Disposition` 헤더에 `name`과 `filename` 필드가 있다고 가정합니다: `Content-Disposition: form-data;
    name="user"; filename="somefile"`. RFC-7578에 따르면 `filename` 필드는 선택사항이지만, 이는 
    Starlette가 어떤 데이터를 파일로 처리해야 하는지 구별하는 데 도움이 됩니다. `filename` 필드가 제공된 경우 
    기본 파일에 접근하기 위해 `UploadFile` 객체가 생성되며, 그렇지 않으면 form-data 부분이 파싱되어 원시 문자열로 사용 가능합니다.

#### 애플리케이션

원래의 Starlette 애플리케이션은 `request.app`을 통해 접근할 수 있습니다.

#### 기타 상태

요청에 추가 정보를 저장하려면 `request.state`를 사용할 수 있습니다.

예를 들어:

`request.state.time_started = time.time()`
