# Implemented automation architecture

This page describes the existing modules; proposed future modules remain in the [archived working plan](archive/ROCKY_PLATEAU_WORKING_PLAN.md). No new gameplay design is introduced by documentation organization.

| Source | Responsibility |
|---|---|
| `scripts/main.txt`, `scripts/metrics/RunMetrics.txt` | Preserved observer entry and measurement helper; import is `SpeedRun/main` |
| `scripts/basic/main.txt` | Installed B2.1-TS entry, lifecycle, route classification, one Generic tick and one metrics observation |
| `scripts/basic/config/Settings.txt` | Shared combat/travel/diagnostic flags and broad gear criteria |
| `scripts/basic/equipment/Catalog.txt` | Init-time inventory lookup and one-handed `Apply`/`ApplyPair` executor |
| `scripts/basic/combat/Generic.txt` | Shared offense, optional sustain, conservative travel and bounded collection |
| `scripts/basic/locations/Dispatcher.txt` | Eight-route classification; unknown/quest gate |
| `scripts/rocky/main.txt` | R15 entry; calls Rocky first only on the Rocky route; shared fallback only if unhandled |
| `scripts/rocky/config/RockySettings.txt` | ★15 target, explicit candidate selectors, owner-confirmed nickname and fallback settings |
| `scripts/rocky/equipment/RockyGear.txt` | Cached one-copy role availability, allowed-element selection and shield status |
| `scripts/rocky/locations/RockyPlateau.txt` | Scout/phases, adaptive exclusions, armor priority and boss-gap ownership |
| `scripts/selector_validation/main.txt` | Isolated count-only diagnostic; never combine with automation |

R15 uses the shared B2.1 modules and original metrics dependency without changing their live files. A handled Rocky frame owns the equipment request; Generic is skipped. An unhandled Rocky frame issued no Rocky equipment request. Specialized requests go through the existing pair executor with the cached Rocky shield; transformations retain combat ownership rather than entering travel. These are implemented contracts, not evidence of successful native execution.

Imports are deployment namespaces (`SpeedRun`, `SpeedRunBasic`, `SpeedRunRocky`, `EquipmentSelectorTest`), not repository folder names. Use only one active entry. [R15](rocky/ROCKY_PLATEAU_15.md) is authoritative for its current manifest and future activation; [B2.1](guides/BASIC_AUTOMATION.md) and [observer installation](guides/INSTALLATION.md) cover the other entries.

Inventory checks stay at preparation; changing target/HP/armor/phase data is considered per frame. Keep diagnostics optional and histories bounded. The [knowledge base](STONESCRIPT_KNOWLEDGE.md) owns native API/evidence rules. Private save importing and selector hypotheses are offline tooling, not a runtime gear database. See [import workflow](gear/PRIVATE_INVENTORY_IMPORT.md) and [gear review](gear/GEAR_REFERENCE_REVIEW.md).

No Heavy Hammer executor, protected active-ability sequence, calibrated dodge or AAC is implemented in R15. No schema or gameplay change is part of this organization.
