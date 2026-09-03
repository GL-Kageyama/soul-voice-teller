# 評価4 —— 外部評価（novel-council-layer）の実行メモ

## 位置づけ

評価3（council 外部評価 text/full）から、6品質スキル研ぎ＋scene-writer 深書き＋revise-for-reader／entertainment 全48話照査を経た現行稿に対する再評価。

## 入力（準備済み）

| ファイル | 内容 |
|---|---|
| `input-anonymized.md` | 匿名化済み全文（設計書＋散文全48話）。タイトル「白地図」→〔匿名〕。**評価者に渡すのはこちら** |
| `input-concept.md` | 匿名化前の同一全文（執筆者側の参照用） |

## 実行方法（評議会レベル検証は novel-council-layer 内の新セッション必須）

評価は書き手レイヤーと切り離すため、**novel-council-layer 内の新セッション**で実行する（この制約は memory に明記）。

```
cd "/Users/user/AI評価者たちによる「知恵の評議会」/novel-council-layer"
claude   # 新セッション
```

そのセッションで `/story-council` を起動し、以下を渡す:

- **content**: `soul-voice-teller/examples/hakuchizu/評価4/input-anonymized.md` の全文（Read で読んで渡す）
- **content_type**: `text`
- **domain**: `pure-literature`
- **mode**: `full`（13評価者全員）
- **lang**: `ja`

## 期待される出力（評価4 へ書き出す）

- `report.json` — 統合 Story Report（story_vector／disagreement_map／classification／revision_direction）
- `report.md` — `python utils/render_report.py report.json -o report.md --lang ja` による可視化
- `individual_reports/*.json` — 評価者13名分の素の出力（弱点・改善提案・予想不一致点を保全）
- `comparison.md` — `python utils/compare_reports.py 評価3/report.json 評価4/report.json` による改善度の差分

## ループ

評価4 → `revision_direction`（次回の修正方向）→ リライト → 再評価 → compare_reports.py で改善度確認、を繰り返す。
