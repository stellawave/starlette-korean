Starlette는 Starlette와 통합되는 도구를 구축하거나 Starlette에 의존하는 도구 등을 개발하는 개발자 커뮤니티가 빠르게 성장하고 있습니다.

다음은 이러한 서드파티 패키지들입니다:

## 플러그인

### Apitally

<a href="https://github.com/apitally/python-client" target="_blank">GitHub</a> |
<a href="https://docs.apitally.io/frameworks/starlette" target="_blank">문서</a>

Starlette(및 기타 프레임워크)를 위한 간단한 트래픽, 에러 및 응답 시간 모니터링과 API 키 및 권한 관리.

### Authlib

<a href="https://github.com/lepture/Authlib" target="_blank">GitHub</a> |
<a href="https://docs.authlib.org/en/latest/" target="_blank">문서</a>

OAuth 및 OpenID Connect 클라이언트와 서버를 구축하기 위한 궁극의 Python 라이브러리입니다. [Starlette](https://docs.authlib.org/en/latest/client/starlette.html)와의 통합 방법을 확인하세요.

### ChannelBox

<a href="https://github.com/Sobolev5/channel-box" target="_blank">GitHub</a>

웹소켓 브로드캐스트를 위한 또 다른 솔루션. 코드의 어느 부분에서든 채널 그룹으로 메시지를 보낼 수 있습니다.
`channel-box`와 `starlette`를 사용하여 구축된 간단한 채팅 애플리케이션인 <a href="https://channel-box.andrey-sobolev.ru/" target="_blank">MySimpleChat</a>을 확인해보세요.

### Imia

<a href="https://github.com/alex-oleshkevich/imia" target="_blank">GitHub</a>

플러그인 가능한 인증자와 로그인/로그아웃 흐름을 갖춘 Starlette용 인증 프레임워크.

### Mangum

<a href="https://github.com/erm/mangum" target="_blank">GitHub</a>

AWS Lambda & API Gateway를 위한 서버리스 ASGI 어댑터.

### Nejma

<a href="https://github.com/taoufik07/nejma" target="_blank">GitHub</a>

웹소켓을 사용하여 채널 그룹에 메시지를 관리하고 보냅니다.
`nejma`와 `starlette`를 사용하여 구축된 간단한 채팅 애플리케이션인 <a href="https://github.com/taoufik07/nejma-chat" target="_blank">nejma-chat</a>을 확인해보세요.

### Scout APM

<a href="https://github.com/scoutapp/scout_apm_python" target="_blank">GitHub</a>

애플리케이션을 계측하여 성능 병목 현상을 찾을 수 있는 APM(애플리케이션 성능 모니터링) 솔루션.

### SpecTree

<a href="https://github.com/0b01001001/spectree" target="_blank">GitHub</a>

Python 어노테이션을 사용하여 OpenAPI 스펙 문서를 생성하고 요청 및 응답을 검증합니다. 보일러플레이트 코드가 적습니다(YAML 불필요).

### Starlette APISpec

<a href="https://github.com/Woile/starlette-apispec" target="_blank">GitHub</a>

Starlette를 위한 간단한 APISpec 통합.
엔드포인트의 독스트링에 YAML 형식으로 OpenAPI(Swagger) 스키마를 선언하여 Starlette로 구축된 REST API를 문서화합니다.

### Starlette Compress

<a href="https://github.com/Zaczero/starlette-compress" target="_blank">GitHub</a>

Starlette-Compress는 Starlette에서 응답을 압축하기 위한 빠르고 간단한 미들웨어입니다.
합리적인 기본 구성으로 ZStd, Brotli 및 GZip 압축을 지원합니다.

### Starlette Context

<a href="https://github.com/tomwojcik/starlette-context" target="_blank">GitHub</a>

요청의 컨텍스트 데이터를 저장하고 접근할 수 있게 해주는 Starlette용 미들웨어.
로깅과 함께 사용하여 x-request-id나 x-correlation-id와 같은 요청 헤더를 로그에 자동으로 사용할 수 있습니다.

### Starlette Cramjam

<a href="https://github.com/developmentseed/starlette-cramjam" target="_blank">GitHub</a>

최소한의 요구 사항으로 **brotli**, **gzip** 및 **deflate** 압축 알고리즘을 사용할 수 있게 해주는 Starlette 미들웨어.

### Starlette OAuth2 API

<a href="https://gitlab.com/jorgecarleitao/starlette-oauth2-api" target="_blank">GitLab</a>

JWT를 통한 인증 및 권한 부여를 추가하기 위한 Starlette 미들웨어.
클라이언트에게 액세스 및/또는 ID 토큰을 발급하기 위해 인증 제공자에만 의존합니다.

### Starlette Prometheus

<a href="https://github.com/perdy/starlette-prometheus" target="_blank">GitHub</a>

[공식 Python 클라이언트](https://github.com/prometheus/client_python)를 기반으로 [Prometheus](https://prometheus.io/) 메트릭을 노출하는 엔드포인트를 제공하는 플러그인.

### Starlette WTF

<a href="https://github.com/muicss/starlette-wtf" target="_blank">GitHub</a>

Starlette와 WTForms를 통합하기 위한 간단한 도구. 우수한 Flask-WTF 라이브러리를 모델로 삼았습니다.

### Starlette-Login

<a href="https://github.com/jockerz/Starlette-Login" target="_blank">GitHub</a> |
<a href="https://starlette-login.readthedocs.io/en/stable/" target="_blank">문서</a>

Starlette를 위한 사용자 세션 관리.
로그인, 로그아웃 및 장기간에 걸친 사용자 세션 기억과 같은 일반적인 작업을 처리합니다.

### Starsessions

<a href="https://github.com/alex-oleshkevich/starsessions" target="_blank">GitHub</a>

사용자 정의 가능한 스토리지 백엔드를 갖춘 대체 세션 지원 구현.

### webargs-starlette

<a href="https://github.com/sloria/webargs-starlette" target="_blank">GitHub</a>

[webargs](https://github.com/marshmallow-code/webargs)를 기반으로 한 Starlette용 선언적 요청 파싱 및 유효성 검사 라이브러리입니다.

타입 어노테이션을 사용하여 쿼리스트링, JSON, 폼, 헤더 및 쿠키를 파싱할 수 있습니다.

### DecoRouter

<a href="https://github.com/MrPigss/DecoRouter" target="_blank">GitHub</a>

Starlette를 위한 FastAPI 스타일의 라우팅입니다.

데코레이터를 사용하여 라우팅 테이블을 생성할 수 있습니다.

### Starception

<a href="https://github.com/alex-oleshkevich/starception" target="_blank">GitHub</a>

Starlette 앱을 위한 아름다운 예외 페이지입니다.

### Starlette-Admin

<a href="https://github.com/jowilf/starlette-admin" target="_blank">GitHub</a> |
<a href="https://jowilf.github.io/starlette-admin" target="_blank">문서</a>

간단하고 확장 가능한 관리자 인터페이스 프레임워크입니다.

[Tabler](https://tabler.io/)와 [Datatables](https://datatables.net/)로 구축되어 모델에 대해 완전히 사용자 정의 가능한 관리자 인터페이스를 빠르게 생성할 수 있습니다. 데이터를 여러 형식(*CSV*, *PDF*, *Excel* 등)으로 내보낼 수 있고, `AND`와 `OR` 조건을 포함한 복잡한 쿼리로 데이터를 필터링하고, 파일을 업로드할 수 있습니다.

### Vellox

<a href="https://github.com/junah201/vellox" target="_blank">GitHub</a>

GCP Cloud Functions를 위한 서버리스 ASGI 어댑터입니다.

## Starlette Bridge

<a href="https://github.com/tarsil/starlette-bridge" target="_blank">GitHub</a> |
<a href="https://starlette-bridge.tarsild.io/" target="_blank">문서</a>

`on_startup`과 `on_shutdown`의 지원 중단으로, Starlette Bridge는 여전히 이벤트를 선언하는 기존 방식을 사용할 수 있게 해줍니다. 내부적으로는 실제로 `lifespan`을 생성합니다. 이를 통해 기존 패키지의 후방 호환성을 보장하면서 Starlette의 새로운 `lifespan` 이벤트의 무결성을 유지합니다.

## 프레임워크

### FastAPI

<a href="https://github.com/tiangolo/fastapi" target="_blank">GitHub</a> |
<a href="https://fastapi.tiangolo.com/" target="_blank">문서</a>

고성능, 배우기 쉽고, 코딩이 빠르며, 프로덕션 준비가 된 웹 API 프레임워크입니다. 
**APIStar**의 이전 서버 시스템에서 영감을 받아 라우트 파라미터에 대한 타입 선언을 사용하며, OpenAPI 명세 버전 3.0.0+ (JSON Schema 포함)를 기반으로 하고, 데이터 처리를 위해 **Pydantic**을 사용합니다.

### Flama

<a href="https://github.com/vortico/flama" target="_blank">GitHub</a> |
<a href="https://flama.dev/" target="_blank">문서</a>

Flama는 현대적이고 견고한 **머신 러닝**(ML) API를 빠르게 구축하기 위한 **데이터 과학 지향 프레임워크**입니다. 프레임워크의 주요 목표는 ML API의 배포를 매우 간단하게 만드는 것입니다. Flama를 사용하면 데이터 과학자들은 이제 단 한 줄의 코드로 ML 모델을 비동기식, 자동 문서화된 API로 빠르게 전환할 수 있습니다. 모든 것이 단 몇 초 만에 이루어집니다!

Flama는 직관적인 CLI를 제공하며, **고성능** GraphQL, REST 및 ML API 구축을 가속화하기 위한 쉽게 배울 수 있는 철학을 제공합니다. 또한 비동기식 및 **프로덕션 준비** 서비스 개발을 위한 이상적인 솔루션을 구성하며, ML 모델을 위한 **자동 배포**를 제공합니다.

### Greppo

<a href="https://github.com/greppo-io/greppo" target="_blank">GitHub</a> |
<a href="https://docs.greppo.io/" target="_blank">문서</a>

지리공간 대시보드 및 웹 애플리케이션을 구축하기 위한 Python 프레임워크입니다.

Greppo는 지리공간 대시보드와 웹 애플리케이션을 쉽게 만들 수 있는 오픈소스 Python 프레임워크입니다. 데이터, 알고리즘, 시각화 및 상호작용을 위한 UI를 빠르게 통합할 수 있는 툴킷을 제공합니다. 백엔드의 변수를 업데이트하고, 로직을 재계산하며, 프론트엔드에 변경사항을 반영하는 API를 제공합니다(데이터 변경 훅).

### Responder

<a href="https://github.com/taoufik07/responder" target="_blank">GitHub</a> |
<a href="https://python-responder.org/en/latest/" target="_blank">문서</a>

비동기 웹 서비스 프레임워크입니다. 주요 기능: flask 스타일의 라우트 표현식, yaml 지원, OpenAPI 스키마 생성, 백그라운드 작업, GraphQL.

### Starlette-apps

[Django-GDAPS](https://gdaps.readthedocs.io/en/latest/)나 [CakePHP](https://cakephp.org/)와 같은 간단한 앱 시스템으로 자신만의 프레임워크를 만들어보세요.

<a href="https://github.com/yourlabs/starlette-apps" target="_blank">GitHub</a>

### Dark Star

HTML을 브라우저로 전송하는데 필요한 코드를 최소화하는 간단한 프레임워크입니다. 파일 경로를 Starlette 라우트로 변환하고 템플릿 바로 옆에 뷰 코드를 배치합니다. 프론트엔드 향상을 위해 [htmx](https://htmx.org) 지원을 포함합니다.

<a href="https://lllama.github.io/dark-star" target="_blank">문서</a>
<a href="https://github.com/lllama/dark-star" target="_blank">GitHub</a>

### Xpresso

Starlette, Pydantic 및 [di](https://github.com/adriangb/di)를 기반으로 구축된 유연하고 확장 가능한 웹 프레임워크입니다.

<a href="https://github.com/adriangb/xpresso" target="_blank">GitHub</a> |
<a href=https://xpresso-api.dev/" target="_blank">문서</a>

### Ellar

<a href="https://github.com/eadwinCode/ellar" target="_blank">GitHub</a> |
<a href="https://eadwincode.github.io/ellar/" target="_blank">문서</a>

Ellar는 빠르고 효율적이며 확장 가능한 REST API와 서버 사이드 애플리케이션을 구축하기 위한 ASGI 웹 프레임워크입니다. 서버 사이드 애플리케이션 구축에 높은 수준의 추상화를 제공하며 OOP(객체 지향 프로그래밍)와 FP(함수형 프로그래밍)의 요소를 결합합니다 - Nestjs에서 영감을 받았습니다.

**Starlette**, **Pydantic**, **injector** 3개의 핵심 라이브러리를 기반으로 구축되었습니다.

### Apiman

Starlette 프로젝트에 Swagger/OpenAPI 문서를 쉽게 통합하고 [SwaggerUI](http://swagger.io/swagger-ui/)와 [RedocUI](https://rebilly.github.io/ReDoc/)를 제공하는 확장입니다.

<a href="https://github.com/strongbugman/apiman" target="_blank">GitHub</a>

### Starlette-Babel

Babel 통합을 통해 번역, 현지화 및 시간대 지원을 제공합니다.

<a href="https://github.com/alex-oleshkevich/starlette_babel" target="_blank">GitHub</a>

### Starlette-StaticResources

<a href="https://github.com/DavidVentura/starlette-static-resources" target="_blank">GitHub</a>

[StaticFiles](https://www.starlette.io/staticfiles/)와 유사하게 정적 데이터를 위한 [패키지 리소스](https://docs.python.org/3/library/importlib.resources.html#module-importlib.resources) 마운팅을 허용합니다.

### Sentry

<a href="https://github.com/getsentry/sentry-python" target="_blank">GitHub</a> |
<a href="https://docs.sentry.io/platforms/python/guides/starlette/" target="_blank">문서</a>

Sentry는 소프트웨어 오류 감지 도구입니다. 성능 문제와 오류를 해결하기 위한 실행 가능한 통찰력을 제공하여 사용자가 Python 디버깅을 진단, 수정 및 최적화할 수 있습니다. 또한 Python 애플리케이션 개발을 위해 Starlette와 원활하게 통합됩니다. Sentry의 기능에는 오류 추적, 성능 인사이트, 상황별 정보, 알림/통지가 포함됩니다.

### Shiny

<a href="https://github.com/posit-dev/py-shiny" target="_blank">GitHub</a> |
<a href="https://shiny.posit.co/py/" target="_blank">문서</a>

Starlette와 asyncio를 활용하여 Shiny는 개발자가 반응형 프로그래밍의 힘을 사용하여 손쉽게 Python 웹 애플리케이션을 만들 수 있게 해줍니다. Shiny는 수동 상태 관리의 번거로움을 제거하고 런타임에 앱에 가장 적합한 실행 경로를 자동으로 결정하면서 동시에 재렌더링을 최소화합니다. 이는 Shiny가 가장 간단한 대시보드부터 모든 기능을 갖춘 웹 앱까지 지원할 수 있음을 의미합니다.
