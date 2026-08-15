---
name: research-verify
description: A preparation skill that checks the facts and historical reality of the settings and draft. Points out errors in period detail (custom, language, institutions, level of technology) and specialist knowledge, and distinguishes deliberate departures from errors to propose corrections. Keeps errors out of the story. Optional preparation. After plot-design, or after the draft.
argument-hint: '(optional) the path of the object to check (design.md or draft.md). If omitted, look in the working directory. Add lang=en|ja|zh to switch output language (default en).'
---

# research-verify — checking (keep out errors of historical reality · period detail · specialist knowledge)

## Language Mode

This skill writes in English by default. To write in another language, pass a `lang` argument (e.g. `/research-verify lang=ja`) or set `SOUL_VOICE_TELLER_LANG=ja` in the environment. Resolution order: `$ARGUMENTS.lang` > `SOUL_VOICE_TELLER_LANG` > `en`.

- `en` (default): use this file (`SKILL.md`) and `../references/*.md`.
- `ja`: read `SKILL-ja.md` and `../references/ja/*.md`; output in Japanese.
- `zh`: read `SKILL-zh.md` and `../references/zh/*.md`; output in Chinese.

Write all output in the resolved language.

## Skill Metadata

- **id**: `research-verify`
- **version**: `0.1.0`
- **category**: `writing` (design layer · optional preparation)
- **standalone**: `true`
- **language**: `en` (canonical. ja/zh mirrored in `SKILL-ja.md` / `SKILL-zh.md`)

## Position

Optional preparation (technical catalogue §13 research). Checks whether **errors of historical fact · custom · language · institutions · level of technology** have slipped into the world · character settings (design.md) or the draft (draft.md). Keeps errors out of the story (§13 opening). After plot-design (checking settings), or after fast-draft (checking the draft).

**Source**: technical catalogue §13 (13-A investigation · 13-B period detail).

## Input Contract

- **Object to check**: design.md (world · character · period setting) or draft.md (the draft). Given by argument-hint or dialogue.
- **persona**: `${SOUL_VOICE_HOME:-$HOME/.soul-voice-teller}/persona.md` (forbidden moves · subject-matter preference — used to judge how strictly to check).

## Procedure

1. Read the object to check, and identify the story's genre · period · specialist domain.
2. Check for errors (§13-B):
   - **accuracy of historical fact (13-6)**: are the historical events · people · years wrong?
   - **custom · life (13-7)**: did the clothing · food · housing · tools · transport · currency exist in that period?
   - **language · address (13-8)**: has modern language slipped into that period's wording · honorifics · forms of address?
   - **institutions · law · weights and measures (13-9)**: law · status system · units · ways of counting time
   - **level of technology · knowledge (13-10)**: has something that did not exist then slipped in?
   - **specialist knowledge (13-3)**: the accuracy of the trade · learning · technique · law
3. Distinguish each point into **error (to fix) and deliberate departure (may keep)** (13-11):
   - error: unintended inaccuracy that breaks the reader's immersion
   - deliberate departure: a departure intended for the story (should be marked)
4. Propose corrections (the transmutation of investigation 13-5: transmute knowledge into story; don't make investigation into explanation).
5. Reflect the correction in design.md / draft.md (or propose the reflection and confirm).

## Output

The result of checking (a list of errors + proposed corrections + the distinction of deliberate departures), and design.md / draft.md with the correction reflected.

## Notes

- **The balance of period detail and story** (13-11): the weight of period detail must not crush the story. Errors break immersion, but a list of period detail also breaks immersion.
- Mark **deliberate departures** and keep them (the same root as the way of breaking the genre promise 18-D). Don't confuse error with deliberate departure.
- Transmute investigation **into story** (13-5). Don't explain what you researched; show it as story.
