# 使い方

レイヤーの導入方法と、スキルを順に呼ぶ手順。

## 導入

```bash
# 導入（グローバル / プロジェクト内）
./install.sh            # ~/.claude/skills/（どこからでも呼べる）
./install.sh --local    # .claude/skills/（このリポジトリのみ）
```

## 呼び出しの順序

導入後、Claude Code でスキルを順に呼ぶ:

```
/writer-persona        # まず書き手設定を引き出す（5項目の persona を作る）
/premise               # 種を渡して発想
/plot-design           # 設計書を作る（必須構想＋任意下準備）
/fast-draft            # 草稿を書く（内省ループ＋発露と抑制の美学）
/voice-ledger          # 声をためる・読み返す

# 下準備（任意。plot-design の前後で）
/narration-design      # 語りの詳細設計
/character-forge       # 人物設計
/character-in-action   # 人物の場面での活かし方
/character-bond        # 二人の間の関係を描く
/worldbuild            # 世界設計
/world-iceberg         # 未描の世界の資料化
/research-verify       # 史実・時代考証の照合

# 書く質・改稿・長期
/prose                 # 文体で研ぐ
/scene-writer          # 1場面を深く書く
/series-bible          # 作品聖典・台帳
/revise-for-reader     # 読者体験で改稿
/entertainment         # 6つの反応軸で検品し、弱い軸を補う
/whole-work-review     # 一冊として閉じているか全体を見直す

# 届ける
/package               # 完成した作品を読者へ包む
```

## 出力言語の切り替え

各スキルは `lang` 引数（例: `/premise lang=ja`）か環境変数 `SOUL_VOICE_TELLER_LANG` で出力言語を切り替える（既定 `en`）。日本語（または中国語）で既定出力するには、シェルプロファイルで環境変数を設定する:

```bash
# ~/.zshenv
export SOUL_VOICE_TELLER_LANG=ja   # または zh
```

解決順序と3層構造の詳細は [README](../README-ja.md) の「言語（i18n）」節を参照。
