#!/usr/bin/env python3
"""前後を較べる——検査器の⛔が、この段で生じたのか、前から在ったのかを数える。

git HEAD の草稿を `examples/.head-NN/` へ出し、いまと同じ検査器を当てて突き合わせる。
置き場は検査のあとで消す。

    python3 前後を較べる.py
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
EX = REPO / "examples"
CHECK = EX / "habits" / "検査" / "check.py"


def run_check(d: Path) -> tuple[int, list[str]]:
    r = subprocess.run([sys.executable, str(CHECK), str(d)], capture_output=True, cwd=REPO)
    out = (r.stdout + r.stderr).decode("utf-8")
    bad = [l.strip() for l in out.splitlines() if "⛔" in l or "❌" in l]
    return len(bad), bad


def head_out(v: str) -> Path:
    rel = f"examples/habits-{v}/草稿"
    names = subprocess.run(["git", "ls-tree", "-r", "-z", "--name-only", "HEAD", rel + "/"],
                           capture_output=True, cwd=REPO).stdout.decode("utf-8").split("\0")
    # ⚠ 置き場の名に `habits-NN` を残す——検査器は、パスに巻の名が入っているかで
    #   第四巻だけの検査（手前）を切り替える。名を変えると、検査そのものが走らない。
    d = EX / f".head-habits-{v}"
    if d.exists():
        shutil.rmtree(d)
    d.mkdir()
    for p in filter(None, names):
        content = subprocess.run(["git", "show", f"HEAD:{p}"],
                                 capture_output=True, cwd=REPO).stdout
        (d / Path(p).name).write_bytes(content)
    return d


def main() -> int:
    for v in ["01", "02", "03", "04"]:
        d = head_out(v)
        try:
            h, hb = run_check(d)
        finally:
            shutil.rmtree(d)
        n, nb = run_check(EX / f"habits-{v}" / "草稿")
        mark = "同じ" if h == n else ("減った" if n < h else "⛔ 増えた")
        print(f"habits-{v}  HEAD {h} 件 → いま {n} 件　（{mark}）")
        for line in nb:
            if line not in hb:
                print(f"    新: {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
