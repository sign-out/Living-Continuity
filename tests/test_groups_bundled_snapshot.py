"""Regression gates for the corrected LC + Groups full Voyage export."""
import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "exports" / "LC_Groups_Bundled_Quest_Summary_Fixed_2026-11-03.json"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

class BundledGroupsExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = load(BUNDLE)
        cls.core = load(ROOT / "Living_Continuity.json")
        cls.addon = load(ROOT / "addons" / "LC_Groups_That_Remember.json")

    def test_export_structure_and_no_accidental_replacement(self):
        t = self.bundle["triggerDefinitions"]
        self.assertEqual(self.bundle["heroesVersion"], 37)
        self.assertEqual(len(t), 206)
        self.assertEqual(sum(bool(v.get("script", "").strip()) for v in t.values()), 198)
        self.assertEqual(sum(k.startswith("sys_lcmg_") for k in t), 6)
        self.assertIn("sys_lc_command_prerouter", t)
        self.assertNotIn("sys_lc_npc_competence_initialize", t)
        self.assertIn("sys_lc_npc_competence_initialize", self.core["triggerDefinitions"])
        standalone = self.addon["triggerDefinitions"]
        self.assertEqual(len(standalone), 6)
        self.assertTrue(all(k.startswith("sys_lcmg_") for k in standalone))
        self.assertIn("ev.evidence?.source", standalone["sys_lcmg_commit"]["script"])

    def test_every_script_parses_and_quest_summary_executes(self):
        js = r"""
const fs = require("fs");
const data = JSON.parse(fs.readFileSync(process.argv[1], "utf8"));
let count = 0;
for (const [id, entry] of Object.entries(data.triggerDefinitions)) {
  if (!entry.script || !entry.script.trim()) continue;
  try { new Function(entry.script); ++count; }
  catch (e) { throw new Error(id + ": " + e.message); }
}
if (count !== 198) throw new Error("Expected 198 parseable scripts, got " + count);
const storage = {
  sys_lc_systems_config: {questIndex: {enabled: true}},
  sys_continuity_config: {quests: {}},
  sys_quest_ledger: {registry: {}, stats: {}}
};
const effects = [];
new Function("storage", "effects", "skip",
  data.triggerDefinitions.sys_lc_quest_summary_command.script
)(storage, effects, false);
if (effects.length !== 1 ||
    !effects[0].instruction.includes("host world's quest wiring") ||
    !effects[0].instruction.includes("ACTIVE QUESTS")) {
  throw new Error("Quest summary output is invalid: " + JSON.stringify(effects));
}
"""
        p = subprocess.run(["node", "-e", js, str(BUNDLE)],
                           capture_output=True, text=True, check=False)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)

if __name__ == "__main__":
    unittest.main()
