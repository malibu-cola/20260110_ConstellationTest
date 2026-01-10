# 88星座テスト

IAU（国際天文学連合）が定める88星座の名称を学習・テストするWebアプリケーションです。

## デモ

GitHub Pagesで公開中: `https://<username>.github.io/<repository>/`

## 機能

### フラッシュカード
- 88星座をカード形式で学習
- 日本語名から学名・略称を確認
- シャッフル機能付き

### クイズ
3種類の出題パターンから選択できます：

| 出題 | 回答例 |
|------|--------|
| 日本語 → 学名 | オリオン座 → Orion |
| 日本語 → 略称 | オリオン座 → Ori |
| 略称 → 日本語 | Ori → オリオン座 |

回答方式：
- **選択式**: 4択から正解を選ぶ
- **入力式**: キーボードで回答を入力

## GitHub Pagesで利用する

このアプリはstlite（Streamlit WebAssembly版）を使用しており、GitHub Pagesで静的にホスティングできます。

### 設定手順

1. このリポジトリをGitHubにプッシュ
2. リポジトリの Settings → Pages に移動
3. Source を「Deploy from a branch」に設定
4. Branch を「main」、フォルダを「/ (root)」に設定
5. Save をクリック

数分後に `https://<username>.github.io/<repository>/` でアクセス可能になります。

## ローカルで実行する

### 方法1: stlite版（index.html）

`index.html` をブラウザで直接開くか、ローカルサーバーで配信します：

```bash
python -m http.server 8000
```

ブラウザで http://localhost:8000 にアクセス

### 方法2: Streamlit版（app.py）

```bash
# 依存関係のインストール
uv sync

# アプリを起動
uv run streamlit run app.py
```

ブラウザで http://localhost:8501 にアクセス

## プロジェクト構成

```
.
├── index.html                # GitHub Pages用（stlite版）
├── app.py                    # Streamlitメインアプリ
├── data/
│   └── constellations.json   # 88星座データ（日本語名、学名、略称）
├── pyproject.toml            # プロジェクト設定
└── uv.lock                   # 依存関係ロックファイル
```

## データ形式

`data/constellations.json` には以下の形式で88星座のデータが格納されています：

```json
[
  {"japanese": "オリオン座", "latin": "Orion", "abbr": "Ori"},
  ...
]
```

- `japanese`: 日本語名
- `latin`: 学名（ラテン語）
- `abbr`: 略称（3文字）

## 技術スタック

- [Streamlit](https://streamlit.io/) - PythonのWebアプリフレームワーク
- [stlite](https://github.com/whitphx/stlite) - StreamlitのWebAssembly実装
