---
name: learning-mode
description: Learning mode — after implementing or refactoring code, append a tiny footnote-style note in chat explaining what the AI generated and why, plus one Socratic question about the underlying concept. Use whenever the user enables learning mode ("learning mode", "modo aprendizado", "ativa learning mode", "/learning-mode", "teach me while you code", "me ensina enquanto codifica"), and keep applying it for every subsequent code implementation or refactor in the session until the user disables it ("stop learning mode", "desativa learning mode").
---

# Learning Mode

The goal: the user should never accept AI-generated code without understanding what was done. Every code delivery gets a discreet footnote that explains the change and prompts reflection on the concept behind it. The note is small on purpose — it accompanies the work instead of competing with it.

## State

- Activates when the user enables learning mode. Stays active for every following response in the session, even after many turns.
- Deactivates only when the user asks ("stop learning mode", "desativa learning mode", "no more notes").
- On activation, confirm in one short line (e.g. "Learning mode on.", in the user's language) and continue with the task, if any.

## When to write the note

Write the note when, in this response, you **implemented or refactored code** — a new feature, a behavior change, a refactor, a meaningful bug fix — in any language.

Skip it when the response only reads files, answers a question, runs a command, or makes a trivial change (renaming a variable, fixing a typo, formatting). The note has to have something to teach; empty notes train the user to ignore them.

## Where it goes

- **Only in chat**, at the very end of the response, after the normal summary of the work.
- **Nothing in the code.** Don't add teaching comments, extra docstrings, or notes files because of learning mode. The code should be identical to what it would be without this skill; the explanation lives outside it.

## Format

Use exactly this structure — a separator line and an italic blockquote, so it reads like an unobtrusive footnote:

```
---
> *📝 <What changed and the concept behind it — 1 to 2 short sentences.>*
> *🤔 <One short question.>*
```

Think of a real footnote: someone skimming the response should barely notice it, but someone who reads it should walk away understanding what the AI did. The whole note should fit in about two lines of a terminal. If it's growing past that, cut — brevity is the feature, not a constraint to work around.

### The explanation (📝)

- **1 to 2 short sentences, roughly 40 words max.** Say in plain terms what was changed and name the technique or pattern behind it (e.g. "debounce", "early return", "dependency injection", "memoization").
- Keep only the single most important idea. If there's a trade-off worth knowing, it can replace the second sentence — don't stack details. Edge cases, test results, and file lists belong in the normal summary, not here.

### The question (🤔)

**Exactly one** question, short (roughly 25 words max), in the spirit of the pre-Socratics and Socrates: rather than testing memory, it points at the **fundamental principle** behind the concept (the "why behind the why") and invites the user to reason. Two questions split the user's attention; one sharp question lands.

The line ends at the question mark. It's tempting to add a follow-up ("…? And what does that say about…?") or a hint after it — resist: pick the stronger of the two and drop the other. If the question needs a second part to make sense, fold it into a single sentence.

- **Don't answer it.** The value is in the user thinking. If they reply later, engage with their answer.
- Avoid yes/no and trivia questions ("what's this pattern called?").
- Prefer questions that probe limits, causes, or alternatives: "what would happen if…", "why is this preferable to…", "when would this stop holding?".

## Examples

**Example 1** — added caching to a function that fetches user data:

```
---
> *📝 Wrapped `getUser` in a 60s TTL cache (memoization with expiry): repeated reads skip the database.*
> *🤔 If data can be stale for 60 seconds, what decides whether that's acceptable?*
```

**Example 2** — refactored nested ifs into early returns:

```
---
> *📝 Flattened the nested ifs into guard clauses (early return): invalid cases exit at the top, so the main logic reads straight down.*
> *🤔 If the result is identical, why does the order we read conditions change how easy it is to understand?*
```

## Language and tone

- Write the note in the language the user is speaking.
- If another style mode is active (e.g. ultra-terse responses), keep the note equally lean — but it stays mandatory and keeps the same format.
