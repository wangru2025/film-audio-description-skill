# Project layout and schemas

Use this layout when producing a film project:

```text
project/
  project.json
  media/probe.json
  materials/manifest.json
  materials/subtitles/source.srt
  materials/character-references/
  timeline/transcript.json
  timeline/scenes.json
  timeline/candidate-slots.json
  timeline/dialogue-events.json
  timeline/visual-evidence.json
  timeline/title-credit-events.json
  bible/characters.json
  bible/locations.json
  bible/objects.json
  bible/story-state.json
  segments/segment-001/manifest.json
  segments/segment-001/observations.json
  segments/segment-001/draft-cues.json
  script/merged-draft.json
  script/review.srt
  script/review-map.json
  script/approved.json
  narration/cues/
  narration/narration-master.wav
  qc/uncertainty-report.json
  qc/timeline-audit.json
  qc/listening-review.json
  qc/duck-envelope.json
  qc/final-report.json
  output/
```

`project.json` records source path, detected media facts, preferences, current script version, approval version, per-batch approvals, stage, and output choices. Stages are `initialized`, `preferences_confirmed`, `media_analyzed`, `segments_analyzed`, `script_drafted`, `awaiting_user_review`, `script_approved`, `narration_generated`, `mixed`, `quality_checked`, and `complete`. `awaiting_user_review` means the current version is not yet approved; `approved_script_version` must identify a real approved merged artifact. Merged-draft coverage must equal the union of completed segments. An empty segment directory is never evidence of completed work.

`materials/manifest.json` records every supplied/generated artifact with type, path, SHA-256, provenance (`user`, `production`, `embedded`, or `generated`), trust level, intended use, validation result, conflicts, and which expensive step was skipped. A supplied SRT replaces full ASR only after encoding, duration, synchronization, and sampled text checks. Character references require an explicit label/role manifest; unlabeled images remain unidentified.

`script/approved.json` is independent evidence, not a project flag. It contains script version, SHA-256 of the exact merged artifact and exact review SRT, approval time, and a reference to the verbatim user message. Recompute both hashes before TTS and mixing. Omission and protected-overlap approvals reference this or another immutable approval record; an agent-authored paraphrase is invalid.

Minimum cue fields:

```json
{
  "id": "cue-0001",
  "start": 137.0,
  "text": "一个蓝色手电筒从坡上滚落。",
  "observation_ids": ["obs-0042"],
  "evidence_frames": [136.8, 137.4, 138.1],
  "reason": "重要物品首次出现",
  "confidence": 0.98,
  "requires_user_review": false,
  "placement_class": "A",
  "available_slot": {"start": 136.7, "end": 139.2},
  "computed_dialogue_overlaps": [],
  "overlap_permission": "none_needed",
  "placement_decision": "dialogue-free gap",
  "visual_event_time": 137.0,
  "temporal_displacement": 0.0,
  "atomic_facts": [
    {"role": "subject", "text": "蓝色手电筒", "priority": "required"},
    {"role": "action", "text": "滚落", "priority": "required"}
  ],
  "placement_attempts": [],
  "voice": null,
  "rate": null,
  "duration": null
}
```

Minimum observation fields:

```json
{
  "id": "obs-0042",
  "start": 136.8,
  "end": 138.1,
  "subject": "蓝色手电筒",
  "action": "从坡上滚落",
  "object": null,
  "location": "山坡",
  "evidence_frames": [136.8, 137.4, 138.1],
  "evidence_type": "visual",
  "sound_sufficient": false,
  "dialogue_support_only": true,
  "confidence": 0.98,
  "uncertainty": null
}
```

Evidence frames are numeric, ordered, within media and observation bounds, and tied to real extracted frames/contact-sheet cells. Continuous actions require distinct beginning/process/result frames. Reusing identical evidence for unrelated observations is a failure. A coverage observation with `sound_sufficient: true` still records visible subject/state, why the image is stable, what sound conveys, at least one frame, and cannot cross a shot change, entrance/exit, or meaningful action. It must not generate narration.

`timeline/visual-evidence.json` indexes every cited frame with a stable ID, exact timestamp, extracted image path, SHA-256, and source-media artifact ID. Observation/cue `evidence_ids` resolve to this index, and their declared timestamps agree with the indexed timestamps. Numeric timestamps without extracted evidence do not satisfy the gate.

Character records include ID, canonical name, aliases, visual description, voice notes, first visual appearance, first spoken line, reveal time, safe pre-reveal name, safe post-reveal name, reference asset IDs, and screen-track binding evidence.

Character records include separate `name_evidence` and `person_binding`: type, start/end, observed/source text, transcript/subtitle provenance and IDs, linked observation/frame IDs, binding steps, confidence, and conflicts. They also record `production_known_at`, `narration_allowed_after`, first spoken line, and first naming cue. Actor recognition or outside knowledge may be an unconfirmed lead, never confirmation.

When opening/end-title description is selected, `timeline/title-credit-events.json` stores exact scope enum, media end, checked opening/ending ranges, inspection evidence, raw detections, and curated events. Every raw detection is retained or linked to an exclusion reason. Each event records type, interval, exact displayed text, OCR confidence, evidence, and either matching cue IDs or an omission approval record. Empty results require evidence. Checked ending range reaches the final frame.

`timeline/dialogue-events.json` contains verified speech intervals and provenance; protected events include their reason. Synthesized cues add actual audio path, measured duration and audible interval. The auditor computes intersection rather than accepting overlap claims. `qc/listening-review.json` accounts for every required listening item and re-listen. `qc/duck-envelope.json` records automation and return-to-unity times.

`qc/final-report.json` includes reproducible audio measurements: source/output artifact hashes, commands or method, sampled intervals, source and output levels, tolerance, narration-presence measurements at cue locations, and source-presence measurements beneath narration. Assertions without measurements do not complete QC.

The primary review artifact is `script/review.srt`, the production review interchange. Each entry contains only proposed spoken narration, sequential indices, and `HH:MM:SS,mmm --> HH:MM:SS,mmm` timing. Its end is the proposed narration end (measured after TTS, otherwise an explicit estimate), not the visual-observation end. Never put reasons, confidence, IDs, or editorial notes in spoken SRT text.

`script/review-map.json` maps every SRT index to cue ID, script version, evidence, uncertainty, placement class, estimated/measured timing, and review status. Generate both deterministically with `scripts/render_review_srt.py`. If the user edits SRT, reconcile it into a new cue version before approval, preserve the reviewed file, and invalidate the old hash. The auditor requires SRT, map, and cues to agree in order, timing, and text.
