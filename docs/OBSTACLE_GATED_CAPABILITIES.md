# Obstacle-gated resolution and positive capability continuity

## Design tournament

Candidates evaluated against host safety, prompt budget, false restrictions, durability, and feasibility:

1. **Prompt-only policy:** simplest and essential for stopping adjective-driven difficulty; cannot persist capabilities across long gaps.
2. **Unstructured narration mining:** automatically extracts abilities from prose, but risks promoting hallucinated successes and adding inferred ceilings. Rejected.
3. **Evidence-gated structured registry + prompt policy (selected):** persistent positive statements admitted only from confirmed, owner-attributed events; relevance-based retrieval; native outcomes still lead.
4. **Independent dice/difficulty engine:** adds checks and conflicts with Voyage host resolution. Rejected.

## Contract

- Action interpretation: require a concrete preexisting obstacle before narrator-generated difficulty. No promised success; host results still authoritative.
- Capability evidence input: `storage.sys_lc_capability_evidence` array of `{id?,entityId,capability,sourceEventId,source?,confirmed:true}`. Producers MUST submit a **generalized positive capability**, not a literal feat. Only independently confirmed evidence is eligible; player claims and attempted actions are not confirmations.
- Persistent output: `storage.sys_lc_positive_capabilities` keyed by stable capability ID; source event retained. A record is not a host skill unlock.
- Retrieval: match meaningful words from the effective player action, emit at most three compact records. Omission is not deletion.
- Configuration: `storage.sys_continuity_config.positiveCapabilities = {enabled:true,maxRecords:96,maxRelevant:3}` (all optional).
- Existing `sys_lc_capability_progression` remains authoritative for progression stages. This new registry is a non-mechanical continuity memory, not a competing progression system.

## Known limitations

No trustworthy generic event-to-capability semantic extractor exists in the current trigger runtime. This PR intentionally **does not** claim automatic inference from arbitrary prose. Existing host or LC event producers must explicitly submit generalized confirmed evidence. Matching is lexical, so synonyms may miss. The policy instructions apply even when no record matches. Multiplayer owner/privacy projection needs further integration before submitting private records; avoid feeding private player evidence into a shared party storage queue.

## Regression scenarios (manual Voyage Studio)

1. "I walk across the thin one-meter-wide bridge" with no established hazard: no invented wind, slipperiness, check or ordeal.
2. Same bridge explicitly broken and collapsing: narrator can recognize real obstacle; host mechanics decide.
3. "I catch the thrown red ball": no mandatory skill check from color or mundane action.
4. A confirmed gravity-field cargo manipulation yields positive capability "can manipulate external objects using gravitational fields"; later attempts must not treat original cargo mass as a maximum.
5. A failed or attempted action with `confirmed:false` creates no capability record.
6. Native failed roll remains failed; this module does not override the host.
7. Capability evidence attributed to actor A must not be merged into actor B's existing record.
8. No evidence, no action keyword match, or disabled config: no capability context emitted.
9. Test private multiplayer capability evidence only after a per-player projection path is implemented.

Static JSON shape and JS scripts require validation in the target Voyage Studio runtime; no runtime success is asserted here.
