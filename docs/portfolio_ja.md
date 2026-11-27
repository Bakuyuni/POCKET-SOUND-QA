# POCKET SOUND QA — Audio Asset Inspector

**ゲームオーディオアセットの品質検証・管理を自動化するPythonベースのデスクトップツール**

---

# 01. Project Overview

| 項目 | 内容 |
|---|---|
| プロジェクト種別 | ゲームオーディオアセット検証ツールの開発 |
| 開発環境 | Python 3.12 / Windows |
| 使用技術 | Python, PySide6, SoundFile, CSV |
| 担当範囲 | 企画、設計、開発、テスト |

POCKET QAは、ゲームオーディオ制作工程で発生するWAVアセットの検証作業を自動化するために開発したデスクトップツールです。

指定したフォルダおよびサブフォルダを再帰的に検索してWAVファイルを収集し、オーディオのメタデータと設定された検証基準を照合します。

検査結果はGUI上で確認でき、CSVレポートとして出力できます。

# 02. Problem

ゲームオーディオ制作では、多数のサウンドアセットをゲームエンジンに組み込む前に、フォーマットやメタデータを確認する必要があります。

従来の手動検証には、以下のような課題がありました。

- 多数のWAVファイルを個別に確認する必要があるため、繰り返し作業が発生する
- Sample RateやBit Depthなどの設定ミスを見落とす可能性がある
- 破損しているファイルや読み込みできないファイルを個別に確認する必要がある
- 異なるフォルダに同じファイル名が存在する場合、ファイルの識別が難しい
- 検証結果の記録および管理に手間がかかる

これらの課題を解決するため、WAVファイルの検証作業を自動化し、結果を一貫した形式で管理できるツールが必要でした。

# 03. Plan / Design

## 3.1 Functional Design

検証プロセスを以下のように設計しました。

1. ユーザーが検査対象のフォルダを選択する
2. 選択したフォルダとサブフォルダからWAVファイルを検索する
3. 各ファイルのメタデータを取得し、検証基準と照合する
4. 検査結果をPASSED / FAILED / ERRORに分類する
5. GUI上で全体の検査結果と個別ファイルの詳細情報を確認する
6. 検査結果をCSVレポートとして出力する

## 3.2 Validation Criteria

| 項目 | 検証基準 |
|---|---|
| Sample Rate | GUIで選択した基準値と照合 |
| Bit Depth | GUIで選択した基準値と照合 |
| Channels | Mono（1）、Stereo（2）を許可 |
| Subtype | PCMやFLOAT系などの実際のフォーマットを確認 |

検査結果は以下の3種類に分類しました。

| Status | Description |
|---|---|
| **PASSED** | すべての検証基準を満たしている |
| **FAILED** | ファイルの読み込みは可能だが、検証基準と一致しない |
| **ERROR** | ファイルの読み込み、または検査中にエラーが発生した |

## 3.3 Module Architecture

保守性と拡張性を考慮し、機能ごとにモジュールを分離しました。

| Module | Responsibility |
|---|---|
| `pocket_qa.py` | ユーザーインターフェースおよび各機能の連携 |
| `scanner.py` | フォルダ検索およびWAVファイルの収集 |
| `validator.py` | WAVメタデータの検証 |
| `exporter.py` | 検査結果のCSV出力 |

プロジェクト構成：

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

# 04. Solution

## 4.1 Recursive Folder Scanning

Pythonの`pathlib`を使用し、選択したフォルダだけでなく、その配下にあるサブフォルダも含めて検索できるように実装しました。

これにより、ユーザーがフォルダを一つずつ指定することなく、複数のWAVアセットをまとめて検査できるようにしました。

## 4.2 Audio Metadata Validation

SoundFileライブラリを使用してWAVファイルのメタデータを取得し、設定された検証基準と照合する機能を実装しました。

以下の項目を検査し、ファイルごとの検証結果を生成します。

- Sample Rate
- Bit Depth
- Channels
- Subtype

## 4.3 Error Handling

ファイルの読み込み時に発生する可能性のあるエラーを個別に処理しました。

正常に読み込めるものの検証基準を満たさないファイルと、ファイル自体を読み込めないケースを区別することで、検査結果の信頼性を高めました。

## 4.4 GUI Inspector

PySide6を使用し、検査プロセスと結果を直感的に確認できるGUIを実装しました。

主な機能：

- 検査対象フォルダの選択
- Sample RateおよびBit Depthの設定
- 検査結果テーブルの表示
- 検査総数およびPASSED / FAILED / ERRORの集計
- 選択したファイルの詳細情報の表示
- CSVレポートの出力

## 4.5 CSV Report Export

検査結果をCSVファイルとして保存する機能を実装しました。

異なるフォルダに同じファイル名のアセットが存在する場合でも識別できるよう、検査対象フォルダを基準とした相対パスを記録する仕組みを導入しました。

また、以下の対応を行いました。

- UTF-8-SIGエンコーディングを適用し、Excelで日本語などの文字が文字化けする問題を防止
- 既存ファイルの誤った上書きを防止
- 相対パスを利用したファイル識別と検査結果の管理

# 05. Technical Details

## 5.1 File System Management

- `pathlib`によるファイルパスの管理
- `rglob()`によるサブフォルダの再帰検索
- `relative_to()`による相対パスの生成
- ファイル名とパスを分離した同名ファイルの管理

## 5.2 Data Processing

- DictionaryとListを使用した検査結果の管理
- ファイルごとのメタデータおよびエラー情報の保存
- ファイルパスを基準とした検査結果の照合

## 5.3 GUI Development

- PySide6によるデスクトップGUIの実装
- SignalとSlotを使用したイベント処理
- 検査結果に応じたUIの更新
- 選択したファイルの詳細情報の表示

## 5.4 Exception Handling

- ファイル読み込み時のエラー処理
- 検査結果のステータス分類
- CSVファイルの上書き防止

# 06. Validation & Testing

開発完了後、以下の項目についてテストを実施しました。

| Test Case | Expected Result | Result |
|---|---|---|
| サブフォルダ検索 | すべてのWAVファイルを検索 | PASS |
| Sample Rate検査 | 基準値との照合 | PASS |
| Bit Depth検査 | 基準値との照合 | PASS |
| Channel検査 | Mono / Stereoの確認 | PASS |
| Subtype検査 | 実際のフォーマットを確認 | PASS |
| ファイルエラー処理 | ERRORとして分類 | PASS |
| 同名ファイルの識別 | 相対パスによる識別 | PASS |
| CSV出力 | 検査結果を正常に保存 | PASS |
| 既存CSVの保護 | 上書きを防止 | PASS |
| 文字コード | Excelで正常に表示 | PASS |

# 07. Result & Future Improvements

## 7.1 Result

POCKET QAの開発により、WAVオーディオアセットの反復的な検証作業を自動化しました。

フォルダ検索からメタデータ検証、結果の分類、CSVレポートの出力まで、一つのアプリケーションで処理できるようにしました。

特に、相対パスを利用して同じファイル名を持つアセットを識別し、検査結果を一貫した形式で管理できるように改善しました。

## 7.2 Future Improvements

今後、以下の機能への拡張を計画しています。

- ファイル名およびアセットの命名規則の検証
- 対応するオーディオフォーマットおよびメタデータ項目の追加
- REAPERのレンダリング結果の自動分類および検証
- Wwise Importフォルダの自動生成
- Unreal EngineおよびWwiseのアセットパイプラインとの連携

## 7.3 Technical Sound Design Relevance

本プロジェクトでは、ゲームオーディオアセットの品質管理と反復作業の自動化に対する技術的なアプローチを実装しました。

今後はREAPER、Wwise、Unreal Engineとの連携を進め、サウンド制作からゲームエンジンへの実装までをつなぐ、自動化および検証パイプラインへと発展させることを目指しています。

---

**Project: POCKET SOUND QA — Audio Asset Inspector**