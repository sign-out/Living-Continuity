# Living Continuity (LC)

Modular, host-safe continuity infrastructure for Latitude Voyage.

## Which JSON should I install?

Use **[Living_Continuity.json](Living_Continuity.json)** as the modular LC core. Optional independent add-ons are [Groups That Remember](addons/LC_Groups_That_Remember.json) and [SkillWeave](addons/LC_SkillWeave.json). They are separate add-ons, not additional copies of the core.

The `exports/` directory retains dated **unmodified-in-meaning** Voyage source exports for comparison. Those are not the recommended modular install files: a complete Voyage export can include world-specific defaults and may lack compatibility shims maintained in this repo.

See the [November 3, 2026 release notes](docs/releases/2026-11-03.md), [October 2026 Voyage compatibility notes](docs/VOYAGE_OCTOBER_2026_COMPATIBILITY.md), and [GitHub releases](https://github.com/sign-out/Living-Continuity/releases).

## Validation

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
```

This is static validation. Runtime outcomes must still be checked in Voyage Studio.

## Corrected bundled Groups export

The [quest-summary-syntax-fixed LC + Groups bundle](exports/LC_Groups_Bundled_Quest_Summary_Fixed_2026-11-03.json) is a **complete Voyage world/export snapshot**, not a standalone add-on or a replacement for the installable modular LC core. It includes six Groups triggers but follows a different LC runtime branch and does not contain the separate core's NPC-competence triggers. Use it only when reproducing that particular combined source. See [patch release notes](docs/releases/2026-11-03.1.md).
