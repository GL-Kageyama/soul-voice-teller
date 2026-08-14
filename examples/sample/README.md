# examples/sample/ —— デモ用サンプル（一気通しの実演）

パイプライン（writer-persona → premise → plot-design → fast-draft）の**動きを見せる**ためのサンプル一式。

> **重要**: ここにある persona は**架空のデモ用サンプル**であり、実在の書き手の実経験ではない。
> 実際の persona は `/writer-persona` の対話でユーザー自身から引き出し、`~/.soul-voice-teller/persona.md` に置く。
> **persona / voice-ledger はユーザーごとの状態で、リポジトリには含めない（固定しない）**——色々な人が使うため。
> スキルは `~/.soul-voice-teller/` を読むだけで、この sample を既定として参照しない。

## 中身

```
sample/
├── sample-persona.md           # サンプル persona（5項目。デモ用の架空設定）
└── lighthouse/                 # 種「灯台守は海を怖がるのに、海からしか来ない唯一の客を待つ」
    ├── premise.md              # /premise の出力（ログライン・核心の問い・テーマ・読者像と約束）
    ├── design.md               # /plot-design の出力（必須構想＋任意下準備）
    ├── draft.md                # /fast-draft の出力（抑制の美学で書いた草稿）
    └── voice-ledger-sample.md  # 内省で聞こえた声のサンプル（/voice-ledger が貯める1件の書式）
```

## 読みどころ

- **premise** がサンプル persona の魂の物語（「待つこと」）に照らしてテーマを選んでいる（B問い＝照合）。
- **design** のシーン表が fast-draft の入力仕様になっている（必須構想＋任意下準備、未定は `?`）。
- **draft** が「感情を説明しない・名指ししない・総括しない・余白を残す」（抑制の美学）を体現している。
- **voice-ledger-sample** が内省ループ（C-1 フロー検出）で聞こえた声を原文のまま記録している。
