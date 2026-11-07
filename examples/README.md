# examples/

パイプラインの成果物とデモを置く。

## 配置

```
examples/
├── works/
│   ├── novels/   作品（フルフロー・ja）
│   └── music/    主題歌・サムネイル
├── series/       連作（複数作品を並べる企画）
├── demos/        最小パイプラインと多言語のデモ
├── _archive/     旧版・backup
└── README.md
```

## 置き方の指針

新しい成果物は、次の順で置き場所を決める。

1. **特定の小説・物語に属するか** → `works/novels/<作品名>/`
2. **主題歌・タイトル・サムネイルか** → `works/music/<作品名>/`
3. **複数作品を並べる連作か** → `series/<名前>/`
4. **スキルの動きを見せるデモ・検証か** → `demos/<名前>/`
5. **一度きりの出力・旧版・backup か** → `_archive/`

- 直下に作品を置かない。必ず分類フォルダの下に置く。
- 1作品1フォルダ。作品名は kebab-case。
- 作品フォルダの中は、スキルの出力名をそのまま使う（`premise.md` `design.md` `draft_*.md`）。
- 追加したら上の配置図を更新する。

## 作品（`works/novels/<slug>/`）

各 `<slug>/` に、スキルを順に呼んだ結果が並ぶ:

```
<slug>/
├── premise.md           # /premise の出力（ログライン・核心の問い・テーマ・読者像と約束）
├── design.md            # /plot-design の出力（必須構想＋任意下準備）
├── draft_1_<場面>.md     # /fast-draft の場面単位の草稿
├── draft.md             # 全場面を連結した草稿
├── draft_revised.md     # /revise-for-reader の出力（あれば）
└── series-bible.md      # /series-bible の出力（あれば）
```

長編は、`構想/` `草稿/` `評価/` `届ける/` のように工程で分けてよい。

## 主題歌（`works/music/<slug>/`）

`theme-song.md` と、その読み違い予防版・ミックス版を置く。曲名・読み・裁定は各ファイルに書く。

## series/

`series/<名前>/` は、複数の作品（例: 職種別の連作）を1つの企画として並べる。各作品は独立したフォルダにする。

## demos/

- `sample/` — 最小パイプライン（writer-persona → premise → plot-design → fast-draft）のデモ。詳細は [demos/sample/README.md](demos/sample/README.md)。
- `i18n/` — 同じ種（灯台守）を en / ja / zh の3言語でフルフローした検証。
- `personas/` — 同じ最小パイプラインに、フォーマットも声も違う5つの persona を流したデモ。
- `axes/` — 6つの反応軸をそれぞれ主軸に据えた6本のサンプル。
- `hook-sample/` — フック設計のサンプル。

### personas の一覧

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
/plot-design                             # examples/works/novels/<work>/design.md を作る
/fast-draft                              # examples/works/novels/<work>/draft_*.md を書く
```

- 書き手の永続状態（persona / voice-ledger）は `~/.soul-voice-teller/` に置き、作品ごとの成果物だけをここに置く。
- `draft_<n>_<場面>.md` は**再草稿の単位**。外部評価の結果を該当場面に反映するとき、そのファイルを `/fast-draft` で書き直す。
