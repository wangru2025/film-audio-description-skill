#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

def probe(path: Path):
    raw = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
        "format=duration,size:stream=index,codec_type,codec_name,sample_rate,channels",
        "-of", "json", str(path)], text=True, encoding="utf-8")
    return json.loads(raw)

def main():
    p = argparse.ArgumentParser(description="Verify a rendered audio-described video container.")
    p.add_argument("source")
    p.add_argument("output")
    p.add_argument("--duration-tolerance", type=float, default=0.25)
    p.add_argument("--report")
    args = p.parse_args()
    source, output = Path(args.source), Path(args.output)
    issues = []
    if output.suffix.lower() == ".partial" or ".partial." in output.name.lower():
        issues.append({"type": "partial_output_name"})
    if not output.exists() or output.stat().st_size == 0:
        issues.append({"type": "missing_or_empty_output"})
        result = {"passed": False, "issues": issues}
    else:
        try:
            src, out = probe(source), probe(output)
            src_duration = float(src["format"]["duration"]); out_duration = float(out["format"]["duration"])
            if abs(src_duration - out_duration) > args.duration_tolerance:
                issues.append({"type": "duration_mismatch", "source": src_duration, "output": out_duration})
            types = [s.get("codec_type") for s in out.get("streams", [])]
            if "video" not in types: issues.append({"type": "missing_video_stream"})
            if "audio" not in types: issues.append({"type": "missing_audio_stream"})
            result = {"passed": not issues, "issues": issues, "source_probe": src, "output_probe": out,
                      "manual_audio_checks_required": ["narration audible at sampled cues", "source audible under narration"]}
        except Exception as exc:
            result = {"passed": False, "issues": issues + [{"type": "probe_failure", "error": str(exc)}]}
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.report: Path(args.report).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    sys.exit(0 if result["passed"] else 1)

if __name__ == "__main__":
    main()
