# 기여하기

Starlette에 기여하는 데 관심을 가져주셔서 감사합니다.
프로젝트에 기여할 수 있는 여러 가지 방법이 있습니다:

- Starlette를 사용해보고 [발견한 버그/이슈를 보고](https://github.com/encode/starlette/issues/new)하세요
- [새로운 기능을 구현](https://github.com/encode/starlette/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)하세요
- [다른 사람의 Pull Request를 검토](https://github.com/encode/starlette/pulls)하세요
- 문서를 작성하세요
- 토론에 참여하세요

## 버그 또는 기타 이슈 보고하기

Starlette가 지원해야 할 것을 발견하셨나요?
예상치 못한 동작을 발견하셨나요?

기여는 일반적으로 [토론](https://github.com/encode/starlette/discussions)으로 시작해야 합니다.
잠재적인 버그는 "Potential Issue" 토론으로, 기능 요청은 "Ideas" 토론으로 제기할 수 있습니다. 
그 후 해당 토론을 "Issue"로 격상시킬지 여부나 pull request를 고려할지 결정할 수 있습니다.

가능한 한 자세히 설명하려고 노력하고, 버그 보고의 경우 다음과 같은 정보를 최대한 제공하세요:

- OS 플랫폼
- Python 버전
- 설치된 의존성 및 버전 (`python -m pip freeze`)
- 코드 스니펫
- 오류 트레이스백

항상 이슈를 보여주는 *가능한 가장 간단한 사례*로 예제를 줄이려고 노력해야 합니다.

## 개발

Starlette 개발을 시작하려면 GitHub에서 [Starlette 저장소](https://github.com/encode/starlette)를 **포크**하세요.

그런 다음 `YOUR-USERNAME`을 GitHub 사용자 이름으로 바꿔 다음 명령으로 포크를 클론하세요:

```shell
$ git clone https://github.com/YOUR-USERNAME/starlette
```

이제 다음을 사용하여 프로젝트와 그 의존성을 설치할 수 있습니다:

```shell
$ cd starlette
$ scripts/install
```

## 테스트 및 린팅

우리는 테스트, 린팅, 문서 빌드 워크플로우를 자동화하기 위해 사용자 정의 셸 스크립트를 사용합니다.

테스트를 실행하려면 다음을 사용하세요:

```shell
$ scripts/test
```

추가 인수는 `pytest`에 전달됩니다. 자세한 정보는 [pytest 문서](https://docs.pytest.org/en/latest/how-to/usage.html)를 참조하세요.

예를 들어, 단일 테스트 스크립트를 실행하려면:

```shell
$ scripts/test tests/test_application.py
```

코드 자동 포맷팅을 실행하려면:

```shell
$ scripts/lint
```

마지막으로, 코드 검사를 별도로 실행하려면 (`scripts/test`의 일부로도 실행됨):

```shell
$ scripts/check
```

## 문서 작성

문서 페이지는 `docs/` 폴더 아래에 있습니다.

문서 사이트를 로컬에서 실행하려면 (변경 사항을 미리 보는 데 유용함):

```shell
$ scripts/docs
```

## 빌드 / CI 실패 해결하기

풀 리퀘스트를 제출하면 테스트 스위트가 자동으로 실행되고 결과가 GitHub에 표시됩니다.
테스트 스위트가 실패하면 "Details" 링크를 클릭하여 테스트 스위트가 실패한 이유를 확인해야 합니다.

<p align="center" style="margin: 0 0 10px">
  <img src="https://raw.githubusercontent.com/encode/starlette/master/docs/img/gh-actions-fail.png" alt='실패한 PR 커밋 상태'>
</p>

테스트 스위트가 실패할 수 있는 몇 가지 일반적인 방법은 다음과 같습니다:

### Check 작업 실패

<p align="center" style="margin: 0 0 10px">
  <img src="https://raw.githubusercontent.com/encode/starlette/master/docs/img/gh-actions-fail-check.png" alt='실패한 GitHub action lint 작업'>
</p>

이 작업이 실패하면 코드 형식 문제 또는 타입 주석 문제가 있다는 의미입니다.
작업 출력을 확인하여 실패 이유를 파악하거나 셸에서 다음을 실행할 수 있습니다:

```shell
$ scripts/check
```

`$ scripts/lint`를 실행하여 코드를 자동 포맷팅하고 
작업이 성공하면 변경 사항을 커밋하는 것이 좋습니다.

### Docs 작업 실패

이 작업이 실패하면 문서 빌드에 실패했다는 의미입니다. 이는 잘못된 마크다운이나 
`mkdocs.yml` 내 누락된 설정 등 다양한 이유로 발생할 수 있습니다.

### Python 3.X 작업 실패

<p align="center" style="margin: 0 0 10px">
  <img src="https://raw.githubusercontent.com/encode/starlette/master/docs/img/gh-actions-fail-test.png" alt='실패한 GitHub action 테스트 작업'>
</p>

이 작업이 실패하면 유닛 테스트가 실패했거나 모든 코드 경로가 유닛 테스트로 커버되지 않았다는 의미입니다.

테스트가 실패하면 커버리지 보고서 아래에 다음 메시지가 표시됩니다:

`=== 1 failed, 435 passed, 1 skipped, 1 xfailed in 11.09s ===`

테스트는 통과했지만 커버리지가 현재 임계값에 도달하지 않으면 커버리지 보고서 
아래에 다음 메시지가 표시됩니다:

`FAIL Required test coverage of 100% not reached. Total coverage: 99.00%`

## 릴리스

*이 섹션은 Starlette 메인테이너를 대상으로 합니다.*

새 버전을 릴리스하기 전에 다음을 포함하는 풀 리퀘스트를 생성하세요:

- **변경 로그 업데이트**:
    - [keepachangelog](https://keepachangelog.com/en/1.0.0/) 형식을 따릅니다.
    - `master`를 최신 릴리스의 태그와 [비교](https://github.com/encode/starlette/compare/)하고 사용자에게 관심 있는 모든 항목을 나열하세요:
        - 변경 로그에 **반드시** 포함되어야 하는 항목: 추가, 변경, 폐기 또는 제거된 기능 및 버그 수정.
        - 변경 로그에 **포함되지 말아야 할** 항목: 문서, 테스트 또는 도구 변경.
        - 영향력/중요도 순으로 내림차순 정렬하세요.
        - 간결하고 핵심적으로 작성하세요. 🎯
- **버전 증가**: `__version__.py` 참조.

예시는 [#1600](https://github.com/encode/starlette/pull/1600)을 참조하세요.

릴리스 PR이 병합되면 다음을 포함하는 [새 릴리스](https://github.com/encode/starlette/releases/new)를 생성하세요:

- `0.13.3`과 같은 태그 버전.
- `Version 0.13.3`과 같은 릴리스 제목.
- 변경 로그에서 복사한 설명.

생성되면 이 릴리스가 자동으로 PyPI에 업로드됩니다.

PyPI 작업에 문제가 발생하면 `scripts/publish` 스크립트를 사용하여 
릴리스를 게시할 수 있습니다.
