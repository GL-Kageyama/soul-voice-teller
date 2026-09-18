# 評価 —— 外部評価（novel-council-layer）の実行メモ（巻三）

## 位置づけ

巻三の設計（`構想/design.md`・`構想/話割り.md`・`構想/各話/` の場面表16ファイル）に対する外部評価である（2026-09-19）。**執筆に入る前**の設計を対象とする。

- **評価するのは設計であって、散文ではない。** 散文はまだ一行も無い。ゆえに `content_type` は `plot`、招集は十名（`prose-style`・`narrative-technique`・`reader-experience` は招集外）。
- 五単位（巻一〜巻四＋系列）のひとつである。**単位の切り方・招集する席・匿名化・評議会に渡す文脈・SKILL.md からの逸脱・反映の作法は、系列の [`../../habits/評価/README.md`](../../habits/評価/README.md) に一本化して書いてある。ここには巻三に固有のことだけを書く。**

## 入力（準備済み・実測）

| ファイル | 内容 | 実測バイト |
|---|---|---|
| `input-concept.md` | `design.md` ＋ `話割り.md` ＋ `各話/*.md`（16ファイル）を**話順に逐語で連結**しただけ。**本文は一行も直していない・整形していない** | 126,996 |
| `input-anonymized.md` | **評価者に渡すのはこちら** | 126,996 |

**出典の数は 18。**（`design.md` 1 ＋ `話割り.md` 1 ＋ 各話 16）

## 匿名化について（実測）

`utils/anonymize.py` に `--title "ハビッツ！！！"` と `--title "ハビッツ"` を渡して実行。**赤字0件**であり、`input-concept.md` と `input-anonymized.md` は**バイト単位で同一**である。**作品名は設計文書に一度も現れない**——ゆえにこの入力では、第一の盲は入力そのものが満たしている。

## 実行方法

**novel-council-layer 内の新セッション**で [`../../habits/評価/起動カード.md`](../../habits/評価/起動カード.md) の枠内を貼る。巻三は**3番目**に走る。

> **本文は評価者に Read させる**（議長の文脈に通さない）。`SKILL.md` の「インラインで渡す」という字面からの意図的な逸脱である。理由は系列の README を参照。

## 期待される出力

`report.json` ／ `report.md`（`python utils/render_report.py report.json -o report.md --lang ja`）／ `individual_reports/`（評価者十名分の素の出力）。

## 進捗

[`../../habits/評価/進捗.md`](../../habits/評価/進捗.md) ——五単位の進み具合と、著者待ちの一覧。
