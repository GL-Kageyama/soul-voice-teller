---
name: prose
description: A skill that rewrites prose for stylistic quality (rhythm, sensory texture, an irreplaceable voice, and control of time through long and short sentences). Checked against the persona's voice, it sharpens sentences "anyone could write" into sentences "only this writer could write". Used per scene of the draft.
argument-hint: '(optional) the prose / scene to rewrite (the path to draft_<n>.md), or a quoted sentence. If omitted, confirm in dialogue. Add lang=en|ja|zh to switch output language (default en).'
---

# prose — prose style (sharpen sentences by rhythm · sense · voice)

## Language Mode

This skill writes in English by default. To write in another language, pass a `lang` argument (e.g. `/prose lang=ja`) or set `SOUL_VOICE_TELLER_LANG=ja` in the environment. Resolution order: `$ARGUMENTS.lang` > `SOUL_VOICE_TELLER_LANG` > `en`.

- `en` (default): use this file (`SKILL.md`) and `../references/*.md`.
- `ja`: read `SKILL-ja.md` and `../references/ja/*.md`; output in Japanese. The source concepts (内省 / 余白 / 間) live here.
- `zh`: read `SKILL-zh.md` and `../references/zh/*.md`; output in Chinese (留白 / 含蓄).

Write all output in the resolved language.

## Skill Metadata

- **id**: `prose`
- **version**: `0.1.0`
- **category**: `writing` (execution layer · prose style)
- **standalone**: `true`
- **language**: `en` (canonical. ja/zh mirrored in `SKILL-ja.md` / `SKILL-zh.md`)

## Position

The prose-style skill of the **execution layer** in the three-layer model. fast-draft "writes", prose "sharpens". Leaving the draft's roughness in place, it raises only the quality of the prose style (rhythm · sense · voice). The prose-family skills work language by language (English prose's rhythm · negative space · caesura are its home ground — re-derived here in the English tradition of negative space and restraint, not translated word-for-word).

**Source**: technical catalogue §7 (7-A language material · 7-B metaphor · 7-C effect · 7-D kinds of style · 7-E English prose mechanics).

## Input Contract

- **Prose to rewrite**: the relevant scene of `draft_<n>_<scene>.md`, or a quoted sentence.
- **design.md**: `<working-dir>/design.md` (direction of prose style).
- **persona**: `${SOUL_VOICE_HOME:-$HOME/.soul-voice-teller}/persona.md` (voice & brushwork · concrete-sentence anchor).

## Procedure

1. Read the prose to rewrite, design.md's "direction of prose style", and persona's "voice & brushwork (concrete-sentence anchor)".
2. Inspect the prose from the viewpoint of style (§7):
   - **rhythm (7-3)**: sentence length · breathing · reading speed. The division between long sentences (thought · rumination) and short sentences (velocity · severing) (7-1)
   - **lexical precision (7-6)**: the concreteness of nouns · the force of verbs. Don't settle for "it", "thing"
   - **sensory description (7-17)**: sight · hearing · touch · smell · taste · balance
   - **metaphor (7-B)**: wary of the stale (worn out) · the mixed metaphor (collision of metaphors) · hyperbole, yet simile · metaphor · implied metaphor in the persona's voice
   - **diction & mechanics (7-E)**: the register of the vocabulary (the English analog of the kanji/hiragana split — Latinate abstraction vs Anglo-Saxon concreteness), punctuation, paragraph breaks, white space
3. Rewrite. But **do not break the voice** — checked against the persona's concrete-sentence anchor, don't stray from "this writer's prose" (7-23 brushwork · voice).
4. Aim for the **irreplaceable voice (7-23)**: prose anyone could write, into prose only this writer could write.
5. Save the rewritten prose (overwrite the draft, or keep it as a new version).

## Output

The rewritten prose (overwrite `draft_<n>_<scene>.md`, or a new version).

## Notes

- Metaphor is **the main battlefield of individuality but the greatest trap** (7-14). Stale metaphor · mixed metaphor · hyperbole breed mediocrity. Use only the metaphors that could only be born from the persona's voice.
- Don't fill with rhetoric; **let empty space and omission work** (7-25 the plain style). Hold back the AI's impulse to fill, through the persona's forbidden moves and the aesthetic of restraint.
- Prose style is **unity and variation** (7-33): carry it through the whole work, or switch it per scene · character. Follow design.md's direction of prose style.
