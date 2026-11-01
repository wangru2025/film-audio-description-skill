# Timing and dialogue-safe mixing

## Build a speech-aware timeline

Combine reliable subtitle timings, ASR, voice activity, waveform inspection, and listening. ASR text may be wrong; use it to locate speech, then verify important lines by ear or subtitle. Mark dialogue, breaths that belong to a line, narratively important effects, music transitions, and intentional silence. Add modest guard margins around dialogue boundaries, normally about 150–300 ms, then adjust by listening rather than treating the margin as law.

For each cue, record the available slot, measured synthesized duration, nearby dialogue/effects, overlap permission, and placement decision. A gap is usable only when narration plus natural entry/exit fits; do not force a cue into the numeric silence if it clips the last syllable, first syllable, laugh, gasp, door slam, reveal sting, or other meaningful sound.

## Placement order

Try these options in order:

1. Place the cue in a genuine nearby gap while keeping it close enough to the visual event.
2. Rewrite to retain subject + concrete action and remove lower-priority detail.
3. Split only when two visual moments naturally support two cues.
4. Increase speech rate modestly after measuring the actual voice; stay within the approved maximum.
5. If the user permits limited overlap, overlap only the least important portion of dialogue or ambience and record why it was necessary.

Never cover a character's first identification, key name/number, punchline, whispered clue, emotional confession, command that drives action, or line needed to understand the next scene. Avoid starting narration and dialogue on the same instant. If overlap is unavoidable, prefer a dialogue tail or redundant phrase, keep the original speech intelligible, and review the mixed result by listening—not waveform alone. User permission for “limited overlap” is not blanket permission to narrate across dialogue.

## Gain automation and ducking

Use the narration's actual audible envelope—not the whole export duration—as the sidechain/control signal. Apply smooth automation or compression only around narration: a useful starting point is about 300 ms attack, 650 ms release, and light reduction near a 3:1 ratio. Tune by listening. The aim is separation, not suppression: the source dialogue, music, and effects remain recognizable beneath narration.

Outside narration plus its short transition tails, source gain is exactly unity. Do not lower the whole film, do not duck because dialogue is absent, and do not let padded control silence hold the compressor open. Route narration audibly to the final mix as well as separately to the control path. Keep source, narration master, control envelope, and mixed output separable for revision.

## Dialogue-protection verification

Listen to every cue that overlaps or sits within one second of dialogue, plus samples from ordinary non-overlap cues. Compare source and mix at the beginning, middle, and end of the film. Confirm that words remain understandable, important effects retain their function, narration is audible without sounding detached, and source level returns smoothly to unity after every cue. Move or rewrite a cue that fails; stronger ducking is not the default fix.
