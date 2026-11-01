# Feature-length orchestration

## Pre-scan before delegation

Inspect the entire media, create the transcript/VAD timeline, detect scene boundaries, and make a low-frequency visual overview before dividing work. The scene table must cover the complete source before segment drafting begins. Split on scene or chapter boundaries, normally into 8–15 minute **analysis segments** with 15–30 seconds of context overlap. Do not cut an important dialogue or action chain merely to meet a fixed duration.

Analysis segments and review batches are different units. A roughly 20-minute review batch may combine several completed analysis segments; never use fixed 20-minute review blocks as coarse visual-analysis units. Sample adaptively: action and silent visual storytelling need dense evidence. Any observation gap over 60–90 seconds needs an explicit coverage record explaining that the image is stable or the soundtrack is sufficient, and every scene needs at least one coverage record even when it yields no cue.

## Roles

The coordinating agent owns project state, canonical names, reveal policy, segmentation, merged script, approvals, synthesis, mix, and QC. Segment agents provide structured observations and candidate cues only. When useful, assign a separate audio/speaker pass and a film-wide continuity audit.

With limited concurrency, process segments in waves. Never spawn more agents than available slots. Each agent writes only inside its assigned segment directory; do not let parallel agents edit the same bible or merged script.

## Segment work package

Provide boundaries, overlapping context, transcript, contact sheets or clips, current character/location/object bible, reveal restrictions, user preferences, and output schema. Ask for evidence-first observations with subject, action, object, location, evidence frames, importance, soundtrack sufficiency, confidence, and uncertainty. Candidate cues are a later step and must cite observations. Contact sheets spaced tens of seconds apart are only navigation aids; inspect additional frames or clips around every meaningful action.

Create this package with `scripts/prepare_segment.py PROJECT SEGMENT_ID --start SECONDS --end SECONDS`. It selects shots, slices transcript context, snapshots the current bible, extracts and hashes evidence frames, and creates `work-package.json` plus a compact `analysis-input.json`. Do not ask a segment agent to reproduce those mechanics.

The segment agent's job is visual judgment and writing. It may inspect supplied frames/clips and fill semantic fields in `analysis-input.json`: subject, visible action/state, location, evidence IDs, confidence, uncertainty, candidate narration, and required facts. It must not create executables or directly manufacture canonical manifests/evidence indexes. After analysis, the coordinator runs `scripts/finalize_segment.py PROJECT SEGMENT_ID`; that tool resolves evidence timestamps, assigns stable IDs, calculates nearby-dialogue intersections, writes canonical JSON artifacts, and rejects unresolved references.

If a segment needs denser evidence, rerun `prepare_segment.py` with additional timestamps or a denser interval. Do not solve the gap by writing `extract.ps1`, `build_segment.py`, or similar one-off tools. A genuinely new recurring operation belongs in the skill's `scripts/` directory with tests.

Overlap gives context but not duplicate output. The coordinator resolves overlapping observations and chooses one cue or none.

Segment agents propose bible changes but never edit shared bible files. After each wave, the coordinator merges character, location, object, and story-state proposals and regenerates later work packages. Do not start the next wave until this merge is complete. After the first substantive segment, all bible files cannot remain empty.

Before a wave becomes a review batch, run a dedicated identity-convergence pass. Normalize every record to one canonical `id`; merge duplicate IDs, aliases, overlapping evidence tracks, and repeated safe labels that refer to the same person. For every character visible in the batch, choose exactly one resolution: `confirmed`, `not_yet_revealed`, or `unresolved_after_evidence_review`. Confirmed characters need name evidence, person binding, and reveal time. Unresolved characters need the evidence sources actually checked, a reason, and an uncertainty item for the user. Rewrite the merged cues only after this pass.

## Iterative review

For work over 30 minutes, default to approximately 20-minute review batches assembled from analysis segments. Track approval per batch. Apply corrections to the bible and instructions for later waves. Approved batches are stable, but the final film-wide pass may propose changes; any meaning-changing merged revision requires final approval.

When the project stage is `awaiting_user_review`, freeze orchestration. Existing segments inside the current review range may be completed and merged, but do not create empty future segment directories, issue future work packages, or let agents analyze beyond the batch end. Resume only after explicit approval/correction handling changes the stage and records the batch decision.

## Film-wide audit

Run `scripts/audit_project.py` before each review batch and before final approval. Check aliases, repeated first introductions, cross-segment cause and effect, object continuity, location clarity, reveal order, observation and cue-density drift, growing cue length, dialogue similarity, duplicated overlap cues, contradictory observations, and unresolved low-confidence items. Supply the auditor the merged artifacts rather than asking it to re-watch the whole film from scratch.
