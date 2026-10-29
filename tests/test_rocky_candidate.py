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


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.strings = Strings()
        self.settings = SimpleNamespace(swords=Array(Text(x + " sword") for x in ("poison","vigor","aether","fire","ice")),
            wands=Array(Text(x + " wand") for x in ("poison","vigor","aether","fire","ice")),
            hammers=Array(Text(x + " hammer") for x in ("poison","vigor","aether","fire","ice")),
            healingSword=Text("vigor sword dL"), usePotion=False, potionHpRatio=.25, healingHpRatio=.4)
        counts = {str(x): 1 for family in (self.settings.swords, self.settings.wands, self.settings.hammers)
                  for x in family}
        counts.update({"stone sword -big -socket": 1, "vigor sword dL": 1})
        self.items = Items(counts)
        self.native = dict(string=self.strings, item=self.items, foe=Foe(), hp=100, maxhp=100,
                           ai=SimpleNamespace(enabled=True, paused=False))
        self.profile = load_module(ROOT / "scripts/rocky/config/RockySettings.txt", self.native)
        self.equipment = load_module(ROOT / "scripts/rocky/equipment/RockyGear.txt", self.native)
        self.equipment.Prepare(self.settings, self.profile)
        self.handler = load_module(ROOT / "scripts/rocky/locations/RockyPlateau.txt", self.native)
        self.gear = Gear()
        self.combat = SimpleNamespace(travelBossSeen=False, starUntil=100)

    def frame(self, value="", buffs="", armor=0, hp=100, player_hp=100):
        state = Foe(value, buffs, armor, hp)
        # Compiled functions use their own global namespace, sharing fake native inputs.
        for obj in (self.handler, self.equipment):
            for name in dir(type(obj)):
                method = getattr(type(obj), name)
                if hasattr(method, "__globals__"):
                    method.__globals__.update(foe=state, hp=player_hp)
        self.gear.calls.clear()
        return self.handler.Tick(self.gear, self.settings, self.equipment, self.profile, self.combat)

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
        self.assertEqual(self.gear.calls, ["stone sword -big -socket"])

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
        self.assertEqual(self.gear.calls, ["stone sword -big -socket"])
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
        self.equipment.Prepare(self.settings, self.profile)
        self.frame("dysangelos phase3")
        self.assertEqual(str(self.handler.strategy), "no-safe-selector-manual")
        self.assertIn("STOP", str(self.handler.warning))

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


class SourceAndBundleTests(unittest.TestCase):
    def test_static_contracts_and_no_live_paths(self):
        data = PACKAGE.inspect(ROOT)
        self.assertEqual(len(data), 10)
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
            self.assertEqual(len(files), 5)  # Four candidate modules + manifest; dependencies not overwritten.
            (first / "SpeedRunRocky/main.txt").write_text("tampered")
            with self.assertRaises(ValueError): PACKAGE.prepare(root)

    def test_guard_regressions_are_rejected(self):
        for relative, before, after in [
            ("main.txt", "?!rockyHandled", "?true"),
            ("locations/RockyPlateau.txt", 'phase = "transition-gap"', 'phase = "gap"'),
            ("locations/RockyPlateau.txt", 'physicalOnly = unknownAdaptive | (phase = "unknown")',
             'physicalOnly = false'),
        ]:
            with self.subTest(file=relative):
                with tempfile.TemporaryDirectory() as temp:
                    root = Path(temp)
                    shutil.copytree(ROOT / "scripts", root / "scripts")
                    path = root / "scripts/rocky" / relative
                    path.write_text(path.read_text().replace(before, after))
                    with self.assertRaises(ValueError): PACKAGE.inspect(root)


if __name__ == "__main__": unittest.main()
