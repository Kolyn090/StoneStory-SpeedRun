# B2 diagnostic update deployment record

Date: 2026-10-29. Scope: shared diagnostic stabilization only. No advanced boss behavior or AAC. Native parser execution, new-import success, location completions and measurement accuracy are unverified pending owner tests.

## Preservation and backups

Original observer scripts and `backups/pre-basic-20261029/` remain unchanged. Before replacing any candidate files, the existing candidate is copied and hash-verified at:

```text
backups/pre-basic-b2-20261029/steam-SpeedRunBasic
backups/pre-basic-b2-20261029/save-SpeedRunBasic
```

This preserves the pre-B2 candidate separately from the earlier known-working observer backups. Existing backups are never overwritten. Files not belonging to these candidate modules are not changed. Mind Stone text is not changed.

## Destinations and dependency

```text
<game-install>/Stone Story_Data/StreamingAssets/Stonescript/SpeedRunBasic
<save-folder>/Stonescript/SpeedRunBasic
```

Both roots contain the same five source modules: main, config/Settings, equipment/Catalog, combat/Generic, locations/Dispatcher. All new/import references resolve to files in their own root, including the preserved sibling `SpeedRun/metrics/RunMetrics.txt`. Deployed file hashes are compared to repository sources. This is filesystem consistency verification, not in-game import execution.

## B2 changes

- Compact twelve-line optional overlay with current location, handler, strategy, requested/actual equipment, missing core families, preferred-selector misses and policy warnings.
- Per-frame requests cleared even when decisions are skipped; two-handed harvesting no longer displays a nonexistent shield request.
- Missing core gear suppresses project equipment/potion commands. No native error-catching API is invented; native AI remains active and Tab reports game errors.
- Potion default remains off. Original metrics object and lifecycle ordering remain in use; the compact display reads its state instead of drawing the original full overlay.

## Validation and next step

Source static lint and B2 contract checks pass. Both deployment roots have matching imports/files; original observer, historical backup, and inventory hashes are checked for preservation. No location's NOT RUN status changes from these checks.

Use the existing `import SpeedRunBasic/main`, start a fresh Rocky Plateau run, and look for the `B2` header. Follow [BASIC_TEST_PLAN.md](BASIC_TEST_PLAN.md); record actual results in [BASIC_TEST_RESULTS.md](BASIC_TEST_RESULTS.md). Roll back to the unchanged observer with `import SpeedRun/main`. Do not restore full game saves.
