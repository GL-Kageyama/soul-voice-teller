#!/usr/bin/env python3
"""五文以上の段落を、話ごとに書き出す（読み取り専用）。

`段落化_著者への申し送り.md` §10 が三例だけ引いていたものを、全件に開くための器。
"""
import glob
import pathlib
import sys

SENT = "。？！?"


def bun(p: str) -> int:
    return sum(p.count(c) for c in SENT)


HEAD = """# 五文以上の段落——全件の一覧（実測）

**⚠ 2026-09-26。** **⚠ この紙は、`段落化_著者への申し送り.md` §10 が「実物」として三例だけ引いていたものを、
全件に開いたものである。** **⚠ 裁定は要らない。著者が読むための一覧である。**

**⚠ 走査した集合**——**四巻六十三話の草稿 63 本**（`habits-01`〜`habits-04`。第二巻第八話を含む）。
**⚠ 数え方**——**いまの草稿の、空行でない・見出しでない物理行を一つの段落とし、
その行の句点・疑問符・感嘆符の数を数えた。** **⚠ 行番号は、そのファイルの物理行番号である**（1 から数え、空行も数える）。
**⚠ 段落化の前の番号ではない**——**段落化で行が減っているゆえ、前の番号とは違う。**

**⚠ 数える器は `段落の形を数える.py` と `段落の文数を数える.py` である。**

| 巻 | 五文以上 | 誰が作ったか |
|---|---:|---|
| 第一巻 | **29** | **⚠ 段落化の台帳が組んだものである**（当てる前は一行一文であった） |
| 第二巻（適用済み十四話） | **28** | **著者が既に書いた段落である** |
| 第二巻第八話（未適用） | **29** | **著者が既に書いた段落である** |
| 第三巻 | **0** | —— |
| 第四巻 | **0** | —— |
| **計** | **86** | **29 ＋ 28 ＋ 29 ＝ 86** |

**⚠ 第一巻の 29 は、承認済みである**（`段落化_著者への申し送り.md` §10）。**⚠ 戻していない。**
**⚠ ゆえに、この一覧のうち裁定の相手になりうるのは、第一巻の 29 件だけである。**
**⚠ 第二巻の 57 件は、著者が最初からそう書いたものであり、第五段の作ったものではない。**

---
"""


def main() -> int:
    root = pathlib.Path(__file__).resolve().parent
    order = [
        ("01", "第一巻", "**⚠ 段落化の台帳が組んだもの——29件。裁定の相手になりうるのは、ここだけである。**"),
        ("02", "第二巻", "**著者が既に書いた段落である。⚠ 第八話（未適用）の 29 件を含む。**"),
        ("03", "第三巻", "**0件。**"),
        ("04", "第四巻", "**0件。**"),
    ]
    out = [HEAD]
    total = 0
    for v, name, note in order:
        out.append(f"## {name}\n\n{note}\n")
        for f in sorted(glob.glob(str(root / f"../../habits-{v}/草稿/draft_*.md"))):
            p = pathlib.Path(f)
            lines = p.read_text(encoding="utf-8").split("\n")
            hits = [
                (i, l.strip())
                for i, l in enumerate(lines, 1)
                if l.strip() and not l.strip().startswith("#") and bun(l.strip()) >= 5
            ]
            if not hits:
                continue
            total += len(hits)
            out.append(f"### {p.name}（{len(hits)}件）\n")
            for i, s in hits:
                out.append(f"- **`:{i}`**（{bun(s)}文）——{s}")
            out.append("")
        out.append("")
    out.append(f"**⚠ 合計 {total} 件である。**\n")
    (root / "段落化_五文以上の段落_全件.md").write_text("\n".join(out), encoding="utf-8")
    print(f"書いた——{total} 件")
    return 0


if __name__ == "__main__":
    sys.exit(main())
