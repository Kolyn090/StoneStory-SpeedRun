# B2 selector and API review

B2.1-PS addition: documented `pickup`, `pickup.distance`, `ai.walking`, `foe.count`, `totaltime`, `hp`/`maxhp`, cached `item.GetCount("star stone")`, existing `equipL`/`equipR` application and scalar project state. The [official tutorial](https://stonestoryrpg.com/stonescript/) demonstrates equipping Star Stone for pickups below 10 units; the manual also gives a below-5 example. Neither example establishes the exact maximum attraction radius. No Star Stone activation, native cooldown identifier, pickup ID/event/enumeration or range-query API is assumed. Slot replacement and actual movement/attraction require in-game validation.

Current B2.1-NR delta: optional `harvest` queries and shovel selectors/commands are removed from basic automation. Entries below mentioning them describe historical API review, not active behavior. No new native API is introduced. Standalone selector-validation shovel probes remain diagnostic-only and are not a farming policy.

Reviewed 2026-10-29 against the [official manual](https://stonestoryrpg.com/stonescript/manual.html), displayed v4.35.2 (2026-09-25). This verifies documented forms/APIs, not parser execution of B2 or availability/quality of inventory items.

| Used forms / API | Manual section | Review |
|---|---|---|
| `new`, object fields/methods, `func`, parameters, `return` | Functions; Importing External Scripts | Supported composition |
| `?`, `:`, `:?`, boolean/numeric operators, `var`, string concatenation | Basics; Comparisons; Variables; Math | Supported forms |
| Fixed arrays, indexing, `Add`, `Clear`, bounded `for` | Loops; Arrays | Supported containers/operations |
| `loc.id`, `loc.stars`, `loc.isQuest`, `loc.begin`, `loc.loop`, `loc` | Game State | Supported location/lifecycle inputs |
| `foe`, distance, armor, `foe.GetCount`, `boss`, `undamageable`, physical/ranged immunity | Game State; Search Filters | Supported inputs/filters |
| `ai.enabled`, `ai.paused`, `hp`, `maxhp`, `harvest`, harvest distance | Game State | Supported inputs |
| `item.GetCount(criteria)`, `string.Equals` | Native Functions | Supported existence and exact-string checks |
| `equipL`, `equipR`, `equip @selector@`, subtractive criteria | Commands | Supported selection syntax; two-handed shovel uses `equip` |
| `item.left`, `item.right`, `item.potion`, `item.CanActivate()`, `activate potion` | Game State; Native Functions; Commands | Supported inputs/activation; potion setting remains off |
| Advanced prints with interpolation, `time`, `totaltime`, `lbtime` | Commands; Game State | Supported diagnostics/measurement forms |

## Complete configured selector families

Configuration: `scripts/basic/config/Settings.txt`; fallback literals: `equipment/Catalog.txt`.

- Five elemental swords: `{poison,vigor,aether,fire,ice} sword -big`.
- Five elemental wands: `{poison,vigor,aether,fire,ice} wand`.
- Five elemental hammers: `{poison,vigor,aether,fire,ice} hammer -heavy`.
- Defaults/utilities: `stone sword -big`, `vigor wand`, `vigor hammer -heavy`, `compound shield`, `vigor sword dL -big`, `shovel`.
- Additional fallback literals: `sword -big`, `wand`, `hammer -heavy`, `vigor shield`.

The brace notation above describes five concrete strings; it is documentation, not Stonescript syntax. All strings use documented criteria and subtractive forms within the seven-criterion equip limit. `dL` is explicitly demonstrated by the manual's low-HP vigor-sword example. The manual does not certify every concrete inventory name or enchantment combination. Therefore each configured preferred selector is checked at initialization, misses are exposed in B2, and the exact selected item must still be observed in-game. A valid query can return zero or select an unintended duplicate.

There is no documented native parser-error capture/query API used here. Project warnings expose missing gear and unsupported conditions; read native errors using the game's diagnostics. Elemental matchups, distance thresholds, AoE benefit, lifesteal adequacy, and boss effectiveness are policies to test, not API guarantees.
