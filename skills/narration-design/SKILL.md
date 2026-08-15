---
name: narration-design
description: A preparation skill that designs the "narration" of the design document in detail. Fixes the type of point of view, reliability, distance, tense, nesting, and speech style, and deepens the narration that plot-design roughly fixed to the granularity at which fast-draft can write it consistently. Optional preparation (writing works without it). After plot-design, before fast-draft.
argument-hint: '(optional) the path to design.md. If omitted, look for design.md in the working directory. Add lang=en|ja|zh to switch output language (default en).'
---

# narration-design — detailed design of narration (who · from where · at what distance)

## Language Mode

This skill writes in English by default. To write in another language, pass a `lang` argument (e.g. `/narration-design lang=ja`) or set `SOUL_VOICE_TELLER_LANG=ja` in the environment. Resolution order: `$ARGUMENTS.lang` > `SOUL_VOICE_TELLER_LANG` > `en`.

- `en` (default): use this file (`SKILL.md`) and `../references/*.md`.
- `ja`: read `SKILL-ja.md` and `../references/ja/*.md`; output in Japanese.
- `zh`: read `SKILL-zh.md` and `../references/zh/*.md`; output in Chinese.

Write all output in the resolved language.

## Skill Metadata

- **id**: `narration-design`
- **version**: `0.1.0`
- **category**: `writing` (design layer · optional preparation)
- **standalone**: `true`
- **language**: `en` (canonical. ja/zh mirrored in `SKILL-ja.md` / `SKILL-zh.md`)

## Position

Optional preparation (technical catalogue §6 narration). Deepens the "narration (point of view · tense · narrator)" that plot-design roughly fixed to the granularity at which fast-draft can write **consistently**. Writing works without it, but a consistent decision on narration is precisely what produces non-average prose.

**Source**: technical catalogue §6 (the narrator 6-A · the classification of point of view 6-B · techniques of narration 6-C).

## Input Contract

- **design.md**: `<working-dir>/design.md` (the skeleton of narration = point of view · tense · narrator).
- **premise.md**: `<working-dir>/premise.md` (direction of prose style · reader image & promise).
- **persona**: `${SOUL_VOICE_HOME:-$HOME/.soul-voice-teller}/persona.md` (voice & brushwork. Checked so the choice of narration does not become "a choice no one made").

## Procedure

1. Read design.md's "narration", premise's "direction of prose style" and "reader image & promise", and persona's "voice & brushwork (concrete-sentence anchor)".
2. Fix the six items below (§6):
   - **type of point of view (§6-B)**: first person (monologue / recollection / witness / letter · diary) · second person · third person (omniscient / limited = internal focalization / objective = camera). Which type, and **why that type**.
   - **reliability (§6-4)**: is the narrator reliable? How much lie · illusion · ignorance · bias is allowed?
   - **distance (§6-6)**: how close to the character's interior? Far (objective · action only) or near (internal focalization)?
   - **tense (§5-8 · §7-22)**: past (a sense of distance) or present (rawness)?
   - **nesting (§6-8 · nesting of points of view)**: does it interpose a frame story · letter · diary · testimony?
   - **speech style (§6-7)**: the division among direct · indirect · free indirect · interior monologue.
3. Write each decision into design.md's "narration" together with its "why". In particular, mark **the consistency of point of view (§6-10)** — where it is kept, and where it is broken (and the reason if broken).
4. Confirm the narration does not contradict the persona's voice (concrete-sentence anchor). If it does, pull it back toward the persona.

## Output

The elaboration of design.md's "narration" (type of point of view · reliability · distance · tense · nesting · speech style · where consistency is broken).

## Notes

- Narration is **the main battlefield of particularity**. "Thin particularity" (a consistent distance of the limited type) produces more non-average prose than "thick generality" (omniscient, anyone could tell it).
- **Wavering point of view** (an unintended slip of point of view) is a hotbed of mediocrity. Keep consistency, or have a reason if you break it (§6-10).
- Don't over-decide. Narration is a map (plan), not an order — loosen it if fast-draft's introspection departs.
