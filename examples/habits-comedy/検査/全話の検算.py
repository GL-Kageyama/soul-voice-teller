#!/usr/bin/env python3
"""全話の検算——変換稿63話を、原本と並べて一望する。

    python3 検査/全話の検算.py            # 表を出す
    python3 検査/全話の検算.py --json     # JSON で出す
    python3 検査/全話の検算.py --diff     # 差の内訳（増えた行・消えた行）も出す

これは検査であって、評価ではない。出すのは数だけである。

⚠ 作法 §3 の八つのうち、機械が数えられるのは ②⑤⑥⑦⑧ である。
   ①禁則は check.py を別に当てる（この器は呼ばない——遅いため）。
   ③④は人が読む（場面表 §4・§3）。

⚠ 2026-10-15——会話劇への Upgrade で、列を二つ足した。
   ・「独白」——丸括弧 `（…）` の行（作法 §0-2）
   ・「声なし節」——会話も独白も一行も無い節（作法 §2 段4の内側）
   ⛔ 印は現象ではない。括弧を置けば数は増えるが、声は増えない
      （[marker-is-not-the-phenomenon]）。この列は門であって、判定ではない。
"""

import argparse
import glob
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                      # examples/habits-comedy
EX = ROOT.parent                        # examples
sys.path.insert(0, str(HERE))
import importlib.util
_spec = importlib.util.spec_from_file_location("k", HERE / "検算.py")
K = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(K)

VOLS = ["01", "02", "03", "04"]


def episodes():
    """(巻, 話番号, 題, 原本パス, この稿パス, 場面表パス, 原本場面表パス)"""
    for vol in VOLS:
        for p in sorted(glob.glob(str(EX / f"habits-{vol}" / "草稿" / f"draft_{vol}-*.md"))):
            name = Path(p).name                      # draft_01-03_題.md
            tail = name[len("draft_"):]              # 01-03_題.md
            ep = tail[:5]                            # 01-03
            t = tail[6:-3]                           # 題
            yield (vol, ep, t,
                   Path(p),
                   ROOT / "草稿" / name,
                   ROOT / "構想" / "各話" / f"{ep[3:]}_{t}.md",
                   EX / f"habits-{vol}" / "構想" / "各話" / f"{ep[3:]}_{t}.md")


def row(vol, ep, t, old_p, new_p, table_p, old_table_p):
    r = {"巻": vol, "話": ep, "題": t,
         "原本": str(old_p), "この稿": str(new_p),
         "場面表": str(table_p), "原本の場面表": str(old_table_p),
         "ある": new_p.exists(), "場面表がある": table_p.exists()}
    if not new_p.exists():
        return r
    n = K.summarize(new_p)
    o = K.summarize(old_p) if old_p.exists() else None
    d = K.diff_sentences(old_p, new_p) if old_p.exists() else None
    r.update({
        "字数": n["字数"], "原本字数": o["字数"] if o else None,
        "差": (n["字数"] - o["字数"]) if o else None,
        "本文行": n["本文行"], "原本本文行": o["本文行"] if o else None,
        "会話行": n["会話行"], "原本会話行": o["会話行"] if o else None,
        "独白行": n["独白行"], "原本独白行": o["独白行"] if o else None,
        "声の無い節": n["声の無い節"], "声の無い節の数": len(n["声の無い節"]),
        "節数": len(n["節"]), "原本節数": len(o["節"]) if o else None,
        "五文以上": n["段落"]["五文以上"],
        "原本五文以上": o["段落"]["五文以上"] if o else None,
        "最長": n["段落"]["最長"],
        "文/行": n["段落"]["文/行"],
        "である末": n["地の文"]["である末の割合"],
        "原本である末": o["地の文"]["である末の割合"] if o else None,
        "落とした文": d["この稿に無い文"] if d else None,
        "原本の文数": d["原本の文数"] if d else None,
    })
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--diff", action="store_true")
    a = ap.parse_args()

    rows = [row(*e) for e in episodes()]

    if a.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return

    done = [r for r in rows if r["ある"]]
    tables = [r for r in rows if r["場面表がある"]]
    print(f"■ 変換稿 {len(done)}/{len(rows)} 話   場面表 {len(tables)}/{len(rows)} 枚\n")
    print(f"{'話':<7}{'題':<24}{'原本':>7}{'この稿':>8}{'差':>7}{'会話':>9}"
          f"{'独白':>8}{'5文+':>7}{'落とし':>8}{'声なし節':>9}{'場面表':>7}")
    print("-" * 110)
    for r in rows:
        t = r["題"]
        if len(t) > 22:
            t = t[:21] + "…"
        if not r["ある"]:
            print(f"{r['話']:<7}{t:<24}{'—':>7}{'—':>8}{'—':>7}{'—':>9}{'—':>8}"
                  f"{'—':>7}{'—':>8}{'—':>9}"
                  f"{'✅' if r['場面表がある'] else '—':>7}")
            continue
        d = r["差"]
        ds = f"{d:+,}" if d is not None else "—"
        talk = f"{r['原本会話行']}→{r['会話行']}"
        mono = f"{r['原本独白行']}→{r['独白行']}"
        five = f"{r['原本五文以上']}→{r['五文以上']}"
        miss = f"{r['落とした文']}/{r['原本の文数']}" if r["落とした文"] is not None else "—"
        nov = str(r["声の無い節の数"]) if r["声の無い節の数"] else "0"
        print(f"{r['話']:<7}{t:<24}{r['原本字数']:>7,}{r['字数']:>8,}{ds:>7}"
              f"{talk:>9}{mono:>8}{five:>7}{miss:>8}{nov:>9}"
              f"{'✅' if r['場面表がある'] else '—':>7}")

    # 巻ごとの集計
    print()
    for vol in VOLS:
        v = [r for r in rows if r["巻"] == vol]
        vd = [r for r in v if r["ある"]]
        so = sum(r["原本字数"] for r in vd)
        sn = sum(r["字数"] for r in vd)
        print(f"  第{int(vol)}巻  {len(vd)}/{len(v)}話  原本 {so:,} → この稿 {sn:,}"
              f"  ({sn - so:+,})")

    # 検査の通し
    print()
    ng = []
    for r in done:
        if r["五文以上"] != 0:
            ng.append(f"  ⛔ {r['話']} 五文以上の段落 {r['五文以上']}個")
        if r["原本節数"] and r["節数"] != r["原本節数"]:
            ng.append(f"  ⚠ {r['話']} 節の数が違う（原本 {r['原本節数']} → {r['節数']}）")
        if not r["場面表がある"]:
            ng.append(f"  ⚠ {r['話']} 場面表が無い")

    # ⑧ 声の無い節——2026-10-15 に足した門（作法 §2 段4の内側）
    silent = [r for r in done if r["声の無い節の数"]]
    if silent:
        ng.append(f"  ⚠ 声（会話＋独白）が一つも無い節がある話 {len(silent)}/{len(done)}話"
                  f"——{'・'.join(r['話'] for r in silent[:24])}"
                  f"{'…' if len(silent) > 24 else ''}")
        ng.append("     （作法 §2 段4の内側。⚠ 印は現象ではない——"
                  "括弧を置けば数は増えるが、声は増えない）")

    if ng:
        print("■ 気づいたこと")
        for s in ng:
            print(s)
    else:
        print("✅ 五文以上の段落 0・節の数は原本と同じ・場面表あり・声の無い節 0")

    if a.diff:
        print()
        for e in episodes():
            vol, ep, t, old_p, new_p, tp, otp = e
            if not new_p.exists():
                continue
            import difflib
            old = [s for _, s in K.prose_lines(K.load(old_p))]
            new = [s for _, s in K.prose_lines(K.load(new_p))]
            sm = difflib.SequenceMatcher(None, old, new)
            add = rep = dele = 0
            for tag, i1, i2, j1, j2 in sm.get_opcodes():
                if tag == "insert":
                    add += j2 - j1
                elif tag == "delete":
                    dele += i2 - i1
                elif tag == "replace":
                    rep += max(i2 - i1, j2 - j1)
            print(f"{ep}  挿入 {add:>3}  置換 {rep:>3}  削除 {dele:>3}")


if __name__ == "__main__":
    main()
