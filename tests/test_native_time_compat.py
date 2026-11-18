"""LC native Voyage time compatibility: static and sandboxed JavaScript checks.

These checks do not prove live Voyage trigger execution order.
"""
import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORLD = ROOT / "Living_Continuity.json"
SOURCE = ROOT / "exports/LC_Voyage_2026-11-03.json"


class NativeTimeCompatibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.world = json.loads(WORLD.read_text(encoding="utf-8"))
        cls.source = json.loads(SOURCE.read_text(encoding="utf-8"))

    def test_preserve_full_world_and_existing_triggers(self):
        a, b = self.source, self.world
        self.assertEqual(a["heroesVersion"], b["heroesVersion"])
        for field in a:
            if field != "triggerDefinitions":
                self.assertEqual(a[field], b[field], field)
        old, new = a["triggerDefinitions"], b["triggerDefinitions"]
        self.assertEqual(len(old), 204)
        self.assertEqual(len(new), 206)
        self.assertEqual(set(new) - set(old), {
            "sys_lc_native_time_bridge_planning",
            "sys_lc_native_time_bridge_state",
        })
        self.assertEqual({k for k in old if old[k] != new[k]}, {
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

    def test_bridge_runtime_contract(self):
        tr = self.world["triggerDefinitions"]
        for phase in ("planning", "state"):
            t = tr["sys_lc_native_time_bridge_" + phase]
            self.assertTrue(t["recurring"])
            self.assertEqual(t["scope"], "party")
            self.assertEqual(t["phase"], phase)
            self.assertIn("check({type:'day'})", t["script"])
            self.assertIn("check({type:'time-of-day'})", t["script"])
        self.assertIn("Object.assign({}, defaults.nativeTime", tr["sys_clock_initialize"]["script"])
        self.assertIn("mode==='legacy'", tr["sys_lc_native_time_bridge_state"]["script"])
        self.assertIn("no elapsed-time evidence", tr["sys_lc_previous_prose_time_reconcile"]["script"])

    def test_all_triggers_compile_and_native_clock_smoke(self):
        js = r"""
const fs = require('fs'), assert = require('assert');
const d=JSON.parse(fs.readFileSync(process.argv[1],'utf8'));
const ts=d.triggerDefinitions, keys=Object.keys(ts);
assert.strictEqual(keys.length,206);
let compiled=0;
for(const [k,v] of Object.entries(ts)) {
  assert.strictEqual(k,v.name);
  assert.ok(JSON.stringify(v).length <= 10000,k+' too large');
  if(v.script?.trim()){new Function('storage','check','effects','info','log','let skip=false;'+v.script);compiled++;}
}
assert.strictEqual(compiled,198);
const scripts={
 planning:ts.sys_lc_native_time_bridge_planning.script,
 state:ts.sys_lc_native_time_bridge_state.script
};
const mk=(period='morning',mode='prefer-native',abs=0)=>({
 day:1,period,tick:1,action:'I look around',
 storage:{sys_clock_initialized:true,sys_clock_absolute_minutes:abs,
 sys_continuity_config:{calendar:{startHour:12,startMinute:0,minutesPerTurn:1},
 nativeTime:{enabled:true,mode,minutesPerOrdinaryTurn:1}},
 sys_lc_systems_config:{clock:{enabled:true}},sys_lc_command_only_turn:false}
});
const run=(s,phase)=>{
 const c=({type})=>({day:s.day,'time-of-day':s.period,'game-tick':s.tick,'action-text':[s.action]})[type];
 new Function('storage','check','effects','info','log','let skip=false;'+scripts[phase])(s.storage,c,[],{},()=>{});
};
let s=mk();run(s,'planning');assert.equal(s.storage.sys_clock_absolute_minutes,0);
assert.equal(s.storage.sys_lc_native_time_bridge.active,true);
s.tick=2;run(s,'state');assert.equal(s.storage.sys_clock_absolute_minutes,1);
s.tick=3;s.day=3;s.period='noon';run(s,'planning');
assert.equal(s.storage.sys_clock_absolute_minutes,3180,'two-day native skip must not double-count');
s.tick=4;s.day=2;s.period='night';run(s,'planning');
assert.equal(s.storage.sys_clock_absolute_minutes,3180,'clock regression must not rewind');
assert.equal(s.storage.sys_lc_native_time_bridge.status,'native-regression-held');
s=mk('', 'prefer-native');run(s,'planning');
assert.equal(s.storage.sys_lc_native_time_bridge.active,false,'empty native time falls back');
s=mk('morning','legacy');run(s,'planning');
assert.equal(s.storage.sys_lc_native_time_bridge.active,false,'legacy opt-out remains available');
s=mk('afternoon','prefer-native',123456);run(s,'planning');
assert.equal(s.storage.sys_clock_absolute_minutes,123456,'existing-save minute state survives');
console.log('LC native-time smoke checks passed; scripts compiled: '+compiled);
"""
        p = subprocess.run(["node", "-e", js, str(WORLD)],
                           capture_output=True, text=True, check=False)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)


if __name__ == "__main__":
    unittest.main()
