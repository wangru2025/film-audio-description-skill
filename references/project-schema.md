# Project layout and schemas

Use this layout when producing a film project:

```text
project/
  project.json
  media/probe.json
  timeline/transcript.json
  timeline/scenes.json
  timeline/candidate-slots.json
  bible/characters.json
  bible/locations.json
  bible/objects.json
  bible/story-state.json
  segments/segment-001/manifest.json
  segments/segment-001/observations.json
  segments/segment-001/draft-cues.json
  script/merged-draft.json
  script/review.md
  script/approved.json
  narration/cues/
  narration/narration-master.wav
  qc/uncertainty-report.json
  qc/timeline-audit.json
  qc/final-report.json
  output/
```

`project.json` records source path, detected media facts, preferences, current script version, approval version, per-batch approvals, stage, and output choices. Stages are `initialized`, `preferences_confirmed`, `media_analyzed`, `segments_analyzed`, `script_drafted`, `awaiting_user_review`, `script_approved`, `narration_generated`, `mixed`, `quality_checked`, and `complete`. `awaiting_user_review` means the current version is not yet approved; `approved_script_version` must identify a real approved merged artifact. Merged-draft coverage must equal the union of completed segments. An empty segment directory is never evidence of completed work.

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

Use a coverage observation with `sound_sufficient: true` for a scene or long stable interval that needs no cue. Such observations prove analysis coverage but must not generate narration. Continuous actions require multiple evidence frames spanning beginning, process, and result.

Character records include ID, canonical name, aliases, visual description, voice notes, first visual appearance, first spoken line, reveal time, safe pre-reveal name, and safe post-reveal name.

The primary review artifact is accessible Markdown with timestamp, cue, reason, confidence/uncertainty, recommended rate, and overlap status. JSON supports machines; do not require the user to edit it.
