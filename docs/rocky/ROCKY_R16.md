# R16 Scout ability experiments — local, disabled, undeployed

Branch `feat/rocky-r16-advanced-combat` was fast-forwarded safely from `876b0cf`
to `5d57ccf`, incorporating gameplay `1c696fe` and its successful-run documentation.
The six pre-existing staged entries, including the local R16 research note, are
preserved unchanged and excluded from this experiment's commit. Main and R17 are
not merged with R16. No live scripts, private inventory or gear CSVs are modified.

The comparison baseline is the owner-confirmed Rocky ★15 clear at `1c696fe`,
[approximately two minutes](ROCKY_PLATEAU_TEST_RESULTS.md#successful-baseline-1c696fe).
This is not a matched multi-run benchmark. R16 has no gameplay result or speed claim.

## Evidence and deliberate scope

The [official manual](https://stonestoryrpg.com/stonescript/manual.html) documents
`equip @selector@`, `activate R`, native count searches, global/item-specific
activation eligibility, cooldown IDs `mask` and `quarterstaff`, and object `Type`.
Specific eligibility requires equipped gear. A cooldown of -1 alone is not proof
of readiness. The [official tutorial](https://stonestoryrpg.com/stonescript/) shows
Quarterstaff approach with a target farther than 17 and equip/activate-R; its
distance is an example, not proof of safety against every enemy/variant.

Source study: [Cobblestone Mask helper](https://github.com/alexbarker234/stonescript/blob/bd9ed98f5331e72bd2fbeb0b80546615316e4825/Cobblestone.txt)
uses equip-mask plus right activation. [Eunomiac utilities](https://github.com/Eunomiac/stone-story/blob/e9921f9b141d45ab650797e03915e737a6ba3fc0/Scripts-PC/Utilities.txt)
provide historical effect guards. These are design leads, not copied code, verified
current effect IDs or borrowed boss timing. The R16 sequence code is original.

Agent visual inspection of the original local images in this task:

| Gear evidence | Displayed behavior | Ownership/selector boundary |
|---|---|---|
| `photograph/cropped/page_008/item_0059.png`, screenshot_0059 | Cultist Mask +21/21; +150% debuff duration; six Feeble applications to random foes; **affected foes lose 10 HP**, -2 damage penalty; 1.5s Feeble; 20s cooldown | One Mask record in the offline save. Candidate `cultist mask`; exact native count must be one |
| `photograph/cropped/page_002/item_0011.png`, screenshot_0011 | DashStaff +21/21; damage 16, DPS 34.29, range 5, armor/sec 1.75, armor 13.4; mini-dash with brief stun, cooldown 4.4s | Two saved Quarterstaff records, one raw primary enchantment level 21. This does not prove the join to the screenshot. Candidate `quarterstaff DashStaff`; require exactly one native match, with **no generic Quarterstaff fallback** |

The CSV values remain provisionally transcribed; this agent's targeted visual review
is not owner manual verification or a native ability test. No raw-save identifier,
inventory index or private source pointer is embedded in scripts/docs. Current native
availability is checked at preparation, not inferred from permanent save positions.
No copy independence, star mapping or exact selector success is assumed. Refresh
the existing private inventory after crafting/renaming and start a fresh trial.

## Implemented controls and sequence

Settings live in `scripts/rocky_r16/config/Experiments.txt`:

| Flag/default | Behavior when enabled |
|---|---|
| `maskEnabled = false` | Scout-only Mask trial, within 5 units, enemy observed HP >=100, player HP >=95%, no recovery/armor/immunity/physical fallback |
| `dashEnabled = false` | Scout-only approach while walking, player HP >=95%, distance **>17 and <=28**, same combat constraints |
| `showDiagnostics = false` | Four compact rows: phase/strategy/status, cached selectors, attempt counts/cooldowns, actual hands |

These eligibility thresholds are configurable conservative **experiment choices**,
not native effect range, stun duration or verified safe Scout attack windows.
All Dysangelos phases, transformations, unknown encounters and other difficulties
remain entirely R15-controlled. No new boss attack timing or susceptibility rule
is introduced. Mask is considered only close up; dash only at approach distance.

The coordinator caches exactly-one-match selectors once at existing preparation
points. An arm consumes an attempt even if interrupted or unavailable. Default
budgets are one Mask and one dash per run/loop. Configurable budgets are bounded
1–3; retry intervals cannot be below 600 Mask frames /132 dash frames, based on
displayed 20s/4.4s cooldowns at documented 30fps, and native cooldown still gates use.
These are retry caps, not assertions that an effect is active. With no verified
Feeble UID, **no effect-status or boss-immunity claim/query is invented**.

1. Validate context, cached equipment, cooldown and global eligibility.
2. Equip with the generic `equip` form, safely permitting a two-handed Quarterstaff;
   reserve exclusive equipment ownership and reset AAC sampling. No ability is
   activated on the first equip frame.
3. On a later frame, require `item.CanActivate("mask"/"quarterstaff")` and a matching
   **right-hand** item before one `activate R`. Unknown cooldown -1 may enter the
   bounded equip trial, but cannot bypass specific eligibility or the hand check.
4. Retain the item for a configurable post-activation hold (default one frame).
   Equip timeout defaults six frames; both bounds are limited to 1–30. These are
   experimental settling bounds, **not measured cast completion**. Actual activation,
   stun, backflip compatibility and interruption need native observation.
5. Return equipment ownership to R15, which recomputes the current allowed dual
   loadout. No stale pre-ability pair is restored. A consumed budget prevents loops.

Healing, constraints, AI suspension, target changes or lost eligibility cancel the
experiment without a stale restoration command. Protected Mind Stone handling
returns before the hook, so it owns the frame even if a Scout experiment was armed
previously. A phase change/timeout prevents resuming that old activation afterward.
The 23/30/90 ray helper, Vigor selection/thresholds, AAC component, equipment catalog,
elemental matching and shared B2.1 scripts are unchanged. Optional resource behavior
is inherited from R15; no farming, shovel, detour or collection wait is added.

## Integration and independent packaging

The existing Rocky handler gains only a nullable optional object and a five-line
hook after the intended pair/recovery decision, before AAC. R15 main never attaches
this object. With all new flags off, tested equipment decisions equal R15; this is
not a claim of byte-identical runtime cost. There is no per-frame inventory scan.

`scripts/rocky_r16/main.txt` attaches the coordinator and follows existing lifecycle
and measurement rules. The [local packager](../../tools/prepare_r16_candidate.py)
maps the shared handler source to **`SpeedRunRockyR16/locations/RockyPlateau.txt`**
without keeping a duplicate handler in the repository. The immutable bundle under
ignored `artifacts/rocky-r16/` contains four R16-only payload scripts plus a manifest.
Its nine baseline dependencies are recorded and required; they are **not copied
over the existing R15/B2.1 installation**. Handler ownership stays isolated.

Run `python -B tools/prepare_r16_candidate.py --prepare` to create/check this local
bundle. This command does not deploy. After separate authorization, back up any
existing `SpeedRunRockyR16` targets, install only the four new-namespace payload
files in both roots, verify all payload/dependency hashes, and use only:

```stonescript
import SpeedRunRockyR16/main
```

Do not import R15 main or B2.1 main beside it. Rollback is to restore the Mind Stone
line `import SpeedRunRocky/main`; existing R15 files are preserved. The current task
does not perform either Mind Stone edit or deployment.

## Deferred effects and potion

Each future effect must get its own opt-in flag and evidence gate; this release adds
only the Mask's flag, not unused switches or a generic effect framework.

| Candidate evidence | Decision |
|---|---|
| Fire Crossbow screenshot_0020 applies Burn; CSV describes 195 damage over time | Distinct ranged variant; no transplantation to ordinary Fire Sword or new rotation |
| Ice Crossbow screenshot_0022 / Big Ice Sword screenshot_0031 apply Chill; 18.6s displayed duration | Two-handed/ranged differences and altered enemy attack timing need targeted tests; deferred |
| Explosive Wand screenshot_0072 Burn; Frost Wand screenshot_0073 Chill and active stun | Distinct passives/abilities, selector and boss effect persistence not established; deferred |
| Plague Wand screenshot_0074 poison wave/Weaken | Weaken is not a proven Poison DoT or Feeble UID; deferred |
| Ordinary elemental Poison Sword | Elemental damage alone does not establish a Poison DoT configuration; no DoT maintained |
| Berserk Potion | `activate potion` and `item.potion` are documented, but current recipe/content identity, remaining-use availability and any applicable restrictions have not been confirmed for this player/build. No consumption, brewing or speculative availability check added |

No active effect IDs, exact stun duration, boss susceptibility or repeatable speed
benefit can be inferred from the description alone. Extra effects could change ray
timing; the successful ray parameters are deliberately preserved.

## Validation and first supervised experiments

Local checks: full Python suite, Rocky regressions, both packagers/import checks,
shared B2 checks and documentation validation. `Test-RockyNativeExpressions.ps1`
with `-ManagedDirectory <game>/Stone Story_Data/Managed -R16` retains the 17 native
AAC regression cases, parses four prepared control-flow sources and executes only
the disabled flag declarations offline. The standalone grammar lacks native command
registration: documented `equip @selector@` / `activate R` and the unchanged baseline
`activate potion` lines are excluded from that syntax pass, not falsely claimed
executed natively. Actual command paths and ownership are covered by the synthetic
source-policy harness; abilities and gameplay effects remain **unverified**.

After a separately authorized installation, test individually:

1. **All off:** load the separate import; reproduce the `1c696fe` loadout/recovery/
   phase/ray behavior and a complete run. No R16 equip/ability requests should occur.
2. **Dash only**, compact diagnostics on: first confirm a unique cached DashStaff
   selector and actual Quarterstaff in the right hand. Record one Scout approach's
   before/after distance, activation/cooldown, restored combat pair, time to first
   hit, interruptions and total clear time versus walking/Triskelion. Stop if the
   variant/activation is wrong or the approach is unsafe. No boss dash is expected.
3. **Mask only:** confirm unique Mask match, later-frame activation, cooldown start,
   return to dual combat and no repeat attempt that run. Capture enemy HP/debuff
   strings before/after if practical; random distribution means current-target HP
   alone cannot prove all six applications. Verify player HP is not being confused
   with the affected-foe 10-HP effect. No claim that Feeble is active is displayed.
4. **Combine only after individual passes.** Recheck Vigor interruption, armor,
   phase gaps and Perfected ray ownership. Report exact revision, flags/selectors,
   build, first-entry/loop, completion/deaths/interventions and consistent timing.

Defaults remain off until these observations. No deployment or improved-time claim
is authorized by passing local tests.

Local validation recorded 2026-10-30: **146 Python tests passed**, including **18 R16 tests**. The 17 native AAC regression checks passed; four prepared R16 control-flow sources passed syntax checks and disabled flags executed offline, with documented command exclusions above. R15/R16 import/package, shared B2, documentation-link and diff checks passed. All six pre-existing staged blobs and all 617 deployed files retained their initial hashes. No R16 in-game trial, deployment, merge into main or push was performed.
