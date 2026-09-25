#!/usr/bin/env python3
"""草稿の検査器——『ハビッツ！！！』

これは検査であって、評価ではない。出すのは「在る／無い」と「どこに在るか」だけである。
「良い／悪い」は出さない（soul-voice-teller は評価の機構を持ち込まない）。

規則は、このスクリプトに写さない。
  禁則の語群  —— examples/habits/README.md「## 禁則」から読む
  感情        —— 下の C18_WORDS（正文＝構想/design.md:120）と、
                 EMOTION_WORDS（走査語。正文ではない。出典は台帳の各行）
  呼びかけ    —— 下の SECOND_PERSON（正文＝habits-01/構想/design.md:21）

使い方:
    python3 check.py <draft.md>                # 一話
    python3 check.py <volume_dir>/草稿          # 巻ぜんぶ（逐語の再利用も見る）
    python3 check.py <draft.md> --volume-dir <dir>   # 一話＋同巻との突き合わせ
"""

import argparse
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
# examples/habits/検査/check.py → examples/habits/
HABITS = HERE.parent
README = HABITS / "README.md"

# ⚠ C-18 第二条（examples/habits/構想/design.md:120）が禁じる語は、三つである——
#    「悲しい」「さびしい」「うれしい」を、地の文の内面記述として置かない。
#    正文は、ひらがなで書く。ゆえに、同じ語の漢字の綴り（寂し・嬉し）も、同じ側へ置く。
#    ⚠ この三語だけが、⛔ の根拠を持つ。
C18_WORDS = ["悲し", "さびし", "寂し", "うれし", "嬉し"]

# ⚠ 下の十二語は、正文ではない。台帳の各行が申告に用いている走査語である。
#    出典: examples/habits/台帳/series-bible.md 五、改稿履歴の各行
#    ⚠ ゆえに「在る／無い」を出すだけにして、⛔ にしない（2026-09-25、著者裁定）。
#      前半の四語（気づ・分か・感じ・思っ・考え）は、そもそも感情語ではなく認識の語であり、
#      C-18 第二条の三語とは重なっていない。実測では、この十二語のうち当たるのは「分か」だけである
#      （十三箇所のうち十二箇所は「分かる／分からない」の触覚・聴覚の報告、
#        一箇所は「分かれている」＝分割である）。人が読む。
EMOTION_WORDS = [
    "気づ", "分か", "感じ", "思っ", "考え",
    "悲し", "嬉し", "寂し", "怖", "不安", "怒り", "驚い",
]

# ⚠ 呼びかけ——正文は habits-01/構想/design.md:21
#    「声: 地の文に呼びかけが一度も出ない。」「立てる人称は「私」、欠けている人称は「あなた」。」
#    語の一覧は与えられていないが、欠けている人称が「あなた」と定められているゆえ、
#    二人称の語を走査する。⚠ 「君」だけは、名に付く接尾の用法（佐藤君）がありうるゆえ、
#    他の四語と分けて「人が読む」側に置く。
SECOND_PERSON = ["あなた", "あんた", "お前", "きみ"]
REVIEW_SECOND_PERSON = {"君"}

# ⚠ 縁 は「ふち」の意味なら同字別語であり、禁則の対象ではない（README:149）。
#    ゆえに自動で落とさず、当たった箇所を人が読む。
REVIEW_ONLY = {"縁"}

# ⚠ この巻には基底語がある——「音が、する。」（6字）「小さい、音である。」（9字）
#    「扉が、開く。」「立ち上がる。」。既執筆29話を走査すると、両巻にまたがって
#    繰り返し現れるのは、この短い行だけである（実測・2026-09-25）。
#    ゆえに 12字未満は「逐語の再利用」として数えず、基底語として別に数える。
MIN_LINE_FOR_REUSE = 12
BASE_PHRASE_CEIL = 12

# ⚠ 手前——第四巻の義務である（habits-04/構想/design.md 決定9。
#    読み（あ）＝「四つの手前は、巻が担う。話ごとに、その話に立ちうる通路の数だけ」——2026-09-25、著者裁定）。
#    この巻は、四つの通路が閉じることを能動の形で書く——「その動作の手前で止まる」。
#    ゆえに本文には、その手前が要る（habits/構想/design.md:233「空欄には、手前が無い」）。
#    ⚠ この走査は、語を見るだけである。「手前」の字が在っても、その手前が意味の側で立っているとは限らない
#      ——実測、04-01:319「向こうの、角と、手前の、角である。」は、手前の字を持つが、止まる手前ではない。
#      ゆえに当たった行は、全部、印字する。人が読む。
MAETE_VOLUME = "habits-04"
MAETE_RE = re.compile(r"手前|前で、止ま")


# ---------------------------------------------------------------- 禁則の読み込み

def load_kinzoku():
    """README の「## 禁則」節を読み、{分類: [語]} を返す。スクリプトには写さない。"""
    if not README.exists():
        sys.exit(f"README が見つからない: {README}")
    lines = README.read_text(encoding="utf-8").splitlines()

    groups, name, inside = {}, None, False
    for raw in lines:
        line = raw.rstrip()
        if line.startswith("## "):
            inside = line.strip() == "## 禁則"
            name = None
            continue
        if not inside or not line.startswith("- "):
            continue
        body = line[2:].strip()

        if "——" in body:
            head, rest = body.split("——", 1)
            src = rest          # 語は —— の右に在る
        else:
            head, rest = body, ""
            src = body          # ⚠ 「——」の無い行は、語が左側に在る

        # ⚠ 「読者」の行は、語の一覧ではない（文単位の規則）。別に数える。
        if "読者" in head:
            continue

        # ⚠ 一行に、二つの語群が `／` で並ぶことがある——README:144
        #    「上限・定員・キャパ・枠／煙草・煙管・吸い殻・路上喫煙」が、それである。
        #    ⚠ これに対し、:142 の `／` は語の区切りである（「カット／シーン／…」）。
        #    ゆえに「`／` で割った切片の、どれもが `・` を含むとき」だけ、語群として割る。
        #    ⚠ 割らずに一語群として数えると、印字する数（六）が、台帳の各行の「八つの語群」と
        #      食い違う。台帳の数え方は「`／` で割って七、これに「読者」の一行を足して八」である。
        parts = [p for p in re.split(r"／", src) if p.strip()]
        if len(parts) > 1 and all("・" in p for p in parts):
            segments = parts
        else:
            segments = [src]

        quoted = re.findall(r"「([^」]+)」", head)

        for k, seg in enumerate(segments):
            tail = re.split(r"[。]", seg)[0]
            tail = re.split(r"（", tail)[0]
            tail = re.sub(r"「[^」]+」", "", tail)
            plain = [w.strip().strip("*") for w in re.split(r"[・／]", tail)]
            # ⚠ 6字を超える切片は、語ではなく説明文である（README の書き方）
            plain = [w for w in plain if w and len(w) <= 6]

            words = (quoted + plain) if k == 0 else plain
            if not words:
                continue

            if k > 0:
                name = words[0]        # 二つ目以降の語群は、先頭の語を名とする
            elif "——" in body:
                name = head.strip().strip("*").strip("「」")
            else:
                name = (quoted[0] if quoted
                        else head.split("・")[0].split("／")[0].strip())

            groups.setdefault(name, [])
            for w in words:
                if w not in groups[name]:
                    groups[name].append(w)

    if not groups:
        sys.exit("禁則の語群が、README から一行も読めなかった（検査を空で通さない）")
    return groups


# ---------------------------------------------------------------- 草稿の読み込み

TITLE_RE = re.compile(r"^#\s+第\d+話")
SCENE_RE = re.compile(r"^##\s+(\d+)\s*$")


def load_draft(path):
    """(題名行, [(行番号, 見出し or None, 本文 or None)]) を返す。

    ⚠ 行番号は、ファイルの物理行である（1 から）。引用に使う。
    """
    text = path.read_text(encoding="utf-8")
    return text.splitlines()


def prose_lines(lines):
    """本文の行だけを (行番号, 文) で返す。題名行・見出し・空行を除く。"""
    out = []
    for i, line in enumerate(lines, start=1):
        s = line.strip()
        if not s:
            continue
        if TITLE_RE.match(s) or s.startswith("#"):
            continue
        if SCENE_RE.match(s):
            continue
        out.append((i, s))
    return out


def count_chars(lines):
    """非空白文字を数える。題名行・空行・`## N` 見出しを除く（進捗表 §5 と同じ数え方）。"""
    total = 0
    for _, s in prose_lines(lines):
        for ch in s:
            if not ch.isspace() and unicodedata.category(ch) != "Cf":
                total += 1
    return total


def scenes(lines):
    """[(節番号, [行番号...])] を返す。節が無ければ []。"""
    result, current = [], None
    for i, line in enumerate(lines, start=1):
        m = SCENE_RE.match(line.strip())
        if m:
            current = (int(m.group(1)), [])
            result.append(current)
            continue
        if current is not None and line.strip() and not line.strip().startswith("#"):
            current[1].append(i)
    return result


# ---------------------------------------------------------------- 検査

def find_words(lines, words):
    """語が現れる (行番号, 文) を返す。"""
    hits = []
    for i, s in prose_lines(lines):
        for w in words:
            if w in s:
                hits.append((i, w, s))
    return hits


def check_format(lines):
    """見出しと、行ごとの空行の規則を見る。"""
    problems = []
    if not any(TITLE_RE.match(l.strip()) for l in lines):
        problems.append("題名行（`# 第N話「…」`）が無い")

    nums = [int(m.group(1)) for l in lines if (m := SCENE_RE.match(l.strip()))]
    if nums != [1, 2, 3]:
        problems.append(f"節の見出しが `## 1/2/3` でない: {nums}")

    prose = prose_lines(lines)
    if not prose:
        problems.append("本文が、一行も無い")
        return problems

    # 行ごとに空行——本文の行が二行続いてはいけない
    for (i1, _), (i2, _) in zip(prose, prose[1:]):
        if i2 - i1 < 2:
            problems.append(f"{i2}行目——本文の行が、空行を挟まずに続いている")
    return problems


def check_reader(lines):
    """「読者」——地の文ではゼロ、節ごとに一つまで。"""
    hits = find_words(lines, ["読者"])
    return hits


# ⚠ 第四巻の会話は、問い一声のみであり、鉤括弧で区別しない
#    （habits-04/構想/design.md 決定5）。前三巻は逆に、鉤括弧が会話の印である。
#    ゆえに「在る／無い」を出すだけで、良し悪しは言わない。
QUOTE_OPEN = "「『"


def count_quotes(lines):
    """本文の行の鉤括弧を数える。題名行は prose_lines が既に外している。"""
    hits = []
    for i, s in prose_lines(lines):
        n = sum(s.count(c) for c in QUOTE_OPEN)
        if n:
            hits.append((i, n, s))
    return hits


def build_index(paths):
    """行 → その行を持つ話の名の集合。

    ⚠ 文字数では、基底語と再利用を切れない（実測・2026-09-25）。
       「蛍光灯が、点いて、いる。／白い。／紙の、上に、落ちて、いる。」は
       9〜14字であり、しかも基底語である。ゆえに数の側で切る——
       その行が三話以上に現れるなら基底語、二話にしか現れないなら再利用の候補。
    """
    idx = {}
    for p in paths:
        for _, s in prose_lines(load_draft(p)):
            if len(s) < MIN_LINE_FOR_REUSE:
                continue
            idx.setdefault(s, set()).add(p.name)
    return idx


def find_reuse(target_path, other_paths, index):
    """二話にしか現れない行の、2行以上の連なりを返す。"""
    me = target_path.name
    found = []
    for other in other_paths:
        if other == target_path:
            continue
        run_start, run = None, []
        for i, s in prose_lines(load_draft(other)):
            if len(s) >= MIN_LINE_FOR_REUSE and index.get(s) == {me, other.name}:
                if run_start is None:
                    run_start = i
                run.append((i, s))
            else:
                if len(run) >= 2:
                    found.append((other.name, run_start, list(run)))
                run_start, run = None, []
        if len(run) >= 2:
            found.append((other.name, run_start, list(run)))
    return found


# ---------------------------------------------------------------- 出力

def count_base_phrases(target_path, other_paths):
    """短い行（基底語）が、同巻の他の話にも現れる数。再利用としては数えない。"""
    def short(path):
        return {s for _, s in prose_lines(load_draft(path))
                if 0 < len(s) < BASE_PHRASE_CEIL}

    target = short(target_path)
    seen = set()
    for other in other_paths:
        if other == target_path:
            continue
        seen |= (target & short(other))
    return len(seen)


def report(path, volume_dir, groups, as_json):
    lines = load_draft(path)
    prose = prose_lines(lines)
    n_chars = count_chars(lines)
    total_lines = len(lines)

    print(f"■ {path.name}")
    print(f"  走査した範囲——この1ファイルのみ（{total_lines}行・本文 {len(prose)}行・{n_chars}字）")
    print()

    if not prose:
        print("  ⛔ 本文が空である。検査は落ちる（0件で通さない）。")
        return 1

    failed = False

    # 形式
    problems = check_format(lines)
    print("  【形式】")
    if problems:
        failed = True
        for p in problems:
            print(f"    ⛔ {p}")
    else:
        print("    ✅ 題名行・`## 1/2/3`・行ごとの空行——すべて在る")
    print()

    # 字数
    sc = scenes(lines)
    print("  【字数】")
    print(f"    計 {n_chars}字")
    for num, nums in sc:
        sub = sum(count_chars([lines[i - 1] for i in nums]) for _ in [0])
        # 節ごとの字数は、その節の行だけを数える
        cnt = 0
        for i in nums:
            for ch in lines[i - 1].strip():
                if not ch.isspace():
                    cnt += 1
        print(f"    第{num}節 {cnt}字")
    print()

    # 禁則
    print("  【禁則】——README「## 禁則」を読んで走査")
    any_hit = False
    for name, words in groups.items():
        hits = find_words(lines, words)
        if hits:
            any_hit = True
            for i, w, s in hits:
                mark = "⚠ 人が読む（ふちの意味なら対象外）" if w in REVIEW_ONLY else "⛔"
                print(f"    {mark} [{name}] 「{w}」——{i}行目: {s}")
                if w not in REVIEW_ONLY:
                    failed = True
    if not any_hit:
        print("    ✅ 0件")
    print()

    # 感情——⛔ は C-18 第二条の三語だけである。十二語は「人が読む」側に置く。
    print("  【感情】")
    hits = find_words(lines, C18_WORDS)
    if hits:
        failed = True
        for i, w, s in hits:
            print(f"    ⛔ [C-18 第二条] 「{w}」——{i}行目: {s}")
    else:
        print(f"    ✅ C-18 第二条の三語（{'・'.join(C18_WORDS)}）——0件")
    scan = find_words(lines, EMOTION_WORDS)
    if scan:
        print(f"    ⚠ 走査語（{len(EMOTION_WORDS)}語）に {len(scan)}箇所——人が読む。"
              f"正文は、この十二語を禁じていない")
        for i, w, s in scan:
            print(f"      「{w}」——{i}行目: {s}")
    else:
        print(f"    ✅ 走査語（{len(EMOTION_WORDS)}語）——0件")
    print()

    # 人称
    print("  【人称・その他】")
    for label, words in [("彼女", ["彼女"]), ("彼", ["彼"]), ("AI", ["AI"])]:
        hits = find_words(lines, words)
        if hits:
            failed = True
            for i, w, s in hits:
                print(f"    ⛔ 「{w}」——{i}行目: {s}")
        else:
            print(f"    ✅ 「{label}」0件")
    hits = check_reader(lines)
    if hits:
        for i, w, s in hits:
            print(f"    ⚠ 「読者」——{i}行目: {s}（地の文なら 0 でなければならない）")
    else:
        print("    ✅ 「読者」0件")
    print()

    # 呼びかけ——二人称。正文は habits-01/構想/design.md:21。
    print("  【呼びかけ】——二人称。題名行は数えていない")
    hits = find_words(lines, SECOND_PERSON)
    if hits:
        failed = True
        for i, w, s in hits:
            print(f"    ⛔ 「{w}」——{i}行目: {s}")
    else:
        print(f"    ✅ 0件（{'・'.join(SECOND_PERSON)}）")
    hits = find_words(lines, sorted(REVIEW_SECOND_PERSON))
    if hits:
        for i, w, s in hits:
            print(f"    ⚠ 「{w}」——{i}行目: {s}（名に付く接尾なら、呼びかけではない）")
    else:
        print(f"    ✅ 「{'・'.join(sorted(REVIEW_SECOND_PERSON))}」0件")
    print()

    # 鉤括弧——第四巻は 0 が設計である（決定5）。前三巻は会話の印である。
    print("  【鉤括弧】——題名行は数えていない")
    q = count_quotes(lines)
    if q:
        total_q = sum(n for _, n, _ in q)
        print(f"    ⚠ 本文に {total_q}個（{len(q)}行）")
        for i, n, s in q:
            print(f"      {i}行目（{n}個）: {s[:60]}")
    else:
        print("    ✅ 本文に 0個")
    print()

    # 手前——第四巻だけの義務である（決定9）
    if MAETE_VOLUME in str(path):
        hits = [
            (i, s)
            for i, s in enumerate(lines, 1)
            if s.strip() and not s.lstrip().startswith("#") and MAETE_RE.search(s)
        ]
        print("  【手前】——第四巻。決定9「その動作の手前で止まる」")
        if hits:
            print(f"    ✅ {len(hits)}行——⚠ 語の一致である。意味の側は、人が読む")
            for i, s in hits:
                print(f"      {i}行目: {s}")
        else:
            failed = True
            print("    ⛔ 0行——この巻の本文は、手前を持たねばならない"
                  "（habits/構想/design.md:233「空欄には、手前が無い」）")
        print()

    # 逐語の再利用
    if volume_dir:
        others = sorted(Path(volume_dir).glob("draft_*.md"))
        if len(others) <= 1:
            print("  【逐語の再利用】")
            print(f"    ⚠ 同巻に、突き合わせる相手が無い（{len(others)}ファイル）")
        else:
            index = build_index(others)
            reuse = find_reuse(path, others, index)
            base = count_base_phrases(path, others)
            print("  【逐語の再利用】")
            if reuse:
                for name, start, run in reuse:
                    failed = True
                    print(f"    ⛔ {name} の {start}行目から {len(run)}行が、完全に一致する")
            else:
                print(f"    ✅ {MIN_LINE_FOR_REUSE}字以上の行の、2行以上の一致は 0件"
                      f"（{len(others) - 1}ファイルと突き合わせ）")
            print(f"    ⚠ {MIN_LINE_FOR_REUSE}字未満の行の一致——{base}件。"
                  f"基底語として数えている")
        print()

    return 1 if failed else 0


def main():
    ap = argparse.ArgumentParser(description="草稿の検査器——「在る／無い」だけを出す")
    ap.add_argument("path", help="draft_*.md、または草稿ディレクトリ")
    ap.add_argument("--volume-dir", help="逐語の再利用を見る相手（同巻の草稿ディレクトリ）")
    args = ap.parse_args()

    groups = load_kinzoku()
    target = Path(args.path)

    if target.is_dir():
        files = sorted(target.glob("draft_*.md"))
        if not files:
            sys.exit(f"⛔ 草稿が、一本も無い: {target}（空の検査は通さない）")
        volume_dir = str(target)
    else:
        files = [target]
        volume_dir = args.volume_dir

    print(f"禁則の分類——{len(groups)}（README から読んだ）")
    for name, words in groups.items():
        print(f"  {name}: {'・'.join(words)}")
    print()

    rc = 0
    for f in files:
        rc |= report(f, volume_dir, groups, False)
        print("─" * 60)
    return rc


if __name__ == "__main__":
    sys.exit(main())
