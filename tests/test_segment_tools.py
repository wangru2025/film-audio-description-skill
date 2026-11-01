import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).parents[1]

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")

class SegmentToolTests(unittest.TestCase):
    def test_prepare_packages_existing_evidence_and_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); media = root / "movie.mp4"; media.write_bytes(b"movie")
            write(root / "project.json", {"source_media": str(media), "preferences": {"density": "medium"}})
            write(root / "timeline/scenes.json", {"scenes": [{"id": "s1", "start": 0, "end": 10}]})
            write(root / "timeline/transcript.json", {"segments": [{"id": 1, "start": 3, "end": 4, "text": "对白"}]})
            for name, value in (("characters", []), ("locations", []), ("objects", []), ("story-state", {})):
                write(root / f"bible/{name}.json", value)
            evidence = root / "segments/segment-001/evidence"
            evidence.mkdir(parents=True)
            # start, midpoint, and near-end timestamps chosen by the packager
            for index, millis in enumerate((0, 5000, 9950), 1):
                (evidence / f"frame-{index:04d}-{millis:010d}ms.jpg").write_bytes(f"frame-{index}".encode())
            subprocess.run([sys.executable, str(SKILL / "scripts/prepare_segment.py"), str(root), "segment-001",
                "--start", "0", "--end", "10", "--max-gap", "20", "--reuse-evidence"], check=True)
            package = json.loads((root / "segments/segment-001/work-package.json").read_text(encoding="utf-8"))
            self.assertEqual(package["shots"][0]["id"], "s1")
            self.assertEqual(package["transcript_context"][0]["text"], "对白")
            self.assertEqual(len(package["evidence"]), 3)
            self.assertTrue((root / "segments/segment-001/analysis-input.json").is_file())

    def test_finalize_expands_compact_analysis_and_computes_overlap(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); segment = root / "segments/segment-001"
            write(segment / "work-package.json", {"segment_id": "segment-001", "start": 0, "end": 60,
                "overlap_before": 0, "overlap_after": 20, "shots": [{"id": "s1"}],
                "evidence": [{"id": "ev-1", "timestamp": 10, "path": "x.jpg", "sha256": "x", "source_media_id": "m"}],
                "transcript_context": [{"id": 7, "start": 11, "end": 13, "text": "对白"}]})
            write(segment / "analysis-input.json", {"segment_id": "segment-001", "observations": [{
                "local_id": "o1", "evidence_ids": ["ev-1"], "subject": "女人", "action": "关门",
                "location": "走廊", "confidence": .9, "subject_character_ids": ["c1"]}],
                "cues": [{"observation_ref": "o1", "text": "女人关门。", "start": 10, "review_duration": 3}],
                "bible_proposals": {"characters": [], "locations": [], "objects": [], "story_state": {}}})
            subprocess.run([sys.executable, str(SKILL / "scripts/finalize_segment.py"), str(root), "segment-001"], check=True)
            cues = json.loads((segment / "draft-cues.json").read_text(encoding="utf-8"))["cues"]
            self.assertEqual(cues[0]["computed_dialogue_overlaps"], ["7"])
            for name in ("manifest.json", "observations.json", "draft-cues.json", "evidence-index-proposal.json", "bible-proposals.json"):
                self.assertTrue((segment / name).is_file(), name)

if __name__ == "__main__":
    unittest.main()
