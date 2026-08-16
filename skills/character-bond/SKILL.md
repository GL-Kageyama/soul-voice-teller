---
name: character-bond
description: A skill that renders the relationship born between two characters — the axis of want, reversal/mirror (one's active becoming the other's passive), the turning point (the moment the relationship changes), bidirectionality (not one-way), and embodiment (body · action · thing · sound, not explanation). Draws the emergence and change of a relationship concretely, without breaking expression and restraint.
argument-hint: '(optional) the path to draft.md. If omitted, find draft.md in the working directory. Add lang=en|ja|zh to switch output language (default en).'
---

# character-bond — what is born between two

## Language Mode

This skill writes in English by default. To write in another language, pass a `lang` argument (e.g. `/character-bond lang=ja`) or set `SOUL_VOICE_TELLER_LANG=ja`. Resolution order: `$ARGUMENTS.lang` > `SOUL_VOICE_TELLER_LANG` > `en`.

- `en` (default): use this file (`SKILL.md`) and `../references/*.md`.
- `ja`: read `SKILL-ja.md` and `../references/ja/*.md`; output in Japanese.
- `zh`: read `SKILL-zh.md` and `../references/zh/*.md`; output in Chinese.

Write all output in the resolved language.

## Skill Metadata

- **id**: `character-bond`
- **version**: `0.1.0`
- **category**: `writing` (design · relationship)
- **standalone**: `true`
- **language**: `en` (canonical. ja/zh mirrored in `SKILL-ja.md` / `SKILL-zh.md`)

## Position

The **preparation (design)** skill of the three-layer model. Where character-forge handles **one character** and character-in-action **revealing a character through action**, character-bond handles **the space between two**. A relationship is not born in one person; it is born in the space between two (間). Draw its emergence and change through the concrete (body · action · thing · sound), **without breaking expression and restraint** (negative space · don't name it · no moral at the ending).

**Source**: technical catalogue §character + §4 structure (the turn).

## Input Contract

- **draft.md**: `<working-dir>/draft.md` (what to revise).
- **design.md**: `<working-dir>/design.md` (reader image & promise · the design of the two).
- **persona**: `${SOUL_VOICE_HOME:-$HOME/.soul-voice-teller}/persona.md` (forbidden moves · voice).

## The five axes of relationship

1. **The axis of want** — name what each of the two wants from the other. One side alone is a device.
2. **Reversal / mirror** — one's active becomes the other's passive. If one "sends", the other "receives". Return the other's verb in the reverse direction.
3. **The turning point** — the moment one first turns *toward* the other. A relationship that stays passive never changes.
4. **Bidirectionality** — don't make it one-way. Draw both A→B and B→A. A one-directional relationship is a device, not a bond.
5. **Embodiment** — draw the relationship through body · action · thing · sound, not explanation · naming · moral.

## Procedure

1. Read design.md's "reader image & promise" and the design of the two (character-forge).
2. Inspect against the five axes. Find which axis is weak.
3. Fill **reversal/mirror**: return the other's active verb in the reverse (passive) direction.
4. Place the **turning point**: the moment one first turns toward the other, as one action.
5. Check **bidirectionality**: are both A→B and B→A present?
6. Add the relationship through **body · action · thing · sound**, not explanation.
7. Save the revised draft.md.

## Output

The revised `<working-dir>/draft.md`.

## Notes

- Drawing the relationship with **explanation** breaks the soul. Don't write "they are close"; write the finger that touches.
- **Reversal/mirror** means returning the other's verb in the reverse direction. It is the same shape as the tilt toward the passive voice.
- A relationship without a **turning point** does not move. Left passive, no relationship is born.
- A **one-way** relationship is a device, not a person. Keep it bidirectional.
