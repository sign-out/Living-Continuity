# Native Voyage time compatibility — LC preview

This draft updates the **modular** `Living_Continuity.json` only. It is rebased onto the repo core (Heroes v37, 204 original triggers); **archived Voyage exports and add-ons are unchanged**.

## Overview

Voyage's built-in `day` and `time-of-day` become preferred world-time observations when both are readable. LC continues to expose `sys_clock_absolute_minutes` as a monotonic **compatibility ledger** for existing needs, NPC schedules, autonomous projects, weather, forecasts, and deadlines. Existing saves are not zeroed or force-migrated; all their time-relative storage remains valid.

Two independent bridge triggers run in `planning` and `state` before the original time consumers. Named periods are mapped to approximate hourly anchors, strictly for compatibility math — native Voyage does **not** expose an exact minute count here. The adapter reconciles native transitions against elapsed minutes already credited. It does not rewind the ledger if a native timestamp regresses. Until a usable native reading appears, legacy time handling remains available.

### Configuration

`storage.sys_continuity_config.nativeTime` (created and preserved by `sys_clock_initialize`):

```json
{"enabled":true,"mode":"prefer-native","minutesPerOrdinaryTurn":1,"showApproximateClock":false}
```

- `mode: "prefer-native"`: follow native day/period once initialized.
- `mode: "legacy"` or `enabled: false`: retain old independent LC time writers.
- `minutesPerOrdinaryTurn`: bounded compatibility estimate, **not** native precision.
- `showApproximateClock: true`: opt into approximate minute display; otherwise HUD/time command present native named periods.

Bridge diagnostics: `storage.sys_lc_native_time_bridge` tracks activation, source status, observed day and period, transition deltas, and any non-monotonic reading.

### Scope of edits

Only 9 original triggers have changed (`sys_clock_initialize`, time writers, prose reconciliation, HUD and time command). Two native bridge triggers are added. All 195 remaining original triggers, all non-trigger world fields, five newer NPC-competence triggers, and add-ons remain untouched.

Native time owns day/week transitions. Explicit **sub-day** durations and substantial activities can still contribute minutes to LC's compatibility ledger so autonomous systems continue moving. The speculative 60-minute fallback in prose reconciliation is removed when actual time passage was not established.

### Testing and cautions

- `python -m unittest discover -s tests -p 'test_*.py' -v` runs repo snapshot/contract tests and the new native-time smoke checks.
- The local precursor build passed 21 behavioral tests; this branch is independently validated by static script compilation and a native-time smoke harness.
- **Not production proven.** Live Voyage Studio testing is necessary for trigger order, first empty native period, sleep/skips, exact-duration activities, OOC commands, save migrations, and narrator/clock synchronization.
- Native day/period changes do not prove an NPC met a schedule or completed any action. Existing calendar catch-up gaps for must-happen events remain a separate concern.
- Because native time is period-granular, hour/minute rates remain approximations; avoid claiming exact native timestamps in user-facing HUD or story text.
- Existing calendar-origin or saved-state offsets may persist intentionally to protect deadline continuity.
