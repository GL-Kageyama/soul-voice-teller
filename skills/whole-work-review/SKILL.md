---
name: whole-work-review
description: A skill that reviews the draft as a whole — not scene by scene, but as one book that closes. It checks structural coherence, the setup and payoff of foreshadowing, the distribution of density and pacing, cross-chapter redundancy, over-reliance on world-closed vocabulary, and the balance of expression and restraint across the whole. Checked against series-bible.md (the work's ledger). Does not build in sublation (the evaluation layer).
argument-hint: '(optional) the path to draft.md. If omitted, find draft.md in the working directory. Add lang=en|ja|zh to switch output language (default en).'
---

# whole-work-review — review the work as one book that closes

## Language Mode

This skill writes in English by default. To write in another language, pass a `lang` argument (e.g. `/whole-work-review lang=ja`) or set `SOUL_VOICE_TELLER_LANG=ja`. Resolution order: `$ARGUMENTS.lang` > `SOUL_VOICE_TELLER_LANG` > `en`.

- `en` (default): use this file (`SKILL.md`) and `../references/*.md`.
- `ja`: read `SKILL-ja.md` and `../references/ja/*.md`; output in Japanese.
- `zh`: read `SKILL-zh.md` and `../references/zh/*.md`; output in Chinese.

Write all output in the resolved language.

## Skill Metadata

- **id**: `whole-work-review`
- **version**: `0.1.0`
- **category**: `writing` (revision · whole-work)
- **standalone**: `true`
- **language**: `en` (canonical. ja/zh mirrored in `SKILL-ja.md` / `SKILL-zh.md`)

## Position

The **whole-work** revision skill of the three-layer model. Where prose (style) · scene-writer (scene) · revise-for-reader (reader experience) · entertainment (the pleasures) each work on the scene, whole-work-review checks what emerges **only when you step back to the whole** — whether the work closes as one book. Its ground is **series-bible.md** (setting · foreshadowing · the structure's promises), not a scene.

**Source**: series-bible (the ledger) + technical catalogue §15 revision.

## Input Contract

- **draft.md**: `<working-dir>/draft.md` (what to review).
- **series-bible.md**: `<working-dir>/series-bible.md` (the ground — setting · foreshadowing table · the structure's promises).
- **persona**: `${SOUL_VOICE_HOME:-$HOME/.soul-voice-teller}/persona.md` (forbidden moves · voice).

## The six axes of the whole (what only the whole reveals)

1. **Structural coherence** — the work's core mechanism (organ = verb · the tilt of voice · the refrain) holds across every chapter. A chapter that breaks the mechanism is a break.
2. **Foreshadowing: setup → payoff** — check against series-bible's foreshadowing table. Find setups left unclosed and payoffs without setups.
3. **Density & pacing distribution** — the pivotal chapter is densest, the rest restrained. No flatness, no inversion of weight.
4. **Cross-chapter redundancy** — the same expression · image · rhythm reused across chapters without variation (a loop, not a refrain).
5. **Over-reliance on world-closed vocabulary** — the setting's own words (proper nouns · the system's terms) doing the work that concrete detail (thing · sound · body) should do. A closed word must be grounded, not float as an abstract operation.
6. **Balance of expression & restraint · voice consistency** — no explanation · naming · moral creeps in over the whole; the voice does not drift chapter to chapter.

## Procedure

1. Read draft.md and series-bible.md (setting · foreshadowing table · the promises).
2. Read the draft as a WHOLE (not scene by scene). The unit of judgment is the work.
3. Inspect against the six axes. For each, find the concrete spot (chapter · line) that breaks.
4. Revise at the whole-work level, in harmony with restraint: add nothing that explains · names · moralizes. Ground a floating closed word in a thing · sound · body.
5. A refrain must earn its repetition (tremble · variation), not merely recur. If a recurring phrase no longer varies, it is a loop — vary it or cut it.
6. Save the revised draft.md.

## Output

The revised `<working-dir>/draft.md`.

## Notes

- **The unit is the whole, not the scene.** A scene can be good and the work still not close. Check what only stepping back reveals.
- **series-bible.md is the ground.** Without it, "does the whole hold" is a feeling, not an observation.
- **The world's closed vocabulary is a scaffold, not a substitute for the concrete.** When a closed word does the work, ground it in thing · sound · body — or the world becomes a rulebook, not a story.
- **A refrain is repetition that varies (trembles).** A loop is repetition that doesn't. Change the loop into a refrain, or cut it.
- Sublation (negation · preservation · elevation) is the evaluation layer's mechanism; don't do it here.
