#!/usr/bin/env python3
"""貼り直し——記録に散らばる本文の引用を、凍った本文に合わせて貼り直す。

読点の解放は**行を動かさない**。だから `02-13:309` のような行番号は生きたままである。
貼り直しが要るのは、`02-13:309「僕の、足の、裏が、重い。」` の**引用の本文だけ**である。

そこで、引用の位置を旧の本文（git HEAD）で見つけ、同じ範囲を新しい本文から取り直す。
読点が一字消えれば、引用からも一字消える。

    python3 貼り直し.py            # 調べるだけ（何も書かない）
    python3 貼り直し.py --write    # 貼り直す
    python3 貼り直し.py --path <ファイル> --write

⚠ 引けなかった引用は、書き換えずに「引けない」として報告する。**勝手に直さない。**
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

EX = Path(__file__).resolve().parents[2]      # examples/
REPO = Path(__file__).resolve().parents[3]    # soul-voice-teller/
QUO = re.compile(r"(\d{2})-(\d{2}):(\d+)「([^」\n]*)」")


def draft_path(vol: str, ep: str) -> Path | None:
    d = EX / f"habits-{vol}" / "草稿"
    hits = sorted(d.glob(f"draft_{vol}-{ep}_*.md"))
    return hits[0] if hits else None


def head_lines(p: Path) -> list[str] | None:
    """git HEAD の同じファイルを行の配列で返す。"""
    rel = p.resolve().relative_to(REPO)
    r = subprocess.run(["git", "show", f"HEAD:{rel}"], capture_output=True, cwd=REPO)
    if r.returncode != 0:
        return None
    return r.stdout.decode("utf-8").splitlines()


def new_quote(old_line: str, new_line: str, quote: str) -> str | None:
    """旧の行のうち quote の占める範囲を、新しい行から取り直す。"""
    s = old_line.find(quote)
    if s < 0:
        return None
    e = s + len(quote)
    # 旧の一字ずつを、新しい行のどこへ移ったかに対応づける
    keep = []          # (旧の位置, 新の位置) —— 残った字だけ
    j = 0
    for i, ch in enumerate(old_line):
        if j < len(new_line) and new_line[j] == ch:
            keep.append((i, j))
            j += 1
    inside = [(i, k) for i, k in keep if s <= i < e]
    if not inside:
        return None
    return new_line[inside[0][1]:inside[-1][1] + 1]


def main() -> int:
    ap = argparse.ArgumentParser(description="記録の引用を凍った本文へ貼り直す")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--path", action="append", default=None)
    args = ap.parse_args()

    targets = [Path(p) for p in args.path] if args.path else sorted(
        f for f in EX.rglob("*.md") if "/草稿/" not in str(f))
    targets = [t for t in targets if t.is_file()]

    changed = unchanged = missing = 0
    for t in targets:
        text = t.read_text(encoding="utf-8")
        if "「" not in text:
            continue
        out, pos, hits = [], 0, 0
        for m in QUO.finditer(text):
            vol, ep, ln, quote = m.group(1), m.group(2), int(m.group(3)), m.group(4)
            dp = draft_path(vol, ep)
            if dp is None:
                continue
            old = head_lines(dp)
            if old is None or ln > len(old):
                continue
            new = dp.read_text(encoding="utf-8").splitlines()
            if ln > len(new):
                continue
            fixed = new_quote(old[ln - 1], new[ln - 1], quote)
            if fixed is None:
                missing += 1
                print(f"  ⚠ 引けない  {t}:{vol}-{ep}:{ln}「{quote}」")
                continue
            if fixed == quote:
                unchanged += 1
                continue
            changed += 1
            hits += 1
            out.append(text[pos:m.start(4)])
            out.append(fixed)
            pos = m.end(4)
            print(f"  ✓ {t.name} {vol}-{ep}:{ln}")
            print(f"      旧「{quote}」")
            print(f"      新「{fixed}」")
        if hits:
            out.append(text[pos:])
            if args.write:
                t.write_text("".join(out), encoding="utf-8")

    print()
    print(f"貼り直す引用 {changed}／そのまま {unchanged}／引けない {missing}")
    if not args.write:
        print("（調べただけ。書くには --write）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
