---
name: worldbuild
description: A preparation skill that designs the world. Fixes setting, society, culture, history, rules, and internal consistency, and writes how the setting loads the story into design.md's "world". The supernatural and magic carry cost and constraint. Optional preparation (writing works without it). After plot-design.
argument-hint: '(optional) the path to design.md. If omitted, look for design.md in the working directory. Add lang=en|ja|zh to switch output language (default en).'
---

# worldbuild — world design (setting · rules · consistency)

## Language Mode

This skill writes in English by default. To write in another language, pass a `lang` argument (e.g. `/worldbuild lang=ja`) or set `SOUL_VOICE_TELLER_LANG=ja` in the environment. Resolution order: `$ARGUMENTS.lang` > `SOUL_VOICE_TELLER_LANG` > `en`.

- `en` (default): use this file (`SKILL.md`) and `../references/*.md`.
- `ja`: read `SKILL-ja.md` and `../references/ja/*.md`; output in Japanese.
- `zh`: read `SKILL-zh.md` and `../references/zh/*.md`; output in Chinese.

Write all output in the resolved language.

## Skill Metadata

- **id**: `worldbuild`
- **version**: `0.1.0`
- **category**: `writing` (design layer · optional preparation)
- **standalone**: `true`
- **language**: `en` (canonical. ja/zh mirrored in `SKILL-ja.md` / `SKILL-zh.md`)

## Position

Optional preparation (technical catalogue §1 world). Deepens plot-design's "world" (may be blank) to the granularity at which fast-draft can write "a story that could only happen in this world". Writing works without it, but in genres where the world moves the story (SF · fantasy · historical) it is close to required.

**Source**: technical catalogue §1 (1-1〜1-20).

## Input Contract

- **design.md**: `<working-dir>/design.md` (the world section. Blank or `?` is fine).
- **premise.md**: `<working-dir>/premise.md` (the genre promise — the world's rules become the promise).
- **persona**: `${SOUL_VOICE_HOME:-$HOME/.soul-voice-teller}/persona.md` (subject-matter preference · the settings that draw you).

## Procedure

1. Read design.md's "world", premise's "genre promise", and persona's "subject-matter preference".
2. Fix the core of the world (§1). Weight it by genre:
   - setting · place (1-1) · era (1-2) · geography · nature (1-3)
   - social structure (1-4) · politics · economy · law (1-5) · culture · custom (1-6) · religion · myth (1-7) · history · chronology (1-8)
   - technology · level of civilization (1-9) · science · theory (1-10 SF) · the rules of the supernatural · magic (1-11 the fantastic. **Don't make it omnipotent; give it cost and constraint**)
   - language · names (1-12) · the world's promise (1-13 the contract with the reader)
3. Check **internal consistency (1-14)**: how far the rules do not break. Don't make too many exceptions to magic · technology.
4. Fix **the setting ⇔ story connection (1-15)**: so the setting is not mere background but moves the story (how the world's rules bind conflict · choice · ending). This is the key to "a story that could only happen in this world".
5. Fix the policy of **conveying the setting (1-16)**: don't make the setting all explanation (show it through description · action).
6. Write into design.md's "world". Undecided may be left as `?`.

## Output

The elaboration of design.md's "world" (setting · society · culture · history · rules · internal consistency · setting ⇔ story connection · the policy of conveying the setting).

## Notes

- The supernatural · magic **carry cost and constraint** (1-11). Omnipotent magic erases conflict.
- A setting **means something only when it moves the story** (1-15). A list of background is material, not a novel.
- **Internal consistency** (1-14) over originality. The world's rules not breaking is what protects the reader's immersion.
- Conveying the setting is "description", not "explanation" (1-16). All-explanation breaks immersion (the same root as the aesthetic of expression and restraint).
- **The world is a carrier (器) of the hook.** The setting · rules you fix are what the reader will trust; the hook engine ([../references/hook-engine.md](../references/hook-engine.md)) breaks that trust to plant the unknown.
