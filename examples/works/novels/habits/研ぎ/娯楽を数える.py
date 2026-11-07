#!/usr/bin/env python3
"""娯楽を数える——四巻六十三話の「面白さの側」を、機械で見える分だけ測る（読み取り専用）。

⚠ この器は、判断をしない。**在る／無いと、どこに在るか**だけを出す。
   「面白い／面白くない」は出さない——それは人が読む（`第七段階_第四段_娯楽台帳.md` の読者の欄）。

⚠ `段落の形を数える.py` を置き換えない。**あれが既に出しているもの（節・段落・文・入口・話末）は、
   同じ物差しで出し直す。**この器が足すのは、四つである——

   1. **入口の型**——第一文の形を分類する（存在文／所在文／状態文／会話／その他）。
      ⚠ 設計は入口を「多くは楽しい・心地よい」と定めている（`構想/design.md:189`）。
        ゆえに「入口が物の目録である話が何話あるか」は、設計との差の実測である。
   2. **章末の形**——最終文の形を分類する（`whole-work-review` の反復句の規則のため）。
   3. **会話の有無**——その話に `「` で始まる行が何行あるか（設計は声を許していない。著者の裁定で開いた）。
   4. **三話以上に現れる行**——**検査器はこれを見ない**（`check.py` の ⛔ は、ちょうど二話に一致する
      ときだけ鳴る。三話以上は基底語として黙る）。ゆえに、別に数える。

⚠ 数え方は `検査/check.py` と同じ物差しである——本文行は題名・見出し・`＊`・空行を除いた行、
   字数は非空白文字（Cf を除く）。**ゆえに、検査器の数と突き合わせられる。**

使い方:
    python3 娯楽を数える.py                       # 四巻六十三話の要約
    python3 娯楽を数える.py --tsv                 # 一節一行の台帳を、標準出力へ
    python3 娯楽を数える.py --tsv > 台帳.tsv
    python3 娯楽を数える.py --min 8 --chapters 3   # 反復句の閾値を変える（既定 12・2）
"""

import argparse
import glob
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent          # examples/habits/研ぎ
HABITS = HERE.parent                            # examples/habits
EXAMPLES = HABITS.parent                        # examples

RULE_RE = re.compile(r"^＊$")                    # 場面の区切り（全角アスタリスク）——著者裁定 2026-10-13
TITLE_RE = re.compile(r"^#\s+第\d+話")
SENT = "。？！?"

# ⚠ 入口の分類——**二分割だけである。** 片側は、取りこぼしの無い形に限る。
#   ⚠ 機械で「動作」を当てると必ず壊れる——この作品は現在形ゆえ、動作も「〜る。」で終わり、
#     存在の「〜がある。」と同じ語尾になる。**ゆえに、堅い側（物・状態の報告）だけを数え、
#     残りは実物を出す**（--list）。**網の粗さを、数に化けさせない。**
OPENING_TYPES = [
    ("会話", re.compile(r"^[「『]")),
    # 「〜がある／いる／ない／ている／てある／である／にある」で終わる文＝物か状態の報告。
    ("物・状態の報告", re.compile(r"(ある|いる|ない|無い|ている|てある|である|ままだ|ままである)。$")),
    ("その他", re.compile(r".")),
]

# ⚠ 章末の形——`whole-work-review`「反復句が変化しなくなったら、それはループである」の物差し。
#   ⚠ **「まだ〜」を先に当てる**（保留の印として、いちばん強い）。
#   ⚠ 状態と動作は、語尾では分けきれない。**実物を全部出す**（--list）。
ENDING_TYPES = [
    ("会話", re.compile(r"[」』]$")),
    ("まだ〜（保留）", re.compile(r"まだ")),
    ("存在・所在", re.compile(r"(が|は)(ある|無い|ない)。$|に(ある|いる|無い)。$")),
    ("状態（である・ている・まま）", re.compile(r"(である|ている|てある|ままである|ままだ)。$")),
    ("状態（形容詞）", re.compile(r"[いか]い。$|[白黒赤青]い。$")),
    ("否定", re.compile(r"ない。$|無い。$")),
    ("動作", re.compile(r"た。$")),
]


def classify(patterns, s: str) -> str:
    for name, pat in patterns:
        if pat.search(s):
            return name
    return "その他"


def prose_lines(lines):
    """本文の行だけを (行番号, 文) で返す。題名・見出し・`＊`・空行を除く（check.py と同じ）。"""
    out = []
    for i, line in enumerate(lines, start=1):
        s = line.strip()
        if not s or s.startswith("#") or RULE_RE.match(s):
            continue
        out.append((i, s))
    return out


def count_chars(s: str) -> int:
    return sum(1 for ch in s if not ch.isspace() and unicodedata.category(ch) != "Cf")


def bun(s: str) -> int:
    return sum(s.count(c) for c in SENT)


def scenes(lines):
    """[(節番号, [(行番号, 文), ...])]。区切りは `＊`、最初の区切りより前が第1節（check.py と同じ）。"""
    result = [[1, []]]
    for i, line in enumerate(lines, start=1):
        s = line.strip()
        if RULE_RE.match(s):
            result.append([len(result) + 1, []])
            continue
        if s and not s.startswith("#") and not TITLE_RE.match(s):
            result[-1][1].append((i, s))
    return [(n, xs) for n, xs in result if xs]


def first_sentence(para: str) -> str:
    """段落の第一文。句点・疑問符・感嘆符のいずれかで切る（無ければ全体）。"""
    m = re.search(r"[。？！]", para)
    return para[: m.end()] if m else para


def last_sentence(para: str) -> str:
    m = re.findall(r"[^。？！]*[。？！]", para)
    if m:
        tail = para[sum(len(x) for x in m):]
        # ⚠ 末尾に句点の無い断片が残るなら、それが最後の一文である
        return (tail if tail else m[-1]).strip()
    return para.strip()


def draft_files():
    files = []
    for v in ("01", "02", "03", "04"):
        files.extend(sorted(glob.glob(str(EXAMPLES / f"habits-{v}" / "草稿" / "draft_*.md"))))
    return files


def main() -> int:
    ap = argparse.ArgumentParser(description="四巻六十三話の娯楽の側を、機械で見える分だけ測る")
    ap.add_argument("--tsv", action="store_true", help="一節一行の台帳を標準出力へ")
    ap.add_argument("--list", action="store_true", help="六十三話の入口と章末の実物を出す")
    ap.add_argument("--min", type=int, default=12, help="反復句の最低字数（既定 12）")
    ap.add_argument("--chapters", type=int, default=2, help="反復句を報告する最小話数（既定 2＝検査器と同じ）")
    a = ap.parse_args()

    files = draft_files()
    if not files:
        sys.exit("⛔ 草稿が一本も無い（空の検査は通さない）")

    rows = []                 # 一節一行
    chapters = []             # 話ごとの要約
    seen = {}                 # 行 -> set(話)

    for f in files:
        p = Path(f)
        vol = p.parent.parent.name.replace("habits-", "")
        text = p.read_text(encoding="utf-8")
        if not text.strip():
            sys.exit(f"⛔ 空の草稿がある——{p}")
        lines = text.split("\n")
        sc = scenes(lines)
        prose = prose_lines(lines)
        dialogue = [(n, s) for n, s in prose if s.startswith("「") or s.startswith("『")]
        n_chars = sum(count_chars(s) for _, s in prose)

        # ⚠ `draft_01-01_消さなかった一行.md` → `01-01`。**先頭の `draft` を落とす**——
        #   `split("_")[0]` は `draft` であり、話の名ではない（一度これを踏んだ）。
        key = p.name.split("_")[1]                            # 01-01
        for num, xs in sc:
            body = "".join(s for _, s in xs)
            rows.append({
                "話": key, "節": num,
                "行": f"{xs[0][0]}-{xs[-1][0]}",
                "字数": sum(count_chars(s) for _, s in xs),
                "段落": len(xs), "文": sum(bun(s) for _, s in xs),
                "会話": sum(1 for _, s in xs if s.startswith(("「", "『"))),
                "入口": xs[0][1],
                "場面末": xs[-1][1],
            })
        for _, s in prose:
            if len(s) >= a.min:
                seen.setdefault(s, set()).add(key)
        chapters.append({
            "話": key, "節数": len(sc),
            "本文行": len(prose), "字数": n_chars,
            "会話行": len(dialogue),
            "入口第一文": first_sentence(prose[0][1]) if prose else "",
            "章末": last_sentence(prose[-1][1]) if prose else "",
        })

    if a.tsv:
        print("話\t節\t行\t字数\t段落\t文\t会話\t入口\t場面末")
        for r in rows:
            print("\t".join(str(r[k]) for k in
                            ("話", "節", "行", "字数", "段落", "文", "会話", "入口", "場面末")))
        return 0

    # ---------------------------------------------------------------- 要約
    n_files = len(files)
    all_prose = sum(c["本文行"] for c in chapters)
    all_dial = sum(c["会話行"] for c in chapters)
    zero_dial = [c["話"] for c in chapters if c["会話行"] == 0]

    print("走査した集合——%d 巻 %d ファイル（本文 %d 行・%s 字）"
          % (4, n_files, all_prose, f"{sum(c['字数'] for c in chapters):,}"))
    print("数え方——本文行は題名・見出し・`＊`・空行を除いた行。字数は非空白文字（Cf を除く）。"
          "検査器 check.py と同じ物差しである。")
    print()

    print("【会話】")
    print(f"  会話の行——{all_dial} / {all_prose} 行（{100*all_dial/all_prose:.1f}%）")
    print(f"  会話が一行も無い話——{len(zero_dial)} / {n_files} 話")
    if zero_dial:
        print(f"    {', '.join(zero_dial)}")
    print()

    print("【入口——第一文の型】（設計は「多くは楽しい・心地よい」と定めている。design.md:189）")
    print("  ⚠ 二分割である。動作は語尾で状態と分けられないゆえ、**堅い側だけを数える。**")
    ent = [classify(OPENING_TYPES, c["入口第一文"]) for c in chapters]
    for name in [n for n, _ in OPENING_TYPES]:
        n = ent.count(name)
        if n:
            print(f"    {name:14s} {n:3d} 話")
    print("    ⚠ 「その他」の実物——動作で始まる話の候補である")
    for c in chapters:
        if classify(OPENING_TYPES, c["入口第一文"]) == "その他":
            print(f"      {c['話']}  {c['入口第一文']}")
    print()

    print("【章末——最終文の型】（whole-work-review「反復句が変化しなくなったら、それはループである」）")
    print("  ⚠ 「まだ〜」を先に当てる——ゆえに「まだある。」は、存在・所在 ではなく まだ〜 に入る。")
    edn = [classify(ENDING_TYPES, c["章末"]) for c in chapters]
    for name in [n for n, _ in ENDING_TYPES] + ["その他"]:
        n = edn.count(name)
        if n:
            print(f"    {name:24s} {n:3d} 話")
    print()

    if a.list:
        print("【実物——入口の第一文と、章末の最終文】（六十三話）")
        for c in chapters:
            print(f"  {c['話']}  入口[{classify(OPENING_TYPES, c['入口第一文'])}] {c['入口第一文']}")
            print(f"         章末[{classify(ENDING_TYPES, c['章末'])}] {c['章末']}")
        print()

    # ⚠ 見出しに閾値を書く。**「三話以上」と固定で書くと、--chapters 2 のとき嘘になる**
    #   （出した数が、名乗った数え方と食い違う）。
    print(f"【{a.chapters} 話以上に現れる行】"
          f"（検査器は見ない——⛔ は、ちょうど二話に一致するときだけ鳴る）")
    print(f"  閾値——{a.min} 字以上、{a.chapters} 話以上に逐語で現れる行")
    multi = sorted(((len(v), k) for k, v in seen.items() if len(v) >= a.chapters), reverse=True)
    print(f"  該当——{len(multi)} 種")
    for n, s in multi[:25]:
        print(f"    {n:2d} 話  {s}")
    if len(multi) > 25:
        print(f"    …以下 {len(multi)-25} 種")
    print()

    print("【節数】")
    dist = {}
    for c in chapters:
        dist[c["節数"]] = dist.get(c["節数"], 0) + 1
    for k in sorted(dist):
        print(f"    {k} 節——{dist[k]} 話")
    return 0


if __name__ == "__main__":
    sys.exit(main())
