---
name: voice-ledger
description: A store (ledger) for storing and reading back the writer's soul-voice. Appends the voices, departures, flow, and resonance of evaluation heard in introspection (the A/B/C questions) in a one-entry form, and reads them back for ideation, escaping a stall, and updating the persona. Use standalone or alongside the other writing skills.
argument-hint: '(optional) "store" or "read", and the voice content if storing. Add lang=en|ja|zh to switch output language (default en).'
---

# voice-ledger — the store of the soul's voice (store + read)

## Language Mode

This skill writes in English by default. To write in another language, pass a `lang` argument (e.g. `/voice-ledger lang=ja`) or set `SOUL_VOICE_TELLER_LANG=ja` in the environment. Resolution order: `$ARGUMENTS.lang` > `SOUL_VOICE_TELLER_LANG` > `en`.

- `en` (default): use this file (`SKILL.md`) and `../references/*.md`.
- `ja`: read `SKILL-ja.md` and `../references/ja/*.md`; output in Japanese.
- `zh`: read `SKILL-zh.md` and `../references/zh/*.md`; output in Chinese.

Write all output in the resolved language.

## Skill Metadata

- **id**: `voice-ledger`
- **version**: `0.1.0`
- **category**: `writing` (writer layer · permanent)
- **standalone**: `true`
- **language**: `en` (canonical. ja/zh mirrored in `SKILL-ja.md` / `SKILL-zh.md`)

## Position

The second skill of the **writer layer** in the three-layer model. writer-persona "fixes the voice" (present-tense setting); this skill "stores the voice" (past-tense diary). It accumulates the voices heard in introspection across works, and reads them back.

**Distinction from persona**: the persona is "I write like this", the store is "I have written like this". **Separate files.**

## Input Contract

- **When storing**: the voice (five kinds) · its source · its context. Received via argument-hint or dialogue.
- **When reading**: the purpose of reading back (start of ideation / persona update / a stall / fast-draft going dry).
- **Save location**: `${SOUL_VOICE_HOME:-$HOME/.soul-voice-teller}/voice-ledger.md`

## Store (five kinds of voice)

| Kind | Source | Example |
|---|---|---|
| The voice of ideation | B questions · a flash | a fragment heard as "this material answers my recurring question this way" |
| The voice of the draft | C questions · a record of a departure | where the character left the plan and began to move · their line |
| The moment the writing took off | flow | the conditions under which emergence happened (material · constraint · empty space). Record **the conditions themselves** as a clue for reproducing it |
| The moment you touched a forbidden move | A-4 | almost broke it · broke it. Whether it became depth or breakage |
| The resonance of evaluation | reader reaction | what resonated · what didn't, in external evaluation. Keep only the sound, without being swept along |

**When to store (evoke, don't force)**: only when a voice is heard. On days nothing is heard, don't force a line; don't add empty lines.

**The form of one entry** ([../references/voice-store.md](../references/voice-store.md)):

| Field | Content |
|---|---|
| Date · work · scene | when · in which work · where it was heard |
| The voice heard | **verbatim. Do not summarize — the voice dies in summary** |
| Context (which question it answered) | quote the question form (A/B/C) so the same question can re-evoke it |
| Used / unused | a mark for connecting later |

```markdown
- [x] 2026-08-14 / The Man Walking at Night / chapter 2 · the climactic line
  voice: this man doesn't "not apologize" — he "cannot apologize". Because if he apologizes, something ends.
  context: C-1 (did this line come from the plan's demand, or from the character himself?)
  used: the climax of chapter 2. The resonance of evaluation is here too (originality was high).
```

## Read (do not end at storing)

The store exists not only to store but to **read**. A ledger never read becomes a dumping ground.

- **At the start of ideation** (premise's B questions) — call the previous work's voice into the new question
- **When updating writer-persona** — read the accumulated voices as "where the soul-story went", and revise the setting
- **At a stall** — the water source when you cannot write
- **When fast-draft goes dry** (C-4, nothing heard → fall back to following the plan) — before falling back, listen to the store

## Procedure

1. Confirm "store" or "read" (via argument-hint or dialogue).
2. **Store**: receive the voice, decide which of the five kinds it is, and append it to `voice-ledger.md` in the one-entry form. Keep the voice **verbatim**, and always attach the context (which question).
3. **Read**: reread the store for the purpose, quote the relevant voice, and present it as update material · the source of ideation · a water source.

## Notes

- **The store itself does not judge** — it stores, and reads. The choice of "what counts as a voice" is made by the question-asking skills (persona / premise / fast-draft).
- The soul-story and the voice are **the human's (user's)**. The AI is a mirror that reflects · stores · returns them, not the author.
- When storing the resonance of evaluation, **do not be swept along** by external evaluation — don't copy scores or verdicts; keep only the "sound" that resonated with you.
