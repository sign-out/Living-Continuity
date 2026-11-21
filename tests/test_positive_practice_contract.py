"""Regression contract for obstacle-gated positive practice. Run: python -m unittest discover -s tests -p 'test_*.py'."""
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
WORLD = ROOT / ("LCX.json" if (ROOT / "LCX.json").exists() else "Living_Continuity.json")

class PositivePracticeContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.world = json.loads(WORLD.read_text(encoding="utf-8"))
        cls.triggers = cls.world["triggerDefinitions"]
        cls.prefix = "lcx_" if WORLD.name == "LCX.json" else "sys_lc_"

    def test_four_native_player_scoped_probes_retained(self):
        for category in ("social", "knowledge", "consequence", "progression"):
            key = "sys_lc_mp_attribute_" + category
            self.assertIn(key, self.triggers)
            self.assertEqual(self.triggers[key]["scope"], "player")
            self.assertTrue(any(effect.get("target") == "satisfyingPlayers" for effect in self.triggers[key].get("effects", [])))

    def test_confirmed_actor_and_source_required(self):
        key = "lcx_positive_capability_ingest" if WORLD.name == "LCX.json" else "sys_lc_positive_capability_ingest"
        script = self.triggers[key]["script"]
        for required in ("e.confirmed!==true", "!e.entityId", "!e.sourceEventId", "meaningfulAttempt", "possible!==false", "successful&&cap", "seen.includes(source)", "Q.splice(0,128)"):
            self.assertIn(required, script)

    def test_practice_retrieval_and_privacy(self):
        key = "lcx_positive_capability_context" if WORLD.name == "LCX.json" else "sys_lc_positive_capability_context"
        script = self.triggers[key]["script"]
        self.assertIn("practice", script.lower())
        self.assertIn("maximum capability", script)
        if WORLD.name == "LCX.json":
            self.assertIn("x.visibility==='public'", script)
        else:
            self.assertIn("multi", script)

if __name__ == "__main__":
    unittest.main()
