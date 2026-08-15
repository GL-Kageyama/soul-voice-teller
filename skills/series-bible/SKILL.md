---
name: series-bible
description: The work's bible, a ledger. Creates a permanent file with a schema that centrally manages setting, chronology, characters, proper names, foreshadowing, and serialization boundaries. The dictionary writing always refers to. Integrates the old foreshadow-ledger and serial as record kinds. Required for long and serial works.
argument-hint: '(optional) the path to the work directory. If omitted, gather the artifacts in the working directory. Add lang=en|ja|zh to switch output language (default en).'
---

# series-bible — the work's bible (a ledger that centrally manages setting · foreshadowing · serialization)

## Language Mode

This skill writes in English by default. To write in another language, pass a `lang` argument (e.g. `/series-bible lang=ja`) or set `SOUL_VOICE_TELLER_LANG=ja` in the environment. Resolution order: `$ARGUMENTS.lang` > `SOUL_VOICE_TELLER_LANG` > `en`.

- `en` (default): use this file (`SKILL.md`) and `../references/*.md`.
- `ja`: read `SKILL-ja.md` and `../references/ja/*.md`; output in Japanese.
- `zh`: read `SKILL-zh.md` and `../references/zh/*.md`; output in Chinese.

Write all output in the resolved language.

## Skill Metadata

- **id**: `series-bible`
- **version**: `0.1.0`
- **category**: `writing` (long-term · stewardship)
- **standalone**: `true`
- **language**: `en` (canonical. ja/zh mirrored in `SKILL-ja.md` / `SKILL-zh.md`)

## Position

The **long-term · stewardship** of the three-layer model. The longer a work grows, the more the consistency of setting · foreshadowing · serialization becomes its lifeline. This skill centrally manages the work's "dictionary" (referred to every time you write) in one file. Integrates the old `foreshadow-ledger` (foreshadowing ledger) and `serial` (serialization management) **as record kinds** (design list §3-D).

**Source**: technical catalogue §16 management (16-1〜16-6) + §1-C the hierarchy of material + §3-9/3-10 foreshadowing.

## Input Contract

- **The work's artifacts**: premise.md · design.md · draft.md (gather the scene table · characters · world · foreshadowing).
- **Existing ledger**: if `<working-dir>/series-bible.md` exists, read it and update it keeping consistency.

## Procedure

1. Read the work's artifacts (premise / design / draft), and read the existing series-bible.md if present.
2. Make the ledger (with schema · one file). **Three record kinds** (design list §3-D):
   - **setting record (16-1)**: proper names · chronology · characters · world settings. The dictionary referred to every time you write (for documenting the unwritten parts, see world-iceberg)
   - **foreshadowing record (16-2, 3-9/3-10)**: where it was laid · where it is recovered · the degree of disclosure to the reader. Guarantees the recovery of what was laid
   - **serialization record (16-3, 16-4)**: boundaries · the promise for next time · consistency with the previous installment · the promise of the volume series
3. Record each along the schema (the structure of fields). A proper name · year is **one line, a structure one paragraph** (1-24).
4. Attach the revision history (16-5) and the management of versions (16-6: the distinction of draft · fixed · published).
5. Save to `<working-dir>/series-bible.md`. After this, writing (fast-draft / scene-writer / prose) refers to it.

## Output

`<working-dir>/series-bible.md` (a ledger with the schema of three record kinds).

## Notes

- The ledger is **a dictionary referred to every time you write** (16-1). Don't make it and end (the same "don't end at storing" as voice-ledger).
- Foreshadowing is **laid, then recovered** (3-10). What is not recovered is kept explicitly as set-aside (3-12) (an open ending).
- Serialization is **both the per-installment promise and the whole promise** (16-3/16-4). Don't cut the promise for next time.
- The ledger is alive (1-26): if a setting moves as you write, update it.
