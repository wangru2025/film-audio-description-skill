#!/usr/bin/env python3
"""Audit evidence, coverage, continuity, and state in an AD project."""
import argparse
import difflib
import json
import re
import sys
from pathlib import Path

SUMMARY_TERMS = (
    "任务目标", "行动计划", "救援行动失败", "核心方案", "唯一希望",
    "计划启动", "行动分成", "行动被拆成", "这意味着", "因此", "原本要",
)
REQUIRED_OBS = ("id", "start", "end", "subject", "action", "location",
                "evidence_frames", "evidence_type", "sound_sufficient",
                "dialogue_support_only", "confidence", "uncertainty")

def load(path, issues, required=True):
    if not path.is_file():
        if required:
            issues.append(issue("error", "missing_artifact", path=str(path)))
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        issues.append(issue("error", "invalid_json", path=str(path), detail=str(exc)))
        return None

def issue(severity, kind, **details):
    return {"severity": severity, "type": kind, **details}

def records(value, key):
    if isinstance(value, list):
        return value
    if isinstance(value, dict) and isinstance(value.get(key), list):
        return value[key]
    return []

def number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

def normalized(text):
    return "".join(re.findall(r"[\u4e00-\u9fffA-Za-z0-9]", str(text))).lower()

def grams(text, n=2):
    text = normalized(text)
    if len(text) < n:
        return {text} if text else set()
    return {text[i:i+n] for i in range(len(text)-n+1)}

def similarity(left, right):
    a, b = normalized(left), normalized(right)
    if not a or not b:
        return 0.0
    ga, gb = grams(a), grams(b)
    jaccard = len(ga & gb) / len(ga | gb) if ga | gb else 0.0
    return max(jaccard, difflib.SequenceMatcher(None, a, b).ratio())

def interval(record):
    start = number(record.get("start", record.get("time")))
    end = number(record.get("end", start))
    return start, end

def get_duration(root, project, transcript):
    candidates = [project.get("media_duration"), project.get("duration")] if isinstance(project, dict) else []
    if isinstance(transcript, dict):
        candidates.append(transcript.get("duration"))
    probe = root / "media" / "probe.json"
    if probe.is_file():
        try:
            data = json.loads(probe.read_text(encoding="utf-8-sig"))
            candidates.extend([data.get("duration"), (data.get("format") or {}).get("duration")])
        except (OSError, json.JSONDecodeError, AttributeError):
            pass
    return next((number(x) for x in candidates if number(x) is not None), None)

def audit(root):
    issues = []
    project = load(root / "project.json", issues) or {}
    transcript_data = load(root / "timeline" / "transcript.json", issues, False) or {}
    transcript = records(transcript_data, "segments")
    scene_data = load(root / "timeline" / "scenes.json", issues) or {}
    scenes = records(scene_data, "scenes")
    duration = get_duration(root, project, transcript_data)

    if not scenes:
        issues.append(issue("error", "empty_scene_table"))
    elif duration is not None:
        starts = [interval(s)[0] for s in scenes if interval(s)[0] is not None]
        ends = [interval(s)[1] for s in scenes if interval(s)[1] is not None]
        if not starts or min(starts) > 2 or not ends or max(ends) < duration - 5:
            issues.append(issue("error", "incomplete_scene_coverage", media_duration=duration,
                                scene_start=min(starts) if starts else None, scene_end=max(ends) if ends else None))

    bible_nonempty = 0
    for name in ("characters", "locations", "objects", "story-state"):
        value = load(root / "bible" / f"{name}.json", issues)
        if value not in (None, [], {}):
            bible_nonempty += 1
    if bible_nonempty == 0:
        issues.append(issue("error", "all_bibles_empty"))

    segment_root = root / "segments"
    dirs = sorted(p for p in segment_root.glob("segment-*") if p.is_dir()) if segment_root.is_dir() else []
    if not dirs:
        issues.append(issue("error", "no_segments"))
    all_observations, all_cues, completed_ranges, stats = [], [], [], []
    for directory in dirs:
        manifest = load(directory / "manifest.json", issues, False)
        obs_data = load(directory / "observations.json", issues, False)
        cue_data = load(directory / "draft-cues.json", issues, False)
        if not manifest or obs_data is None or cue_data is None:
            issues.append(issue("error", "incomplete_segment_directory", segment=directory.name))
            continue
        observations, cues = records(obs_data, "observations"), records(cue_data, "cues")
        seg_start, seg_end = number(manifest.get("start")), number(manifest.get("end"))
        if seg_start is None or seg_end is None or seg_end <= seg_start:
            issues.append(issue("error", "invalid_segment_bounds", segment=directory.name))
            continue
        seg_minutes = (seg_end - seg_start) / 60
        if seg_minutes > 15.5:
            issues.append(issue("error", "analysis_segment_too_coarse", segment=directory.name, minutes=round(seg_minutes, 2)))
        minimum = max(3, int(seg_minutes + 0.999))
        if len(observations) < minimum:
            issues.append(issue("error", "insufficient_observation_density", segment=directory.name,
                                observations=len(observations), minimum_review_threshold=minimum))
        timed = sorted(x for x in (interval(o)[0] for o in observations) if x is not None)
        checkpoints = [seg_start] + timed + [seg_end]
        for left, right in zip(checkpoints, checkpoints[1:]):
            if right - left > 90:
                issues.append(issue("error", "unexplained_observation_gap", segment=directory.name,
                                    start=left, end=right, seconds=round(right-left, 2)))
        obs_ids = set()
        for obs in observations:
            missing = [field for field in REQUIRED_OBS if field not in obs]
            if missing:
                issues.append(issue("error", "observation_missing_fields", segment=directory.name,
                                    observation=obs.get("id"), fields=missing))
            if obs.get("id"):
                obs_ids.add(obs["id"]); all_observations.append(obs)
            frames = obs.get("evidence_frames")
            if obs.get("evidence_type") == "visual" and not isinstance(frames, list):
                issues.append(issue("error", "missing_visual_evidence_frames", observation=obs.get("id")))
        for cue in cues:
            refs = cue.get("observation_ids")
            frames = cue.get("evidence_frames")
            if not refs or not isinstance(refs, list):
                issues.append(issue("error", "cue_without_observation_reference", segment=directory.name, cue=cue.get("id")))
            else:
                unknown = [ref for ref in refs if ref not in obs_ids]
                if unknown:
                    issues.append(issue("error", "cue_references_unknown_observation", cue=cue.get("id"), ids=unknown))
                if any(o.get("sound_sufficient") is True for o in observations if o.get("id") in refs):
                    issues.append(issue("error", "sound_sufficient_observation_generated_cue", cue=cue.get("id")))
            if not isinstance(frames, list) or not frames:
                issues.append(issue("error", "cue_without_evidence_frames", cue=cue.get("id")))
            text = str(cue.get("text", ""))
            cue_start = number(cue.get("start"))
            nearby = [str(t.get("text", "")) for t in transcript
                      if cue_start is not None and number(t.get("start")) is not None
                      and cue_start - 30 <= number(t.get("start")) <= cue_start + 30]
            best = max((similarity(text, spoken) for spoken in nearby), default=0.0)
            if len(normalized(text)) >= 6 and best >= 0.72:
                issues.append(issue("error", "suspected_dialogue_restatement", cue=cue.get("id"), score=round(best, 3)))
            terms = [term for term in SUMMARY_TERMS if term in text]
            if terms or len(normalized(text)) > 48:
                issues.append(issue("warning", "possible_plot_summary", cue=cue.get("id"), terms=terms, characters=len(normalized(text))))
            all_cues.append(cue)
        if manifest.get("status") in ("analyzed", "drafted", "reviewed", "approved", "complete"):
            completed_ranges.append((seg_start, seg_end, directory.name))
        avg_len = sum(len(normalized(c.get("text", ""))) for c in cues) / len(cues) if cues else 0
        stats.append({"segment": directory.name, "minutes": seg_minutes, "observations_per_minute": len(observations)/seg_minutes, "average_cue_characters": avg_len})

    if stats:
        baseline = stats[0]
        for current in stats[1:]:
            if current["observations_per_minute"] < baseline["observations_per_minute"] * 0.55:
                issues.append(issue("error", "possible_summary_drift", segment=current["segment"], reason="observation_density_drop"))
            if baseline["average_cue_characters"] and current["average_cue_characters"] > baseline["average_cue_characters"] * 1.8:
                issues.append(issue("warning", "possible_summary_drift", segment=current["segment"], reason="cue_length_growth"))

    for scene in scenes:
        ss, se = interval(scene)
        if ss is not None and se is not None and not any((interval(o)[0] is not None and interval(o)[1] is not None and interval(o)[0] <= se and interval(o)[1] >= ss) for o in all_observations):
            issues.append(issue("error", "scene_without_observation_coverage", scene=scene.get("id"), start=ss, end=se))

    stage = project.get("stage")
    current, approved = project.get("script_version"), project.get("approved_script_version")
    if stage == "awaiting_user_review" and approved is not None and approved == current:
        issues.append(issue("error", "approval_state_contradiction", stage=stage, script_version=current))
    merged = load(root / "script" / "merged-draft.json", issues, False)
    if completed_ranges and merged is None:
        issues.append(issue("error", "missing_merged_draft"))
    elif completed_ranges and isinstance(merged, dict):
        coverage = merged.get("coverage")
        if not isinstance(coverage, dict) or number(coverage.get("start")) is None or number(coverage.get("end")) is None:
            issues.append(issue("error", "merged_draft_missing_coverage"))
        else:
            expected_start = min(x[0] for x in completed_ranges); expected_end = max(x[1] for x in completed_ranges)
            if number(coverage["start"]) > expected_start + 1 or number(coverage["end"]) < expected_end - 1:
                issues.append(issue("error", "merged_coverage_incomplete", expected=[expected_start, expected_end], actual=[coverage["start"], coverage["end"]]))

    errors = [x for x in issues if x["severity"] == "error"]
    return {"schema_version": 1, "project": str(root), "passed": not errors,
            "summary": {"errors": len(errors), "warnings": len(issues)-len(errors),
                        "segments": len(dirs), "observations": len(all_observations), "cues": len(all_cues)},
            "segment_stats": stats, "issues": issues}

def main():
    parser = argparse.ArgumentParser(description="Audit an audio-description project for evidence and summary drift.")
    parser.add_argument("project_dir")
    parser.add_argument("--report")
    args = parser.parse_args()
    report = audit(Path(args.project_dir).resolve())
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        Path(args.report).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["passed"] else 1

if __name__ == "__main__":
    sys.exit(main())
