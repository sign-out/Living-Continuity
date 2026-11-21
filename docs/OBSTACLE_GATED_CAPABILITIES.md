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

## Native Voyage multiplayer attribution discovery (2026-11-21)

The current community-maintained Voyage trigger documentation confirms that `scope: "player"` evaluates conditions against satisfying players and routes applicable effects to those players. A player-scoped `story` effect receives a host-generated attribution parenthetical identifying the affected player(s). `target: "satisfyingPlayers"` likewise directs individual player effects. Source: https://wiki.unofficial.voyage/mechanics/triggerDefinitions#targeting-a-specific-player

This is **native attribution for player-scoped trigger matching/effects**, not proof that scripts receive a per-action actor ID. The documented `check({type:'action-text'})` return is a raw array of player action strings, without a documented player-ID association. Therefore do not assume the array position maps to a player or parse the host's narrator parenthetical as a stable machine-readable ID.

Integration decision: use native player-scoped matching and player-specific effects for future capability evidence producers when appropriate; require explicit verified actor IDs for storage writes until a documented native actor-attribution script API is identified. Never assign a capability to the first/only guessed player in a multiplayer turn. Existing registry and narration policy remain usable. Do not claim complete automatic multiplayer evidence ingestion until this is verified in Voyage Studio.

## Tournament follow-up: practice from meaningful unsuccessful attempts

Selected: reuse native player-scoped progression attribution, retain four existing semantic probes, and distinguish **attempt evidence** from **demonstrated success**. Rejected: narrator-only memory, speculative extraction of a technique from generic progression marks, and a parallel numerical skill/difficulty system.

The ingestion trigger now accepts `outcome` (`success`, `failure`, `partial`, or `attempt`), `meaningfulAttempt: true`, and `possible` alongside existing confirmed, actor-attributed evidence. A successful event records a demonstrated capability and practice; a meaningful unsuccessful attempt records practice only. `possible: false` blocks practice accrual for impossible tasks. Unspecified outcome remains success for backwards compatibility with existing evidence producers; this does **not** mean a generic progression mark proves success.

Practice is stored separately by owner and technique (`storage.sys_lc_practice_continuity`) with idempotent source-event deduplication, attempt and success counts, and private-by-default visibility. These counts are evidence of experience, **not** automatic success thresholds, ability ceilings, or replacement Voyage skill values. Generic native progression marks alone cannot reliably name a technique or establish outcome; they remain attribution signals, not invented confirmed evidence.

### Regression matrix to run in Voyage Studio
1. Confirmed successful action -> one practice attempt + one demonstrated capability.
2. Confirmed failed meaningful action -> one practice attempt, no demonstrated success.
3. Repeat the same source event -> no additional attempt.
4. Different confirmed source events -> cumulative practice.
5. `possible:false`, unconfirmed, or unattributed event -> no new practice.
6. Two players performing different actions -> each record remains under its verified owner; no cross-player transfer.
7. Private practice and capability evidence -> never emit in a shared multiplayer story context.
8. Four existing social/knowledge/consequence/progression probes -> remain enabled and unchanged.
9. More than 128 queued evidence events -> bounded FIFO processing across turns without losing older events.
10. Future action resolution -> accumulated practice informs generous, proportionate outcomes but never guarantees success or imposes a ceiling.

**Still needed:** connect native attributed progression events and verified action outcomes to the structured evidence queue. A generic progression marker is not sufficient by itself to identify the practiced technique. Live Studio behavior has not been verified.
