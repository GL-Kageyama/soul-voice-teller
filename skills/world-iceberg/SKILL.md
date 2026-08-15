---
name: world-iceberg
description: A preparation skill that decides the extent to document the unwritten world. Prioritizes the unwritten parts the story is likely to touch, in order of the probability of touching them, and draws the line between what to document and what not to. Keeps the world's thickness and consistency without the burden of material. Optional preparation. After worldbuild.
argument-hint: '(optional) the path to design.md. If omitted, look for design.md in the working directory. Add lang=en|ja|zh to switch output language (default en).'
---

# world-iceberg — documenting the unwritten world (how far to write down what is below the surface)

## Language Mode

This skill writes in English by default. To write in another language, pass a `lang` argument (e.g. `/world-iceberg lang=ja`) or set `SOUL_VOICE_TELLER_LANG=ja` in the environment. Resolution order: `$ARGUMENTS.lang` > `SOUL_VOICE_TELLER_LANG` > `en`.

- `en` (default): use this file (`SKILL.md`) and `../references/*.md`.
- `ja`: read `SKILL-ja.md` and `../references/ja/*.md`; output in Japanese.
- `zh`: read `SKILL-zh.md` and `../references/zh/*.md`; output in Chinese.

Write all output in the resolved language.

## Skill Metadata

- **id**: `world-iceberg`
- **version**: `0.1.0`
- **category**: `writing` (design layer · optional preparation)
- **standalone**: `true`
- **language**: `en` (canonical. ja/zh mirrored in `SKILL-ja.md` / `SKILL-zh.md`)

## Position

Optional preparation (technical catalogue §1-C documenting the unwritten world). Of the world worldbuild "made", decides how far to **document the parts not written**. The extent of documentation is itself the crux of worldview design (§1-C opening) — too much is a burden, too little is contradiction. After worldbuild.

**Source**: technical catalogue §1-C (1-21〜1-26).

## Input Contract

- **design.md**: `<working-dir>/design.md` (world section = already designed · scene table).
- **Prerequisite**: the world already designed by worldbuild.

## Procedure

1. Read design.md's "world" and "scene table".
2. Order the unwritten parts **by the probability of touching them** (1-21): document the unwritten parts the story is likely to touch; keep in mind the parts it won't touch first.
3. Decide the extent of documentation (1-22〜1-25):
   - **the purpose of documentation (1-22)**: for consistency · for depth · for reducing hesitation while writing. The granularity changes with the purpose
   - **the hierarchy of material (1-23)**: separate the material the reader sees (map · chronology) from the material only you see (backstage settings · origin)
   - **the unit (1-24)**: a proper name · year · rule is one line, a structure is one paragraph, a spatial expanse is a figure
   - **the freedom not to document (1-25)**: some empty space is preserved only by not verbalizing it
4. Append to design.md's "world" the minimal material so "it does not contradict the moment it is touched" (the standing of the unseen world 1-19).
5. State that the parts not documented are "kept in mind" (don't make them a burden of material).

## Output

Append to design.md's "world" (the documentation list of the unwritten parts = in order of touching probability · the hierarchy of material · the unit · the parts not documented).

## Notes

- **The purpose of documentation is consistency · depth · reducing hesitation** (1-22). Material without a purpose is a burden.
- Prioritize by touching probability (1-21). Don't make material for the parts you won't touch.
- Keep **the freedom not to document** (1-25). The empty space preserved by not verbalizing it is the same root as the aesthetic of restraint (leave space).
- Material is alive (1-26): if the world moves as you write, update it (linked to fast-draft's departure).
