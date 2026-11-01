#!/usr/bin/env python3
"""Prepare a segment package so agents analyze instead of coding."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

def load(path, default=None):
    return json.loads(path.read_text(encoding="utf-8-sig")) if path.is_file() else default

def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()

def rows(value, key):
    return value if isinstance(value, list) else value.get(key, []) if isinstance(value, dict) else []

def main():
    p = argparse.ArgumentParser(description="Create a ready-to-analyze segment package with hashed evidence frames.")
    p.add_argument("project_dir")
    p.add_argument("segment_id")
    p.add_argument("--start", type=float, required=True)
    p.add_argument("--end", type=float, required=True)
    p.add_argument("--overlap", type=float, default=20.0)
    p.add_argument("--max-gap", type=float, default=20.0)
    p.add_argument("--timestamp", type=float, action="append", default=[])
    p.add_argument("--reuse-evidence", action="store_true", help="Package already-extracted segment evidence without invoking FFmpeg.")
    p.add_argument("--force", action="store_true")
    args = p.parse_args()
    root = Path(args.project_dir).resolve()
    segment = root / "segments" / args.segment_id
    if args.end <= args.start:
        raise SystemExit("--end must be greater than --start")
    project = load(root / "project.json", {}) or {}
    source = Path(project.get("source_media", ""))
    if not source.is_file():
        raise SystemExit(f"Source media missing: {source}")
    scenes = rows(load(root / "timeline/scenes.json", {}), "scenes")
    selected = [s for s in scenes if float(s.get("start", -1)) < args.end and float(s.get("end", -1)) > args.start]
    if not selected:
        raise SystemExit("No scene/shot records overlap the requested range")
    times = []
    for shot in selected:
        left = max(args.start, float(shot["start"]))
        right = min(args.end, float(shot["end"]))
        times.append((left + right) / 2)
    cursor = args.start
    while cursor < args.end:
        times.append(cursor)
        cursor += args.max_gap
    times.extend(args.timestamp)
    times.append(max(args.start, args.end - 0.05))
    times = sorted({round(t, 6) for t in times if args.start <= t < args.end})
    segment.mkdir(parents=True, exist_ok=True)
    evidence_dir = segment / "evidence"
    evidence_dir.mkdir(exist_ok=True)
    package_path = segment / "work-package.json"
    input_path = segment / "analysis-input.json"
    if package_path.exists() and not args.force:
        raise SystemExit(f"Package exists; use --force to refresh: {package_path}")
    evidence = []
    for index, timestamp in enumerate(times, 1):
        evidence_id = f"{args.segment_id}-ev-{index:04d}"
        name = f"frame-{index:04d}-{round(timestamp * 1000):010d}ms.jpg"
        target = evidence_dir / name
        if not target.is_file() and args.reuse_evidence:
            raise SystemExit(f"Reusable evidence missing: {target}")
        if not target.is_file():
            subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-ss", f"{timestamp:.6f}", "-i", str(source), "-frames:v", "1", "-q:v", "3", "-y", str(target)], check=True)
        shot = next((s for s in selected if float(s["start"]) <= timestamp < float(s["end"])), None)
        evidence.append({"id": evidence_id, "timestamp": timestamp, "path": target.relative_to(root).as_posix(), "sha256": digest(target), "source_media_id": "source-media", "source_shot_id": shot.get("id") if shot else None})
    transcript = rows(load(root / "timeline/transcript.json", {}), "segments")
    speech = [x for x in transcript if float(x.get("start", -1)) < args.end + args.overlap and float(x.get("end", -1)) > args.start - args.overlap]
    bible = {name: load(root / f"bible/{name}.json", [] if name != "story-state" else {}) for name in ("characters", "locations", "objects", "story-state")}
    package = {"schema_version": 1, "segment_id": args.segment_id, "start": args.start, "end": args.end, "overlap_before": args.overlap, "overlap_after": args.overlap, "source_media": str(source), "shots": selected, "transcript_context": speech, "bible_snapshot": bible, "preferences": project.get("preferences", {}), "evidence": evidence, "agent_instructions": ["Inspect evidence and request denser extraction through prepare_segment.py when needed.", "Edit analysis-input.json only; do not create scripts or canonical artifact files.", "Describe visible evidence, not plot knowledge or dialogue restatement."]}
    write(package_path, package)
    if not input_path.exists() or input_path.stat().st_size == 0:
        write(input_path, {"schema_version": 1, "segment_id": args.segment_id, "observations": [], "cues": [], "bible_proposals": {"characters": [], "locations": [], "objects": [], "story_state": {}}, "agent_notes": []})
    print(json.dumps({"segment": args.segment_id, "shots": len(selected), "evidence_frames": len(evidence), "transcript_segments": len(speech), "analysis_input": str(input_path)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
