# examples/

作品ごとの成果物を置く。各 `<work-slug>/` に、パイプラインを一気通しした結果が並ぶ。

```
examples/
└── <work-slug>/          # 作品ごと（例: lighthouse）
    ├── premise.md        # /premise の出力（ログライン・核心の問い・テーマ・読者像と約束）
    ├── design.md         # /plot-design の出力（必須構想＋任意下準備）
    ├── draft_1_<場面>.md  # /fast-draft の場面単位の草稿
    └── draft.md          # 全場面を連結した草稿
```

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
