# soul-voice-teller

**魂を運ぶことが目的、anti-generic は手段。** —— 小説執筆スキルのレイヤー。

書き手（人間）の魂・声・嗜好を映す `writer-persona`、発想の `premise`、設計の `plot-design`、草稿の `fast-draft`、声を貯める `voice-ledger` の第1弾5スキルに、任意下準備6種（第2弾）と文体・改稿・台帳4種（第3弾）を加えた15スキルで、「構想 → 草稿 → 改稿」を執筆スキル単体で成立させる。

> **役割分担**: このレイヤーは**執筆のみ**。作品の評価（見抜く）は外部の評価レイヤー（[novel-council-layer](../novel-council-layer/) / [wisdom-council-layer](../wisdom-council-layer/) / [elevate-draft-engine](../elevate-draft-engine/)）が担う。

## 核心命題

- **魂を運ぶことが目的、anti-generic は手段**。非平均性（個別性）は目的でなく手段。
- **人間が作者、AI は草案装置、persona は人間の嗜好を映す鏡**。
- **内省は「照合」であって「捏造」ではない**。照合対象（ground）が無い内省は観測にならない。
- **抑制の美学が魂のマスターレバー**（E5 で実証）: 感情を説明しない・名指ししない・総括しない・余白を残す。

## 三層モデル

```
書き手層（永続）   writer-persona ──→ 魂の物語・声・禁じ手・美意識（人間の実経験に照合）
                  voice-ledger ──→ 聞こえた声を貯め、読み返す
構想層（作品ごと） premise → plot-design ──→ 必須構想（設計書）
実行層            fast-draft ──→ ラフ散文（内省で逸脱を検出・抑制の美学で届ける）
外部（評価レイヤー）評価・昇華 ──→ 再草稿の材料
```

## 15スキル（第1弾〜第3弾）

| スキル | 役割 | 入力 → 出力 |
|---|---|---|
| `writer-persona` | 対話で書き手設定を引き出す（A問い・ground=人間の実経験） | 対話 → `~/.soul-voice-teller/persona.md`（魂の物語/美意識/声・筆致/禁じ手/題材の嗜好） |
| `premise` | 発想（B問い・ground=persona＋ため庫） | 種＋persona＋ため庫 → `<work>/premise.md`（ログライン/核心の問い/テーマ/ジャンルの約束/文体の方向/読者像と約束） |
| `plot-design` | 設計書（fast-draft の入力仕様） | premise＋persona → `<work>/design.md`（必須構想欄＋任意下準備欄） |
| `fast-draft` | 草稿（抑制の美学＋内省ループ） | design＋persona＋ため庫 → `<work>/draft_*.md`＋計画更新＋ため庫への声 |
| `voice-ledger` | 声を貯め、読み返す | 声（発想/草稿/筆の乗り/禁じ手/評価の響き）→ `~/.soul-voice-teller/voice-ledger.md` |

**第2弾（任意下準備）**——plot-design から任意に呼ぶ。空白でも執筆可

| スキル | 役割 | 入力 → 出力 |
|---|---|---|
| `narration-design` | 語りの詳細設計（視点の型・信頼性・距離・時制・入れ子・話法） | design → design.md の「語り」欄詳細化 |
| `character-forge` | 人物設計（欲求・傷・声・変化弧・内面葛藤） | design＋premise＋persona → design.md の「人物」欄詳細化 |
| `character-in-action` | 人物設定を場面で機能させる（段階的開示・設定の機能化） | design → シーン表への連動点追記 |
| `worldbuild` | 世界設計（舞台・ルール・内部一貫性・設定⇔物語の接続） | design＋premise＋persona → design.md の「世界」欄詳細化 |
| `world-iceberg` | 未描の世界の資料化の加減（触れる確率順） | design → 資料化リスト追記 |
| `research-verify` | 史実・時代考証・専門知識の照合（誤りを混ぜない） | design/draft → 誤りリスト＋訂正 |

**第3弾（書く質・改稿・長期）**

| スキル | 役割 | 入力 → 出力 |
|---|---|---|
| `prose` | 文体で研ぐ（リズム・感覚・言い換え不能な声） | 文/場面＋persona → 書き直した文 |
| `scene-writer` | 1場面を深く書く（空白の設計・見せて語る・場の切れ目） | design＋persona → draft_<n>_<場面>.md |
| `series-bible` | 作品聖典（設定・伏線・連載を一元管理する台帳） | 作品成果物 → series-bible.md |
| `revise-for-reader` | 読者体験で改稿（没入・ページターナー・約束・再読） | draft＋design → 改稿 draft.md |

## 使い方

```bash
# 導入（グローバル / プロジェクト内）
./install.sh            # ~/.claude/skills/（どこからでも呼べる）
./install.sh --local    # .claude/skills/（このリポジトリのみ）
```

導入後、Claude Code でスキルを順に呼ぶ:

```
/writer-persona        # まず書き手設定を引き出す（5項目の persona を作る）
/premise               # 種を渡して発想
/plot-design           # 設計書を作る（必須構想＋任意下準備）
/fast-draft            # 草稿を書く（内省ループ＋抑制の美学）
/voice-ledger          # 声をためる・読み返す

# 下準備（第2弾・任意。plot-design の前後で）
/narration-design      # 語りの詳細設計
/character-forge       # 人物設計
/character-in-action   # 人物の場面での活かし方
/worldbuild            # 世界設計
/world-iceberg         # 未描の世界の資料化
/research-verify       # 史実・時代考証の照合

# 書く質・改稿・長期（第3弾）
/prose                 # 文体で研ぐ
/scene-writer          # 1場面を深く書く
/series-bible          # 作品聖典・台帳
/revise-for-reader     # 読者体験で改稿
```

## 書き手の永続状態

- `~/.soul-voice-teller/persona.md` —— 「私はこう書く」（現在形・肖像）。writer-persona が作る
- `~/.soul-voice-teller/voice-ledger.md` —— 「私はこう書いてきた」（過去形・日記）。voice-ledger が積む
- 場所は環境変数 `SOUL_VOICE_HOME` で変更できる（既定 `~/.soul-voice-teller`）

> **persona / voice-ledger はユーザーごとの状態で、リポジトリには含めない（固定しない）**——色々な人が使うため。スキルが参照する persona の既定は存在しない。`examples/sample/` の persona はデモ用サンプルであり、スキルの既定ではない。

## リポジトリ構成

- `skills/{name}/SKILL.md` — 15スキルの正本（ja 本訳）
- `references/` — 運用原理（内省問い・抑制の美学・ため庫）
- `locales/` — i18n 骨組み（ja 実体、en/zh スタブ）
- `examples/<work>/` — 作品ごとの成果物
- `install.sh` — symlink 導入（グローバル／ローカル／アンインストール）

## i18n

ja 先行（本訳）。en/zh は3層骨組み（locales・references ミラー）を用意済みで、本訳と「内省の作法の言語別再導出」は次工程。

## ライセンス

MIT（[LICENSE](LICENSE)）
