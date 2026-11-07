#!/usr/bin/env python3
"""検める——読点の解放が、読点だけを削ったかを検める。

この段で本文にしてよいことは、**読点を削ることだけ**である。語を足すことも、
語を替えることも、行を増やすことも、行を減らすことも、ここでは許されない。

そこで、前と後を一行ずつ突き合わせ、変わった行については
    （新の読点を全部取ったもの）== （旧の読点を全部取ったもの）
が成り立つこと、および行数が変わっていないことを確かめる。

使い方:
    python3 検める.py <草稿ディレクトリ>          # git の HEAD と比べる
    python3 検める.py <草稿ディレクトリ> --against <旧ファイル群のディレクトリ>
"""

import argparse
import subprocess
import sys
from pathlib import Path


def repo_root() -> Path:
    """リポジトリの根。cwd ではない——cwd で測ると、外から当てたときに全部を飛ばす。"""
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True)
    return Path(r.stdout.decode("utf-8").strip())


def head_version(path: Path) -> str | None:
    """git の HEAD にある同じパスを読む。無ければ None。"""
    try:
        rel = path.resolve().relative_to(repo_root())
    except ValueError:
        return None
    r = subprocess.run(["git", "show", f"HEAD:{rel}"], capture_output=True, cwd=repo_root())
    return r.stdout.decode("utf-8") if r.returncode == 0 else None


def compare(old: str, new: str) -> list[str]:
    """読点以外の違いを、人の読める形で返す。空なら合格。"""
    bad = []
    a, b = old.splitlines(), new.splitlines()
    if len(a) != len(b):
        bad.append(f"行数が違う: {len(a)} → {len(b)}")
    for i, (x, y) in enumerate(zip(a, b)):
        if x == y:
            continue
        if y.replace("、", "") != x.replace("、", ""):
            bad.append(f"{i + 1}行目——読点以外が違う\n    旧: {x}\n    新: {y}")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser(description="読点の解放が読点だけを削ったかを検める")
    ap.add_argument("path")
    args = ap.parse_args()

    d = Path(args.path)
    files = sorted(f for f in d.glob("*.md") if f.name.startswith("draft_"))
    if not files:
        print(f"草稿が見つからない: {d}", file=sys.stderr)
        return 2

    ng = 0
    released = 0
    before = after = 0
    skipped = []
    for f in files:
        old = head_version(f)
        if old is None:
            skipped.append(f.name)
            continue
        new = f.read_text(encoding="utf-8")
        bad = compare(old, new)
        o, n = old.count("、"), new.count("、")
        before += o
        after += n
        if o != n:
            released += 1
        if bad:
            ng += 1
            print(f"■ {f.name}")
            for b in bad:
                print("   " + b)
        elif o != n:
            print(f"✅ {f.name}  読点 {o} → {n}")

    print()
    print(f"触ったファイル {released}/{len(files)}　読点 計 {before} → {after}")
    if skipped:
        # ⚠ 飛ばしたファイルが在るなら、✅ を出してはならない。測っていないものは、
        #   通ったのではない。かつて cwd を根として測り、六十三本すべてを黙って
        #   飛ばしたうえで「✅ 読点だけが削られている」と出した（2026-09-26）。
        print(f"⛔ HEAD に無く、測れなかったファイル {len(skipped)} 本——検査は成立していない")
        for name in skipped:
            print(f"   {name}")
        return 1
    if ng:
        print(f"⛔ 読点以外が動いているファイル {ng} 本——この段では許されない")
        return 1
    print("✅ 読点だけが削られている")
    return 0


if __name__ == "__main__":
    sys.exit(main())
