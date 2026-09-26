#!/usr/bin/env python3
"""一案を検める——差し替え案が、この巻の規則に叶っているかを、機械で見える分だけ検める。

見えるのは、次の五つである。

1. **逐語**——その案が、第四巻の本文のどこかに、既に一字一句そのまま在るか。
2. **巻をまたいだ反復**——その案が、他の話にも現れるか（十二字以上）。
3. **禁じられた語**——色語（青・緑・黄・茶・灰・銀・紫・桃・橙）と、匂いの語（匂・におい・臭・香・嗅）。
4. **「答えない」**——置き換えた後も、この形を使っていないか。
5. **同じ話の中の近さ**——その話の既存の行と、語の重なりが大きすぎないか。

見えないもの——**その案が、その話の本文に既に真であるか。** これは人が読む。

使い方:
    python3 一案を検める.py <話番号> "<案>" [<案> ...]
"""

import collections
import pathlib
import re
import sys

DRAFTS = pathlib.Path(__file__).resolve().parents[2] / "habits-04" / "草稿"

COLOR = re.compile(r"[青緑黄茶灰銀紫桃橙]")
SMELL = re.compile(r"匂|におい|臭|香|嗅")
FORBIDDEN_SHAPE = re.compile(r"答えない")
MIN_LEN = 12


def load(ep: str) -> list[str]:
    fs = list(DRAFTS.glob(f"draft_04-{ep}_*.md"))
    if not fs:
        raise SystemExit(f"本文が見つからない: 04-{ep}")
    return [l.strip() for l in fs[0].read_text(encoding="utf-8").splitlines() if l.strip()]


def index_all() -> dict[str, set[str]]:
    idx = collections.defaultdict(set)
    for f in sorted(DRAFTS.glob("draft_04-*.md")):
        ep = f.name.split("_")[1][-2:]
        for l in f.read_text(encoding="utf-8").splitlines():
            s = l.strip()
            if s:
                idx[s].add(ep)
    return idx


def bigrams(s: str) -> set[str]:
    return {s[i:i + 2] for i in range(len(s) - 1)}


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    ep = sys.argv[1]
    mine = load(ep)
    idx = index_all()
    mine_set = set(mine)

    for plan in sys.argv[2:]:
        print(f"===== 04-{ep}  「{plan}」")
        bad = []

        if plan in mine_set:
            bad.append("⛔ この話の本文に、既に一字一句そのまま在る")
        others = idx.get(plan, set()) - {ep}
        if others:
            bad.append(f"⛔ 他の話にも現れる: {''.join(sorted(others))}")
        if len(plan) >= MIN_LEN:
            pass
        if COLOR.search(plan):
            bad.append(f"⛔ 色語を含む: {COLOR.search(plan).group(0)}")
        if SMELL.search(plan):
            bad.append(f"⛔ 匂いの語を含む: {SMELL.search(plan).group(0)}")
        if FORBIDDEN_SHAPE.search(plan):
            bad.append("⛔ 「答えない」の形を使っている")

        # 同じ話の中の、いちばん近い行
        pb = bigrams(plan)
        near = []
        for l in mine:
            if l == plan:
                continue
            lb = bigrams(l)
            if not lb or not pb:
                continue
            j = len(pb & lb) / len(pb | lb)
            if j >= 0.5:
                near.append((j, l))
        near.sort(reverse=True)
        if near:
            bad.append("⚠ この話の既存行と近い: " + " / ".join(f"「{l}」（{j:.2f}）" for j, l in near[:3]))

        if bad:
            for b in bad:
                print("   " + b)
        else:
            print("   ✅ 機械で見える範囲では、問題なし")
        print(f"   （長さ {len(plan)} 字。この話の既存行に完全一致は {'あり' if plan in mine_set else 'なし'}）")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
