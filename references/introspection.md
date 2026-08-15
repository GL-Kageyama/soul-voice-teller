# Introspection Questions — Asking for the Writer's Voice

> Implementation of the design principle "the inner voice is the source of everything; introspect and listen."
> Introspection has two roles: **the source of ideas** (to draw inspiration from the voice) and **the detector of flow** (to loosen the design in the middle of writing).
> There are three layers of question: **A the writer's setting** (permanent) → **B ideation** (per work) → **C the draft loop** (per scene).
> The voice you hear is stored in **D (the store)** and read back across works ([voice-store.md](voice-store.md)).

---

## 0. The structure of introspection

Introspection is not "judgment" but "**checking against**" (照合). When you report a voice you heard, you must say **what it was checked against** (its ground). Introspection without a ground is "fabrication", not "observation". Judgment happens at a different stage (the criteria for deciding whether a departure deepens or breaks).

| Question layer | Ground (what it is checked against) | What it is compared to |
|---|---|---|
| A the writer's setting | **the writer's real experience** | the works this writer has actually written, the questions they actually carry, their forbidden moves. The AI asks the human and holds the answers as the ground. The AI does not fabricate its own "wound" |
| B ideation | **persona + the store** | this writer's preferences, forbidden moves, past voices. "How would this writer choose?" is checked |
| C the draft loop | **the plan (scene table)** | the generated prose is checked against the plan to judge whether "the character has left the plan" |

```
① Ask (turn your ear to the voice)
② Check (hold it against the ground. Do not judge)
③ The voice has left the plan and begun to move → allow the departure (departure over compliance)
④ Judge by the criteria for departure (deepens or breaks)
⑤ If it deepens, update the plan and follow
⑥ Store the heard voice · the departure · the flow in the store (the store of the soul's voice)
```

**Conditions every question must satisfy**:

- **Open** — it cannot be answered with yes/no
- **Checked against the writer's setting** — it does not allow an answer that could be anyone's. It pulls toward soul, voice, forbidden moves
- **Asks for checking** — not judgment, but a report of the voice held against the ground
- **Evokes, does not force** — forcing the asking averages it out. On days nothing is heard, fall back to following the plan

**Who asks**: A is dialogue (skill ↔ user). B and C are introspection the AI asks of itself.

---

## A. Questions for the writer's setting (writer-persona · permanent profile)

The first questions, to fix the voice. Drawn out **in dialogue with the human (user)**, kept permanent across works. The output is a profile (soul-story · aesthetic sense · voice · forbidden moves · subject-matter preference), against which all later introspection checks. The ground is **the writer's real experience** — the AI does not fabricate its own "wound".

### A-1 The soul-story (why you write)

> ground: **the writer's real experience**. The questions below are asked of the human (user). The AI only draws out and holds the answers; it does not invent a "wound" of its own. It extracts the **recurring question** from the works the writer has written.

- What is the story you **want to write again and again**? What is its core?
- What question do your works **return to again and again**? What question is left unsettled?
- When you write which theme do you feel **yourself being elevated**?
- What question are you trying to resolve over a lifetime?
- Which work did you first decide to "write" after encountering? What in it made you?

### A-2 Aesthetic sense (what makes good prose)

- For you, what is a "good sentence"? A "bad sentence"?
- What aesthetic do you believe in? (negative space · restraint · honesty · piling on…) Where did you learn it?
- What negative space do you not want to fill? Why not fill it?

### A-3 Voice & brushwork (how you write)

- What is the **breathing** of your sentences? Long or short, where do you take breath?
- **Concrete-sentence anchor** (optional · may be undecided) — a **real sentence** of yours that carries your "concrete observation", **taken out** (checked), not written (invented). If none comes, "undecided" is fine:
  1. a line of your own that, on rereading, you thought "this is me"
  2. a concrete thing you actually saw (a smell, a gesture, a light) that you wanted to tell someone about
  3. a line by someone else that you thought "this is the line I wanted to write"
- What words do you like? What words do you avoid?
- In your style, what distance do you want the reader to take?

### A-4 Forbidden moves (what you do not write)

- What will you **absolutely never write**? (easy simile · explanation · sentimentality · pretty words…)
- What genre · form · manner of telling do you not want to write?
- If you broke your own forbidden moves, what depth would it reach? What price would it cost?

### A-5 Subject-matter preference (what you are drawn to)

- What **subjects · settings · times of day · seasons** are you drawn to?
- What kind of person draws you? What kind of relationship?
- Where does your story always stand?

---

## B. Questions for ideation (premise · drawing inspiration from the voice)

Questions per work. Choose the theme and logline checked against the soul-story (which is the human's). The AI asks itself. The ground is **persona + the store**. But persona has two layers at different temperatures:

- **The soul's voice (HOW) = soul-story · aesthetic sense · voice · brushwork · forbidden moves** → **checked at low temperature** (kept faithfully. If this wavers, the prose becomes "no one's prose").
- **Subject-matter preference (WHAT) = A-5** → **ideated at high temperature** (used as a seed. Pulling too close makes every work the same = mediocre).

Subject-matter preference is "**an affinity** (the direction this writer is drawn)" not "**a template** (a model to trace every time)". If it matches too closely, consciously move away (let it waver). It is precisely "when the initial idea naturally departs" that you are elevated (persona A-1).

### B-1 Theme (binding soul and work)

- How does this material answer your **question you keep writing**?
- From your soul-story, which story rises now?
- Behind this story, **what of your own is moving**?
- Where is the core that might elevate you as you write?

### B-2 Logline (sounding it in your voice)

- Said in your voice, how does this logline sound?
- Don't summarize this story — **in your own words**, say its core.
- What does this story ask of you? (held against the soul-story)

### B-3 Character & world (what draws you)

- In this world, who is the character you most want to write?
- Which of the characters you have written does this one resemble? Differ from?
- Where in this world is the place that draws you?

### B-4 Seed × subject-matter preference (mixing wavering into the affinity)

- Is the season · setting · time of day · character · relationship of this seed **overlapping too much** with your subject-matter preference (A-5)? If so, what do you deliberately shift (the inverse of the preference · outside the preference · recombining)?
- A mismatch is "**welcomed as a wavering**", not "pulled back in". A deliberate departure is recorded with `?` and kept.
- **Voice · aesthetic sense · forbidden moves (HOW) must not waver.** Only the subject matter (WHAT) wavers.

---

## C. The introspection loop during drafting (fast-draft · detecting flow)

Run it after finishing each scene. It precedes the judgment that loosens the design. The ground is **the plan (scene table)** — the generated prose is checked against the plan to judge whether there is a departure.

### C-1 Detecting flow (has the voice begun to move?)

- Is this character moving as planned? Or **moving on their own**?
- Where is this scene heading now? Is it trying to go somewhere other than the plan?
- Did this line · this action come from the plan's demand, or **from the character themselves**?
- What is my inner voice asking for now?

### C-2 Judging the departure (deepens or breaks)

- Does this departure **deepen** the story, or **break** it?
- What effect does this departure have on the promise · foreshadowing · ending?
- Does it violate my forbidden moves (A-4)? If so, does that violation become depth?

### C-3 Updating the plan

- How do I write this departure into the plan? Which scene · which foreshadowing changes?
- Am I mechanically regressing to the old plan?

### C-4 Am I forcing it? (the limit)

- Am I **forcing the flow**? Pretending to hear what I don't hear?
- If I don't hear it, fall back to following the plan. The voice is something to wait for, not something to push out.

---

## D. Handling the heard voice (the store)

- The heard voice · departure · flow · flash is stored in [voice-store.md](voice-store.md) (the `voice-ledger`)
- The stored voice is read back for later ideation (B) · escaping a stall (C-4) · updating writer-persona
- Even a voice you cannot use right now, stored, connects to something later
