# Audio-description writing rules

## Core sentence shape

Prefer **subject + action**, adding object or consequence when useful: “光头强按下按钮。”“女人把钥匙藏进花盆。” Avoid subjectless ambiguity and decorative prose that consumes time without improving access.

## Fit meaning into the available slot

Start from the indispensable visual change, not from a full sentence that is later trimmed. Rank facts: actor/action and plot-critical object first; direction/result second; appearance and atmosphere only when they change comprehension. Use an already established name instead of repeating clothing or relationships. Prefer one precise verb over a verb plus explanation, delete “正在”“可以看到”“画面中”“这时” and redundant causes, and avoid narrating what dialogue or effects already establish.

Draft in semantic units that may be removed from the end without damaging the core: “王磊夺过火石，转身冲向舱门” can become “王磊夺过火石” when the slot is short. Never compress by dropping the subject or replacing concrete action with a plot-summary label. Measure the chosen TTS voice at the intended rate; do not rely on a fixed characters-per-second estimate. If it does not fit, try in order: move into a nearby safe gap, remove lower-priority facts, split across two genuine visual moments, then modestly increase rate within the approved limit.

## Describe when sound alone is insufficient

- Location and meaningful scene changes.
- A character's first identification before first speech.
- Entrances, exits, silent reactions, and who performs an audible action.
- Causal action chains, object transfers, and important object state or location.
- Plot-relevant expressions, especially when they contradict speech or reveal concealed emotion.
- On-screen text needed for the story.
- Montages, time jumps, dreams, memories, surveillance, imagination, or split-screen status.
- Scale, spatial relationships, and fast action that source sound does not establish.

Do not mechanically repeat dialogue, narrate every background object, identify every blink or head turn, or read all end credits unless requested. Preserve important effects, music transitions, and purposeful silence.

Before accepting a cue, ask: **What visible information does this add that the soundtrack does not already convey?** Dialogue, subtitles, transcripts, synopses, franchise knowledge, and model memory may orient analysis, but they are not visual evidence. Do not convert audible mission briefings, broadcasts, plans, causes, or consequences into narration. Describe the visible screen, gesture, action, expression, spatial relationship, object change, or necessary on-screen text instead.

Write observations before cues. A continuing action needs evidence of its beginning, process, and result rather than one isolated still. A normal cue cites the supporting observation IDs and frame timestamps. If a nonvisual editorial clarification is exceptionally needed, label it explicitly and require user review; never disguise it as observed fact.

## Naming and continuity

Assign canonical character IDs. Name a character once before first speech; do not repeat on every line. Re-identify only after a long absence, severe disguise or costume change, confusing voices, or a discontinuous scene where comprehension requires it.

Determine identity from a film-local evidence chain. Strong evidence includes an on-screen name/title, reliable subtitle speaker label, an unambiguous spoken introduction or address, and a credit explicitly pairing actor and role. Link that evidence to the same person across shots using face, clothing, location, action continuity, companions, and voice. A transcript spelling, face recognition, actor familiarity, synopsis, or model memory is only a lead and cannot establish the character by itself. Record `identity_evidence`, first confirmed time, confidence, aliases, and contradictory clues in the character bible. When evidence is incomplete, use a stable neutral label such as “红衣男子”; ask for review rather than guessing.

Do not reveal a name before the film does. Credit text shown before a deliberate story reveal does not automatically authorize using the concealed identity in narration; preserve the film's intended reveal order unless the user explicitly requests otherwise.

Before an identity reveal, use the safe contemporary label such as “蒙面人” or “女医生.” Store the reveal time and switch names only after the film reveals it.

## Opening, logos, titles, and credits

When the user selected opening/end-title description, inspect the entire opening and ending and create a title/credit event inventory before drafting. Every detected event within the selected scope must be read or have an explicit user-approved omission.

- For a company or studio logo, read the displayed official company/studio name directly, for example: “某某影业有限公司。” Do not spend the slot describing decorative logo animation unless it carries story meaning or the user requests it.
- Read the film title as displayed. State “片名” only when it improves clarity.
- Read cast pairings in the compact form “演员名饰角色名”, for example: “张三饰李明。”
- For other credits, use “姓名，职务” or the screen's natural order: “导演，张三。”“摄影，李四。”
- Preserve the visible order. Consolidate simultaneous names only when the relationship remains unambiguous. Do not invent obscured text or silently correct uncertain OCR; inspect a clearer frame and flag unresolved text.
- Do not treat the ending as complete until the selected credit scope has been checked through the final frame.

## Confidence

Do not convert guesses into facts. Record confidence and uncertainty separately. Mark cues for review when identity, action direction, text, chronology, or speaker assignment is uncertain. Use additional frames or adjacent audio before settling an ambiguity.

## Timing and density

Silence detection alone is insufficient; continuous music is common. Combine transcript timestamps, voice activity, effects, music, scene changes, and measured TTS duration. Rank placement:

- A: no dialogue; normal narration.
- B: music or ambience; preserve important effects.
- C: limited dialogue overlap when approved and necessary for comprehension.

Prefer moving or shortening a cue over excessive acceleration. Never allow narration cues to speak over each other.
