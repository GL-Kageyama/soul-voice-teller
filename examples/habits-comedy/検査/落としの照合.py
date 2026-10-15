#!/usr/bin/env python3
"""会話劇 Upgrade の前後で、原本の文がどう動いたかを見る照合器。

これは検査であって、評価ではない。出すのは数と、文そのものである。

    python3 落としの照合.py                 # 全63話の集計
    python3 落としの照合.py --list          # ⓑ（新たに落ちた文）を前後つきで印字
    python3 落としの照合.py --talk 03-04    # 一話だけ

## なぜ要るか

`検算.py` の⑤は「原本の文が〝逐語で〟この稿に在るか」を数える。
ゆえに一句でも書き換えれば増える——**数は門ではない**（依頼文 §9-1）。
著者が「よかった」と認めた `01-01`(141/347)・`01-02`(195/414) が最大である。

そこで、**数をやめて、文そのものを見る**。
原本の一文ごとに、この稿に「近い文」がどれだけ在るかを測り、三つに割る:

    ⓐ ほぼ同じ   ratio >= 0.90  —— 手を入れていない
    ⓑ 書き換え   0.60 <= r < 0.90 —— 変換の手が入った（**これは美点**）
    ⓒ 引き当てなし  r < 0.60      —— **ここだけが人の目に掛かる**

## 三つの時点

    原本      = ../habits-NN/草稿/draft_NN-EE_*.md
    前        = Upgrade 前の走行の着地（git 08f21e6 の、このリポジトリの草稿）
    後        = いまの作業木

差の意味:
    **前にも無く、後にも無い** —— 前の走行で既に落ちていた文（＝約束した36文の側）
    **前には在り、後に無い**   —— ⛔ Upgrade で新たに落ちた文。**これを見る**
    **前には無く、後に在る**   —— Upgrade で戻った文（良い知らせ）

⚠ 多重度は見ない（集合で受ける）。`検算.py` の⑤と同じ数え方に揃えてある。
"""

import argparse
import difflib
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent          # soul-voice-teller
WORK = HERE.parent                          # examples/habits-comedy
HEAD = "08f21e6"                            # Upgrade 前の走行の着地

VOL = {"01": "habits-01", "02": "habits-02", "03": "habits-03", "04": "habits-04"}
BANDS = ((0.90, "ⓐほぼ同じ"), (0.60, "ⓑ書き換え"), (0.0, "ⓒ引き当てなし"))


def load_checker():
    """検算.py をそのまま借りる——数え方を二重に持たないため。"""
    spec = importlib.util.spec_from_file_location("kensa", HERE / "検算.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def head_text(rel):
    """08f21e6 時点の草稿。無ければ None（その話は当時まだ無かった）。"""
    try:
        out = subprocess.run(
            ["git", "show", f"{HEAD}:{rel}"],
            cwd=REPO, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError:
        return None
    return out.stdout.splitlines()


def band(ratio):
    for floor, name in BANDS:
        if ratio >= floor:
            return name
    return BANDS[-1][1]


def classify(old_sents, new_sents):
    """原本の一文ごとに、この稿のなかで最も近い文を当てて、帯に割る。

    ⚠ 総当たりにしない。ratio の上限は `2*min/(len(a)+len(b))` ゆえ、
       長さが 2 倍以上離れた相手は 0.5 を超えない——**ⓒの床（0.60）に届かない**。
       ゆえに、まず長さで候補を絞り、それでも空なら全体に落とす。
       （全63話＝原本 約19,000文。総当たりでは現実的な時間で終わらない）
    """
    exact = set(new_sents)
    rows = []
    for s in old_sents:
        if s in exact:                       # 逐語で残っている——いちばん多い
            rows.append((s, s, 1.0, band(1.0)))
            continue
        lo, hi = len(s) * 0.42, len(s) * 2.4   # 0.60 に届きうる長さの幅
        cand = [t for t in new_sents if lo <= len(t) <= hi]
        best, best_r = None, -1.0
        for t in (cand if cand else new_sents):
            r = difflib.SequenceMatcher(None, s, t).ratio()
            if r > best_r:
                best, best_r = t, r
                if r >= 0.999:
                    break
        rows.append((s, best, best_r, band(best_r)))
    return rows


def pairs():
    """(話, 原本のパス, この稿の相対パス)。題の表記は草稿のファイル名から取る。"""
    out = []
    for vol, repo in VOL.items():
        for p in sorted((WORK / "草稿").glob(f"draft_{vol}-*.md")):
            num = p.name.split("_")[1]
            old = sorted((REPO / "examples" / repo / "草稿").glob(f"draft_{num}_*.md"))
            if not old:
                print(f"  ⚠ 原本が見つからない: {num}", file=sys.stderr)
                continue
            rel = str(p.relative_to(REPO))
            out.append((num, old[0], p, rel))
    return out


def one(num, old_path, new_path, rel, kensa, want_rows):
    old = [s for _, s in kensa.narration_sentences(kensa.load(old_path))]
    after = kensa.sentences_of(kensa.load(new_path))
    before_lines = head_text(rel)
    if before_lines is None:
        before = []
        existed = False
    else:
        before = kensa.sentences_of(before_lines)
        existed = True

    rows_after = classify(old, after)
    rows_before = classify(old, before) if existed else []

    def bucket(rows):
        c = {"ⓐほぼ同じ": 0, "ⓑ書き換え": 0, "ⓒ引き当てなし": 0}
        for _, _, _, b in rows:
            c[b] += 1
        return c

    b_after = bucket(rows_after)
    b_before = bucket(rows_before)

    set_after = set(after)
    set_before = set(before)
    # 原本の文が、前／後に「逐語で」残っているか
    word_before = {s for s in old if s in set_before}
    word_after = {s for s in old if s in set_after}

    newly_lost = sorted(word_before - word_after)     # ⛔ Upgrade で消えた逐語
    restored = sorted(word_after - word_before)       # ✅ Upgrade で戻った逐語

    row = {
        "話": num, "原本の文": len(old),
        "前": b_before, "後": b_after,
        "新たに落ちた": newly_lost, "戻った": restored,
        "ⓒの文": [r for r in rows_after if r[3] == "ⓒ引き当てなし"],
        "ⓒだったが直った": [r for r in rows_before if r[3] == "ⓒ引き当てなし"],
    }
    if want_rows:
        print(f"\n■ {num}  原本 {len(old)}文")
        print(f"    ⓐ{b_after['ⓐほぼ同じ']}  ⓑ{b_after['ⓑ書き換え']}  ⓒ{b_after['ⓒ引き当てなし']}"
              f"   （前は ⓐ{b_before['ⓐほぼ同じ']} ⓑ{b_before['ⓑ書き換え']} ⓒ{b_before['ⓒ引き当てなし']}）")
        for s, near, r, _ in row["ⓒの文"]:
            print(f"    ⓒ {s}")
            print(f"       ↳ 最も近い文 r={r:.2f}: {near}")
        for s in newly_lost:
            print(f"    ⛔ 新たに消えた逐語: {s}")
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true", help="ⓒ と新たな脱落を印字")
    ap.add_argument("--talk", default=None, metavar="NN-EE")
    a = ap.parse_args()

    kensa = load_checker()
    rows = []
    for num, old_path, new_path, rel in pairs():
        if a.talk and num != a.talk:
            continue
        rows.append(one(num, old_path, new_path, rel, kensa,
                        want_rows=a.list or a.talk))

    if a.talk:
        return

    tot = lambda k, w: sum(r[w][k] for r in rows)  # noqa: E731
    o = sum(r["原本の文"] for r in rows)
    print(f"\n■ {len(rows)}話／原本 {o}文")
    print(f"  {'':<14}{'ⓐほぼ同じ':>10}{'ⓑ書き換え':>10}{'ⓒ引き当てなし':>14}")
    for w, name in (("前", f"{HEAD}（Upgrade 前）"), ("後", "いまの作業木")):
        print(f"  {name:<14}{tot('ⓐほぼ同じ', w):>10}{tot('ⓑ書き換え', w):>10}"
              f"{tot('ⓒ引き当てなし', w):>14}")

    lost = [(r["話"], s) for r in rows for s in r["新たに落ちた"]]
    back = [(r["話"], s) for r in rows for s in r["戻った"]]
    fixed = [r["話"] for r in rows if r["ⓒだったが直った"] and not r["ⓒの文"]]
    print(f"\n  ✅ Upgrade で戻った逐語      {len(back)}文（{len({t for t, _ in back})}話）")
    print(f"  ⛔ Upgrade で新たに消えた逐語 {len(lost)}文（{len({t for t, _ in lost})}話）")
    print(f"  ✅ ⓒ が空になった話          {len(fixed)}話 {fixed if fixed else ''}")
    if lost and not a.list:
        print("\n  ⚠ 中身は `--list` で出る。**数を門にしない**（依頼文 §9-1）。")


if __name__ == "__main__":
    main()
