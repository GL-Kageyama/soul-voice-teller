# The 20 skills

The reference of what each skill does (input → output). See [Usage](usage.md) for how to call them.

## The main line

| skill | role | input → output |
|---|---|---|
| `writer-persona` | draw out the writer's setting in dialogue (A questions · ground = real experience) | dialogue → `${SOUL_VOICE_HOME}/persona.md` (soul-story / aesthetic sense / voice & brushwork / forbidden moves / subject-matter preference) |
| `premise` | ideation (B questions · ground = persona + store) | seed + persona + store → `<work>/premise.md` (logline / core question / theme / genre promise / direction of prose style / reader image & promise) |
| `plot-design` | the design document (fast-draft's input specification), revised against the promise + voice (C questions · ground = premise + persona) | premise + persona + store → `<work>/design.md` (required design + optional preparation) |
| `fast-draft` | the draft (the aesthetic of expression and restraint + the introspection loop) | design + persona + store → `<work>/draft_*.md` + plan update + voices for the store |
| `voice-ledger` | store the voice, read it back | the voice (ideation / design / draft / flow / forbidden moves / resonance of evaluation) → `${SOUL_VOICE_HOME}/voice-ledger.md` |

## Optional preparation

Called optionally from plot-design. Writing works even with blanks.

| skill | role | input → output |
|---|---|---|
| `narration-design` | detailed design of narration (type of point of view · reliability · distance · tense · nesting · speech style) | design → the elaboration of design.md's "narration" |
| `character-forge` | character design (desire · wound · voice · change arc · inner conflict) | design + premise + persona → the elaboration of design.md's "character" |
| `character-in-action` | make the character setting function in the scene (staged disclosure · making the setting function) | design → append linkage points to the scene table |
| `character-bond` | render the relationship between two characters (the axis of want · reversal/mirror · the turning point · bidirectionality · embodiment) | design + draft → the elaborated relationship between the two |
| `worldbuild` | world design (setting · rules · internal consistency · the setting ⇔ story connection) | design + premise + persona → the elaboration of design.md's "world" |
| `world-iceberg` | the extent to document the unwritten world (by touching probability) | design → append the documentation list |
| `research-verify` | checking historical fact · period detail · specialist knowledge (keep errors out) | design/draft → a list of errors + corrections |

## The quality of writing · revision · long-term

| skill | role | input → output |
|---|---|---|
| `prose` | sharpen by prose style (rhythm · sense · an irreplaceable voice) | prose/scene + persona → rewritten prose |
| `scene-writer` | write one scene deeply (the design of empty space · show, don't tell · the seams of the scene) | design + persona → draft_<n>_<scene>.md |
| `series-bible` | the work's bible (a ledger that centrally manages setting · foreshadowing · serialization) | the work's artifacts → series-bible.md |
| `revise-for-reader` | revise by the reader's experience (immersion · page-turner · promise · rereading) | draft + design → the revised draft.md |
| `entertainment` | add the pleasures of entertainment without breaking restraint (hook · page-turner · twist · catharsis · pacing · empathy) | draft + design → the revised draft.md |
| `whole-work-review` | review the work as a whole — one book that closes (structural coherence · foreshadowing payoff · density distribution · redundancy · world-closed vocabulary · restraint balance) | draft + series-bible → the revised draft.md |

## Delivery

| skill | role | input → output |
|---|---|---|
| `package` | wrap the finished work for the reader (title + hooking subtitle · catch copy · synopsis · image prompt · tags), checked against the reader's first impression | draft + premise + series-bible + persona → `<work>/package.md` |
| `theme-song` | condense the finished work into one theme song (song title · structured lyrics · style of music · vocal · song description · placement), checked against the work's soul (the theme + the scenes where emotion surfaces) | draft + premise + series-bible + persona → `<work>/theme-song.md` |
