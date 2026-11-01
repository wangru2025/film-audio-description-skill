# Quality control

## Before approval

- Every cue is supported by visible evidence and does not reveal future knowledge.
- Every cue cites valid observation IDs and frame timestamps; `sound_sufficient` observations produce no cue.
- The cue adds visible information rather than restating nearby dialogue, subtitles, broadcasts, or plans.
- The scene table spans the full film, observations cover every scene, and unexplained gaps or later-segment density collapse have been resolved.
- Continuity bibles have been merged before later segment work begins.
- Character names have film-local identity evidence and respect reveal order.
- If opening/end-title description was selected, the title/credit inventory covers the chosen scope through the final frame and every event has a cue or approved omission. Company logos use the displayed company name; cast pairings use “演员名饰角色名”.
- Canonical names, locations, and objects are consistent.
- Low-confidence claims are listed for review.
- The accessible review script matches the machine cue file.
- `scripts/audit_project.py` passes its hard gates; investigate its similarity and summary-drift findings even when a heuristic needs human judgment.

## After synthesis

- Record actual duration, voice, and rate for every cue.
- No narration-to-narration overlaps.
- Rates above `+40%` require rewriting instead.
- Meaning-changing rewrites invalidate approval; mechanical timing/rate adjustments do not.

## Mix

- Keep a separate narration master.
- Use smooth light ducking by default; source remains clearly audible.
- Duck the source only while narration is audibly active. When no narration is speaking, source gain must be unity. Source dialogue activity is irrelevant: a music-only or dialogue-free passage is not a reason to lower the source.
- Allow only the configured attack/release transition around a narration cue. After the release tail, verify that the source returns to its pre-narration level.
- Narration is routed both to the audible mix and, separately, to ducking control. Never use an audible bus only as a sidechain.
- Pad only the silent sidechain control when needed. The padded zero signal must not trigger compression or change source level, and source audio must not truncate when the last cue ends.
- One render owns one temporary target. Rename to final only after checks pass.
- Every cue within one second of dialogue is listened to in the mix. Key names, numbers, clues, punchlines, emotional lines, and action-driving commands remain intelligible; failed overlaps are moved or rewritten before increasing ducking.

## Final verification

- Output duration matches source within the allowed tolerance and contains the complete ending.
- Expected video and audio streams exist and decode.
- Narration is audibly present at sampled cue locations; absence is a failure even if the stream exists.
- Source is audibly present beneath sampled narration.
- At sampled non-narration locations before, between, and after cues, output source level matches the unducked source within the chosen encoding/limiting tolerance.
- No clipping, corrupt container, abandoned process, or `.partial` file is delivered.
- Provide a QC report with commands, results, deviations, and unresolved issues.
