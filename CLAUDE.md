**Language:** 日本語（本訳） | English / 中文 は追いつき待ち（i18n 骨組みのみ用意）

# soul-voice-teller

## Project Identity（プロジェクトの正体）

これは**小説執筆スキル**のレイヤー。書き手（人間）の魂・声・嗜好を映す `writer-persona`、発想の `premise`、設計の `plot-design`、草稿の `fast-draft`、声を貯める `voice-ledger` の5スキル（第1弾）に、任意下準備の `narration-design` / `character-forge` / `character-in-action` / `worldbuild` / `world-iceberg` / `research-verify`（第2弾）と、書く質・改稿・長期の `prose` / `scene-writer` / `series-bible` / `revise-for-reader`（第3弾）を加えた15スキルで構成する。

> **役割分担**: このレイヤーは**執筆のみ**。作品の**評価**（見抜く）は外部の評価レイヤー（novel-council / wisdom-council / elevate-draft-engine）が担う。このリポジトリは「見抜く」のでなく「書く」。ただし草稿の中の**逸脱判定**は「執筆内在の判断」（書くことの一部）として内省に含める。

## 核心命題（一番上に置く）

**魂を運ぶことが目的、anti-generic（非平均性）は手段。**

- 「誰のものでもない平均的な文」を避けること（個別性）は**目的ではない**。読者の心を動かし、記憶に残るもの（魂）を運ぶことが目的で、個別性はそのための**手段**の一つ。
- この反転は実証済み（[docs/実証.md](docs/実証.md)）。

## 三層モデル

```
書き手層（永続）   writer-persona ──→ 魂の物語・声・禁じ手・美意識（内省で聞く＝人間の実経験に照合）
                  voice-ledger ──→ 聞こえた声を貯め、読み返す（発想・停滞脱出・persona 更新）
構想層（作品ごと） premise → plot-design ──→ 必須構想（設計書）
                  下準備（第2弾・任意）narration-design / character-forge / character-in-action / worldbuild / world-iceberg / research-verify
実行層            fast-draft ──→ ラフ散文（内省で逸脱を検出し計画を更新・抑制の美学で届ける）
                  書く質（第3弾）prose / scene-writer ／ 改稿 revise-for-reader ／ 長期 series-bible
外部（評価レイヤー）評価・昇華 ──→ 再草稿の材料
```

三層を貫く操作が**内省**（声を聞く）。内省は「判定」でなく「**照合**」。

## 内省の三つの ground（照合対象）

| 問いの層 | ground（照合対象） |
|---|---|
| A 書き手設定（writer-persona） | **人間の実経験**——この人間が書いてきた作品・実際に抱える問い・禁じ手。AI は人間に問い、答えを保持する。**AI が自分の「傷」を捏造しない** |
| B 発想（premise） | **persona＋ため庫**——「この人間ならどう選ぶか」を照合 |
| C 草稿ループ（fast-draft） | **計画（シーン表）**——生成した文と計画を照合し、逸脱の有無を判定 |

**照合対象の無い内省は「捏造」であって「観測」ではない。** 各問いに ground を明記し、ground の無い問いは「内省」と呼ばない（[references/内省問い.md](references/内省問い.md)）。

## 抑制の美学（魂のマスターレバー）

- 魂を動かすのは構想の個別性ではなく、**書く仕方＝抑制**。
- fast-draft の**出力仕様**として組み込む: 感情を説明しない・名指ししない・結末に教訓や総括を置かない・読者への余白を残す（[references/抑制の美学.md](references/抑制の美学.md)）。
- ただし抑制は「何を抑制するか」の**源**を必要とする。源は SOURCE（照合＝人間の実経験）。抑制（MANNER）は必要条件であって十分条件ではない。

## 誰が書くか（フレーミング・最初に確定）

**人間が作者、AI は草案装置、persona は人間の嗜好を映す鏡。**

- persona の魂・声は**人間（ユーザー）のもの**。AI はそれを対話で引き出し・保持・反映する鏡であって、作者ではない。
- これにより A/B 問いの内省が「捏造」でなく「照合」になる（構想レビュー Ⅰ-1）。

## Directory Conventions

- `skills/{name}/SKILL.md` — 各スキルの正本（15）。すべて独立して呼び出せる
- `.claude/skills/` — プロジェクト内検出用の symlink（`./install.sh --local` で生成）
- `~/.claude/skills/` — グローバル導入先（`./install.sh`、どこからでも呼べる）
- `.claude-plugin/` — プラグイン配布定義
- `references/` — スキルが引用する運用原理（ja 本訳。内省問い・抑制の美学・ため庫）
- `docs/` — 汎用的に何でも置ける場所（実証・根拠・設計メモなど。ルール本体とは分離）
- `locales/` — i18n 骨組み（ja 本実装、en/zh はスタブ）
- `examples/<work>/` — 作品ごとの成果物（premise.md / design.md / draft_*.md）
- 書き手の永続状態は、ユーザーがワークスペース内に作る**専用フォルダ（private git リポジトリ）**に置く: `persona.md`（私はこう書く＝現在形）と `voice-ledger.md`（私はこう書いてきた＝過去形）。置き場所は `SOUL_VOICE_HOME` で指す（未設定なら `~/.soul-voice-teller/` にフォールバック）。writer-persona の第一手は、この専用フォルダ作成をユーザーに促すこと。**ユーザーごとの状態であり、soul-voice-teller リポジトリには含めない（固定しない）**——色々な人が使うため。スキルが参照する persona の既定は存在せず、常に `SOUL_VOICE_HOME` のものを読む

## 執筆内在の判断 vs 外在の評価（区別）

| 種 | 例 | 属する層 |
|---|---|---|
| **執筆内在の判断**（書くことの一部） | 内省・逸脱判定（深める/壊す）・フロー検出 | **執筆スキル**（fast-draft が持つ） |
| **外在の評価**（書かれたものへの判定） | 評議会・昇華（否定/保存/高次化）・改稿 | **評価レイヤー**（外部） |

「評価機構を内蔵しない」は「**外在の評価機構を内蔵しない**」を意味する。逸脱の**気づき**は内省の一部として fast-draft に認める。委ねるべきは逸脱の**精査・昇華**であって、逸脱の気づきではない。

## i18n（ja 先行＋3層骨組み）

- **ja が本訳**。SKILL.md 本文・問い・references は日本語で書く。
- **3層の骨組みは用意済み**: `locales/{en,ja,zh}.json`（ja 実体、en/zh スタブ）、`references/en/`・`references/zh/`（空箱）。
- en/zh の本訳と、**内省の作法の言語別再導出**（ja=内省/余白/間、en=restraint/negative capability、zh=留白/含蓄）は**次工程**。散文系スキル（`prose` / `scene-writer` / `revise-for-reader`）は言語別に効くため、en/zh 化は逐語訳でなく各言語の執筆伝統での再実装になる。

## 作らないもの（明示的除外）

- 評価ループ・昇華——外部レイヤーが担う。内蔵しない。
- 校正・文法チェック、ジャンル別テンプレ、Python エンジン・サブエージェント（本レイヤーはスキル型）。

## 実証

魂のレバーが何か、各実験（E1/E4・E5・E2・E2b）の結果と残る本丸（SOURCE）は [docs/実証.md](docs/実証.md) に集約した。
