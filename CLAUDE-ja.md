**Language:** [English](CLAUDE.md) | 日本語 | [中文](CLAUDE-zh.md)

# soul-voice-teller

## Project Identity（プロジェクトの正体）

これは**小説執筆スキル**のレイヤー。書き手（人間）の魂・声・嗜好を映す `writer-persona`、発想の `premise`、設計の `plot-design`、草稿の `fast-draft`、声を貯める `voice-ledger` の5スキルに、任意下準備の `narration-design` / `character-forge` / `character-in-action` / `character-bond` / `worldbuild` / `world-iceberg` / `research-verify`と、書く質・改稿・長期の `prose` / `scene-writer` / `series-bible` / `revise-for-reader` / `entertainment` / `whole-work-review`、届けるの `package` / `theme-song` を加えた20スキルで構成する。

## 核心命題（一番上に置く）

**書くことは、魂を運ぶこと。**

- 「誰のものでもない平均的な文」を避けること（個別性）は**目的ではない**。読者の心を動かし、記憶に残るもの（魂）を運ぶことが目的で、個別性はそのための**手段**の一つ。
- この反転は実証済み（[docs/実証.md](docs/実証.md)）。

## 三層モデル

```
書き手層（永続）   writer-persona ──→ 魂の物語・声・禁じ手・美意識（内省で聞く＝人間の実経験に照合）
                  voice-ledger ──→ 聞こえた声を貯め、読み返す（発想・停滞脱出・persona 更新）
構想層（作品ごと） premise → plot-design ──→ 必須構想（設計書。約束＋声に照らして改訂）
                  下準備（任意）narration-design / character-forge / character-in-action / character-bond / worldbuild / world-iceberg / research-verify
実行層            fast-draft ──→ ラフ散文（内省で逸脱を検出し計画を更新・発露と抑制の美学で届ける）
                  書く質 prose / scene-writer ／ 改稿 revise-for-reader / entertainment / whole-work-review ／ 長期 series-bible ／ 届ける package / theme-song
```

三層を貫く操作が**内省**（声を聞く）。内省は「**照合**」——ground に照らした観測。

## 内省の四つの ground（照合対象）

| 問いの層 | ground（照合対象） |
|---|---|
| A 書き手設定（writer-persona） | **人間の実経験**——この人間が書いてきた作品・実際に抱える問い・禁じ手。AI は人間に問い、答えを保持する。**AI が自分の「傷」を捏造しない** |
| B 発想（premise） | **persona＋ため庫**——声・美意識（HOW）は照合、題材（WHAT）は揺らぎを許す（引き寄せすぎると毎回同じになる） |
| C 設計（plot-design） | **premise（約束・反応軸・核心の問い）＋ persona（声・美意識・禁じ手）**——設計を約束と声に照らして改訂する |
| D 草稿ループ（fast-draft） | **計画（シーン表）**——生成した文と計画を照合し、逸脱の有無を判定 |

**照合対象（ground）が無い内省は観測にならない。** 各問いに ground を明記し、ground の無い問いは「内省」と呼ばない（[references/ja/内省問い.md](references/ja/内省問い.md)）。

## 発露と抑制の美学（魂のマスターレバー）

- 魂を動かすのは構想の個別性ではなく、**書く仕方＝発露と抑制**。
- fast-draft の**出力仕様**として組み込む: 感情を情景・行為で発露させ、説明しない・名指ししない・結末に教訓や総括を置かない・読者への余白を残す（[references/ja/発露と抑制の美学.md](references/ja/発露と抑制の美学.md)）。
- ただし抑制は「何を抑制するか」の**源**を必要とする。源は SOURCE（照合＝人間の実経験）。抑制（MANNER）は必要条件であって十分条件ではない。

## 誰が書くか（フレーミング・最初に確定）

**人間が作者、AI は草案装置、persona は作者の鏡。**

- persona の魂・声は**人間（ユーザー）のもの**。AI はそれを対話で引き出し・保持・反映する鏡であって、作者ではない。
- これにより A/B 問いの内省が「捏造」でなく「照合」になる（構想レビュー Ⅰ-1）。

## Directory Conventions

- `skills/{name}/SKILL.md` — 各スキルの正典源（20）。すべて独立して呼び出せる。`SKILL-ja.md` / `SKILL-zh.md` は各言語ミラー
- `.claude/skills/` — プロジェクト内検出用の symlink（`./install.sh --local` で生成）
- `~/.claude/skills/` — グローバル導入先（`./install.sh`、どこからでも呼べる）
- `.claude-plugin/` — プラグイン配布定義
- `references/` — スキルが引用する運用原理（en 正典：内省・発露と抑制・反応軸・フックのエンジン・ため庫；`references/ja/`・`references/zh/` ミラー）
- `docs/` — 汎用的に何でも置ける場所（実証・根拠・設計メモなど。ルール本体とは分離）
- `locales/` — i18n 表示文字列（en 正典；`ja` / `zh` ミラー）
- `examples/<work>/` — 作品ごとの成果物（premise.md / design.md / draft_*.md）
- 書き手の永続状態は、ユーザーがワークスペース内に作る**専用フォルダ（ローカルフォルダでも可・git リポジトリ推奨）**に置く: `persona.md`（私はこう書く＝現在形）と `voice-ledger.md`（私はこう書いてきた＝過去形）。置き場所は `SOUL_VOICE_HOME` で指す（未設定なら `~/.soul-voice-teller/` にフォールバック）。writer-persona の第一手は、この専用フォルダ作成をユーザーに促すこと。**ユーザーごとの状態であり、soul-voice-teller リポジトリには含めない（固定しない）**——色々な人が使うため。スキルが参照する persona の既定は存在せず、常に `SOUL_VOICE_HOME` のものを読む

## 執筆内在の判断 vs 外在の評価（区別）

| 種 | 例 | 属する層 |
|---|---|---|
| **執筆内在の判断**（書くことの一部） | 内省・逸脱判定（深める/壊す）・フロー検出 | **執筆スキル**（fast-draft / plot-design が持つ） |
| **外在の評価**（書かれたものへの判定） | 評議会・昇華（否定/保存/高次化）・改稿 | **評価レイヤー**（外部） |

「評価機構を内蔵しない」は「**外在の評価機構を内蔵しない**」を意味する。逸脱の**気づき**は内省の一部として fast-draft と plot-design に認める。委ねるべきは逸脱の**精査・昇華**であって、逸脱の気づきではない。

## 言語（i18n）

**en / ja / zh** の3言語を3層構造で、**en 正典**として実装。

1. **ロケールJSON** — `locales/{en,ja,zh}.json`
2. **言語別プロンプト** — `skills/{name}/SKILL-{lang}.md` ＋ `references/{lang}/*.md`
3. **ミラーツリー** — `README-{lang}.md` / `CLAUDE-{lang}.md`

言語解決: `lang` 引数 ＞ 環境変数 `SOUL_VOICE_TELLER_LANG` ＞ **en**（既定）。未対応言語は警告して `en` にフォールバック。

**源概念（内省 / 余白 / 間）**は日本語で、en（introspection / negative space / restraint）・zh（内省 / 留白 / 含蓄）へ**逐語訳でなく再導出**する。散文系スキル（`prose` / `scene-writer` / `revise-for-reader`）は各言語の執筆伝統で再実装する。

### i18n baseline（固定方針）

en/ja/zh 多言語対応が以後の全変更の既定。新規・変更のスキル本文・references・テンプレートは3層機構（`SKILL-{lang}.md` / ロケールJSON / ミラーツリー）で解決し、ユーザー向けテキストは解決された言語で出力する。

## 作らないもの（明示的除外）

- 評価ループ・昇華——外部レイヤーが担う。内蔵しない。
- 校正・文法チェック、ジャンル別テンプレ、Python エンジン・サブエージェント（本レイヤーはスキル型）。

## 実証

魂のレバーが何か、各実験（E1/E4・E5・E2・E2b）の結果と残る本丸（SOURCE）は [docs/実証.md](docs/実証.md) に集約した。
