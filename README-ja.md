**Language:** [English](README.md) | 日本語 | [中文](README-zh.md)

# soul-voice-teller

<p align="center">
  <img src="assets/repo-hero.png" width="100%" alt="soul-voice-teller">
</p>

**書くことは、魂を運ぶこと。** —— 小説執筆スキルのレイヤー。

書き手（人間）の魂・声・嗜好を映す `writer-persona`、発想の `premise`、設計の `plot-design`、草稿の `fast-draft`、声を貯める `voice-ledger` の5スキルに、任意下準備7種と文体・改稿・台帳6種・届ける1種を加えた19スキルで、「構想 → 草稿 → 改稿 → 届ける」を執筆スキル単体で成立させる。

## 核心命題

- **書くことは、魂を運ぶこと。**
- **人間が作者、AI は草案装置、persona は作者の鏡。**
- **内省は「照合」——ground（照合対象）に照らした観測。**
- **発露と抑制の美学が魂のマスターレバー。**

## 三層モデル

```
書き手層（永続）   writer-persona ──→ 魂の物語・声・禁じ手・美意識（人間の実経験に照合）
                  voice-ledger ──→ 聞こえた声を貯め、読み返す
構想層（作品ごと） premise → plot-design ──→ 必須構想（設計書）
実行層            fast-draft ──→ ラフ散文（内省で逸脱を検出・発露と抑制の美学で届ける）
```

## ドキュメント

- [使い方](docs/usage-ja.md) — 導入方法とスキルの呼び出し順序、出力言語の切り替え
- [19スキル](docs/skills-ja.md) — 各スキルが何をするか（入力 → 出力）のリファレンス
- [実証](docs/実証.md) — 設計を支える実証の記録

## 書き手の永続状態

- `${SOUL_VOICE_HOME}/persona.md` —— 「私はこう書く」（現在形・肖像）。writer-persona が作る
- `${SOUL_VOICE_HOME}/voice-ledger.md` —— 「私はこう書いてきた」（過去形・日記）。voice-ledger が積む
- 置き場所は、ユーザーがワークスペース内に作る**専用フォルダ（ローカルフォルダでも可・git リポジトリ推奨）**を環境変数 `SOUL_VOICE_HOME` で指す（未設定なら `~/.soul-voice-teller/`）。writer-persona の第一手が、このフォルダ作成を促す

> **persona / voice-ledger はユーザーごとの状態で、リポジトリには含めない（固定しない）**——色々な人が使うため。スキルが参照する persona の既定は存在しない。`examples/sample/` の persona はデモ用サンプルであり、スキルの既定ではない。

> **注記——ため庫の増大とコンテキスト。** `voice-ledger.md` はセッションのコンテキストに自動で読み込まれない——必要時に読むだけなので、コンテキストを圧迫するのは**読む瞬間だけ**。読み方と、増大しても全文読みを軽く保つ方法は [usage「voice-ledger の増大とコンテキスト」](docs/usage-ja.md) 参照。

## リポジトリ構成

- `skills/{name}/SKILL.md` — 19スキル（en 正典）＋各言語の `SKILL-ja.md` / `SKILL-zh.md`
- `references/` — 運用原理（内省・発露と抑制・ため庫、en 正典；`references/ja/`・`references/zh/` ミラー）
- `docs/` — 使い方とスキル一覧（[usage-ja.md](docs/usage-ja.md) / [skills-ja.md](docs/skills-ja.md)）＋汎用的に何でも置ける場所（実証・根拠・設計メモなど）
- `locales/` — 表示文字列（en 正典、`ja` / `zh` ミラー）
- `examples/<work>/` — 作品ごとの成果物
- `install.sh` — symlink 導入（グローバル／ローカル／アンインストール）

## 言語（i18n）

**en / ja / zh** の3言語を3層構造で実装:

1. **ロケールJSON** — `locales/{en,ja,zh}.json`（表示文字列）
2. **言語別プロンプト** — `skills/{name}/SKILL-{lang}.md` ＋ `references/{lang}/*.md`
3. **ミラーツリー** — `README-{lang}.md` / `CLAUDE-{lang}.md`

言語解決: `lang` 引数 ＞ 環境変数 `SOUL_VOICE_TELLER_LANG` ＞ **en**（既定）。未対応言語は警告して `en` にフォールバック。日本語（または中国語）で既定出力するには、[使い方](docs/usage-ja.md) を参照。

**源概念（内省 / 余白 / 間）**は日本語で、en（introspection / negative space / restraint）・zh（内省 / 留白 / 含蓄）へ**逐語訳でなく再導出**する。散文系スキル（`prose` / `scene-writer` / `revise-for-reader`）は各言語の執筆伝統で再実装する。

## ライセンス

MIT（[LICENSE](LICENSE)）
