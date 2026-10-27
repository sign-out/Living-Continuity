"""Static invariants for the October 2026 LC / Voyage V37 instruction pass.

Uses only the Python standard library. This is NOT a Voyage runtime test.
"""
import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "Living_Continuity.json"

PRESERVED = {
    "LC Immediate Want and Social Initiative":
        "LC Preserved Social Initiative (Oct 2026)",
    "System: LC Intent Compatibility Shim":
        "LC Preserved NPC Agency (Oct 2026)",
    "LC Decision Pipeline":
        "LC Preserved Actor Decision Pipeline (Oct 2026)",
}
REQUIRED_INSTRUCTIONS = {
    "generateInitialStart": ["Voyage Oct 2026 - Conditional Start Authority"],
    "generateActionInfo": ["Voyage Oct 2026 - Native Action Boundary"],
    "generateStory": [
        "Voyage Oct 2026 - Native State and Discovery",
        "LC Oct 2026 - Social Initiative Routing",
        *PRESERVED.values(),
    ],
    "generateNPCIntents": ["LC Oct 2026 - Combat Focus"],
    "generateNPCUpdates": ["Voyage Oct 2026 - Committed Effect Reconciliation"],
    "summarization": ["Voyage Oct 2026 - Native Provenance and Visibility"],
    "generateDialogue": ["Voyage Oct 2026 - Speaker Identity and Knowledge"],
}

class VoyageOct2026CompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.world = json.loads(FILE.read_text(encoding="utf-8"))

    def test_release_identity_and_trigger_inventory(self):
        w = self.world
        self.assertEqual(w["heroesVersion"], 37)
        self.assertEqual(len(w["triggerDefinitions"]), 204)
        for key in (
            "sys_lc_mp_attribute_social",
            "sys_clock_advance",
            "sys_lc_background_intents_worker",
        ):
            self.assertIn(key, w["triggerDefinitions"])
        self.assertIn("", w["parties"])

    def test_combat_hook_and_rehomed_social_guidance(self):
        hooks = self.world["aiInstructions"]
        combat = hooks["generateNPCIntents"]
        for old_key, preserved in PRESERVED.items():
            self.assertIn(preserved, hooks["generateStory"])
            self.assertTrue(hooks["generateStory"][preserved].strip())
            self.assertIn(old_key, combat)
            self.assertNotEqual(combat[old_key], hooks["generateStory"][preserved])
        self.assertIn("combat-focused", combat["LC Oct 2026 - Combat Focus"])
        self.assertIn("Zero initiatives is valid",
                      hooks["generateStory"]["LC Oct 2026 - Social Initiative Routing"])

    def test_all_new_contract_blocks_exist(self):
        hooks = self.world["aiInstructions"]
        for hook, names in REQUIRED_INSTRUCTIONS.items():
            for name in names:
                with self.subTest(hook=hook, name=name):
                    self.assertIn(name, hooks[hook])
                    self.assertIsInstance(hooks[hook][name], str)
                    self.assertTrue(hooks[hook][name].strip())

    def test_native_effects_and_discovery_are_described(self):
        hooks = self.world["aiInstructions"]
        self.assertIn("item-add/item-remove",
                      hooks["generateActionInfo"]["Voyage Oct 2026 - Native Action Boundary"])
        self.assertIn("party-discovered geography",
                      hooks["generateStory"]["Voyage Oct 2026 - Native State and Discovery"])
        self.assertIn("failed/skipped",
                      hooks["generateNPCUpdates"]["Voyage Oct 2026 - Committed Effect Reconciliation"])
        self.assertIn("hiddenInfo",
                      hooks["summarization"]["Voyage Oct 2026 - Native Provenance and Visibility"])

    def test_non_instruction_data_equal_to_main_when_available(self):
        result = subprocess.run(
            ["git", "show", "origin/main:Living_Continuity.json"],
            cwd=ROOT, capture_output=True, check=False,
        )
        if result.returncode:
            self.skipTest("origin/main not available; run with full Git history")
        base = json.loads(result.stdout.decode("utf-8-sig"))
        current = self.world
        self.assertEqual(list(base), list(current))
        for key in base:
            if key != "aiInstructions":
                with self.subTest(field=key):
                    self.assertEqual(base[key], current[key])
        self.assertEqual(list(base["aiInstructions"]), list(current["aiInstructions"]))

if __name__ == "__main__":
    unittest.main()
