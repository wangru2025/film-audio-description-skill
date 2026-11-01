import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "audit_project.py"
SPEC = importlib.util.spec_from_file_location("audit_project", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")

def observation(index, start, end=None, sufficient=False):
    return {"id": f"obs-{index}", "start": start, "end": end or start + 2,
            "subject": "女人", "action": "抬手指向屏幕", "object": "屏幕",
            "location": "控制室", "evidence_frames": [start, start + 1, end or start + 2],
            "evidence_type": "visual", "sound_sufficient": sufficient,
            "dialogue_support_only": True, "confidence": 0.95, "uncertainty": None}

class AuditProjectTests(unittest.TestCase):
    def make_base(self, root):
        write(root / "project.json", {"stage": "script_drafted", "script_version": 1,
              "approved_script_version": None, "media_duration": 480})
        write(root / "timeline/scenes.json", {"scenes": [{"id": "s1", "start": 0, "end": 240},
              {"id": "s2", "start": 240, "end": 480}]})
        write(root / "timeline/transcript.json", {"duration": 480, "segments": [
              {"start": 202, "end": 205, "text": "我们马上离开这里"}]})
        for name, value in (("characters", [{"id": "c1"}]), ("locations", [{"id": "l1"}]),
                            ("objects", [{"id": "o1"}]), ("story-state", {"time": 0})):
            write(root / f"bible/{name}.json", value)

    def test_good_project_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); self.make_base(root)
            observations = [observation(i, t) for i, t in enumerate((0, 70, 140, 210, 280, 350, 420, 478), 1)]
            write(root / "segments/segment-001/manifest.json", {"start": 0, "end": 480, "status": "drafted"})
            write(root / "segments/segment-001/observations.json", {"observations": observations})
            write(root / "segments/segment-001/draft-cues.json", {"cues": [{"id": "cue-1", "start": 140,
                  "text": "女人抬手指向屏幕。", "observation_ids": ["obs-3"], "evidence_frames": [140, 141, 142]}]})
            write(root / "script/merged-draft.json", {"coverage": {"start": 0, "end": 480}, "cues": []})
            report = MODULE.audit(root)
            self.assertTrue(report["passed"], report["issues"])

    def test_bad_project_fails_expected_gates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "project.json", {"stage": "awaiting_user_review", "script_version": 5,
                  "approved_script_version": 5, "media_duration": 2400})
            write(root / "timeline/scenes.json", {"scenes": [{"id": "s1", "start": 0, "end": 1200}]})
            write(root / "timeline/transcript.json", {"duration": 2400, "segments": [
                  {"start": 400, "end": 406, "text": "救援行动失败"}]})
            for name, value in (("characters", []), ("locations", []), ("objects", []), ("story-state", {})):
                write(root / f"bible/{name}.json", value)
            write(root / "segments/segment-001/manifest.json", {"start": 0, "end": 1200, "status": "drafted"})
            write(root / "segments/segment-001/observations.json", {"observations": [
                  {"time": i * 150, "subject": "人", "action": "行动"} for i in range(8)]})
            write(root / "segments/segment-001/draft-cues.json", {"cues": [
                  {"id": "cue-1", "start": 400, "text": "救援行动失败"}]})
            (root / "segments/segment-002").mkdir(parents=True)
            write(root / "script/merged-draft.json", {"coverage": {"start": 0, "end": 600}, "cues": []})
            report = MODULE.audit(root)
            kinds = {item["type"] for item in report["issues"]}
            expected = {"all_bibles_empty", "incomplete_scene_coverage", "analysis_segment_too_coarse",
                        "insufficient_observation_density", "cue_without_observation_reference",
                        "suspected_dialogue_restatement", "approval_state_contradiction",
                        "merged_coverage_incomplete", "incomplete_segment_directory"}
            self.assertFalse(report["passed"])
            self.assertTrue(expected <= kinds, expected - kinds)

if __name__ == "__main__":
    unittest.main()
