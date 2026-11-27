# POCKET SOUND QA — Audio Asset Inspector

**게임 오디오 에셋의 품질 검증 및 관리 자동화를 위한 Python 기반 데스크톱 도구**

---

# 01. Project Overview

| 항목 | 내용 |
|---|---|
| 프로젝트 유형 | 게임 오디오 에셋 검증 도구 개발 |
| 개발 환경 | Python 3.12 / Windows |
| 사용 기술 | Python, PySide6, SoundFile, CSV |
| 담당 역할 | 기획, 설계, 개발, 테스트 |

POCKET QA는 게임 오디오 제작 과정에서 발생하는 WAV 에셋의 검수 작업을 자동화하기 위해 개발한 데스크톱 도구입니다.

지정한 폴더와 하위 폴더를 탐색하여 WAV 파일을 수집하고, 오디오 메타데이터 및 설정된 검수 기준을 확인합니다. 검사 결과는 GUI에서 확인할 수 있으며 CSV 리포트로 내보낼 수 있습니다.

# 02. Problem

게임 오디오 제작 과정에서는 다수의 사운드 에셋을 엔진에 적용하기 전에 포맷과 메타데이터를 확인해야 합니다.

기존의 수동 검수 방식에는 다음과 같은 문제가 있었습니다.

- 다수의 WAV 파일을 개별적으로 확인해야 하는 반복 작업
- Sample Rate와 Bit Depth 등의 설정 오류를 놓칠 가능성
- 손상되었거나 읽을 수 없는 파일을 별도로 확인해야 하는 문제
- 서로 다른 폴더에 동일한 파일명이 존재할 경우 파일을 구분하기 어려움
- 검수 결과를 기록하고 관리하는 과정의 비효율성

따라서 반복적인 WAV 검수 과정을 자동화하고, 결과를 일관된 형식으로 관리할 수 있는 도구가 필요했습니다.

# 03. Plan / Design

## 3.1 Functional Design

검수 과정을 다음과 같이 설계했습니다.

1. 사용자가 검사할 폴더를 선택합니다.
2. 선택한 폴더와 하위 폴더에서 WAV 파일을 탐색합니다.
3. 각 파일의 메타데이터를 읽고 검수 기준과 비교합니다.
4. 검사 결과를 PASSED / FAILED / ERROR로 분류합니다.
5. GUI에서 전체 결과와 개별 파일 정보를 확인합니다.
6. 검사 결과를 CSV 리포트로 내보냅니다.

## 3.2 Validation Criteria

| 항목 | 검사 기준 |
|---|---|
| Sample Rate | GUI에서 선택한 기준값과 비교 |
| Bit Depth | GUI에서 선택한 기준값과 비교 |
| Channels | Mono(1), Stereo(2) 허용 |
| Subtype | PCM 및 FLOAT 계열 등의 실제 포맷 확인 |

검사 결과는 다음과 같이 분류했습니다.

| Status | Description |
|---|---|
| **PASSED** | 모든 검수 기준 통과 |
| **FAILED** | 파일은 읽을 수 있지만 검수 기준과 불일치 |
| **ERROR** | 파일을 읽거나 검사하는 과정에서 오류 발생 |

## 3.3 Module Architecture

기능별로 코드를 분리하여 유지보수와 확장이 가능하도록 설계했습니다.

| Module | Responsibility |
|---|---|
| `pocket_qa.py` | 사용자 인터페이스 및 기능 연결 |
| `scanner.py` | 폴더 탐색 및 WAV 파일 수집 |
| `validator.py` | WAV 메타데이터 검사 |
| `exporter.py` | 검사 결과 CSV 출력 |

프로젝트 구조:

```text
POCKET-SOUND-QA/
│
├── audio/
│   ├── exporter.py
│   ├── scanner.py
│   └── validator.py
│
├── docs/
│   └── portfolio.md
│
├── pocket_qa.py
├── requirements.txt
├── README.md
└── .gitignore
```

# 04. Solution

## 4.1 Recursive Folder Scanning

Python의 `pathlib`를 활용하여 선택한 폴더뿐 아니라 하위 폴더까지 탐색하도록 구현했습니다.

이를 통해 사용자가 폴더를 일일이 지정하지 않아도 전체 WAV 에셋을 한 번에 검사할 수 있습니다.

## 4.2 Audio Metadata Validation

SoundFile 라이브러리를 활용하여 WAV 파일의 메타데이터를 읽고 설정된 검수 기준과 비교하도록 구현했습니다.

다음 항목을 검사하여 파일별 검수 결과를 생성합니다.

- Sample Rate
- Bit Depth
- Channels
- Subtype

## 4.3 Error Handling

파일을 읽는 과정에서 발생할 수 있는 오류를 별도로 처리했습니다.

정상적으로 읽을 수 있지만 기준에 맞지 않는 파일과 파일 자체를 읽을 수 없는 경우를 구분하여 결과의 신뢰성을 높였습니다.

## 4.4 GUI Inspector

PySide6를 활용하여 검사 과정을 직관적으로 확인할 수 있는 GUI를 구현했습니다.

주요 기능:

- 검사 폴더 선택
- Sample Rate 및 Bit Depth 설정
- 검사 결과 테이블
- 전체 검사 수 및 PASSED / FAILED / ERROR 요약
- 선택한 파일의 상세 정보 확인
- CSV 리포트 내보내기

## 4.5 CSV Report Export

검사 결과를 CSV 파일로 저장하도록 구현했습니다.

서로 다른 폴더에 동일한 파일명이 존재하더라도 구분할 수 있도록 검사 폴더 기준 상대 경로를 함께 기록했습니다.

또한 다음 사항을 적용했습니다.

- UTF-8-SIG 인코딩을 적용하여 Excel에서 한글이 깨지는 문제 방지
- 기존 파일을 실수로 덮어쓰지 않도록 처리
- 상대 경로를 활용하여 파일 식별 및 결과 관리

# 05. Technical Details

## 5.1 File System Management

- `pathlib`를 이용한 경로 관리
- `rglob()`을 이용한 하위 폴더 탐색
- `relative_to()`를 이용한 상대 경로 생성
- 파일명과 경로를 분리하여 중복 파일명 관리

## 5.2 Data Processing

- Dictionary와 List를 활용한 검사 결과 관리
- 파일별 메타데이터 및 오류 정보 저장
- 파일 경로를 기준으로 검사 결과 매칭

## 5.3 GUI Development

- PySide6 기반 데스크톱 GUI 구현
- Signal과 Slot을 활용한 이벤트 처리
- 검사 결과에 따른 UI 업데이트
- 선택한 파일의 상세 정보 표시

## 5.4 Exception Handling

- 파일 읽기 오류 처리
- 검사 결과 상태 분리
- CSV 파일 덮어쓰기 방지

# 06. Validation & Testing

개발 완료 후 다음 항목을 테스트했습니다.

| Test Case | Expected Result | Result |
|---|---|---|
| 하위 폴더 탐색 | 모든 WAV 파일 검색 | PASS |
| Sample Rate 검사 | 기준값과 비교 | PASS |
| Bit Depth 검사 | 기준값과 비교 | PASS |
| Channel 검사 | Mono / Stereo 확인 | PASS |
| Subtype 검사 | 실제 포맷 확인 | PASS |
| 파일 오류 처리 | ERROR로 분류 | PASS |
| 중복 파일명 | 상대 경로로 구분 | PASS |
| CSV 출력 | 검사 결과 정상 저장 | PASS |
| 기존 CSV 보호 | 덮어쓰기 차단 | PASS |
| 한글 인코딩 | Excel에서 정상 표시 | PASS |

# 07. Result & Future Improvements

## 7.1 Result

POCKET QA를 통해 WAV 오디오 에셋의 반복적인 검수 과정을 자동화했습니다.

폴더 탐색부터 메타데이터 검사, 결과 분류, CSV 리포트 출력까지 하나의 프로그램에서 처리할 수 있도록 구현했습니다.

특히 상대 경로를 기반으로 동일한 파일명을 가진 에셋을 구분하고, 검사 결과를 일관된 형식으로 관리할 수 있도록 개선했습니다.

## 7.2 Future Improvements

향후 다음과 같은 기능으로 확장할 계획입니다.

- 파일명 및 에셋 네이밍 규칙 검증
- 추가 오디오 포맷 및 메타데이터 검사
- REAPER 렌더링 결과 자동 분류 및 검증
- Wwise Import 폴더 자동 생성
- Unreal Engine 및 Wwise 에셋 파이프라인 연동

## 7.3 Technical Sound Design Relevance

이 프로젝트는 게임 오디오 에셋의 품질을 관리하고 반복적인 작업을 자동화하는 기술적 접근을 보여줍니다.

향후 REAPER, Wwise, Unreal Engine과 연계하여 사운드 제작부터 엔진 적용까지 이어지는 자동화 및 검증 파이프라인으로 발전시키는 것을 목표로 합니다.

---

**Project: POCKET SOUND QA — Audio Asset Inspector**