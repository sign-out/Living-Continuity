"""Release snapshot regression gates for the modular LC distribution."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

class ReleaseSnapshotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.core = read("Living_Continuity.json")
        cls.source = read("exports/LC_Voyage_2026-11-03.json")
        cls.groups = read("addons/LC_Groups_That_Remember.json")

    def test_native_runtime_equals_supplied_voyage_source(self):
        self.assertEqual(self.core["heroesVersion"], 37)
        self.assertEqual(self.core["triggerDefinitions"], self.source["triggerDefinitions"])
        self.assertEqual(len(self.core["triggerDefinitions"]), 204)
        self.assertEqual(sum(bool(t.get("script")) for t in self.core["triggerDefinitions"].values()), 196)

    def test_october_compatibility_not_lost_to_source_export(self):
        ai = self.core["aiInstructions"]
        self.assertIn("LC Oct 2026 - Social Initiative Routing", ai["generateStory"])
        self.assertIn("LC Oct 2026 - Combat Focus", ai["generateNPCIntents"])
        self.assertIn("Voyage Oct 2026 - Native Action Boundary", ai["generateActionInfo"])
        self.assertIn("Voyage Oct 2026 - Native Provenance and Visibility", ai["summarization"])

    def test_groups_addon_remains_standalone(self):
        self.assertEqual(len(self.groups["triggerDefinitions"]), 6)
        self.assertTrue(all(k.startswith("sys_lcmg_") for k in self.groups["triggerDefinitions"]))
        self.assertNotIn("sys_lc_quest_summary_command", self.groups["triggerDefinitions"])
        self.assertIn("ev.evidence?.source", self.groups["triggerDefinitions"]["sys_lcmg_commit"]["script"])

if __name__ == "__main__":
    unittest.main()
