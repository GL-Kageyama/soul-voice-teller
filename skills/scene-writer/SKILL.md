---
name: scene-writer
description: A skill that writes one dramatic scene slowly. Aware of the design of empty space (what not to say), show-don't-tell, and the seams of the scene, it finishes one scene on the desire → conflict → change beat. Where fast-draft writes all at once, use this when you want to write one scene deeply.
argument-hint: '(optional) the scene to write (#n of the scene table) and the path to design.md. If omitted, confirm in dialogue. Add lang=en|ja|zh to switch output language (default en).'
---

# scene-writer — the dramatic scene (write one scene deeply)

## Language Mode

This skill writes in English by default. To write in another language, pass a `lang` argument (e.g. `/scene-writer lang=ja`) or set `SOUL_VOICE_TELLER_LANG=ja` in the environment. Resolution order: `$ARGUMENTS.lang` > `SOUL_VOICE_TELLER_LANG` > `en`.

- `en` (default): use this file (`SKILL.md`) and `../references/*.md`.
- `ja`: read `SKILL-ja.md` and `../references/ja/*.md`; output in Japanese.
- `zh`: read `SKILL-zh.md` and `../references/zh/*.md`; output in Chinese.

Write all output in the resolved language.

## Skill Metadata

- **id**: `scene-writer`
- **version**: `0.1.0`
- **category**: `writing` (execution layer · scene)
- **standalone**: `true`
- **language**: `en` (canonical. ja/zh mirrored in `SKILL-ja.md` / `SKILL-zh.md`)

## Position

The scene skill of the **execution layer** in the three-layer model. Where fast-draft writes "all scenes at once", scene-writer writes "**one dramatic scene deeply**". Suited especially to the pivotal scenes of a story — the climax · the confrontation · the parting.

**Source**: technical catalogue §14-A (writing a scene 14-2) + §3 events + §4 structure + §9 the reader.

## Input Contract

- **Scene to write**: #n of the scene table (or given in dialogue).
- **design.md**: `<working-dir>/design.md` (scene table · narration · direction of prose style · reader image & promise).
- **persona**: `${SOUL_VOICE_HOME:-$HOME/.soul-voice-teller}/persona.md` (voice · forbidden moves).
- **voice-ledger**: `${SOUL_VOICE_HOME:-$HOME/.soul-voice-teller}/voice-ledger.md` (the water source when it goes dry).

## Procedure

1. Read the scene table's relevant scene (purpose · who · what changes), the narration, the direction of prose style, and the persona.
2. Assemble the beats of the scene (§4-3): **desire → conflict → change**. What the character wants, what blocks them, what changes.
3. Decide **the design of empty space** (what not to say) first (§9-5 empty space · §1-18 the line between show and don't-show): what does this scene hand over to the reader by not saying it?
4. Write **show, don't tell**: don't explain emotion; show it through action · line · silence (the same root as the aesthetic of expression and restraint).
5. Be aware of **the seams of the scene** (§4-16 the start and end of a scene): the entrance (hook) and the exit (aftertaste · pull · presentiment). Control the reader's point of departure.
6. Inspect what you wrote against the five clauses of expression and restraint, and fix what violates them (the same criterion of inspection as fast-draft).
7. Save the scene, and if introspection hears a voice · departure, append to the store.

## Output

`<working-dir>/draft_<n>_<scene>.md` (the draft of one scene) + a voice for the store.

## Notes

- The design of empty space is decided **first** (§9-5). What you don't say makes the intensity of what you do say.
- Show, don't tell: don't explain emotion; show it through action (the same root as the five clauses of restraint).
- The seams of the scene (§4-16) control the reader's departure. Be aware of the hook at the entrance and the aftertaste at the exit.
