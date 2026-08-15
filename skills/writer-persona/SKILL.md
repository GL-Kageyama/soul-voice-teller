---
name: writer-persona
description: Draws out the writer's (the human = user's) soul, voice, and preferences through dialogue and creates a permanent profile (persona) that every other writing skill writes against. Use before starting a work, or when you want to update the persona.
argument-hint: '(optional) the path of the persona to update, or "new" / "update". If omitted, confirm in dialogue. Add lang=en|ja|zh to switch output language (default en).'
---

# writer-persona — the writer's setting (fix the voice by checking against real experience)

## Language Mode

This skill writes in English by default. To write in another language, pass a `lang` argument (e.g. `/writer-persona lang=ja`) or set `SOUL_VOICE_TELLER_LANG=ja` in the environment. Resolution order: `$ARGUMENTS.lang` > `SOUL_VOICE_TELLER_LANG` > `en`.

- `en` (default): use this file (`SKILL.md`) and `../references/*.md`.
- `ja`: read `SKILL-ja.md` and `../references/ja/*.md`; output in Japanese. The source concepts (内省 / 余白 / 間) live here.
- `zh`: read `SKILL-zh.md` and `../references/zh/*.md`; output in Chinese (留白 / 含蓄).

Write all output in the resolved language.

## Skill Metadata

- **id**: `writer-persona`
- **version**: `0.1.0`
- **category**: `writing` (writer layer · permanent)
- **standalone**: `true`
- **language**: `en` (canonical. ja/zh mirrored in `SKILL-ja.md` / `SKILL-zh.md`)

## Position

The first skill of the **writer layer** in the three-layer model. All later introspection (premise's ideation · fast-draft's drafting) writes against the persona fixed here.

**Who writes**: the human is the author, the AI is a drafting device, the persona is a mirror of the author. The soul and voice of the persona made by this skill are **the human's (user's)**. The AI is a mirror that draws them out and holds them in dialogue — not the author.

## Input Contract

- **Input**: dialogue with the user (the A questions). ground = **the writer's real experience**.
- **Absolute principle**: the AI **only asks; it does not fabricate a "wound" of its own**. It draws out and holds the user's answers. It must not invent a fictional biographical pain or a "plausible soul-story". Introspection without a ground is fabrication.

## Procedure

1. First, prompt the user to create the **dedicated folder (repository)** that holds the writer's accumulated state (persona + store). This becomes the home of the writer's permanent state:
   - "Let's put your accumulated voice in a dedicated folder (git repository) inside your workspace. Where should it go? (e.g. <workspace>/voice/)"
   - **Recommend git** — the persona is an irreversible soul-story, the store is a growing diary. They need history and backup. But **private** (do not push to a public remote).
   - Save location = the folder the user names (given explicitly by `SOUL_VOICE_HOME`; if unset, `~/.soul-voice-teller/`). Create it if absent.
   - persona location: `persona.md` in that folder. If it already exists, read it and treat this as an **update** (reread and revise). If not, **create new**.
   - **Do not put the persona inside the soul-voice-teller (distribution skill) repository** — it is per-writer state, not to be fixed or committed.
   - **Also initialize voice-ledger.md** — if `voice-ledger.md` does not exist in that folder, create it with the store's header (the form in [../references/voice-store.md](../references/voice-store.md)). The persona and the store are the paired permanent state of the writer layer; prepare both when the persona is made.
   - On update, also reread the store in [../references/voice-store.md](../references/voice-store.md) and reflect "where the soul-story went".
2. Ask the A questions ([../references/introspection.md](../references/introspection.md) chapter A) **one item at a time**, in dialogue, drawing out the answers. Five items in all:
   - **A-1 the soul-story** (why you write · the question you return to)
   - **A-2 aesthetic sense** (what makes good prose · the aesthetic you believe)
   - **A-3 voice & brushwork** (the breathing of the sentence · the concrete-sentence anchor)
   - **A-4 forbidden moves** (what you do not write)
   - **A-5 subject-matter preference** (what you are drawn to)
3. Honor the conditions on the questions (introspection §0):
   - **open** — don't let it end in yes/no
   - **checked against the writer's setting** — don't allow an answer that could be anyone's
   - **ask for checking** — not judgment, but a report of the voice held against real experience
   - **evoke, don't force** — don't press to draw it out. Items the user doesn't want to answer may be left "undecided"
4. Summarize all items into persona.md and save. The **concrete-sentence anchor** (a real sentence **taken out** in A-3) is kept verbatim — not an adjective, the sentence itself is the substance of the voice. **If none comes, leave it "undecided"** (forcing is fabrication. The pipeline runs even undecided).
5. Finally, confirm the persona is in the form (the output format below) that premise / plot-design / fast-draft can read.

## Output

`${SOUL_VOICE_HOME:-$HOME/.soul-voice-teller}/persona.md` (the permanent profile)

```markdown
# persona (the writer's setting)

> Drawn out in dialogue from the writer's real experience. Not fabricated by the AI.

## The soul-story (why you write)
(the story you want to write again and again · the recurring question · the unsettled question)

## Aesthetic sense (what makes good prose)
(good / bad sentences · the aesthetic you believe · the negative space you won't fill)

## Voice & brushwork (how you write)
(the breathing of the sentence · words you like / avoid · the distance you want the reader to take)
- concrete-sentence anchor: (a real sentence, taken out by checking. May be undecided. Keep verbatim)

## Forbidden moves (what you do not write)
(what you will absolutely never write · forms you don't want · the price of breaking them)

## Subject-matter preference (what you are drawn to)
(subjects · settings · times of day · seasons · the people and relationships that draw you)
```

## Notes

- The persona is "I write like this" (present-tense setting). The store (voice-ledger) is "I have written like this" (past-tense diary) — a **separate file**.
- The soul-story, voice, and forbidden moves are **the user's**. Until the user answers, leave them "undecided"; the AI must not fill them in.
- **The concrete-sentence anchor is optional.** Without it, the breathing · liked/avoided words · forbidden moves · subject matter still fix the voice and the pipeline runs. The anchor is a strong bonus that lets the voice be checked concretely — not a requirement.
- If someone tries to proceed to premise / fast-draft without a persona, prompt this skill first (with "who writes" unsettled, both design and draft become "no one's prose").
