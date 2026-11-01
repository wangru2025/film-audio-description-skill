# Film Audio Description Skill

[简体中文](README.zh-CN.md) | English

[Changelog](CHANGELOG.md)

An interactive Codex skill for producing reviewable Chinese audio description for short videos and feature-length films.

The skill inventories the film and any supplied SRT, cast lists, character/costume photos, or production notes; then it analyzes only what those trusted materials do not already provide. It maintains visual evidence and character continuity and creates a standard SRT narration script for review. It does **not** synthesize narration or mix a final film until the user explicitly approves the exact SRT/cue version.

## Highlights

- Accessible, time-coded Chinese audio-description scripts
- Required user review and approval before narration or mixing
- Standard SRT review delivery with a machine-readable evidence map
- Material-aware workflow: validated dialogue SRT can replace full ASR, while labeled cast references accelerate identity binding
- Scene-aware feature-film segmentation and subagent orchestration
- Evidence-linked observations and cues, with anti-summary quality gates
- Project audit for dialogue restatement, sparse coverage, continuity-state failures, and long-film drift
- Film-local character identification, compact slot-aware writing, and dialogue-safe placement/mixing rules
- Enforced opening/logo/title/credit coverage when selected in the questionnaire
- Character naming, reveal-order, object, location, and continuity tracking
- Natural neural narration with measured duration and adaptive rate
- Narration-only soundtrack ducking: source audio stays at its original level whenever narration is not speaking
- Cue overlap, output duration, stream, and container validation helpers

## Requirements

- Codex with skill support
- Python 3.10 or newer
- FFmpeg and FFprobe on `PATH` for media work and output verification
- A natural TTS provider for narration; the workflow recommends Microsoft neural voices but does not lock production to one provider
- Optional speech-to-text and scene-analysis tools appropriate to the production environment

The skill includes a non-binding [recommended toolchain](references/recommended-tools.md), including FFmpeg/FFprobe, Faster-Whisper, FFmpeg scene detection or PySceneDetect, multimodal visual models, and Microsoft Edge TTS. Equivalent tools are welcome when they satisfy the same timing, quality, and validation requirements.

## Install

### Ask Codex to install it

In Codex, say:

```text
Use $skill-installer to install the skill from
https://github.com/wangru2025/film-audio-description-skill
and name it film-audio-description.
```

The installed skill is available on the next turn.

### Use the bundled Codex installer directly

macOS or Linux:

```bash
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo wangru2025/film-audio-description-skill \
  --path . \
  --name film-audio-description
```

Windows PowerShell:

```powershell
python "$env:USERPROFILE\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py" `
  --repo wangru2025/film-audio-description-skill `
  --path . `
  --name film-audio-description
```

The installer refuses to overwrite an existing `film-audio-description` directory. Remove or rename an older installation first if you intentionally want to replace it.

### Manual installation

Clone the repository into the Codex skills directory:

```bash
git clone https://github.com/wangru2025/film-audio-description-skill.git \
  ~/.codex/skills/film-audio-description
```

On Windows PowerShell:

```powershell
git clone https://github.com/wangru2025/film-audio-description-skill.git `
  "$env:USERPROFILE\.codex\skills\film-audio-description"
```

Restart Codex or begin a new turn after installation.

## Use

Invoke the skill explicitly:

```text
Use $film-audio-description to create audio description for /path/to/movie.mp4.
```

The normal workflow is:

1. Inspect media tracks and duration.
2. Ask a short questionnaire with recommended settings.
3. Map the complete film, analyze scene-aware 8–15 minute segments, and assemble them into review batches.
4. Deliver a standard review SRT plus an evidence/uncertainty map.
5. Wait for user corrections and explicit approval, such as `Y`.
6. Synthesize narration, audit timing, mix, and verify the finished output.

## Safety and production boundaries

- User approval of the current script is mandatory before batch TTS or mixing.
- Approval is bound to hashes of both the reviewed SRT and matching cue artifact.
- A meaning-changing script edit invalidates prior approval.
- Narration cues must not overlap each other.
- Normal cues must cite concrete visual observations; dialogue and plot exposition are not substitutes for visual evidence.
- Run `scripts/audit_project.py PROJECT_DIR` before presenting a review batch or approving a merged script.
- Source audio is ducked only while narration speaks; dialogue-free passages are never automatically attenuated.
- Final output is rendered to a temporary target and promoted only after validation.
- Users are responsible for having the rights and permissions required to process and distribute source media.

## License

MIT. See [LICENSE](LICENSE).

Current release: `v0.5.0`.
