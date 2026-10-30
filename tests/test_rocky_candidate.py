"""Synthetic source-policy tests; no native Stonescript interpreter/game execution."""
import importlib.util
from pathlib import Path
import shutil
from types import SimpleNamespace
import tempfile
import unittest

from stonescript_policy_harness import Array, Foe, Items, Strings, Text, load_module

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("rocky_packager", ROOT / "tools/prepare_rocky_candidate.py")
PACKAGE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PACKAGE)


class Gear:
    missing = 0
    defaultSword = Text("default sword")
    defaultWand = Text("default wand")
    shield = Text("shield")
    def __init__(self): self.calls = []; self.clears = 0
    def ClearRequest(self): self.clears += 1
    def Apply(self, selector): self.calls.append(str(selector))
    def ApplyPair(self, selector, shield):
        self.calls.append(str(selector))
        self.lastShield = str(shield)


class PolicyTests(unittest.TestCase):
    def test_native_reserved_profile_identifier_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(ROOT / "scripts", root / "scripts")
            main = root / "scripts/rocky/main.txt"
            main.write_text(main.read_text().replace("rockyConfig", "profile"))
            with self.assertRaisesRegex(ValueError, "reserved identifier profile"):
                PACKAGE.inspect(root)

    def setUp(self):
        self.strings = Strings()
        self.settings = SimpleNamespace(swords=Array(Text(x + " sword") for x in ("poison","vigor","aether","fire","ice")),
            wands=Array(Text(x + " wand") for x in ("poison","vigor","aether","fire","ice")),
            hammers=Array(Text(x + " hammer") for x in ("poison","vigor","aether","fire","ice")),
            healingSword=Text("vigor sword dL"), usePotion=False, potionHpRatio=.25, healingHpRatio=.4)
        counts = {str(x): 1 for family in (self.settings.swords, self.settings.wands, self.settings.hammers)
                  for x in family}
        counts.update({"stone sword -big +21": 1, "vigor sword dL": 1,
                       "towering shield +21": 1, "FastGenShl": 1, "vigor sword dL -big +21": 1, "mind stone": 1})
        self.items = Items(counts)
        self.native = dict(string=self.strings, item=self.items, foe=Foe(), hp=100, maxhp=100,
                           ai=SimpleNamespace(enabled=True, paused=False), loc=SimpleNamespace(stars=15), totaltime=0)
        self.profile = load_module(ROOT / "scripts/rocky/config/RockySettings.txt", self.native)
        self.profile.dualWieldEnabled = False  # Preserve shielded-policy regression cases.
        self.attacks = load_module(ROOT / "scripts/rocky/combat/AttackCycle.txt", self.native)
        # Synthetic labels keep policy assertions separate from native search claims.
        self.profile.swords = self.settings.swords
        self.profile.wands = self.settings.wands
        self.profile.hammers = self.settings.hammers
        self.equipment = load_module(ROOT / "scripts/rocky/equipment/RockyGear.txt", self.native)
        self.equipment.Prepare(self.settings, self.profile)
        self.handler = load_module(ROOT / "scripts/rocky/locations/RockyPlateau.txt", self.native)
        self.gear = Gear()
        self.combat = SimpleNamespace(travelBossSeen=False, starUntil=100)

    def frame(self, value="", buffs="", armor=0, hp=100, player_hp=100, foe_state=0, foe_time=0, total=0):
        state = Foe(value, buffs, armor, hp)
        state.state, state.time = foe_state, foe_time
        # Compiled functions use their own global namespace, sharing fake native inputs.
        for obj in (self.handler, self.equipment, self.attacks, self.combat):
            for name in dir(type(obj)):
                method = getattr(type(obj), name)
                if hasattr(method, "__globals__"):
                    method.__globals__.update(foe=state, hp=player_hp, totaltime=total)
        self.gear.calls.clear()
        return self.handler.Tick(self.gear, self.settings, self.equipment, self.profile, self.combat, self.attacks)

    def test_ordinary_and_disabled_are_pure_shared_fallback(self):
        self.assertFalse(self.frame("insect"))
        self.assertEqual(self.gear.calls, [])
        self.assertEqual(self.gear.clears, 0)
        self.profile.enabled = False
        self.assertFalse(self.frame("dysangelos phase1"))
        self.assertFalse(self.handler.bossLatched)

    def test_scout_bearer_elementalist_and_perfected_armor(self):
        for target, expected in [("acronian_scout", "fire sword"),
                                 ("dysangelos_bearer phase1", "fire sword"),
                                 ("dysangelos_elementalist phase2 poison", "ice sword")]:
            with self.subTest(target=target):
                self.assertTrue(self.frame(target))
                self.assertEqual(self.gear.calls, [expected])
        self.assertTrue(self.frame("dysangelos_perfected phase3", armor=10))
        self.assertEqual(self.gear.calls, ["fire hammer"])
        self.assertTrue(self.combat.travelBossSeen)
        self.assertEqual(self.combat.starUntil, 0)

    def test_named_phase_aliases_work_without_phase_tag(self):
        for alias, phase in [("dysangelos_bearer", "bearer"),
                             ("dysangelos_elementalist", "elementalist"),
                             ("dysangelos_perfected", "perfected")]:
            self.frame(alias)
            self.assertEqual(str(self.handler.phase), phase)

    def test_all_elemental_choices_blocked_uses_physical_not_resisted_element(self):
        buffs = ",".join("adaptive_defense_" + element + ":1:9" for element in
                         ("poison", "vigor", "aether", "fire", "ice"))
        self.frame("dysangelos phase3", buffs=buffs)
        self.assertEqual(self.gear.calls, ["stone sword -big +21"])

    def test_absent_target_and_undamageable_keep_boss_ownership(self):
        self.frame("dysangelos phase1")
        self.assertTrue(self.frame())
        self.assertEqual(str(self.handler.phase), "transition-gap")
        self.assertEqual(self.gear.calls, ["fire sword"])
        self.frame("dysangelos phase2 undamageable")
        self.assertEqual(str(self.handler.phase), "elementalist-transition")
        self.assertEqual(self.gear.calls, ["fire sword"])
        self.assertTrue(self.frame("dysangelos phase2", hp=0))

    def test_adaptive_multiple_exact_tokens_and_cached_parsing(self):
        buff = "icon:adaptive_defense_fire:1:99,icon:adaptive_defense_ice:1:99"
        self.frame("dysangelos phase3", buffs=buff)
        self.assertEqual(self.gear.calls, ["vigor sword"])
        calls = self.strings.calls
        self.frame("dysangelos phase3", buffs=buff)
        self.assertEqual(self.gear.calls, ["vigor sword"])
        self.assertEqual(self.strings.calls, calls)
        self.frame("dysangelos phase3", buffs="icon:adaptive_defense_vigor:1:99")
        self.assertNotEqual(self.gear.calls, ["vigor sword"])

    def test_unknown_adaptive_and_unknown_phase_have_visible_fallback(self):
        self.frame("dysangelos phase3", buffs="icon:adaptive_defense_unknown:1:99")
        self.assertTrue(self.handler.unknownAdaptive)
        self.assertEqual(self.gear.calls, ["stone sword -big +21"])
        self.frame("dysangelos phase3", buffs="icon:adaptive_defense_fireball:1:99")
        self.assertTrue(self.handler.unknownAdaptive)  # Never mistake a prefix for exact fire UID.
        self.frame("dysangelos_new_phase")
        self.assertEqual(str(self.handler.phase), "unknown")
        self.assertIn("unknown Dysangelos", str(self.handler.warning))

    def test_missing_element_does_not_inherit_falsely_labelled_generic_fallback(self):
        self.items.counts["fire sword"] = 0
        self.equipment.Prepare(self.settings, self.profile)
        self.frame("dysangelos phase1")
        self.assertEqual(self.gear.calls, ["ice sword"])
        self.assertEqual(str(self.equipment.swords[3]), "")

    def test_low_hp_heal_is_blocked_by_adaptive_and_armor_has_priority(self):
        self.profile.bearerRecoveryEnabled = False
        self.profile.useHealingSword = True  # Optional historical R1 behavior, off in R15.
        self.frame("dysangelos phase1", player_hp=20)
        self.assertEqual(self.gear.calls, ["vigor sword dL"])
        self.frame("dysangelos phase3", buffs="adaptive_defense_vigor:1:9", player_hp=20)
        self.assertNotIn("vigor sword dL", self.gear.calls)
        self.frame("dysangelos phase3", armor=10, player_hp=20)
        self.assertIn("hammer", self.gear.calls[0])

    def test_immunity_missing_core_and_suspended_ai(self):
        self.frame("dysangelos phase1 immune_to_physical")
        self.assertEqual(self.gear.calls, ["fire wand"])
        self.frame("dysangelos phase1 immune_to_ranged")
        self.assertEqual(self.gear.calls, ["fire sword"])
        self.frame("dysangelos phase1 immune_to_physical immune_to_ranged")
        self.assertEqual(str(self.handler.strategy), "immunity-conflict-manual")
        self.gear.missing = 1
        self.frame("dysangelos phase1")
        self.assertEqual(self.gear.calls, [])
        self.gear.missing = 0
        self.native["ai"].paused = True
        self.frame("dysangelos phase1")
        self.assertEqual(self.gear.calls, [])

    def test_no_allowed_weapon_is_warning_not_false_success(self):
        self.items.counts.clear()
        self.items.counts["towering shield +21"] = 1
        self.equipment.Prepare(self.settings, self.profile)
        self.frame("dysangelos phase3")
        self.assertEqual(str(self.handler.strategy), "no-safe-selector-manual")
        self.assertIn("STOP", str(self.handler.warning))
        self.assertEqual(self.gear.calls, [""])  # Pair executor emits no L command.
        self.assertEqual(self.gear.lastShield, "towering shield +21")

    def test_unknown_element_unknown_adaptive_immunity_and_armor_fallback(self):
        self.frame("dysangelos phase2")
        self.assertIn("element not recognized", str(self.handler.warning))
        self.frame("dysangelos phase3 immune_to_physical", buffs="adaptive_new:1:5")
        self.assertEqual(str(self.handler.strategy), "adaptive-immunity-manual")
        for selector in list(self.items.counts):
            if "hammer" in selector: self.items.counts[selector] = 0
        self.equipment.Prepare(self.settings, self.profile)
        self.frame("dysangelos phase3", armor=10)
        self.assertTrue(self.equipment.usedFallback)
        self.assertIn("sword", self.gear.calls[0])

    def test_reset_and_stable_selection_without_frame_inventory_queries(self):
        self.frame("dysangelos phase3", buffs="adaptive_defense_fire:1:9")
        queries = len(self.items.queries)
        self.frame("dysangelos phase3", buffs="adaptive_defense_fire:1:9")
        self.assertEqual(self.gear.calls, ["ice sword"])
        self.assertEqual(len(self.items.queries), queries)
        self.handler.Reset()
        self.assertFalse(self.handler.bossLatched)
        self.assertEqual(list(self.handler.blocked), [False] * 5)
        self.assertFalse(self.frame())

    def test_r15_low_hp_keeps_scout_fire_and_bearer_armor_priority(self):
        self.frame("acronian_scout vigor", player_hp=10)
        self.assertEqual(self.gear.calls, ["fire sword"])
        self.assertEqual(self.gear.lastShield, "FastGenShl")
        self.frame("dysangelos phase1", player_hp=10)
        self.assertEqual(self.gear.calls, ["vigor sword dL -big +21"])
        self.frame("dysangelos phase1", armor=20, player_hp=10)
        self.assertEqual(self.gear.calls, ["fire hammer"])

    def test_r15_uses_real_profile_selectors_instead_of_basic_defaults(self):
        actual = load_module(ROOT / "scripts/rocky/config/RockySettings.txt", self.native)
        for family in (actual.swords, actual.wands, actual.hammers):
            for selector in family:
                self.items.counts[str(selector)] = 1
        self.equipment.Prepare(self.settings, actual)
        self.frame("dysangelos phase1")
        self.assertEqual(self.gear.calls, ["fire sword -big +21"])
        self.frame("dysangelos phase3", armor=10)
        self.assertEqual(self.gear.calls, ["fire hammer -heavy +21"])
        self.assertEqual(self.gear.lastShield, "FastGenShl")

    def test_r15_all_observed_element_counters_with_fixed_shield(self):
        for element, counter in [("vigor", "poison"), ("aether", "vigor"),
                                 ("fire", "aether"), ("ice", "fire"), ("poison", "ice")]:
            self.frame("dysangelos phase2 " + element)
            self.assertEqual(self.gear.calls, [counter + " sword"])
            self.assertEqual(self.gear.lastShield, "FastGenShl")

    def test_r15_owner_nickname_and_missing_or_ambiguous_shields(self):
        self.assertTrue(self.profile.fastGenShieldConfirmed)
        self.assertEqual(str(self.profile.preferredShield), "FastGenShl")
        self.assertEqual(str(self.equipment.shield), "FastGenShl")
        self.assertIn("nickname", str(self.equipment.shieldStatus))
        self.frame("dysangelos phase1")
        self.assertEqual(self.gear.lastShield, "FastGenShl")
        for count in (0, 2):
            self.items.counts["FastGenShl"] = count
            self.equipment.Prepare(self.settings, self.profile)
            self.frame("dysangelos phase1")
            self.assertEqual(self.gear.lastShield, "towering shield +21")
            self.assertIn("missing/ambiguous", str(self.equipment.shieldStatus))
        for count in (0, 2):
            self.items.counts["towering shield +21"] = count
            self.equipment.Prepare(self.settings, self.profile)
            self.assertTrue(self.frame("dysangelos phase1"))
            self.assertEqual(self.gear.calls, [])
            self.assertEqual(str(self.handler.strategy), "missing-rocky-shield-manual")

    def test_r15_rejects_ambiguous_weapon_and_never_requeries_in_tick(self):
        self.items.counts["fire sword"] = 2
        self.equipment.Prepare(self.settings, self.profile)
        queries = len(self.items.queries)
        self.frame("dysangelos phase1")
        self.assertEqual(self.gear.calls, ["ice sword"])
        self.assertEqual(len(self.items.queries), queries)

    def test_r15_other_difficulty_falls_through_without_commands_or_latch(self):
        self.native["loc"].stars = 14
        self.assertFalse(self.frame("dysangelos phase1"))
        self.assertEqual(self.gear.calls, [])
        self.assertEqual(self.gear.clears, 0)
        self.assertFalse(self.handler.bossLatched)

    def test_r15_transform_retains_personalized_pair_and_zero_target_first(self):
        self.frame("dysangelos phase1")
        self.frame()
        self.assertEqual(self.gear.calls, ["fire sword"])
        self.assertEqual(self.gear.lastShield, "FastGenShl")
        self.handler.Reset()
        self.frame("dysangelos phase1 undamageable")
        self.assertEqual(self.gear.calls, ["fire sword"])
        self.assertEqual(self.gear.lastShield, "FastGenShl")


    def test_bearer_recovery_hysteresis_and_fixed_shield(self):
        for hp, recovering in [(100, False), (61, False), (60, True), (70, True),
                               (84, True), (85, False), (70, False), (60, True)]:
            self.frame("dysangelos phase1", player_hp=hp)
            self.assertEqual(self.handler.bearerRecoveryActive, recovering)
            self.assertEqual(self.gear.calls, ["vigor sword dL -big +21" if recovering else "fire sword"])
            self.assertEqual(self.gear.lastShield, "FastGenShl")
        self.assertEqual(str(self.handler.strategy), "bearer-recovery-sword-shield")

    def test_recovery_thresholds_are_configurable_and_invalid_values_fall_back(self):
        self.profile.bearerRecoveryEnterRatio = .3
        self.profile.bearerRecoveryExitRatio = .5
        self.frame("dysangelos phase1", player_hp=40)
        self.assertFalse(self.handler.bearerRecoveryActive)
        self.frame("dysangelos phase1", player_hp=30)
        self.assertTrue(self.handler.bearerRecoveryActive)
        self.frame("dysangelos phase1", player_hp=50)
        self.assertFalse(self.handler.bearerRecoveryActive)
        for entry, exit in [(0, .8), (.6, .6), (.9, .6), (.6, 1.1), (-.1, .8)]:
            self.profile.bearerRecoveryEnterRatio = entry
            self.profile.bearerRecoveryExitRatio = exit
            self.frame("dysangelos phase1", player_hp=10)
            self.assertFalse(self.handler.bearerRecoveryActive)
            self.assertEqual(self.gear.calls, ["fire sword"])
            self.assertEqual(str(self.handler.bearerRecoveryStatus), "invalid thresholds")

    def test_recovery_missing_or_ambiguous_weapon_and_disabled_fall_back(self):
        for count in [0, 2]:
            self.items.counts["vigor sword dL -big +21"] = count
            self.equipment.Prepare(self.settings, self.profile)
            self.frame("dysangelos phase1", player_hp=10)
            self.assertFalse(self.handler.bearerRecoveryActive)
            self.assertEqual(self.gear.calls, ["fire sword"])
            self.assertIn("missing/ambiguous", str(self.handler.bearerRecoveryStatus))
        self.items.counts["vigor sword dL -big +21"] = 1
        self.equipment.Prepare(self.settings, self.profile)
        self.profile.bearerRecoveryEnabled = False
        self.frame("dysangelos phase1", player_hp=10)
        self.assertEqual(self.gear.calls, ["fire sword"])

    def test_recovery_yields_to_armor_even_when_hammer_is_missing(self):
        self.frame("dysangelos phase1", player_hp=20)
        self.frame("dysangelos phase1", armor=5, player_hp=20)
        self.assertFalse(self.handler.bearerRecoveryActive)
        self.assertEqual(self.gear.calls, ["fire hammer"])
        for selector in list(self.items.counts):
            if "hammer" in selector: self.items.counts[selector] = 0
        self.equipment.Prepare(self.settings, self.profile)
        self.frame("dysangelos phase1", armor=5, player_hp=20)
        self.assertFalse(self.handler.bearerRecoveryActive)
        self.assertEqual(self.gear.calls, ["fire sword"])

    def test_recovery_yields_to_immunity_and_adaptive_constraints(self):
        for target, buffs in [("dysangelos phase1 immune_to_physical", ""),
                              ("dysangelos phase1 immune_to_physical immune_to_ranged", ""),
                              ("dysangelos phase1", "adaptive_defense_vigor:1:9"),
                              ("dysangelos phase1", "adaptive_new:1:9")]:
            self.frame(target, buffs=buffs, player_hp=20)
            self.assertFalse(self.handler.bearerRecoveryActive)
            self.assertNotIn("vigor sword dL -big +21", self.gear.calls)
        self.frame("dysangelos phase1 immune_to_ranged", player_hp=20)
        self.assertTrue(self.handler.bearerRecoveryActive)  # Compatible melee remains valid.

    def test_recovery_yields_to_gaps_and_resets_outside_bearer(self):
        for next_target, hp in [("", 100), ("dysangelos phase1 undamageable", 100),
                                ("dysangelos phase1", 0), ("dysangelos phase2 fire", 100),
                                ("dysangelos phase3", 100), ("acronian_scout", 100), ("insect", 100)]:
            self.handler.Reset()
            self.frame("dysangelos phase1", player_hp=20)
            last_pair = list(self.gear.calls)
            self.frame(next_target, hp=hp, player_hp=20)
            self.assertFalse(self.handler.bearerRecoveryActive)
            if next_target in ("", "dysangelos phase1 undamageable") or hp == 0:
                self.assertEqual(self.gear.calls, last_pair)  # Hold previous combat pair, no new recovery decision.
            self.frame("dysangelos phase1", player_hp=70)
            self.assertEqual(self.gear.calls, ["fire sword"])  # No stale recovery latch.
        self.frame("dysangelos phase1", player_hp=20)
        self.handler.Reset()
        self.assertFalse(self.handler.bearerRecoveryActive)

    def test_recovery_no_new_inventory_queries_and_ai_suspension_clears_indicator(self):
        queries = len(self.items.queries)
        self.frame("dysangelos phase1", player_hp=20)
        self.frame("dysangelos phase1", player_hp=70)
        self.assertEqual(len(self.items.queries), queries)
        self.native["ai"].paused = True
        self.frame("dysangelos phase1", player_hp=20)
        self.assertFalse(self.handler.bearerRecoveryActive)
        self.assertEqual(self.gear.calls, [])

    def test_post_scout_shared_travel_reinstates_triskelion_only_with_all_guards(self):
        self.frame("acronian_scout")
        self.frame("acronian_scout", hp=0)
        self.assertFalse(self.combat.travelBossSeen)
        self.assertFalse(self.handler.bossLatched)
        self.assertFalse(self.frame())  # Rocky releases ordinary target-free travel to Generic.
        foe = Foe()
        foe.count = 0
        self.native.update(foe=foe, pickup=False, totaltime=100, boss=Text("boss"))
        self.native["ai"].walking = True
        self.settings.triskelionTravelEnabled = True
        self.settings.passiveStarEnabled = False
        self.gear.triskelion = Text("triskelion")
        shared = load_module(ROOT / "scripts/basic/combat/Generic.txt", self.native)
        shared.travelBossSeen = self.combat.travelBossSeen
        shared.Tick(self.gear, self.settings)
        self.assertEqual(self.gear.calls[-1], "triskelion")
        globals_ = type(shared).CanTravelWithTriskelion.__globals__
        for block in ["injured", "nearby", "targeted", "not-walking", "boss", "disabled", "missing"]:
            with self.subTest(block=block):
                globals_["hp"] = 99 if block == "injured" else 100
                foe.value = "insect" if block == "targeted" else ""
                foe.count = 1 if block == "nearby" else 0
                self.native["ai"].walking = block != "not-walking"
                shared.travelBossSeen = block == "boss"
                self.settings.triskelionTravelEnabled = block != "disabled"
                self.gear.triskelion = Text("") if block == "missing" else Text("triskelion")
                self.assertFalse(shared.CanTravelWithTriskelion(self.gear, self.settings))

    def test_dysangelos_still_latches_travel_and_owns_transformations(self):
        self.frame("acronian_scout")
        self.assertFalse(self.combat.travelBossSeen)
        self.frame("dysangelos phase1")
        self.assertTrue(self.combat.travelBossSeen)
        self.assertTrue(self.handler.bossLatched)
        self.assertTrue(self.frame())
        self.assertTrue(self.combat.travelBossSeen)
        self.assertEqual(str(self.handler.phase), "transition-gap")
        self.assertEqual(self.gear.calls, ["fire sword"])


    def test_ray_arms_triggers_once_holds_and_recomputes_armor_element(self):
        self.frame("dysangelos phase3", foe_state=115, foe_time=22, total=100)
        self.assertEqual(str(self.handler.rayDodgeStatus), "armed")
        self.assertEqual(self.gear.calls, ["fire sword"])
        self.frame("dysangelos phase3", foe_state=115, foe_time=23, total=101)
        self.assertEqual(str(self.handler.rayDodgeStatus), "triggered")
        self.assertEqual(self.gear.calls, ["mind stone"])
        self.assertEqual(self.gear.lastShield, "FastGenShl")
        self.assertEqual(self.handler.rayDodgeAttempts, 1)
        self.frame("dysangelos phase3", foe_state=115, foe_time=23, total=101)
        self.assertEqual(str(self.handler.rayDodgeStatus), "holding")
        self.assertEqual(self.handler.rayDodgeAttempts, 1)
        self.frame("dysangelos phase3", armor=10, buffs="adaptive_defense_fire:1:9", foe_state=115, foe_time=52, total=130)
        self.assertEqual(self.gear.calls, ["mind stone"])
        self.frame("dysangelos phase3", armor=10, buffs="adaptive_defense_fire:1:9", foe_state=115, foe_time=53, total=131)
        self.assertEqual(str(self.handler.rayDodgeStatus), "restored")
        self.assertEqual(self.gear.calls, ["ice hammer"])
        self.assertEqual(self.gear.lastShield, "FastGenShl")
        for time in (54, 55, 80):
            self.frame("dysangelos phase3", foe_state=115, foe_time=time, total=132+time)
            self.assertEqual(self.handler.rayDodgeAttempts, 1)
            self.assertNotIn("mind stone", self.gear.calls)
        self.frame("dysangelos phase3", foe_state=2, total=230)
        self.frame("dysangelos phase3", foe_state=115, foe_time=23, total=240)
        self.assertEqual(self.handler.rayDodgeAttempts, 2)

    def test_ray_custom_trigger_and_hold_duration(self):
        self.profile.rayDodgeTriggerFrame = 5
        self.profile.rayDodgeHoldFrames = 3
        self.frame("dysangelos phase3", foe_state=115, foe_time=4, total=10)
        self.assertEqual(str(self.handler.rayDodgeStatus), "armed")
        self.frame("dysangelos phase3", foe_state=115, foe_time=5, total=11)
        self.assertEqual(self.handler.rayDodgeUntil, 14)
        self.frame("dysangelos phase3", foe_state=32, total=13)
        self.assertEqual(self.gear.calls, ["mind stone"])
        self.frame("dysangelos phase3", foe_state=32, total=14)
        self.assertEqual(self.gear.calls, ["fire sword"])
        self.assertEqual(str(self.handler.rayDodgeStatus), "restored")

    def test_ray_missing_ambiguous_mind_and_cooldown_do_not_retry_same_event(self):
        for count in (0, 2):
            self.handler.Reset()
            self.items.counts["mind stone"] = count
            self.equipment.Prepare(self.settings, self.profile)
            self.frame("dysangelos phase3", foe_state=115, foe_time=23, total=50)
            self.assertEqual(str(self.handler.rayDodgeStatus), "unavailable")
            self.assertEqual(self.gear.calls, ["fire sword"])
            self.items.counts["mind stone"] = 1
            self.equipment.Prepare(self.settings, self.profile)
            self.frame("dysangelos phase3", foe_state=115, foe_time=24, total=51)
            self.assertEqual(self.handler.rayDodgeAttempts, 0)
        self.handler.Reset()
        self.items.cooldowns["mind"] = 20
        self.frame("dysangelos phase3", foe_state=115, foe_time=23, total=100)
        self.items.cooldowns["mind"] = 0
        self.frame("dysangelos phase3", foe_state=115, foe_time=44, total=121)
        self.assertEqual(self.handler.rayDodgeAttempts, 0)
        self.assertEqual(str(self.handler.rayDodgeStatus), "unavailable")

    def test_ray_unknown_unused_cooldown_is_explicit_single_experiment(self):
        self.items.cooldowns["mind"] = -1
        self.frame("dysangelos phase3", foe_state=115, foe_time=23, total=1)
        self.assertEqual(self.gear.calls, ["mind stone"])
        self.assertIn("unused/unknown", str(self.handler.rayDodgeReason))
        self.assertEqual(self.items.activations, [])  # Equip-only; no invented activation.

    def test_ray_armed_timeout_and_hold_deadline_never_lock_forever(self):
        self.profile.rayDodgeTriggerFrame = 100
        self.profile.rayDodgeHoldFrames = 3
        self.profile.rayDodgeTimeoutFrames = 10
        self.frame("dysangelos phase3", foe_state=115, foe_time=0, total=100)
        self.frame("dysangelos phase3", foe_state=115, foe_time=0, total=110)
        self.assertEqual(str(self.handler.rayDodgeStatus), "unavailable")
        self.assertIn("timeout", str(self.handler.rayDodgeReason))
        self.assertEqual(self.gear.calls, ["fire sword"])
        self.handler.Reset()
        self.profile.rayDodgeTriggerFrame = 23
        self.frame("dysangelos phase3", foe_state=115, foe_time=23, total=200)
        self.frame("dysangelos phase3", foe_state=115, foe_time=23, total=400)
        self.assertFalse(self.handler.rayDodgeHolding)
        self.assertEqual(str(self.handler.rayDodgeStatus), "restored")
        self.assertEqual(self.gear.calls, ["fire sword"])
        self.assertEqual(self.handler.rayDodgeAttempts, 1)

    def test_ray_phase_change_disabled_and_reset_cancel_hold(self):
        self.frame("dysangelos phase3", foe_state=115, foe_time=23, total=100)
        self.frame("dysangelos phase2 poison", foe_state=115, foe_time=24, total=101)
        self.assertFalse(self.handler.rayDodgeHolding)
        self.assertEqual(self.gear.calls, ["ice sword"])
        self.assertEqual(str(self.handler.rayDodgeStatus), "restored")
        self.frame("dysangelos phase3", foe_state=115, foe_time=23, total=200)
        self.handler.Reset()
        self.assertEqual(self.handler.rayDodgeAttempts, 0)
        self.assertFalse(self.handler.rayDodgeHolding)
        self.profile.rayDodgeEnabled = False
        self.frame("dysangelos phase3", foe_state=115, foe_time=23, total=300)
        self.assertEqual(self.gear.calls, ["fire sword"])

    def test_ray_target_gap_retains_exclusive_hold_then_restores_previous_combat(self):
        self.frame("dysangelos phase3", foe_state=32, total=1)
        self.frame("dysangelos phase3", foe_state=115, foe_time=23, total=2)
        self.assertTrue(self.frame(total=3))
        self.assertEqual(self.gear.calls, ["mind stone"])
        self.assertTrue(self.combat.travelBossSeen)
        self.assertTrue(self.frame(total=32))
        self.assertEqual(self.gear.calls, ["fire sword"])
        self.assertEqual(str(self.handler.rayDodgeStatus), "restored")

    def test_ray_exit_before_trigger_disarms_and_same_state_timer_reset_does_not_retry(self):
        self.frame("dysangelos phase3", foe_state=115, foe_time=10, total=10)
        self.frame("dysangelos phase3", foe_state=32, total=11)
        self.assertEqual(str(self.handler.rayDodgeStatus), "idle")
        self.frame("dysangelos phase3", foe_state=115, foe_time=23, total=12)
        self.frame("dysangelos phase3", foe_state=115, foe_time=0, total=42)
        self.frame("dysangelos phase3", foe_state=115, foe_time=23, total=65)
        self.assertEqual(self.handler.rayDodgeAttempts, 1)
        self.assertEqual(self.gear.calls, ["fire sword"])

    def test_ray_ai_ability_shield_guards_and_invalid_timing(self):
        self.items.abilities_enabled = False
        self.frame("dysangelos phase3", foe_state=115, foe_time=23)
        self.assertEqual(str(self.handler.rayDodgeStatus), "unavailable")
        self.assertEqual(self.gear.calls, ["fire sword"])
        self.items.abilities_enabled = True
        self.handler.Reset()
        self.frame("dysangelos phase3", foe_state=115, foe_time=23, total=1)
        self.native["ai"].paused = True
        self.frame("dysangelos phase3", foe_state=115, foe_time=24, total=2)
        self.assertFalse(self.handler.rayDodgeHolding)
        self.assertEqual(self.gear.calls, [])
        self.native["ai"].paused = False
        for trigger, hold, timeout in [(-1, 30, 90), (23, 0, 90), (23, 30, 5)]:
            self.handler.Reset()
            self.profile.rayDodgeTriggerFrame = trigger
            self.profile.rayDodgeHoldFrames = hold
            self.profile.rayDodgeTimeoutFrames = timeout
            self.frame("dysangelos phase3", foe_state=115, foe_time=23)
            self.assertEqual(str(self.handler.rayDodgeStatus), "unavailable")
            self.assertEqual(self.gear.calls, ["fire sword"])

    def test_ray_never_runs_outside_perfected_or_queries_inventory_per_frame(self):
        queries = len(self.items.queries)
        for target in ("acronian_scout", "dysangelos phase1", "dysangelos phase2 fire"):
            self.frame(target, foe_state=115, foe_time=23)
            self.assertNotIn("mind stone", self.gear.calls)
        self.frame("dysangelos phase3", foe_state=115, foe_time=23)
        self.assertEqual(len(self.items.queries), queries)
        self.assertEqual(self.gear.calls, ["mind stone"])
        self.assertEqual(self.gear.lastShield, "FastGenShl")
        self.assertEqual(self.handler.lastWeapon, "aether sword")  # Mind never becomes cached combat weapon.


    def test_ray_shield_loss_and_dead_target_cancel_protected_hold(self):
        self.frame("dysangelos phase3", foe_state=32, total=1)
        self.frame("dysangelos phase3", foe_state=115, foe_time=23, total=2)
        self.equipment.shield = Text("")
        self.frame("dysangelos phase3", foe_state=115, foe_time=24, total=3)
        self.assertFalse(self.handler.rayDodgeHolding)
        self.assertEqual(self.gear.calls, [])
        self.equipment.shield = Text("FastGenShl")
        self.handler.Reset()
        self.frame("dysangelos phase3", foe_state=32, total=10)
        self.frame("dysangelos phase3", foe_state=115, foe_time=23, total=11)
        self.frame("dysangelos phase3", hp=0, foe_state=115, foe_time=24, total=12)
        self.assertFalse(self.handler.rayDodgeHolding)
        self.assertEqual(self.gear.calls, ["fire sword"])
        self.assertEqual(str(self.handler.rayDodgeStatus), "restored")

    def test_ray_observed_exit_during_hold_allows_a_subsequent_ray(self):
        self.profile.rayDodgeHoldFrames = 3
        self.frame("dysangelos phase3", foe_state=115, foe_time=23, total=10)
        self.frame("dysangelos phase3", foe_state=114, total=11)
        self.assertEqual(self.gear.calls, ["mind stone"])
        self.frame("dysangelos phase3", foe_state=115, foe_time=1, total=12)
        self.frame("dysangelos phase3", foe_state=115, foe_time=2, total=13)
        self.assertEqual(self.gear.calls, ["fire sword"])
        self.frame("dysangelos phase3", foe_state=115, foe_time=23, total=14)
        self.assertEqual(self.handler.rayDodgeAttempts, 2)


class SourceAndBundleTests(unittest.TestCase):
    def test_static_contracts_and_no_live_paths(self):
        data = PACKAGE.inspect(ROOT)
        self.assertEqual(len(data), 11)
        self.assertNotIn(b"steamapps", (ROOT / "tools/prepare_rocky_candidate.py").read_bytes())

    def test_bundle_determinism_and_conflicting_output_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(ROOT / "scripts", root / "scripts")
            first = PACKAGE.prepare(root)
            files = {str(p.relative_to(first)): (p.read_bytes(), p.stat().st_mtime_ns)
                     for p in first.rglob("*") if p.is_file()}
            self.assertEqual(first, PACKAGE.prepare(root))
            self.assertEqual(files, {str(p.relative_to(first)): (p.read_bytes(), p.stat().st_mtime_ns)
                                     for p in first.rglob("*") if p.is_file()})
            self.assertEqual(len(files), 6)  # Five candidate modules + manifest; shared dependencies untouched.
            (first / "SpeedRunRocky/main.txt").write_text("tampered")
            with self.assertRaises(ValueError): PACKAGE.prepare(root)

    def test_guard_regressions_are_rejected(self):
        for relative, before, after in [
            ("locations/RockyPlateau.txt", 'rayDodgeSpent = true', 'rayDodgeSpent = false'),
            ("locations/RockyPlateau.txt", '?TryPerfectedRay(gear, equipment, rockyConfig)\n    attacks.ResetCycle()\n    return true',
             'TryPerfectedRay(gear, equipment, rockyConfig)'),
            ("locations/RockyPlateau.txt", '?bossLatched\n    combat.travelBossSeen = true',
             '?true\n    combat.travelBossSeen = true'),
            ("config/RockySettings.txt", 'var bearerRecoveryEnabled = true', 'var missingRecoveryConfig = true'),
            ("main.txt", 'new SpeedRunBasic/config/Settings', 'new Missing/config/Settings'),
            ("main.txt", "?!rockyHandled", "?true"),
            ("locations/RockyPlateau.txt", 'phase = "transition-gap"', 'phase = "gap"'),
            ("locations/RockyPlateau.txt", 'physicalOnly = unknownAdaptive | (phase = "unknown")',
             'physicalOnly = false'),
            ("config/RockySettings.txt", 'var targetStars = 15', 'var targetStars = 14'),
            ("equipment/RockyGear.txt", 'item.GetCount(selector) = 1', 'item.GetCount(selector) > 0'),
            ("config/RockySettings.txt", 'var preferredShield = "FastGenShl"', 'var preferredShield = "compound shield +21"'),
            ("locations/RockyPlateau.txt", 'gear.ApplyPair(weapon, equipment.shield)', 'gear.Apply(weapon)'),
        ]:
            with self.subTest(file=relative):
                with tempfile.TemporaryDirectory() as temp:
                    root = Path(temp)
                    shutil.copytree(ROOT / "scripts", root / "scripts")
                    path = root / "scripts/rocky" / relative
                    path.write_text(path.read_text().replace(before, after))
                    with self.assertRaises(ValueError): PACKAGE.inspect(root)


if __name__ == "__main__": unittest.main()
