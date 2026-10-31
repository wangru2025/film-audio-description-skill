---
name: film-audio-description
description: Interactively analyze films, create reviewable time-coded Chinese audio-description scripts, and only after user approval synthesize narration, mix it with the original soundtrack, and verify the finished video. Use for short or feature-length audio-description production, script review, or remastering existing descriptions.
---

# Film Audio Description

Create accessible audio description as a staged, reviewable production. Never treat a visual caption dump as a finished script. Preserve the film's dialogue, sound design, suspense, character continuity, and the user's control over the final mix.

## Start interactively

Inspect the supplied media first. Report duration, video/audio/subtitle tracks, language evidence, and any likely existing description track. Then read [references/intake-questionnaire.md](references/intake-questionnaire.md) and ask the short adaptive questionnaire with recommended answers. Reuse preferences the user already confirmed; summarize them and ask whether to carry them forward instead of repeating every question.

Create a project with `scripts/init_project.py`. Record decisions and stage in `project.json`. Do not infer permission to process unrelated files or publish copyrighted media.

## Choose the production path

- For a short work up to about 30 minutes, one agent may analyze it end to end.
- For a longer work, read [references/long-film-orchestration.md](references/long-film-orchestration.md). Use scene-aware batches, shared structured state, overlap context, and subagents when delegation is available and authorized. Subagents write only their assigned segment artifacts; the coordinating agent owns the film-wide bible and final script.
- For script-only work, stop after reviewable script delivery.
- For an existing script or described track, preserve it and perform the requested review or revision rather than rebuilding automatically.

Before visual analysis, read [references/writing-rules.md](references/writing-rules.md). Maintain canonical character, location, object, and reveal-state records. Prefer observations before prose: record who does what, where, when, why it matters, confidence, and whether the soundtrack already conveys it.

## Draft and review

Generate machine-readable cues plus an accessible Markdown review document. Follow [references/project-schema.md](references/project-schema.md). Flag uncertain identities, illegible screen text, ambiguous actions, likely spoilers, and low-confidence speaker assignments.

For films over 30 minutes, normally deliver review batches of roughly 20 minutes, incorporating user corrections before drafting later batches. After all batches, run a film-wide continuity pass and deliver the merged script for final review.

### Mandatory approval gate

After writing or materially changing the script, set the stage to `awaiting_user_review` and stop production. Tell the user how to request changes and that `Y` will approve the current version. Accept other unambiguous approval language such as “开始混音” or “按这个制作”; ask a brief confirmation for ambiguous replies.

Do not batch-synthesize narration, mix audio, or create the final deliverable until the current script version is explicitly approved. Any addition, deletion, or meaning-changing rewrite invalidates approval. Purely mechanical timing shifts or modest rate changes do not.

## Synthesize and mix after approval

Use a natural neural voice. Default Chinese recommendations are `zh-CN-XiaoyiNeural` for animation, comedy, and family material, and `zh-CN-XiaoxiaoNeural` for restrained drama or documentary, unless the user chose otherwise. Measure real generated duration for every cue. Prefer shortening prose over exceeding `+40%` speech rate.

Use `scripts/audit_cues.py` before mixing. Narration cues must not overlap each other. Limited overlap with source dialogue is allowed when the user permits it. Keep an independent narration master so the mix can be revised without regenerating speech.

Apply ducking only while narration is actually audible. Outside narration intervals the source soundtrack must remain at its original level; never apply a permanent base reduction merely because the film has no dialogue. A short release tail after a cue is only a smooth transition back to unity, not permission to keep non-narrated sections attenuated. Default ducking is light and smooth: approximately 300 ms attack, 650 ms release, weak compression near 3:1, and clearly audible source audio under narration. Treat the timing and strength as recommended starting values, but treat narration-gated ducking and unity gain outside it as invariants.

Render to a temporary `.partial` output. Never let concurrent renders write the same target. Only replace the final deliverable after validation succeeds.

## Verify and hand off

Read [references/quality-control.md](references/quality-control.md). Run `scripts/verify_output.py` and meaningful audio checks. Confirm the narration is actually routed into the final mix, the source remains audible, duration and ending are intact, streams are valid, and no partial render is presented as finished.

Deliver the mixed video, independent narration track, accessible review script, machine-readable cue file, uncertainty report, and QC report when those outputs were requested.
