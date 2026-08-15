# examples/

パイプラインの成果物とデモを置く。大きく4種:

```
examples/
├── bonodori/   # 作品サンプル（フルフロー・ja）
├── pool/       # 作品サンプル（フルフロー・ja）
├── sample/     # 最小パイプラインのデモ（lighthouse ＋ サンプル persona）
├── i18n/       # i18n 検証（フルフロー・en/ja/zh）
└── personas/   # persona 多様性のデモ（最小パイプライン・5パターン）
```

## 作品サンプル（`<work-slug>/`）

`bonodori/` `pool/` は、パイプラインを一気通しした作品の成果物。各 `<work-slug>/` に、スキルを順に呼んだ結果が並ぶ:

```
<work-slug>/
├── premise.md           # /premise の出力（ログライン・核心の問い・テーマ・読者像と約束）
├── design.md            # /plot-design の出力（必須構想＋任意下準備）
├── draft_1_<場面>.md     # /fast-draft の場面単位の草稿
├── draft.md             # 全場面を連結した草稿
├── draft_revised.md     # /revise-for-reader の出力（あれば）
└── series-bible.md      # /series-bible の出力（あれば）
```

## sample/（最小パイプラインのデモ）

`sample/` は最小パイプライン（writer-persona → premise → plot-design → fast-draft）の**動きを見せる**ための一式。詳細は [sample/README.md](sample/README.md)。

## i18n/（多言語検証）

`i18n/{en,ja,zh}/` は、同じ種（灯台守）を **en / ja / zh の3言語でフルフロー（全15スキル）** した検証用デモ。

## personas/（persona 多様性のデモ）

`personas/<slug>/` は、同じ最小パイプラインに、**フォーマットも声も違う5つの persona** を流して、persona の効き（声の違い）を示すデモ。各 slug に `sample-persona.md` ／ `premise.md` ／ `design.md` ／ `draft_1〜3_<場面>.md` ／ `draft.md` が並ぶ。

| slug | persona の形式 | 題材（種） |
|---|---|---|
| `tegami` | 手紙（老女・戦後） | 行方不明の夫へ五十年、年賀状を出し続ける妻 |
| `suimin` | 計測ログ（理系・都市） | 眠れない夜に、自分だけの夢を記録するアプリ開発者 |
| `matsuri` | 語り聞かせ（方言・田舎） | 廃村まぎわで最後の祭りを続ける若者 |
| `iro` | 色の断章（少女・幻想） | 色を失った街で、少女だけが夜明けの色を覚えている |
| `katana` | 道具目録（職人・硬質） | 最後の一振りに師の形見の鋼を込める刀鍛冶 |

## 使い方

```bash
# 作品の作業ディレクトリを決めて、スキルを順に呼ぶ
/writer-persona                          # まず persona（~/.soul-voice-teller/persona.md）
/premise 灯台守は海を怖がるのに、海からしか来ない唯一の客を待つ
/plot-design                             # examples/<work>/design.md を作る
/fast-draft                              # examples/<work>/draft_*.md を書く
```

- 書き手の永続状態（persona / voice-ledger）は `~/.soul-voice-teller/` に置き、作品ごとの成果物だけをここに置く。
- `draft_<n>_<場面>.md` は**再草稿の単位**。外部評価の結果を該当場面に反映するとき、そのファイルを `/fast-draft` で書き直す。
