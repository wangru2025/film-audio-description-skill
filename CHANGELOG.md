# Changelog

[简体中文](CHANGELOG.zh-CN.md) | English

All notable changes are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/).

## [0.5.0] - 2026-11-01

### Added

- Added prepare_segment.py to select shots, slice transcript context, snapshot the bible, extract and hash evidence frames, and create ready-to-analyze work packages.
- Added finalize_segment.py to expand compact agent analysis into canonical manifests, observations, cues, evidence proposals, and bible proposals while calculating dialogue intersections.
- Added analysis-input.json as the only normal segment-agent-authored artifact.
- Added mandatory per-batch identity convergence with confirmed, not_yet_revealed, and unresolved_after_evidence_review outcomes.
- Added canonical subject_character_ids on character-bearing cues.

### Changed

- Neutral character labels are now analysis scaffolding only. Review-ready scripts use canonical names after the permitted reveal, or expose unresolved identity to the user.
- Coordinators merge duplicate provisional IDs, aliases, safe labels, and evidence tracks before generating review SRT.
- awaiting_user_review now freezes later work packages and analysis waves until approval or corrections are incorporated.
- Segment agents now focus on watching and writing instead of creating FFmpeg, hashing, schema, or JSON-builder scripts.
- Coverage audits are clipped to the active review batch; without one, they use completed segment coverage.
- Observation-gap detection now merges real start/end intervals before finding uncovered time.

### Fixed

- Fixed review-batch audits checking scenes outside the active batch.
- Fixed long observations being mistaken for gaps because only their start points were compared.
- Fixed confirmed characters retaining obsolete neutral labels after their narration-allowed reveal.
- Fixed duplicate/provisional character records surviving into review-ready bibles.
- Fixed agents creating one-off code inside segment directories; unregistered executables now fail project audit.

### Validation

- Expanded the suite to 19 passing tests, including segment-tool, identity, review-scope, crossing-scene, and long-interval regressions.

## [0.4.0] - 2026-11-01

### Added

- Made standard SRT the primary review artifact, with deterministic rendering and a companion evidence map.
- Added material-aware paths for media-only projects, validated subtitles, cast-role manifests, scripts, and character or costume references.
- Added material provenance and hashes, a hashed visual-evidence index, approval records, dialogue events, listening review, duck envelopes, and reproducible audio measurements.
- Added project-wide auditing for evidence integrity, scene coverage, dialogue similarity, summary drift, bible readiness, merged coverage, and state consistency.

### Changed

- Validated external SRT can replace redundant full ASR; cast references accelerate but do not replace on-screen identity binding.
- Approvals bind both the exact reviewed SRT and matching merged cue artifact.
- Dialogue overlap is computed from measured narration-audible intervals.
- Final QC requires listening, duck-envelope, and source/output measurements instead of container checks alone.

### Fixed

- Prevented arbitrary timestamps, recycled frames, unvalidated subtitles, unlabeled photos, self-authored approvals, and self-attested listening from passing as evidence.

## [0.3.0] - 2026-11-01

### Added

- Added dialogue-safe placement and mixing rules, slot-aware Chinese compression, film-local identity evidence, and binding opening/ending credit coverage.
- Added title/credit inventories for company names, film titles, actor-role pairs, and crew credits.

### Changed

- Placement now tries nearby gaps, rewriting, semantic splitting, and measured rate adjustment before limited overlap.
- Names, numbers, clues, punchlines, whispers, emotional lines, and action-driving commands are protected.

### Fixed

- Prevented selected title/credit coverage from being silently omitted, outside knowledge from establishing identity, and long duck tails from becoming permanent attenuation.

## [0.2.0] - 2026-11-01

### Added

- Added evidence-first observations, cue-to-evidence links, anti-summary gates, and deterministic project auditing.
- Added scene-aware 8–15 minute analysis segments distinct from roughly 20-minute review batches.
- Added coverage, dialogue-restatement, summary-language, density-drift, bible, merged-coverage, empty-segment, and approval-state checks.

### Fixed

- Prevented sparse visual sampling plus noisy ASR from degrading into plot summaries.
- Prevented audible broadcasts, mission plans, and causal exposition from being repeated as narration.
- Prevented fixed review batches from becoming coarse analysis units.

## [0.1.0] - 2026-10-31

### Added

- Initial open-source interactive film audio-description skill.
- Added adaptive intake, short/feature-film paths, structured projects, long-film orchestration, and mandatory user approval before TTS or mixing.
- Added natural neural voice recommendations, adaptive rate, independent narration masters, cue/output checks, temporary renders, and narration-gated ducking with unity source gain outside narration.
- Added bilingual documentation, MIT licensing, installation instructions, and a recommended production toolchain.

Note: the initial public release was not tagged; formal release tags begin with v0.2.0.

[0.5.0]: https://github.com/wangru2025/film-audio-description-skill/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/wangru2025/film-audio-description-skill/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/wangru2025/film-audio-description-skill/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/wangru2025/film-audio-description-skill/releases/tag/v0.2.0
[0.1.0]: https://github.com/wangru2025/film-audio-description-skill/commit/b45d22a
