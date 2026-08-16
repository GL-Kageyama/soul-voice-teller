# 19スキル

各スキルが何をするか（入力 → 出力）のリファレンス。呼び方は [使い方](usage-ja.md) を参照。

## 本線

| スキル | 役割 | 入力 → 出力 |
|---|---|---|
| `writer-persona` | 対話で書き手設定を引き出す（A問い・ground=人間の実経験） | 対話 → `${SOUL_VOICE_HOME}/persona.md`（魂の物語/美意識/声・筆致/禁じ手/題材の嗜好） |
| `premise` | 発想（B問い・ground=persona＋ため庫） | 種＋persona＋ため庫 → `<work>/premise.md`（ログライン/核心の問い/テーマ/ジャンルの約束/文体の方向/読者像と約束） |
| `plot-design` | 設計書（fast-draft の入力仕様） | premise＋persona → `<work>/design.md`（必須構想欄＋任意下準備欄） |
| `fast-draft` | 草稿（発露と抑制の美学＋内省ループ） | design＋persona＋ため庫 → `<work>/draft_*.md`＋計画更新＋ため庫への声 |
| `voice-ledger` | 声を貯め、読み返す | 声（発想/草稿/筆の乗り/禁じ手/評価の響き）→ `${SOUL_VOICE_HOME}/voice-ledger.md` |

## 任意下準備

plot-design から任意に呼ぶ。空白でも執筆可。

| スキル | 役割 | 入力 → 出力 |
|---|---|---|
| `narration-design` | 語りの詳細設計（視点の型・信頼性・距離・時制・入れ子・話法） | design → design.md の「語り」欄詳細化 |
| `character-forge` | 人物設計（欲求・傷・声・変化弧・内面葛藤） | design＋premise＋persona → design.md の「人物」欄詳細化 |
| `character-in-action` | 人物設定を場面で機能させる（段階的開示・設定の機能化） | design → シーン表への連動点追記 |
| `character-bond` | 二人の間の関係を描く（関係の軸・反転／鏡像・転機・双方向・身体化） | design＋draft → 二人の関係の詳細化 |
| `worldbuild` | 世界設計（舞台・ルール・内部一貫性・設定⇔物語の接続） | design＋premise＋persona → design.md の「世界」欄詳細化 |
| `world-iceberg` | 未描の世界の資料化の加減（触れる確率順） | design → 資料化リスト追記 |
| `research-verify` | 史実・時代考証・専門知識の照合（誤りを混ぜない） | design/draft → 誤りリスト＋訂正 |

## 書く質・改稿・長期

| スキル | 役割 | 入力 → 出力 |
|---|---|---|
| `prose` | 文体で研ぐ（リズム・感覚・言い換え不能な声） | 文/場面＋persona → 書き直した文 |
| `scene-writer` | 1場面を深く書く（空白の設計・見せて語る・場の切れ目） | design＋persona → draft_<n>_<場面>.md |
| `series-bible` | 作品聖典（設定・伏線・連載を一元管理する台帳） | 作品成果物 → series-bible.md |
| `revise-for-reader` | 読者体験で改稿（没入・ページターナー・約束・再読） | draft＋design → 改稿 draft.md |
| `entertainment` | 抑制を壊さずにエンタメの快楽を足す（フック・ページターナー・ツイスト・カタルシス・テンポ・共感） | draft＋design → 改稿 draft.md |
| `whole-work-review` | 作品を「全体」として見直す——一冊として閉じているか（構造の一貫性・伏線回収・密度配分・重複・世界観用語への寄りかかり・抑制のバランス） | draft＋series-bible → 改稿 draft.md |

## 届ける

| スキル | 役割 | 入力 → 出力 |
|---|---|---|
| `package` | 完成した作品を読者へ包む（タイトル＋サブタイトル・キャッチコピー・あらすじ・画像プロンプト・タグ）、読者の第一印象に照合 | draft＋premise＋series-bible＋persona → `<work>/package.md` |
