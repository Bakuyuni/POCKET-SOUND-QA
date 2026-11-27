# POCKET SOUND QA — Audio Asset Inspector

**게임 오디오 에셋의 품질을 검사하고 관리하기 위한 Python 기반 WAV 검증 도구입니다.**

렌더링된 WAV 파일을 폴더 단위로 검사하고, 오디오 포맷 및 메타데이터를 검증하여 결과를 CSV 리포트로 출력합니다.

---

## 주요 기능

- **Recursive Folder Scan** — 하위 폴더를 포함한 WAV 파일 자동 검색
- **Audio Validation** — Sample Rate, Bit Depth, Channels, Subtype 검사
- **Status Classification** — PASSED / FAILED / ERROR 결과 분류
- **GUI Inspector** — 검사 결과 및 파일별 상세 정보 확인
- **CSV Export** — 검사 결과를 CSV 리포트로 저장
- **Duplicate Filename Handling** — 서로 다른 폴더에 존재하는 동일 파일명 구분
- **Relative Path Management** — 검사 폴더 기준 상대 경로 기록

## Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.12 |
| GUI | PySide6 |
| Audio Metadata | SoundFile |
| Report | CSV |
| Version Control | Git / GitHub |

## Project Structure

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

## Installation

저장소를 복제합니다.

```bash
git clone https://github.com/Bakuyuni/POCKET-SOUND-QA.git
cd POCKET-SOUND-QA
```

필요한 패키지를 설치합니다.

```bash
pip install -r requirements.txt
```

## Run

```bash
python pocket_qa.py
```

## Validation Status

| Status | Description |
|---|---|
| PASSED | 모든 검사 항목 통과 |
| FAILED | WAV 포맷 또는 메타데이터 기준 불일치 |
| ERROR | 파일 읽기 또는 검사 중 오류 발생 |

## Development Goal

게임 오디오 에셋 제작 과정에서 반복적으로 발생하는 검수 작업을 자동화하고, 사운드 에셋 관리 및 검증 파이프라인의 효율성을 높이는 것을 목표로 개발했습니다.

## Future Development

향후 REAPER 렌더링 자동화 및 Wwise 에셋 파이프라인과 연계하여 게임 오디오 제작 과정의 기술적 자동화 범위를 확장할 계획입니다.

---

## Project Documentation

프로젝트의 기획, 기술 설계, 구현 과정 및 테스트 결과는 아래 문서에서 확인할 수 있습니다.

- [상세 기술 포트폴리오 (Technical Portfolio)](docs/portfolio.md)

---

## Language

- [한국어 (Korean)](README.md)
- [日本語 (Japanese)](README_ja.md)

## 상세 포트폴리오

- [한국어 기술 포트폴리오](docs/portfolio.md)
- [日本語 技術ポートフォリオ](docs/portfolio_ja.md)

---

**Project: POCKET SOUND QA — Audio Asset Inspector**
