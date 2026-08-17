---
name: premise
description: An ideation skill that fixes the logline, core question, theme, genre promise, direction of prose style, and reader image & promise from the human's seed (material they want to write) and persona + store. Checks voice & aesthetic sense, and allows subject matter to waver, to settle the work's entrance. Precedes plot-design.
argument-hint: '(required) seed = the material/subject you want to write (a line or two). Example: /premise "a lighthouse keeper fears the sea, yet waits for the only guest who comes by sea". Add lang=en|ja|zh to switch output language.'
---

# premise — ideation (settle the work's entrance against persona + store)

## Language Mode

This skill writes in English by default. To write in another language, pass a `lang` argument (e.g. `/premise lang=ja`) or set `SOUL_VOICE_TELLER_LANG=ja` in the environment. Resolution order: `$ARGUMENTS.lang` > `SOUL_VOICE_TELLER_LANG` > `en`.

- `en` (default): use this file (`SKILL.md`) and `../references/*.md`.
- `ja`: read `SKILL-ja.md` and `../references/ja/*.md`; output in Japanese. The source concepts (内省 / 余白 / 間) live here.
- `zh`: read `SKILL-zh.md` and `../references/zh/*.md`; output in Chinese (留白 / 含蓄).

Write all output in the resolved language.

## Skill Metadata

- **id**: `premise`
- **version**: `0.1.0`
- **category**: `writing` (design layer · per work)
- **standalone**: `true`
- **language**: `en` (canonical. ja/zh mirrored in `SKILL-ja.md` / `SKILL-zh.md`)

## Position

The front stage of the **design layer** in the three-layer model. `inspire` (ideation) is folded in here — the B questions are ideation itself. Per work, choose the theme and logline checked against the soul-story (the persona).

**Input contract (made explicit)**: `the human's seed (what they want to write) + persona (this writer's preferences) + voice-ledger (past voices)`.

## Input Contract

- **Seed**: the material/subject the user wants to write. Received via argument-hint or dialogue. If absent, draw it out in dialogue.
- **persona**: `${SOUL_VOICE_HOME:-$HOME/.soul-voice-teller}/persona.md`. **Required.** If absent, prompt writer-persona first.
- **voice-ledger**: `${SOUL_VOICE_HOME:-$HOME/.soul-voice-teller}/voice-ledger.md`. Read if present (call the previous work's voice into the new question). May be absent.

## Procedure

1. Read the seed, persona, and store. If persona is absent, prompt writer-persona and stop.
2. Ideate with the B questions ([../references/introspection.md](../references/introspection.md) chapter B). ground = **persona + store**. But use persona in its two layers at different temperatures:
   - **the soul's voice (HOW) = soul-story · aesthetic sense · voice · forbidden moves** → check at low temperature (keep faithfully)
   - **subject-matter preference (WHAT) = A-5** → ideate at high temperature (use as a seed. Don't pull too close)
   - **B-1 theme** — how this material answers the writer's "question they keep writing"
   - **B-2 logline** — how this story sounds in the writer's voice (the core in one line, not a summary)
   - **B-3 character & world** — the character the writer most wants to write, the place that draws them
   - **B-4 seed × subject-matter wavering** — if the seed's season · setting · time of day · character · relationship overlaps the persona's subject matter (A-5) too much, shift it deliberately. A mismatch (e.g. a summer Bon festival against an autumn preference) is welcomed as a wavering; a deliberate departure is recorded with `?`
3. Summarize the ideation result into the output format below. Throw away answers "**anyone could write**" (stock themes · loglines) and pull back toward voice · aesthetic sense (HOW). If the subject matter (WHAT) overlaps the persona's preference too much, deliberately move away — the same subject every time is mediocre.
4. **Always fix the reader image and the promise to the reader** (a novel is "the art of the time it is read"). Until you write who it is for and what promise you make, the draft has no reader. The promise includes **the reaction axis** — name the primary and secondary of the six axes ([../references/six-response-axes.md](../references/six-response-axes.md)).
5. Save the output to `<working-dir>/premise.md`. The working directory is named by the user (if unset, `examples/<slug>/`).

## Output

`<working-dir>/premise.md`

```markdown
# premise — the work's entrance

## Logline
(the story in one line. The core, sounded in the writer's voice)

## The core question
(the unsettled question the story asks. Held against the persona's soul-story)

## Theme
(how it answers the persona's "question you keep writing")

## The genre promise
(what the reader may expect of this work)

## The reaction axis
(primary · secondary of the six axes — which reaction the reader mainly feels. e.g. 恐怖 primary · 感嘆 secondary)

## Direction of prose style
(the direction of this work's prose, checked against the persona's voice & brushwork)

## Reader image & promise
(who it is for · what experience you promise that reader)
```

## Notes

- Ideation is **both checking and wavering**. Voice · aesthetic sense · forbidden moves (HOW) are checked against the ground (persona) and kept. Subject-matter preference (WHAT) is used as a seed but not pulled too close — if it overlaps too much, deliberately move away (high-temperature wavering). Either way, don't fabricate a "plausible theme" from the ground.
- The reader image & promise is **required** (design review flash #1). Do not omit it.
- Don't design here (causal structure · the scene table is plot-design's job). Premise settles "what it asks · in what prose · for whom" and stops there.
- **The promise selects the reaction axis.** Which of the six axes the reader will feel is fixed here as part of the genre promise + reader image & promise ([../references/six-response-axes.md](../references/six-response-axes.md)). plot-design turns that axis into the whole-work arc.
