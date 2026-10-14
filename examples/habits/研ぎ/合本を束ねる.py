#!/usr/bin/env python3
"""合本を束ねる——四巻六十三話の草稿から、合本 `habits/草稿/draft.md` を作り直す。

この作品は、草稿を**話ごとのファイル**（`habits-0N/草稿/draft_0N-NN_題.md`）で持ち、
**読める一本**（`habits/草稿/draft.md`）を別に持つ。この器は、前者から後者を作る。

## 束ね方（実測で確定した。推測ではない）

四巻六十三話の草稿を、**巻の順・話の順**に並べ、**空行一つ（`\\n\\n`）でつなぎ、末尾にも空行一つを足す**。

    "\\n\\n".join(六十三ファイル) + "\\n\\n"

**これは、`fc51f48` の時点の草稿から作った文字列が、同じ commit の合本とバイト一致することで確かめた**
（`--from-git fc51f48` で、いまも検算できる）。

⚠ **草稿は、見出し `# 第N話「題」` を自分で持っている。** ゆえにこの器は、題を組み立てない——
**ファイルの中身をそのまま置くだけ**である。題の出どころは一つでなければならない。

## 使い方

    python3 合本を束ねる.py                  # 当てずに、いまの草稿から作って、いまの合本と較べる
    python3 合本を束ねる.py --write          # 合本を作り直す
    python3 合本を束ねる.py --from-git fc51f48   # その時点の草稿から作り、その時点の合本と較べる（書かない）
"""

import argparse
import difflib
import re
import subprocess
import sys
from pathlib import Path

EXAMPLES = Path(__file__).resolve().parents[2]      # …/examples
ROOT = Path(__file__).resolve().parents[3]          # リポジトリの根
BUNDLE = EXAMPLES / "habits" / "草稿" / "draft.md"

DRAFT_RE = re.compile(r"^habits-0[1-4]/草稿/draft_0[1-4]-\d\d_.+\.md$")
EXPECT_FILES = 63
EXPECT_TALES = 63
EXPECT_RULES = 126      # 一話に二つ（`＊`）


def drafts_from_disk() -> tuple[list[Path], list[str]]:
    paths = sorted(p for p in EXAMPLES.glob("habits-0[1-4]/草稿/draft_0[1-4]-*.md")
                   if DRAFT_RE.match(str(p.relative_to(EXAMPLES))))
    texts = []
    for p in paths:
        t = p.read_text(encoding="utf-8")
        if not t.strip():
            sys.exit(f"⛔ 草稿が空である: {p}（空の検査は通さない）")
        texts.append(t)
    return paths, texts


def drafts_from_git(rev: str) -> tuple[list[Path], list[str]]:
    raw = subprocess.run(["git", "-C", str(ROOT), "ls-tree", "-r", "-z", "--name-only", rev],
                         capture_output=True)
    if raw.returncode != 0:
        sys.exit(f"⛔ commit を引けない: {rev}\n{raw.stderr.decode(encoding='utf-8', errors='replace')}")
    names = sorted(n for n in raw.stdout.decode("utf-8").split("\0")
                   if DRAFT_RE.match(n.replace("examples/", "", 1)))
    texts = []
    paths = []
    for n in names:
        blob = subprocess.run(["git", "-C", str(ROOT), "show", f"{rev}:{n}"], capture_output=True)
        t = blob.stdout.decode("utf-8")
        if not t.strip():
            sys.exit(f"⛔ その時点の草稿が空である: {n}")
        paths.append(Path(n))
        texts.append(t)
    return paths, texts


def count_headings(text: str) -> int:
    return sum(1 for l in text.split("\n") if l.startswith("# "))


def count_rules(text: str) -> int:
    return sum(1 for l in text.split("\n") if l.strip() == "＊")


def main() -> int:
    ap = argparse.ArgumentParser(description="四巻六十三話の草稿から合本を作り直す")
    ap.add_argument("--write", action="store_true", help="合本を作り直す")
    ap.add_argument("--from-git", metavar="REV", help="その commit の草稿から作る（書かない）")
    args = ap.parse_args()

    if args.from_git:
        paths, texts = drafts_from_git(args.from_git)
        old = subprocess.run(["git", "-C", str(ROOT), "show",
                              f"{args.from_git}:{BUNDLE.relative_to(ROOT)}"],
                             capture_output=True).stdout.decode("utf-8")
        label = f"{args.from_git} の時点"
    else:
        paths, texts = drafts_from_disk()
        old = BUNDLE.read_text(encoding="utf-8") if BUNDLE.exists() else ""
        label = "いま"

    # ⚠ 束ねる前に、束ねる相手が揃っていることを確かめる（足りないまま束ねると、短い合本ができる）。
    if len(texts) != EXPECT_FILES:
        sys.exit(f"⛔ 草稿が {len(texts)} 本しか無い（{EXPECT_FILES} 本でなければならない）"
                 "——束ねない（空の検査は通さない）")
    if not old:
        sys.exit(f"⛔ いまの合本が無い、または空である: {BUNDLE}")

    new = "\n\n".join(texts) + "\n\n"

    # 束ねたものの形を数える（本数のほかに、見出しと区切りを数える）。
    tales, rules = count_headings(new), count_rules(new)
    ok_shape = (tales == EXPECT_TALES and rules == EXPECT_RULES)

    print(f"■ 草稿 {len(texts)} 本（{paths[0].name} … {paths[-1].name}）")
    print(f"■ 束ねた合本——{len(new):,} 字／{new.count(chr(10)):,} 行／"
          f"見出し {tales}／`＊` {rules}")
    if not ok_shape:
        print(f"⚠ 形が違う——見出しは {EXPECT_TALES}、`＊` は {EXPECT_RULES} のはずである")

    if args.from_git:
        same = new == old
        print(f"■ {label}の合本と較べる——{'一致する' if same else '一致しない'}"
              f"（作った {len(new):,} 字／あった {len(old):,} 字）")
        if not same:
            n = min(len(new), len(old))
            i = next((k for k in range(n) if new[k] != old[k]), n)
            print(f"   最初の食い違い＝文字 {i}")
            print(f"     作った: {new[max(0, i - 30):i + 30]!r}")
            print(f"     あった: {old[max(0, i - 30):i + 30]!r}")
        return 0 if same else 1

    if new == old:
        print(f"■ いまの合本と一致する——作り直す必要が無い（{BUNDLE.relative_to(ROOT)}）")
        return 0

    # ⚠ 数を、`difflib` の差分行数で数えてはならない。
    #    行数が同じでも、差分は hunk を並べ直すゆえ、**変えていない行まで − と ＋ の両方に数える**
    #    （実測——第四巻まで当て終えた時点で、位置で較べれば 481 行、差分の行数は 16,799 行と出た）。
    #    ゆえに、行数が同じなら**位置で**数える。違うときだけ差分を数え、その旨を書く。
    a, b = old.split("\n"), new.split("\n")
    if len(a) == len(b):
        changed = [i for i in range(len(a)) if a[i] != b[i]]
        print(f"■ いまの合本と違う——{len(changed):,} 行 ／ {len(a):,} 行"
              f"（{len(changed) / len(a) * 100:.1f}%。行数は同じゆえ、位置で較べた）")
        for i in changed[:20]:
            print(f"   {i + 1}行目  − {a[i]}")
            print(f"          ＋ {b[i]}")
        if len(changed) > 20:
            print(f"   …（のこり {len(changed) - 20} 行）")
    else:
        diff = list(difflib.unified_diff(a, b, fromfile="いまの合本",
                                         tofile="束ね直した合本", lineterm="", n=0))
        removed = sum(1 for l in diff if l.startswith("-") and not l.startswith("---"))
        added = sum(1 for l in diff if l.startswith("+") and not l.startswith("+++"))
        print(f"■ いまの合本と違う——行数が違う（{len(a):,} → {len(b):,} 行）"
              f"ゆえ、差分で数えた——− {removed:,} 行 ／ ＋ {added:,} 行")
        for l in diff[:40]:
            print("   " + l)
        if len(diff) > 40:
            print(f"   …（のこり {len(diff) - 40} 行）")

    if not args.write:
        print()
        print("〔確かめのみ〕作り直すには --write を付ける。")
        return 0

    if not ok_shape:
        print("⛔ 形が違うゆえ、書かない。")
        return 1
    BUNDLE.write_text(new, encoding="utf-8")
    print()
    print(f"✅ 合本を作り直した——{BUNDLE.relative_to(ROOT)}（{len(new):,} 字／{tales} 話／`＊` {rules}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
