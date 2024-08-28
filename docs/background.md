Starlette는 프로세스 내 백그라운드 작업을 위한 `BackgroundTask` 클래스를 포함합니다.

백그라운드 작업은 응답에 첨부되어야 하며, 응답이 전송된 후에만 실행됩니다.

### BackgroundTask

응답에 단일 백그라운드 작업을 추가하는 데 사용됩니다.

서명: `BackgroundTask(func, *args, **kwargs)`

```python
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.background import BackgroundTask


...

async def signup(request):
    data = await request.json()
    username = data['username']
    email = data['email']
    task = BackgroundTask(send_welcome_email, to_address=email)
    message = {'status': '가입 성공'}
    return JSONResponse(message, background=task)

async def send_welcome_email(to_address):
    ...


routes = [
    ...
    Route('/user/signup', endpoint=signup, methods=['POST'])
]

app = Starlette(routes=routes)
```

### BackgroundTasks

응답에 여러 백그라운드 작업을 추가하는 데 사용됩니다.

서명: `BackgroundTasks(tasks=[])`

```python
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.background import BackgroundTasks

async def signup(request):
    data = await request.json()
    username = data['username']
    email = data['email']
    tasks = BackgroundTasks()
    tasks.add_task(send_welcome_email, to_address=email)
    tasks.add_task(send_admin_notification, username=username)
    message = {'status': '가입 성공'}
    return JSONResponse(message, background=tasks)

async def send_welcome_email(to_address):
    ...

async def send_admin_notification(username):
    ...

routes = [
    Route('/user/signup', endpoint=signup, methods=['POST'])
]

app = Starlette(routes=routes)
```

!!! important
    작업은 순서대로 실행됩니다. 작업 중 하나가 예외를 발생시키면,
    이후의 작업들은 실행될 기회를 얻지 못합니다.
