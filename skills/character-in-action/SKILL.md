---
name: character-in-action
description: A preparation skill that makes the designed character settings function in each scene of the scene table. Fixes staged disclosure, making the settings function, and making the backstory behave, and creates in each scene the linkage point where "this scene moves this way precisely because of this character's setting". Optional preparation. After character-forge.
argument-hint: '(optional) the path to design.md. If omitted, look for design.md in the working directory. Add lang=en|ja|zh to switch output language (default en).'
---

# character-in-action — making the character act (make the setting function in the scene)

## Language Mode

This skill writes in English by default. To write in another language, pass a `lang` argument (e.g. `/character-in-action lang=ja`) or set `SOUL_VOICE_TELLER_LANG=ja` in the environment. Resolution order: `$ARGUMENTS.lang` > `SOUL_VOICE_TELLER_LANG` > `en`.

- `en` (default): use this file (`SKILL.md`) and `../references/*.md`.
- `ja`: read `SKILL-ja.md` and `../references/ja/*.md`; output in Japanese.
- `zh`: read `SKILL-zh.md` and `../references/zh/*.md`; output in Chinese.

Write all output in the resolved language.

## Skill Metadata

- **id**: `character-in-action`
- **version**: `0.1.0`
- **category**: `writing` (design layer · optional preparation)
- **standalone**: `true`
- **language**: `en` (canonical. ja/zh mirrored in `SKILL-ja.md` / `SKILL-zh.md`)

## Position

Optional preparation (technical catalogue §2-B making the character act). Design that makes the character settings character-forge "made" **work** in each scene of the scene table. Even a made character is dead if never used (§2-B opening). After character-forge, before fast-draft.

**Source**: technical catalogue §2-B (2-17〜2-28).

## Input Contract

- **design.md**: `<working-dir>/design.md` (character section = already designed · scene table).
- **Prerequisite**: characters already designed by character-forge (if not, prompt character-forge first).

## Procedure

1. Read design.md's "character" and "scene table".
2. Fix how the character setting "moves" in each scene (§2-B):
   - **permeation of the setting (2-17)**: so that personality · habit · values appear in action in every scene (move them "carrying" the setting)
   - **transmutation of backstory (2-18)**: "behave" the past wound · experience, not "tell" it. Even unspoken, the behavior betrays the past
   - **staged disclosure (2-20)**: don't show the backbone all at once; reveal it along the progression (linked to information distribution 3-8)
   - **making the setting function (2-21)**: create in each scene the linkage point where "this scene moves this way precisely because of this character's setting"
   - **the constraint of the past (2-22)**: a past promise · guilt · loss binds the present choice (the point of no return)
   - **lighting from outside (2-24)**: bring the character into relief with shading through another's point of view · mention
   - **role functioning (agency)**: in each scene, what the character pursues · reacts to · chooses, per their agency rule. This is what makes the character move autonomously (by their own stake) rather than be moved by the plot.
   - **confrontation**: if the character's challenge names an adversary, mark the scene where they face off — the adversary present and opposing (not offstage). A challenge without a confrontation scene stays static.
   - **consistency check (らしさ)**: after filling every scene, read the reactions across scenes — does the same agency rule produce them, or does the character waver from scene to scene? A reaction that cannot be derived from the agency rule is *wavering — a stake with no rule (意思なき賭け)*. Fix the reaction to match the rule, or the rule is wrong. らしさ is this check, not a number to write.
3. Append to each scene of the scene table "how this character's setting works" (reinforce the scene's "purpose" with the functioning of the character).
4. Fix the order of disclosure (what of the backbone is revealed in which scene) and add the "disclosure" view to the scene table — and, for a hidden role, the **foreshadowing and disclosure**:
    - plant each foreshadowing clue from the foreshadowing map in its scene (as a discrepancy in description · dialogue · behavior — not as an answer)
    - fix the disclosure (turning point) — where the hidden role is revealed, and what it changes (the role changes: ally → antagonist, etc.)
    - check the 4 axes: 温存 (the true role is not answered before the disclosure) · 進み (clues accumulate toward the truth) · 間合い (spacing ∝ the question's size, accelerating toward the disclosure) · 継ぎ (the disclosure opens the next question)
5. Write into design.md's "character" (or the scene table).

## Output

Append to design.md's scene table (the functioning of the setting in each scene · the order of staged disclosure).

## Notes

- The backstory is "behaved", not "told" (2-18). Exposition dialogue and dumping a recollection wholesale are mediocre.
- Disclosure is **distribution** (linked to information distribution 3-8). Showing it all lets the reader read ahead.
- If a setting does not move the scene, either cut the setting or make a scene where it moves. Don't keep a dead setting.
