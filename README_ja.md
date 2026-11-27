# POCKET SOUND QA — Audio Asset Inspector

**ゲームオーディオアセットの品質検証・管理を効率化するPythonベースのデスクトップツールです。**

レンダリングされたWAVファイルをフォルダ単位で検査し、オーディオフォーマットやメタデータを検証します。検査結果はGUIで確認でき、CSVレポートとして出力できます。

---

## 主な機能

- **Recursive Folder Scan** — サブフォルダを含むWAVファイルの自動検索
- **Audio Validation** — Sample Rate、Bit Depth、Channels、Subtypeの検証
- **Status Classification** — PASSED / FAILED / ERRORによる検査結果の分類
- **GUI Inspector** — 検査結果およびファイルごとの詳細情報の表示
- **CSV Export** — 検査結果のCSVレポート出力
- **Duplicate Filename Handling** — 異なるフォルダに存在する同名ファイルの識別
- **Relative Path Management** — 検査対象フォルダを基準とした相対パスの管理

## 技術スタック

| 項目 | 技術 |
|---|---|
| Language | Python 3.12 |
| GUI | PySide6 |
| Audio Metadata | SoundFile |
| Report | CSV |
| Version Control | Git / GitHub |

## プロジェクト構成

```text
POCKET-SOUND-QA/
│
├── audio/
│   ├── exporter.py
│   ├── scanner.py
│   └── validator.py
│
├── docs/
│   ├── portfolio.md
│   └── portfolio_ja.md
│
├── pocket_qa.py
├── requirements.txt
├── README.md
├── README_ja.md
└── .gitignore
```

## インストール

リポジトリをクローンします。

```bash
git clone https://github.com/Bakuyuni/POCKET-SOUND-QA.git
cd POCKET-SOUND-QA
```

必要なパッケージをインストールします。

```bash
pip install -r requirements.txt
```

## 起動方法

```bash
python pocket_qa.py
```

## 検査結果の分類

| Status | Description |
|---|---|
| PASSED | すべての検査項目に合格 |
| FAILED | ファイルの読み込みは可能だが、検査基準と不一致 |
| ERROR | ファイルの読み込みまたは検査中にエラーが発生 |

## プロジェクトの目的

ゲームオーディオ制作において繰り返し発生するアセットの検証作業を自動化し、サウンドアセットの管理および品質検証プロセスの効率化を目指して開発しました。

## 今後の拡張計画

今後はREAPERのレンダリング自動化やWwiseのアセット管理パイプラインとの連携を通じて、ゲームオーディオ制作工程における技術的な自動化の範囲を拡張する予定です。

---

## 詳細ドキュメント

- [日本語版 技術ポートフォリオ](docs/portfolio_ja.md)
- [韓国語版 技術ポートフォリオ](docs/portfolio.md)

---

**Project: POCKET SOUND QA — Audio Asset Inspector**