#!/usr/bin/env python3
"""台帳を作る——娯楽の検品のための、**機械で埋まる欄だけ**を、一つの表に合流させる。

⚠ **この器は、読者の欄を埋めない。** 出すのは**機械で出る欄**だけである——
   「実現した軸」「三種」「掴んでいるか」「ズレの有無」「案」は、**空で出す**。
   **埋めるのは人である**（計画の第二段——読者の欄は、巻ごとに一人）。

⚠ **三つの器を合流させる。** どれも、この台帳のために新しく書いたものではない——

   1. `娯楽を数える.py`——場面の幾何（行・字数・段落・文・会話・入口・場面末）と、章末の形
   2. `軸を数える.py`——場面表の「反応軸」の欄（設計が、その場面に配った軸と三種）
   3. `場面表を検める.py`——設計の入口の句が、第一段落にどれだけ在るか

⚠ **合流の鍵は「話＋場面」である。** ⚠ 巻では合流しない——**話の名は、巻をまたいで重ならない**
   （`01-01` … `04-18`）ゆえ、話だけで足りる。だが**場面の数は巻で違う**ゆえ、場面で引く。

⚠ **入口の四欄（`入口の判定`・`①設計の字を持つ`・`②第一段落の割合`・`最良の段落`）は、
   場面1にしか無い。** 場面2以降には **`—`** を書く——**空欄にはしない。**
   **「空欄が無いこと」を、機械で数えられる形にするためである**（空ファイルは内容でない）。

⚠ **`--keep` を付けずに走らせると、人が埋めた七欄は消える。**
   **この器は、機械の欄しか作らない**（§ 冒頭）。**人が埋めた欄を持ったまま
   機械の欄だけを更新したいときは、必ず `--keep 娯楽台帳.tsv` を付ける。**

使い方:
    python3 台帳を作る.py                    # 標準出力へ（読者の欄は空）
    python3 台帳を作る.py > 娯楽台帳.tsv
    python3 台帳を作る.py --summary          # 合流の検算だけを出す
    python3 台帳を作る.py --keep 娯楽台帳.tsv # ⚠ 読者の欄を、既存の台帳から引き継ぐ
"""

import argparse
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # examples/habits/研ぎ


def load(fname: str, name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / fname)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# ⚠ 機械の欄と、読者の欄。**読者の欄は、空で出す。**
MACHINE = ["話", "場面", "行", "字数", "段落", "文", "会話",
           "設計の軸", "設計の三種", "設計の位相",
           "入口の判定", "①設計の字を持つ", "②第一段落の割合", "最良の段落",
           "章末の形"]
READER = ["実現した軸", "三種", "掴んでいるか", "器（与えた／欠けさせた）",
          "設計との差", "ズレの有無", "案"]


def main() -> int:
    ap = argparse.ArgumentParser(description="娯楽台帳の、機械で埋まる欄を合流させる")
    ap.add_argument("--summary", action="store_true", help="合流の検算だけを出す")
    ap.add_argument("--keep", metavar="FILE",
                    help="既存の台帳。読者の欄を (話,場面) で引き継ぐ")
    a = ap.parse_args()

    # ---------------------------------------------------------- 0. 読者の欄を引き継ぐ
    kept, keep_note = {}, ""
    if a.keep:
        old = [ln.split("\t") for ln in
               Path(a.keep).read_text(encoding="utf-8").split("\n") if ln.strip()]
        oh = old[0]
        if oh[:len(MACHINE)] != MACHINE:
            sys.exit(f"⛔ 引く台帳の機械の欄が、この器の並びと違う——{a.keep}")
        idx = {c: oh.index(c) for c in READER}
        # ⚠ 話＋場面で引く。⚠ 話の名は巻をまたいで重ならない
        for r in old[1:]:
            kept[(r[0], r[1])] = [r[idx[c]] if idx[c] < len(r) else "" for c in READER]
        filled = sum(1 for v in kept.values() if any(x.strip() for x in v))
        keep_note = (f"\n⚠ 引き継いだ読者の欄——{filled} 行（{a.keep}）。"
                     f"空のままの行が {len(kept) - filled} 行ある。")

    ent = load("娯楽を数える.py", "ent")
    ax = load("軸を数える.py", "ax")
    sc = load("場面表を検める.py", "sc")

    # ---------------------------------------------------------- 1. 娯楽を数える
    files = ent.draft_files()
    if not files:
        sys.exit("⛔ 草稿が一本も無い（空の検査は通さない）")

    scenes, chapters = [], {}
    for f in files:
        p = Path(f)
        text = p.read_text(encoding="utf-8")
        if not text.strip():
            sys.exit(f"⛔ 空の草稿がある——{p}")
        key = p.name.split("_")[1]
        lines = text.split("\n")
        prose = ent.prose_lines(lines)
        for num, xs in ent.scenes(lines):
            scenes.append({
                "話": key, "場面": str(num),
                "行": f"{xs[0][0]}-{xs[-1][0]}",
                "字数": sum(ent.count_chars(s) for _, s in xs),
                "段落": len(xs), "文": sum(ent.bun(s) for _, s in xs),
                "会話": sum(1 for _, s in xs if s.startswith(("「", "『"))),
                "入口": xs[0][1], "場面末": xs[-1][1],
            })
        chapters[key] = {
            "章末の形": ent.classify(ent.ENDING_TYPES,
                                     ent.last_sentence(prose[-1][1]) if prose else ""),
            "第一段落": ent.first_sentence(prose[0][1]) if prose else "",
        }

    # ---------------------------------------------------------- 2. 軸を数える
    ref, order = ax.axis_reference()
    axes = {}
    for f in ax.tables():
        p = Path(f)
        key = f"{p.parent.parent.parent.name.replace('habits-', '')}-{p.name.split('_')[0]}"
        for num, cell in ax.scene_rows(p):
            axis, sub, phase = ax.parse_cell(cell)
            axes[(key, str(num))] = {"設計の軸": axis, "設計の三種": sub,
                                     "設計の位相": phase, "逐語": cell}

    # ---------------------------------------------------------- 3. 場面表を検める
    D = sc.drafts()
    entrance = {}
    for v, f in sc.tables():
        p = Path(f)
        key = f"{v}-{p.name.split('_')[0]}"
        cell = sc.entrance_row(p)
        if cell is None or key not in D:
            continue
        paras = sc.scene1_paragraphs(Path(D[key]).read_text(encoding="utf-8"))
        e = next((x for x in sc.clauses(cell) if sc.FIRST_RE.match(x[0])), None)
        if e is None:
            continue
        m = sc.measure(paras, sc.kanji(sc.FIRST_RE.match(e[0]).group(1)))
        entrance[key] = {
            "入口の判定": m["判定"] if m else "—",
            "①設計の字を持つ": f"{100*m['持']:.0f}%" if m else "—",
            "②第一段落の割合": (f"{100*m['一']:.0f}%" if m and m["一"] is not None else "—"),
            "最良の段落": (str(m["最良の段落"]) if m and m["最良の段落"] is not None else "—"),
        }

    # ---------------------------------------------------------- 合流
    rows, gaps = [], {"軸": 0, "入口": 0, "章末": 0}
    for s in scenes:
        k = (s["話"], s["場面"])
        ax_row = axes.get(k)
        if ax_row is None:
            gaps["軸"] += 1
        s.update(ax_row or {"設計の軸": "", "設計の三種": "", "設計の位相": ""})
        if s["場面"] == "1":
            en = entrance.get(s["話"])
            if en is None:
                gaps["入口"] += 1
            s.update(en or {c: "—" for c in ("入口の判定", "①設計の字を持つ",
                                             "②第一段落の割合", "最良の段落")})
        else:
            # ⚠ 入口の四欄は、場面1にしか無い。**空欄にしない——`—` を書く。**
            for c in ("入口の判定", "①設計の字を持つ", "②第一段落の割合", "最良の段落"):
                s[c] = "—"
        s["章末の形"] = chapters.get(s["話"], {}).get("章末の形", "")

    if a.summary:
        print(f"合流した場面——{len(rows) if rows else len(scenes)} 行"
              f"（{len({s['話'] for s in scenes})} 話）")
        print(f"場面表——{len(ax.tables())} 枚。反応軸の欄を読めた場面——{len(axes)}")
        print(f"入口の欄——{len(entrance)} 話ぶん")
        print(f"⚠ 合流しなかった——軸 {gaps['軸']} 場面／入口 {gaps['入口']} 話")
        return 0

    cols = MACHINE + READER
    print("\t".join(cols))
    for s in scenes:
        out = []
        for c in MACHINE:
            v = str(s.get(c, ""))
            out.append(v.replace("\t", " ").replace("\n", " "))
        out += kept.get((s["話"], s["場面"]), ["" for _ in READER])
        print("\t".join(out))

    if keep_note:
        print(keep_note, file=sys.stderr)
    print(f"⚠ 合流しなかった——軸 {gaps['軸']} 場面／入口 {gaps['入口']} 話", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
