#!/usr/bin/env python3
"""読点の解放——連語の読点切断を解く（第一稿。判断は人が上から重ねる）

規則の正文は examples/habits/構想/design.md:81 と persona.md である。
  読点は並列を一息で流し、要の一打（反転・定型句）だけに刻む。連語を原子に分解しない。

この器がやるのは、いちばん確からしい削除だけである:
  読点の直前が、助詞（の・が・を・に・は・も）で終わっているもの。
ただし、その手前が従属節・形式名詞の語尾であるものは残す（〜から、〜ように、〜ために…）。

⚠ これは検査ではない。評価もしない。出すのは「削った結果」だけである。
⚠ 残る判断——連用中止（〜て、／〜った、）の読点、会話のためらい、要の一打——は、
   人が読んで上から重ねる。この器は、その手前までしか行かない。

使い方:
    python3 読点の解放.py <draft.md>            # 標準出力へ
    python3 読点の解放.py <draft.md> --write    # 同じ場所へ上書き
    python3 読点の解放.py <草稿ディレクトリ> --write
"""

import argparse
import sys
from pathlib import Path

# 読点の直前がこの語尾で終わっていれば、残す（従属節・形式名詞・並列の印）
PROTECT_TAIL = [
    "ので", "のに", "けど", "けれど", "ばあい",
    "とおり", "はず", "わけ", "つもり", "ほう", "とき", "あいだ", "うち", "あと",
    "まえ", "ため", "よう", "こと", "もの", "ば", "たら", "なら", "ても", "でも",
    "ながら", "つつ", "おり", "たび",
]
# 後置詞——手前が和語の用言なら従属節（終わるまで、待つ／するために、）で残し、
# 漢語の名詞か「の」なら語を割っている（窓から、入る／束のあいだに、隙間）ので削る
RANGE_PARTICLES = ["から", "まで", "ほど", "くらい", "で", "へ",
                   "あいだに", "うちに", "まえに", "あとに", "ために", "ように", "ことに"]
# 削る対象——読点の直前がこの一字で終わっているもの（助詞）
DROP_TAIL = "のがをにはも"
# 連体形の語尾——この直後の読点は、修飾語と被修飾語を割っている（〜い、空いている、幅）
RENTAI_TAIL = "いるたなのく"  # 「き」は除く（〜とき、は従属節）
# 読点の直後がこの語で始まっていれば、形式名詞・補助用言であり、割ってはいけない
DROP_HEAD = ["まま", "ところ", "だけ", "ぶん", "もの", "こと", "ほう", "うち",
             "あいだ", "とおり", "はず", "わけ", "つもり", "という",
             "ごし", "ごと", "ぶり", "がけ", "どおり"]  # 複合語のうしろ半分（ガラス、ごし）
# 副詞——この直後の読点は、副詞と用言を割っている（まだ、鳴らない）
ADVERBS = ["まだ", "少し", "もう", "すぐ", "一度", "また", "やがて", "ちょうど",
           "ほとんど", "しばらく", "ずっと", "やっと", "ふと", "いちばん",
           "同じ", "同じく", "別", "毎朝", "今年", "いつも", "それぞれ", "たいてい",
           "ところどころ", "ときどき", "あちこち", "一年"]
# 副助詞・形式名詞——この語で読点の手前が終わっていれば、語を割っている
DROP_TAIL_WORD = ["だけ", "ばかり", "ところへ", "ところに", "ほうへ", "ほうに"]
# 助数詞——この直後の読点は、数と助数詞を割っている（四枚、ある）
COUNTERS = "枚つ本個人回度件行字歩段列名冊台杯軒階歳番位割倍円匹羽"


def release(line: str) -> str:
    """一行の読点を解放する。"""
    out = []
    for i, ch in enumerate(line):
        if ch != "、":
            out.append(ch)
            continue
        head, tail = line[:i], line[i + 1:]
        if any(head.endswith(t) for t in PROTECT_TAIL):
            out.append(ch)
            continue
        for p in RANGE_PARTICLES:
            if head.endswith(p) and len(head) > len(p):
                c = head[-len(p) - 1]
                if "一" <= c <= "鿿" or c in ("の", "く"):
                    head = ""  # 語の切断。削る
                break
        if not head:
            continue
        if head and (head[-1] in DROP_TAIL or head[-1] in COUNTERS):
            continue  # 削る
        if any(head.endswith(w) for w in DROP_TAIL_WORD):
            continue  # 削る（副助詞・形式名詞を割っている）
        if head and head[-1] in RENTAI_TAIL:
            continue  # 削る（連体形と被修飾語を割っている）
        if any(tail.startswith(h) for h in DROP_HEAD):
            continue  # 削る（形式名詞を割っている）
        if any(head.endswith(a) for a in ADVERBS):
            continue  # 削る（副詞を割っている）
        out.append(ch)
    return "".join(out)


def process(path: Path, write: bool) -> str:
    src = path.read_text(encoding="utf-8")
    new = "".join(
        ln if (not ln.strip() or ln.lstrip().startswith("#")) else release(ln)
        for ln in src.splitlines(keepends=True)
    )
    if write:
        path.write_text(new, encoding="utf-8")
    return new


def main():
    ap = argparse.ArgumentParser(description="連語の読点切断を解く（第一稿）")
    ap.add_argument("path")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    p = Path(args.path)
    targets = sorted(p.glob("*.md")) if p.is_dir() else [p]
    for t in targets:
        new = process(t, args.write)
        if not args.write:
            print(new, end="")
    if args.write:
        for t in targets:
            print(f"書いた: {t}", file=sys.stderr)


if __name__ == "__main__":
    main()
