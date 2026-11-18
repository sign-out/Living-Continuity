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

    def test_native_time_is_a_bounded_delta_from_voyage_source(self):
        self.assertEqual(self.core["heroesVersion"], 37)
        self.assertEqual(self.source["heroesVersion"], 37)
        base, now = self.source["triggerDefinitions"], self.core["triggerDefinitions"]
        self.assertEqual(len(base), 204)
        self.assertEqual(len(now), 206)
        self.assertEqual(sum(bool(t.get("script")) for t in now.values()), 198)
        added = set(now) - set(base)
        changed = {k for k in base if now[k] != base[k]}
        self.assertEqual(added, {
            "sys_lc_native_time_bridge_planning",
            "sys_lc_native_time_bridge_state",
        })
        self.assertEqual(changed, {
            "sys_lc_semantic_temporal_endpoint",
            "sys_lc_previous_prose_time_reconcile",
            "sys_sleep_to_morning",
            "sys_explicit_duration_time_cost",
            "sys_clock_initialize",
            "sys_clock_advance",
            "sys_time_command",
            "sys_skip_calendar_time",
            "sys_hud_render",
        })
        self.assertEqual(set(self.core) - {"triggerDefinitions"}, set(self.source) - {"triggerDefinitions"})
        for k in self.core:
            if k != "triggerDefinitions":
                self.assertEqual(self.core[k], self.source[k], k)

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
