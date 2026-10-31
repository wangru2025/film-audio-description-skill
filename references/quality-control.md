# Quality control

## Before approval

- Every cue is supported by visible evidence and does not reveal future knowledge.
- Canonical names, locations, and objects are consistent.
- Low-confidence claims are listed for review.
- The accessible review script matches the machine cue file.

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

## Final verification

- Output duration matches source within the allowed tolerance and contains the complete ending.
- Expected video and audio streams exist and decode.
- Narration is audibly present at sampled cue locations; absence is a failure even if the stream exists.
- Source is audibly present beneath sampled narration.
- At sampled non-narration locations before, between, and after cues, output source level matches the unducked source within the chosen encoding/limiting tolerance.
- No clipping, corrupt container, abandoned process, or `.partial` file is delivered.
- Provide a QC report with commands, results, deviations, and unresolved issues.
