#!/usr/bin/env python3
"""変換稿の検算器——『ハビッツ！！！』日常ドタバタコメディ版

これは検査であって、評価ではない。出すのは数だけである。

    python3 検算.py <この稿.md> --old <原本.md>
    python3 検算.py <この稿.md> --old <原本.md> --json

出すもの（作法 §3 の七つに対応）:
    ① 禁則            → check.py を別に当てる（この器は数えない）
    ② 段落の文数       → 五文以上の段落の数
    ③ 内面の欄         → 数えない（人が読む。場面表 §4）
    ④ 一拍に人が入っていないこと → 数えない（人が読む）
    ⑤ 落とした文       → 句点単位の異なり（この稿に無い文の数）
    ⑥ 註の比率         → である末（分母つき）・一文の長さ
    ⑦ 声の帰属         → 鉤括弧の数と、その行（帰属は人が読む）

⚠ 数え方は examples/habits/検査/check.py に合わせてある
   （本文行＝空行・見出し・`＊` を除いた行。字数＝本文行の非空白文字）。
⚠ である末と一文は「地の文の文」だけを数える（鉤括弧で始まる行＝台詞は数えない）。
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECK_PY = HERE.parent.parent / "habits" / "検査" / "check.py"

TITLE_RE = re.compile(r"^#\s")
SCENE_RE = re.compile(r"^(?:＊|\*{1,3}|—{2,}|-{3,})$")
QUOTE_RE = re.compile(r"^[「『]")
SENT_END = re.compile(r"(?<=[。？！])(?![」』])")
PERIOD = "。"


# ------------------------------------------------------------------ 読み込み

def load(path):
    return Path(path).read_text(encoding="utf-8").splitlines()


def prose_lines(lines):
    """本文の行だけを (行番号, 文) で返す。題名行・`＊`・空行を除く。"""
    out = []
    for i, line in enumerate(lines, start=1):
        s = line.strip()
        if not s or TITLE_RE.match(s) or SCENE_RE.match(s):
            continue
        out.append((i, s))
    return out


def count_chars(lines):
    total = 0
    for _, s in prose_lines(lines):
        for ch in s:
            if not ch.isspace() and unicodedata.category(ch) != "Cf":
                total += 1
    return total


def scenes(lines):
    """[(節番号, [行番号...])]"""
    result = [[1, []]]
    for i, line in enumerate(lines, start=1):
        s = line.strip()
        if SCENE_RE.match(s):
            result.append([len(result) + 1, []])
            continue
        if s and not TITLE_RE.match(s):
            result[-1][1].append(i)
    return [(n, nums) for n, nums in result if nums]


def scene_chars(lines, nums):
    body = [s for _, s in prose_lines(lines) if _ in nums]  # noqa: F841
    total = 0
    want = set(nums)
    for i, s in prose_lines(lines):
        if i not in want:
            continue
        for ch in s:
            if not ch.isspace() and unicodedata.category(ch) != "Cf":
                total += 1
    return total


# ------------------------------------------------------------------ 数える

def narration_sentences(lines):
    """地の文の文（句点で切る）を (行番号, 文) で返す。台詞の行は丸ごと除く。"""
    out = []
    for i, s in prose_lines(lines):
        if QUOTE_RE.match(s):
            continue
        for part in SENT_END.split(s):
            part = part.strip()
            if part:
                out.append((i, part))
    return out


def paragraphs(lines):
    """段落＝本文行一本。その行の文の数を返す。"""
    return [len([p for p in SENT_END.split(s) if p.strip()])
            for _, s in prose_lines(lines)]


def quotes(lines):
    out = []
    for i, s in prose_lines(lines):
        if QUOTE_RE.match(s):
            out.append((i, s))
    return out


def sentences_of(lines):
    """本文の文を、句点で切って返す（地の文も台詞も）。⑤の突き合わせに使う。"""
    out = []
    for i, s in prose_lines(lines):
        for part in SENT_END.split(s):
            part = part.strip()
            if part:
                out.append(part)
    return out


def summarize(path):
    lines = load(path)
    pr = prose_lines(lines)
    sc = scenes(lines)
    nar = narration_sentences(lines)
    n_dewa = sum(1 for _, s in nar if s.endswith("である" + PERIOD) or s == "である")
    n_chars = sum(len(s) for _, s in nar)
    para = paragraphs(lines)
    q = quotes(lines)
    talk = [1 for _, s in pr if QUOTE_RE.match(s)]

    return {
        "path": str(path),
        "行": len(lines),
        "本文行": len(pr),
        "字数": count_chars(lines),
        "節": [{"節": n, "行": len(nums), "字数": scene_chars(lines, nums)}
               for n, nums in sc],
        "会話行": len(talk),
        "鉤括弧": len(q),
        "鉤括弧の行": [{"行": i, "文": s[:40]} for i, s in q],
        "段落": {
            "数": len(para),
            "五文以上": sum(1 for n in para if n >= 5),
            "最長": max(para) if para else 0,
            "分布": {str(k): para.count(k) for k in sorted(set(para))},
            "文/行": round(sum(para) / len(para), 2) if para else 0,
        },
        "地の文": {
            "文数": len(nar),
            "である末": n_dewa,
            "である末の割合": round(n_dewa / len(nar) * 100, 1) if nar else 0,
            # ⚠ 工房の慣例——「一文 9.7字」は、句点を含んだ生の平均である
            #    （`habits/進捗表.md` §5 と同じ数え方。+1 しない）。
            "一文の長さ_句点含む": round(n_chars / len(nar), 3) if nar else 0,
        },
    }


def diff_sentences(old_path, new_path):
    """⑤ 落とした文——句点単位の異なり。"""
    old = [s for _, s in narration_sentences(load(old_path))]
    new = set(sentences_of(load(new_path)))
    missing = [s for s in old if s not in new]
    return {"原本の文数": len(old), "この稿に無い文": len(missing),
            "文": missing[:400]}


def report(new_path, old_path, as_json):
    new = summarize(new_path)
    old = summarize(old_path) if old_path else None
    d = diff_sentences(old_path, new_path) if old_path else None

    if as_json:
        print(json.dumps({"この稿": new, "原本": old, "落とした文": d},
                         ensure_ascii=False, indent=2))
        return

    def line(row, o, n):
        ov = old[row] if old else "-"
        print(f"  {row:<16} 原本 {str(ov):>10}   この稿 {str(n):>10}")

    print(f"■ {Path(new_path).name}")
    print(f"  {'行':<16} {'':>10}   {'':>10}   この稿 {new['行']}")
    print(f"  {'本文行':<15} 原本 {old['本文行'] if old else '-':>10}   この稿 {new['本文行']:>10}")
    print(f"  {'字数':<16} 原本 {old['字数'] if old else '-':>10}   この稿 {new['字数']:>10}")
    for k, v in enumerate(new["節"]):
        ov = old["節"][k]["字数"] if old and k < len(old["節"]) else "-"
        print(f"    第{v['節']}節{'':<10} 原本 {str(ov):>10}   この稿 {v['字数']:>10}"
              f"   （{v['行']}行）")
    line("会話行", None, new["会話行"])
    line("鉤括弧", None, new["鉤括弧"])
    print(f"  {'段落の数':<15} 原本 {old['段落']['数'] if old else '-':>10}   この稿 {new['段落']['数']:>10}")
    print(f"  {'五文以上の段落':<13} 原本 {old['段落']['五文以上'] if old else '-':>10}   この稿 {new['段落']['五文以上']:>10}")
    print(f"  {'最長の段落(文)':<13} 原本 {old['段落']['最長'] if old else '-':>10}   この稿 {new['段落']['最長']:>10}")
    print(f"  {'文/行':<16} 原本 {old['段落']['文/行'] if old else '-':>10}   この稿 {new['段落']['文/行']:>10}")
    print(f"  {'段落の文数分布':<12} 原本 {old['段落']['分布'] if old else '-'}")
    print(f"  {'':<16} この稿 {new['段落']['分布']}")
    print(f"  {'地の文の文数':<13} 原本 {old['地の文']['文数'] if old else '-':>10}   この稿 {new['地の文']['文数']:>10}")
    print(f"  {'である末の割合':<13} 原本 {str(old['地の文']['である末の割合']) + '%' if old else '-':>10}"
          f"   この稿 {str(new['地の文']['である末の割合']) + '%':>10}"
          f"   （{new['地の文']['である末']}/{new['地の文']['文数']}文）")
    print(f"  {'一文の長さ(句点込)':<11} 原本 {old['地の文']['一文の長さ_句点含む'] if old else '-':>10}"
          f"   この稿 {new['地の文']['一文の長さ_句点含む']:>10}")
    if d:
        print(f"  {'落とした文(異なり)':<11} 原本 {d['原本の文数']:>10}   この稿に無い {d['この稿に無い文']:>10}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("new")
    ap.add_argument("--old", default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--missing", action="store_true", help="落とした文を印字する")
    a = ap.parse_args()
    report(a.new, a.old, a.json)
    if a.missing and a.old:
        d = diff_sentences(a.old, a.new)
        for s in d["文"]:
            print("  ✂", s)


if __name__ == "__main__":
    main()
