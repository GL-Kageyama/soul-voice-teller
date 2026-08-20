---
name: character-forge
description: A preparation skill that designs characters. Fixes desire, motive, wound, belief, change arc, and a voice distinct from others, and deepens design.md's "character" to the granularity at which fast-draft can "move them in character". Narrows the inner conflict to one. Optional preparation (writing works without it). After plot-design.
argument-hint: '(optional) the path to design.md. If omitted, look for design.md in the working directory. Add lang=en|ja|zh to switch output language (default en).'
---

# character-forge — character design (desire · wound · arc · voice)

## Language Mode

This skill writes in English by default. To write in another language, pass a `lang` argument (e.g. `/character-forge lang=ja`) or set `SOUL_VOICE_TELLER_LANG=ja` in the environment. Resolution order: `$ARGUMENTS.lang` > `SOUL_VOICE_TELLER_LANG` > `en`.

- `en` (default): use this file (`SKILL.md`) and `../references/*.md`.
- `ja`: read `SKILL-ja.md` and `../references/ja/*.md`; output in Japanese.
- `zh`: read `SKILL-zh.md` and `../references/zh/*.md`; output in Chinese.

Write all output in the resolved language.

## Skill Metadata

- **id**: `character-forge`
- **version**: `0.1.0`
- **category**: `writing` (design layer · optional preparation)
- **standalone**: `true`
- **language**: `en` (canonical. ja/zh mirrored in `SKILL-ja.md` / `SKILL-zh.md`)

## Position

Optional preparation (technical catalogue §2-A character design). Deepens plot-design's "character" (may be blank) to the granularity at which fast-draft can "move them in character". Writing works without it, but whether a character becomes "a living person" rather than "a role (protagonist · antagonist)" is decided here.

**Source**: technical catalogue §2-A (2-1〜2-16).

## Input Contract

- **design.md**: `<working-dir>/design.md` (the character section. Blank or `?` is fine).
- **premise.md**: `<working-dir>/premise.md` (the core question · theme — the character's desire · wound tie into the theme).
- **persona**: `${SOUL_VOICE_HOME:-$HOME/.soul-voice-teller}/persona.md` (subject-matter preference · the people and relationships that draw you).

## Procedure

1. Read design.md's "character", premise's theme, and persona's "subject-matter preference".
2. Fix the "core" of each character (§2-A):
   - **desire · goal (2-3)**: what they want (the surface wish)
   - **motive (2-4)**: why they want it (the root)
   - **lack · wound · weakness (2-5)**: the inner lack · a past wound
   - **belief · values (2-6)**: what they hold right · what they will defend to the death
   - **voice (2-13)**: way of speaking · vocabulary · habit of thought. Distinct from others
   - **change arc (2-12)**: how they change / how they don't change
   - **the gap between surface and interior (2-16)**: the mismatch between appearance · words and the interior
2b. Fix the character's **role** — what they *do* in the story (a person without a role does not move; the core alone leaves them static):
    - **stake** (what they stand to lose): the desire · wound tied to the story's causality (e.g. "the place they earned by hiding their identity — lost by confessing")
    - **challenge** (what they stand against): three parts, not a noun — (1) the named adversary, (2) why they actively oppose now, (3) the confrontation scene:
        1. **adversary (named)**: who/what they stand against. Name them (an antagonist, not a vague "the organization").
        2. **the adversary's want (active opposition)**: what the adversary wants and does *now* that opposes this character. The adversary must act, not just exist — a named enemy who never moves is not a challenge.
        3. **confrontation scene**: in which scene the two face off. The adversary must be present and opposing in that scene — not a silent bystander named at the end.
        A challenge that only names the adversary ("the powerful man who covered it up") is static: the adversary will stay a silent figure, and the character will have 向かう先のない不安 (a stake with nothing to stand against).
    - **agency (the rule)**: "they move for X; when X is threatened they do Y; for X they will sacrifice Z." Z (risk-taking) is the test that the stake is real — if they cannot name what they would sacrifice, the stake is not actually on the line. The reaction (Y) is the seed of *consistency (らしさ)* — one Y, the same in every scene.
    Note: the function (protagonist / antagonist / …) is plot-design's, from the causal web; stake and agency are yours, from the desire and wound. The two meet in the stake. *Consistency (らしさ)* is not a value to set here — it is the result of that one reaction staying consistent scene to scene; character-in-action verifies it at the scene level.
3. **Narrow the inner conflict to one**: the point where two opposing desires · beliefs collide (e.g. wanting to protect vs wanting to flee). This is the engine of the change arc.
4. State how the character ties into the theme (premise's core question) — the character should be the theme's "living argument".
5. Write into design.md's "character". Undecided may be left as `?` (preparation allows blanks).

## Output

The elaboration of design.md's "character" (desire · motive · wound · belief · voice · change arc · inner conflict · the gap between surface and interior).

## Notes

- **Keep the desire consistent** (2-3〜2-4): the surface wish (desire) and the root (motive) must not contradict. If they do, that is the inner conflict.
- Build the character as a "person", not a "role (2-11)". Protagonist · antagonist are functions; beneath them are wound · desire · belief.
- **Do not make the antagonist one-sided evil** (2-27): give the antagonist's logic its own rightness.
- The voice must stay within the persona's "forbidden moves". A character who touches a forbidden move is made with a reason.
- **The character is a carrier (器) of the hook.** The desire · wound you fix is what the reader will possess; the hook engine ([../references/hook-engine.md](../references/hook-engine.md)) breaks it. Build the character so something can be given, then broken.
- If a character's true role is hidden (surface role → hidden role, e.g. ally by appearance, antagonist in fact), do not leave it at the core level. Fill design.md's "Foreshadowing" as a **foreshadowing map**:
    - surface role → hidden role
    - who it is hidden from (the reader = twist / the other characters = irony)
    - the trunk question ("who is this character really?")
    - the disclosure (turning point) and the next question it opens
    - the foreshadowing list: scene · clue (a discrepancy, not the answer) · disclosure degree (0→1, monotonic) · disclosure curve (reader / other characters) · recollection (which disclosure collects it)
  A hidden role without this map becomes an ungrounded twist (a clue-less disclosure).
