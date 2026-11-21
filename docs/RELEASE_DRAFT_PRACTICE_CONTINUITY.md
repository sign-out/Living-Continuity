# LC — Obstacle-Gated Action Resolution & Positive Practice (Draft)

**Status:** Experimental draft / not production-ready  
**Source PR:** https://github.com/sign-out/Living-Continuity/pull/3  
**Source branch:** `feature/obstacle-gated-capability-continuity`  
**Suggested prerelease tag:** `practice-continuity-preview-2026-11-21`

## Changes

- Player-favorable action resolution: only established, defensible obstacles should create difficulty, failure, or costs; preserve native mechanics and NPC autonomy.
- Confirmed successes preserve demonstrated capabilities as positive evidence, not maximum limits.
- Confirmed meaningful unsuccessful attempts can accrue practice independently of success.
- Repeated verified practice accumulates without creating a competing numeric skill or guaranteed-success mechanic.
- Idempotent evidence ingestion with bounded processing and owner-specific records.
- Relevant capability and practice evidence may inform subsequent action narration.
- Preserve the four existing native player-scoped attribution probes for social, knowledge, consequence, and progression.
- Add documentation and static regression contracts.

## Known limitations

- **Automatic gameplay evidence production is not complete.** Structured, actor-attributed confirmed events must be supplied to the evidence queue; generic progression matches alone do not identify exact technique or outcome.
- Native player-scoped trigger attribution is documented, but no general per-action actor-ID script API has been verified.
- Shared multiplayer context still has conservative privacy restrictions; full owner-specific private recall is not wired end-to-end.
- Full repository test suites and live Voyage Studio multiplayer regression tests have not been executed.

**Do not mark stable or merge solely on the basis of this draft.**
