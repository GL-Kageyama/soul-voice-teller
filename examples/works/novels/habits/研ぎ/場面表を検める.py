#!/usr/bin/env python3
"""場面表を検める——「入口の掴み」が、本文の第一段落に、どれだけ在るかを測る（読み取り専用）。

⚠ **この器は、意味を判定しない。** 出すのは**字の在り処**だけである。

⚠ **なぜ、逐語一致で測らないか。** 第三巻 `03-08` の場面表が、自ら書いている——
  「**入口の掴み——場面表の、一行を、第一文に、置いた。**……**⚠「書き直しの要る」は、
   地の文に、置かなかった**——**この巻の、地の文は、物の、名を、書かない**」。
  **ゆえに設計の逐語は、本文に無いことがある。** 逐語一致で測る器は、これを「無し」と誤る。

⚠ **そして、「要素の字を全部含む段落」で測る器も、誤る。**
  **それを作って、走らせて、誤りを見た**——`03-08` が「無し」と出た。
  設計が**意図して落とした語**（「書き直しの要る」）が、判定を壊していた。
  **ゆえに、この器は率で測る。**

⚠ **数え方**——設計の句から**漢字を一つ残らず取り出し**（一文字も残す）、
  **本文の第一場面が、その字をどれだけ持っているか**を測る。そして、
  **持っている分の何割が、第一段落にあるか**で判定する。

      `持`——第一場面が持っている字 / 設計の句の字　（**章が、設計の字を残した割合**）
      `一`——第一段落が持っている字 / **第一場面が持っている字**　（**ゆえに分母が、設計ではない**）

  ⚠ **分母を設計にしないのが、この器の要である。** `03-08` の設計は
    「台に、**書き直しの要る**一枚が上がる。」であり、**「書き直しの要る」は、地の文に置かないと
    決められた**。設計を分母にすると、**意図して落とした三字が、判定を壊す**（この器が、一度そうなった）。
  ⚠ これは**字の重なり**であって、**意味の一致ではない**。
  ⚠ 一文字の漢字も数える（「名」「欄」は、この作品では内容語である）。
  ⚠ **閾値は、この器が決めた規約である**（下の三行）。**自然の境目ではない。**

      **在**——第一場面が持っている字の **八割以上** が、第一段落にある
      **後ろ**——第一段落には足りないが、**第一場面の、どこかの段落**が八割を越える
      **無し**——第一場面が、設計の字を一つも持たない。または、どの段落も八割に届かない

⚠ **これは、`第七段階_第五段_⑦_段落の形の検品.md` §4-1 の欄を、再現しない。**
  あの表の「設計が名指した要素」は、**人が行を読んで選んだ**ものである——
  `01-02` では、行の**太字でない側**（「名の欄は、まだ書かれていない」）を採っている。
  **この器は、行の要素を一つも選ばない。行の要素を、全部、並べる。** 選ぶのは人である。

使い方:
    python3 場面表を検める.py               # 六十三話の、要素ごとの在り処
    python3 場面表を検める.py --list        # 逐語で、全部
    python3 場面表を検める.py --off-list    # 「第一文」が第一段落に無い話だけ
    python3 場面表を検める.py --known       # 人手で出た十二話と、突き合わせる
"""

import argparse
import glob
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent          # examples/habits/研ぎ
HABITS = HERE.parent                            # examples/habits
EXAMPLES = HABITS.parent                        # examples
VOLS = ("01", "02", "03", "04")

RULE_RE = re.compile(r"^＊$")                   # 場面の区切り（著者裁定 2026-10-13）
HEAD_RE = re.compile(r"^##\s*(\d+)\s*$")        # 控え（段落化の前）の札
TITLE_RE = re.compile(r"^#\s+第\d+話")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
KANJI_RE = re.compile(r"[一-鿿々]")
FIRST_RE = re.compile(r"^第一場面の第一文——(.*)$")
FULL = 0.8                                       # ⚠ 規約である（docstring を見よ）

# ⚠ 「設計が名指した要素」を人が選んだ結果——`第七階階_第五段_⑦_段落の形の検品.md` §4-1。
#   **この器の欄とは、別の欄である。** 突き合わせて、食い違いを見るために置く。
KNOWN = {
    "01-02": "名の欄は、まだ書かれていない",
    "01-06": "給食室に、名簿が一つある",
    "02-03": "傘立ての前に立ち、数を確かめる",
    "02-07": "車の中で、伝票をめくる",
    "02-11": "箱を、車から降ろす。段差",
    "03-05": "棚の手帳は、綴じ目から見える",
    "03-11": "一通だけ、宛名が違う",
    "03-12": "消す欄が、一つもない",
    "03-14": "棚から、名簿を出す／渡される前の名簿",
    "04-12": "画面と表示名",
    "04-13": "ほどかれた名が糸になっている",
    "04-16": "紙の上に、名前欄がある／欄の中に、！が三つある",
    "04-09": "紙の上に、名が置かれている／その名は、同じ大きさである",
}


def entrance_row(path: Path):
    """「入口の掴み」の行の、値のセルを返す（欄は、見出しの名で引く）。"""
    for line in path.read_text(encoding="utf-8").split("\n"):
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) >= 2 and cells[0].strip("*").strip() == "入口の掴み":
            return cells[1]
    return None


def clauses(cell: str):
    """セルを、要素の並びへ割る——太字のまとまりと、太字でないまとまりを、順に。"""
    out, pos = [], 0
    for m in BOLD_RE.finditer(cell):
        for piece in split_sentences(cell[pos:m.start()]):
            out.append((piece, False))
        for piece in split_sentences(m.group(1)):
            out.append((piece, True))
        pos = m.end()
    for piece in split_sentences(cell[pos:]):
        out.append((piece, False))
    return out


def split_sentences(s: str):
    return [p.strip() for p in re.split(r"(?<=[。．！？])", s) if p.strip()]


def scene1_paragraphs(text: str):
    """第一場面の段落（段落化のあとは、段落＝物理的な一行）。"""
    lines = text.split("\n")
    if any(HEAD_RE.match(l.strip()) for l in lines):
        out, started = [], False
        for ln in lines:
            s = ln.strip()
            if HEAD_RE.match(s):
                if started:
                    break
                started = True
                continue
            if started and s and not s.startswith("#"):
                out.append(s)
        return out
    out = []
    for ln in lines:
        s = ln.strip()
        if RULE_RE.match(s):
            break
        if s and not s.startswith("#") and not TITLE_RE.match(s):
            out.append(s)
    return out


def kanji(s: str):
    return set(KANJI_RE.findall(s))


def measure(paras, ks):
    """設計の句の字が、**この章にどれだけ在り、その何割が第一段落にあるか**。

    ⚠ **分母は、設計ではなく、第一場面が持っている字である**（docstring を見よ）。
       `03-08` の「書き直しの要る」のように、**意図して落とされた字**が、判定を壊さないため。
    """
    if not ks:
        return None
    counts = [len(ks & kanji(p)) for p in paras]
    held = len(ks & kanji("".join(paras)))       # 第一場面が持っている字
    if held == 0:
        return {"持": 0.0, "一": None, "最良": 0, "最良の段落": None, "判定": "無し"}
    best = max(counts)
    at = counts[0] / held
    if at >= FULL and best >= FULL:
        v = "在"
    elif best >= FULL:
        v = "後ろ"
    else:
        v = "無し"
    return {"持": held / len(ks), "一": at, "最良": best / held,
            "最良の段落": counts.index(best), "判定": v}


def tables():
    out = []
    for v in VOLS:
        for f in sorted(glob.glob(str(EXAMPLES / f"habits-{v}" / "構想" / "各話" / "*.md"))):
            out.append((v, f))
    return out


def drafts():
    out = {}
    for v in VOLS:
        for f in sorted(glob.glob(str(EXAMPLES / f"habits-{v}" / "草稿" / "draft_*.md"))):
            out[Path(f).name.split("_")[1]] = f
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="入口の掴みが、第一段落にどれだけ在るか")
    ap.add_argument("--list", action="store_true", help="逐語で全部を出す")
    ap.add_argument("--off-list", action="store_true", help="「第一文」が第一段落に無い話だけを出す")
    ap.add_argument("--known", action="store_true", help="人手で出た十二話と突き合わせる")
    a = ap.parse_args()

    D = drafts()
    if not D:
        sys.exit("⛔ 草稿が一本も無い（空の検査は通さない）")

    rows, missing = [], []
    for v, f in tables():
        p = Path(f)
        key = f"{v}-{p.name.split('_')[0]}"
        cell = entrance_row(p)
        if cell is None:
            missing.append(key)
            continue
        if key not in D:
            sys.exit(f"⛔ 場面表に、本文が無い——{key}")
        text = Path(D[key]).read_text(encoding="utf-8")
        if not text.strip():
            sys.exit(f"⛔ 空の草稿がある——{D[key]}")
        paras = scene1_paragraphs(text)
        if not paras:
            sys.exit(f"⛔ 第一場面の段落が、一行も読めない——{key}")

        els = []
        for piece, bold in clauses(cell):
            m = FIRST_RE.match(piece)
            body = m.group(1) if m else piece
            els.append({"逐語": body, "太字": bold, "第一文": m is not None,
                        "字数": len(kanji(body)), "測": measure(paras, kanji(body))})
        rows.append({"話": key, "巻": v, "段落数": len(paras),
                     "第一段落": paras[0], "要素": els})

    if not rows:
        sys.exit("⛔ 入口の掴みを持つ場面表が、一枚も無い（走査の鍵が掛かっていない）")

    print(f"走査した集合——`examples/habits-0{{1..4}}/構想/各話/*.md`。"
          f"読んだのは「入口の掴み」の欄と、第一場面の段落だけである。")
    print(f"⚠ 数え方——設計の句の漢字（一文字も残す）を、第一場面がどれだけ持ち（①）、"
          f"**そのうち何割が第一段落にあるか**（②）。**字の重なりであって、意味の一致ではない。**")
    print(f"⚠ **分母を設計にしない。** 設計が意図して落とした字（`03-08`「書き直しの要る」）が、"
          f"判定を壊さないため。")
    print(f"⚠ 閾値は、この器の規約である——`在`＝②が八割／`後ろ`＝第一段落には足りないが"
          f"第一場面のどこかで八割／`無し`＝①が零、またはどこも八割に届かない。**自然の境目ではない。**")
    print(f"⚠ 場面表 {len(rows)} 枚。欄を持たない場面表——{len(missing)} 枚"
          + (f"（{', '.join(missing)}）" if missing else ""))
    print()

    def at1(e):
        return e["測"]["一"] if e["測"] and e["測"]["一"] is not None else None

    def vd(e):
        return e["測"]["判定"] if e["測"] else "—"

    firsts = [(r, next((e for e in r["要素"] if e["第一文"]), None)) for r in rows]
    judged = [(r, e) for r, e in firsts if e is not None]

    print("【「第一場面の第一文——」と名指された句】")
    print(f"  その句を持つ行——{len(judged)} / {len(rows)} 枚")
    if len(judged) < len(rows):
        print(f"  ⚠ 持たない行——{', '.join(r['話'] for r, e in firsts if e is None)}")
    dist = Counter(vd(e) for _, e in judged)
    for k in ("在", "後ろ", "無し"):
        if dist.get(k):
            print(f"    {k:4s} {dist[k]:3d} 話  （{100*dist[k]/len(judged):.0f}%）")
    print()
    for v in VOLS:
        sub = [(r, e) for r, e in judged if r["巻"] == v]
        if not sub:
            continue
        d = Counter(vd(e) for _, e in sub)
        m1 = sum(at1(e) for _, e in sub if at1(e) is not None)
        n1 = sum(1 for _, e in sub if at1(e) is not None)
        mh = sum(e["測"]["持"] for _, e in sub if e["測"])
        print(f"    habits-{v}（{len(sub)} 話）——" +
              "  ".join(f"{k} {d.get(k,0)}" for k in ("在", "後ろ", "無し")) +
              f"   ①設計の字を章が持つ割合＝{100*mh/len(sub):.0f}%"
              f"　②そのうち第一段落にある割合＝{100*m1/n1:.0f}%")
    print()
    print("  ⚠ ①が低い巻は、**設計の字を、本文が落としている**（`03-08`「書き直しの要る」の型）。")
    print("  ⚠ ②が低い巻は、**設計の字は在るが、第一段落より後ろにある**（検品 §4-2 の形）。")
    print()

    print("【②——持っている字の、何割が第一段落にあるか】（六十三話。閾値を外して、率で見る）")
    bands = Counter(min(int((at1(e) or 0) * 10), 9) for _, e in judged)
    for b in sorted(bands):
        lo = "1.0" if b == 9 else f"{b/10:.1f}"
        print(f"    {lo} 以上——{bands[b]:3d} 話  " + "█" * bands[b])
    print()

    print("【「第一文」以外の句——設計が、掴みの代わりに書いているもの】")
    others = [(r, e) for r in rows for e in r["要素"] if not e["第一文"]]
    od = Counter(vd(e) for _, e in others)
    print(f"  句 {len(others)} 件——" +
          "  ".join(f"{k} {od[k]}" for k in ("在", "後ろ", "無し") if od.get(k)))
    print()

    if a.known:
        print("【突き合わせ——人手で「弱い」と出た十三話（`検品` §4-1）】")
        print("  ⚠ **別の欄である。** あの表は、人が行を読んで要素を**選んだ**。"
              "この器は、選ばない。")
        print("  ⚠ ゆえに、食い違って当然である。**食い違いの形を見るために置く。**")
        print()
        print("| 話 | 人が選んだ要素（§4-1） | この器——第一文の判定 | ①設計の字を章が持つ | ②第一段落の割合 |")
        print("|---|---|---|---:|---:|")
        for r in rows:
            if r["話"] not in KNOWN:
                continue
            e = next((x for x in r["要素"] if x["第一文"]), None)
            if not e or not e["測"]:
                print(f"| `{r['話']}` | {KNOWN[r['話']]} | — | — | — |")
                continue
            m = e["測"]
            a1 = f"{100*m['一']:.0f}%" if m["一"] is not None else "—"
            print(f"| `{r['話']}` | {KNOWN[r['話']]} | **{m['判定']}** | "
                  f"{100*m['持']:.0f}% | {a1} |")
        print()

    if a.list or a.off_list:
        for r in rows:
            f = next((e for e in r["要素"] if e["第一文"]), None)
            if a.off_list and f is not None and vd(f) == "在":
                continue
            print(f"■ {r['話']}  第一場面 {r['段落数']} 段落  「第一文」の判定＝{vd(f) if f else '—'}")
            print(f"   本文の第一段落——{r['第一段落']}")
            for e in r["要素"]:
                m = e["測"]
                tag = "第一文" if e["第一文"] else "      "
                if not m:
                    print(f"     {tag} 判定  —    （漢字が無い）  {e['逐語']}")
                    continue
                a1 = f"{100*m['一']:.0f}%" if m["一"] is not None else "—"
                bl = f"{m['最良の段落']}段落目" if m["最良の段落"] is not None else "—"
                print(f"     {tag} 判定 {m['判定']:4s} ①{100*m['持']:>4.0f}% ②{a1:>4s}"
                      f" 最良 {bl:>7s}  {e['逐語']}")
            print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
