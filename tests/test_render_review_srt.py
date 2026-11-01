import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "render_review_srt.py"

class RenderReviewSrtTests(unittest.TestCase):
    def test_renders_standard_srt_and_map(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); cues = root / "cues.json"; srt = root / "review.srt"; mapping = root / "map.json"
            cues.write_text(json.dumps({"cues": [{"id": "c1", "start": 61.25, "review_duration": 2.5,
                "text": "李明关上舱门。", "observation_ids": ["o1"], "evidence_frames": [61.2]}]}, ensure_ascii=False), encoding="utf-8")
            subprocess.run([sys.executable, str(SCRIPT), str(cues), str(srt), str(mapping), "--script-version", "2"], check=True)
            self.assertIn("00:01:01,250 --> 00:01:03,750", srt.read_text(encoding="utf-8-sig"))
            data = json.loads(mapping.read_text(encoding="utf-8"))
            self.assertEqual(data["entries"][0]["cue_id"], "c1")

if __name__ == "__main__":
    unittest.main()
