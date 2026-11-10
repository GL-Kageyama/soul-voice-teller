# 評価

novel-council-layer の `story-council` による評価の記録。ループごとに1ディレクトリ。
評価は散文10話を結合した本文に対して行う。

- `loopNN/input.txt` — 評価に渡した本文（10話の結合）
- `loopNN/report.json` — Story Report（13次元）
- `loopNN/report.md` — 読みやすい要約
- `loopNN/{evaluator}.json` — 各評価者の生JSON
- `loopNN/note.md` — その回の弱点と、次の改稿で触った箇所
- [スコア.md](スコア.md) — ループごとの平均と次元別の推移

評価条件は固定する：full（13体）、`lang=ja`、`domain=pure-literature`、`content_type=text`。
