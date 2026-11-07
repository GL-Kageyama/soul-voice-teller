#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""五感を数える.py——本文を、器官ごとの語で数える。

**何のためか。** 系列 第三回（娯楽だけの A/B）の議長推奨②——
「職場ごとに五感の比重をずらす（ある職場は音、ある職場は温度）」——を、
測るためである。**⚠ これは計測器であり、本文を触らない。**

**⚠ 走査の鍵は、その欄に掛ける**（[[scan-key-must-match-the-field]]）。
ここでは「器官の語」そのものが鍵であるゆえ、**語の側に掛ける。**

**⚠ 単位は「話」ではなく「行」である**——**⚠ 出現数と行数は違う**
（[[measured-scope-vs-claimed-scope]]）。**両方を出す。**

    python3 五感を数える.py [--tsv] [--list 器官]
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from importlib import import_module

_m = import_module("娯楽を数える") if False else None  # noqa: F841  (読み込みの副作用を避ける)

ROOT = Path(__file__).resolve().parents[1]          # examples/habits
EX = ROOT.parent                                     # examples
VOLS = ["01", "02", "03", "04"]

# 器官ごとの語。**⚠ 語は、必ず「その器官でしか出ない」ものだけを置く。**
# 名（「名」「欄」「紙」）は器官ではないゆえ、入れない。
ORGAN = {
    "視": ["光", "明る", "暗い", "白い", "黒い", "影", "色", "見える", "まぶし", "見えな", "赤", "青"],
    "聴": ["音", "聞こ", "響", "鳴", "静か", "耳", "ざわ", "物音"],
    "温": ["冷た", "冷え", "ひやり", "温", "熱", "ぬる", "湿", "寒", "暑", "湯気", "蒸気",
           "暖", "ぬく", "火", "日なた", "冷房", "暖房"],
    "触": ["ざら", "つる", "硬", "柔", "重さ", "軽", "手触り",
           "指の腹", "肌", "触", "握", "押", "引", "滑"],
    "嗅": ["匂", "にお", "香"],
    "味": ["味", "苦", "甘", "渋", "塩"],
    "空": ["雨", "風", "曇", "晴", "雪", "天気", "空気"],
    "身": ["疲", "眠", "だる", "痛", "息", "汗", "喉", "肩", "腰", "膝"],
}

HEAD = re.compile(r"^\s*(#|>|```)")
DIVIDER = re.compile(r"^\s*＊\s*$")


def count_chars(s):
    return sum(1 for c in s if not c.isspace())


def prose_lines(path):
    out = []
    for i, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        s = line.rstrip()
        if not s.strip():
            continue
        if HEAD.match(s) or DIVIDER.match(s):
            continue
        out.append((i, s))
    return out


def scan():
    rows = []
    for v in VOLS:
        for f in sorted((EX / f"habits-{v}" / "草稿").glob("draft_*.md")):
            key = f.name.split("_")[1]                 # 01-01
            lines = prose_lines(f)
            n_chars = sum(count_chars(s) for _, s in lines)
            hits = {o: 0 for o in ORGAN}
            lhit = {o: 0 for o in ORGAN}
            for _, s in lines:
                for o, ws in ORGAN.items():
                    n = sum(s.count(w) for w in ws)
                    if n:
                        hits[o] += n
                        lhit[o] += 1
            rows.append({"話": key, "巻": v, "行": len(lines), "字数": n_chars,
                         "出現": hits, "行数": lhit})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tsv", action="store_true", help="話ごとの表を出す")
    ap.add_argument("--list", help="一つの器官だけを、話ごとに並べる")
    a = ap.parse_args()
    rows = scan()
    os_ = list(ORGAN)

    if a.list:
        o = a.list
        if o not in ORGAN:
            sys.exit(f"器官の名が違う: {o}（在るのは {'・'.join(os_)}）")
        print(f"■ {o}——語＝{'・'.join(ORGAN[o])}")
        for r in rows:
            print(f"  {r['話']}  出現 {r['出現'][o]:>3}  行 {r['行数'][o]:>3} / {r['行']:>3}行  {r['字数']:>5}字"
                  f"   {r['出現'][o] / max(r['字数'], 1) * 1000:>5.1f} /1000字")
        return

    if a.tsv:
        print("話\t字数\t" + "\t".join(os_) + "\t" + "\t".join(o + "(行)" for o in os_))
        for r in rows:
            print(f"{r['話']}\t{r['字数']}\t" + "\t".join(str(r['出現'][o]) for o in os_)
                  + "\t" + "\t".join(str(r['行数'][o]) for o in os_))
        return

    print("【巻ごと——1000字あたりの出現数】")
    print("巻\t字数\t" + "\t".join(os_))
    for v in VOLS:
        rs = [r for r in rows if r["巻"] == v]
        n = sum(r["字数"] for r in rs)
        print(f"{v}\t{n}\t" + "\t".join(f"{sum(r['出現'][o] for r in rs) / n * 1000:.1f}" for o in os_))

    print("\n【巻ごと——その語を含む行の割合（%）】")
    print("巻\t本文行\t" + "\t".join(os_))
    for v in VOLS:
        rs = [r for r in rows if r["巻"] == v]
        n = sum(r["行"] for r in rs)
        print(f"{v}\t{n}\t" + "\t".join(f"{sum(r['行数'][o] for r in rs) / n * 100:.1f}" for o in os_))

    print("\n【全巻——1000字あたり】")
    n = sum(r["字数"] for r in rows)
    print("\t" + "\t".join(os_))
    print(f"{n}字\t" + "\t".join(f"{sum(r['出現'][o] for r in rows) / n * 1000:.1f}" for o in os_))

    print("\n数え方——本文行のみ（題名・見出し・`＊`・空行を除く）。"
          "⚠ 出現数と行数は別である（`--tsv` で両方出る）。")
    print(f"走査した集合——{len(rows)} 話。")


if __name__ == "__main__":
    main()
