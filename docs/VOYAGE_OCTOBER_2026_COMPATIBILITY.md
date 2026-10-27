# Voyage October 12–26, 2026 compatibility — LC (modular)

This is an **instruction-layer compatibility pass**, applied directly to the existing
`Living_Continuity.json` world/mod export, not a rewrite of LC's native trigger
system. Voyage V37 remains the target version.

## Source and compatibility status

- Baseline: `main` file `Living_Continuity.json` (original blob
  `fb5ee98064471d9f10420b4da4e27738ca52c690`).
- Existing LC release: 204 named native trigger definitions, 14 AI generation
  hook groups, modular LC architecture.
- This change: 15 instruction fields added or replaced, including three
  verbatim legacy NPC-intent policies preserved under `generateStory`.
- `triggerDefinitions`, `parties`, all other root fields and `heroesVersion`
  remain unchanged. No add-on files are modified.

## Behavior corrected

**Combat-focused NPC intents (October 14).** Voyage now focuses
`generateNPCIntents` on genuine combat. LC's previously generic social intent
instructions are preserved in the scene layer instead of being lost. The
combat hook now requires a real current combatant and respects host/native
combat tactics, available skills/equipment and NPC agency. Zero valid combat
intents are acceptable.

**Native effect precedence (October 17–26).** Native inventory checks and
item-add/item-remove, quest rewards, applied healing/resource/relationship
effects, time/day changes and location/area image effects should not be
duplicated when prose paraphrases the event. Native outcomes are facts;
candidate actions and narrated appearances are not automatic state writes.

**Location/realm discovery (October 14–26).** Hide unavailable geography,
honor explicit reveal conditions, and treat unsuccessful travel as an attempted
action. Gradual hints can be generated from region `hiddenInfo`, but are not
automatically an NPC's knowledge or the player's discovered geography.

**Starts and characters (October 14–26).** The host's conditional Story Start,
starting resources/quests, character creation policy, premade-edit locks,
current save/party and selected mode are authoritative. LC never grants or
reapplies a start just because it is mentioned.

**Identity and memory.** Keep aliases bound to the established NPC; record
confirmed partial/skipped/one-shot trigger outcomes without assuming rollback,
repetition or completion.

## Deliberate non-changes

- No new triggers, trigger script or host runtime field mappings were added.
  Exact JSON shape for newer native time/image effects is not established
  by the patch notes alone.
- Native clocks versus LC clocks have not been reconciled through a new
  runtime contract. No changes to `sys_clock_advance` or storage.
- Separate LC addons `LC_Groups_That_Remember.json` and `LC_SkillWeave.json`
  have not been modified.
- No additional user-created playable world data was introduced.

## Validation

The Python standard-library check in
`tests/test_voyage_oct2026_contract.py` verifies
the release signature, continuity guidance, location of preserved policies,
and (when `origin/main` is present) byte-equivalent JSON values for
all non-instruction top-level fields. Run:

```bash
python -m unittest discover -s tests -p 'test_voyage_oct2026_contract.py' -v
```

**Runtime validation still required:** Studio import/validation, combat vs
conversation routing, native trigger idempotency, clock ownership, discovered
realm filtering, and partial one-time effect behavior in a real game. This PR
is not proof that those behaviors are correct on every host.
