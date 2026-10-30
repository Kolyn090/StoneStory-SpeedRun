"""Rocky optimization policy/command tests. No native game execution claimed."""
import hashlib
from pathlib import Path
from types import SimpleNamespace
import unittest
import test_rocky_candidate as baseline
from stonescript_policy_harness import Foe, Text, load_module

ROOT = Path(__file__).resolve().parents[1]


class OptimizationTests(unittest.TestCase):
    frame = baseline.PolicyTests.frame

    def setUp(self):
        baseline.PolicyTests.setUp(self)
        self.profile.dualWieldEnabled = True
        self.gear.triskelion = Text("triskelion")
        self.gear.starStone = Text("star stone")
        self.settings.triskelionTravelEnabled = True
        self.settings.passiveStarEnabled = True
        self.native["ai"].walking = True

    def assertPair(self, left, right):
        self.assertEqual(self.gear.calls, [left])
        self.assertEqual(self.gear.lastShield, right)

    def test_scout_bearer_and_counter_element_pairs(self):
        for foe, weapon in [("acronian_scout", "fire sword"), ("dysangelos phase1", "fire sword"),
                            ("dysangelos phase2 fire", "aether sword"),
                            ("dysangelos phase2 poison", "ice sword"), ("dysangelos phase3", "ice sword")]:
            self.frame(foe)
            self.assertPair(weapon, "stone sword -big +21")

    def test_perfected_resistance_and_armor_choose_distinct_allowed_weapons(self):
        self.frame("dysangelos phase3", buffs="adaptive_defense_fire:1:99")
        self.assertPair("ice sword", "stone sword -big +21")
        self.frame("dysangelos phase3", armor=10, buffs="adaptive_defense_fire:1:99")
        self.assertPair("ice hammer", "vigor hammer")
        self.assertEqual(self.items.equips, [])
        self.assertFalse(self.equipment.SameWeapon(self.gear.calls[0], self.gear.lastShield))

    def test_recovery_on_all_combat_phases_hysteresis_and_offensive_hand_preserved(self):
        for target in ["acronian_scout", "dysangelos phase1", "dysangelos phase2 ice", "dysangelos phase3"]:
            self.handler.Reset()
            for hp, active in [(100, False), (60, True), (70, True), (84, True), (85, False), (70, False)]:
                self.frame(target, player_hp=hp)
                self.assertEqual(self.handler.bearerRecoveryActive, active)
                self.assertEqual(self.gear.calls, ["fire sword"])
                self.assertEqual(self.gear.lastShield, "vigor sword dL -big +21" if active else "stone sword -big +21")

    def test_vigor_alias_never_requests_same_item_twice(self):
        self.frame("dysangelos phase2 aether", player_hp=30)
        self.assertPair("vigor sword dL -big +21", "stone sword -big +21")
        self.assertFalse(self.equipment.SameWeapon(self.gear.calls[0], self.gear.lastShield))
        self.assertTrue(self.equipment.SameWeapon("vigor sword", "vigor sword dL -big +21"))

    def test_armor_immunity_and_blocked_vigor_outrank_healing(self):
        self.frame("dysangelos phase1", armor=10, player_hp=10)
        self.assertPair("fire hammer", "vigor hammer")
        self.assertFalse(self.handler.bearerRecoveryActive)
        self.frame("dysangelos phase3", buffs="adaptive_defense_vigor:1:99", player_hp=10)
        self.assertNotEqual(self.gear.lastShield, "vigor sword dL -big +21")
        self.frame("dysangelos phase3 immune_to_physical", player_hp=10)
        self.assertIn("wand", self.gear.calls[0]); self.assertIn("wand", self.gear.lastShield)
        self.assertEqual(self.items.equips, [])

    def test_missing_second_weapon_and_unknown_adaptive_keep_shield(self):
        self.items.counts["stone sword -big +21"] = 0
        for key in list(self.items.counts):
            if "sword" in key and key != "fire sword": self.items.counts[key] = 0
        self.equipment.Prepare(self.settings, self.profile)
        self.frame("dysangelos phase1")
        self.assertPair("fire sword", "FastGenShl")
        self.items.counts["stone sword -big +21"] = 1
        self.equipment.Prepare(self.settings, self.profile)
        self.frame("dysangelos phase3", buffs="adaptive_new:1:9")
        self.assertPair("stone sword -big +21", "FastGenShl")

    def test_missing_lifesteal_and_disabled_dual_retain_safe_fallback(self):
        self.items.counts["vigor sword dL -big +21"] = 0
        self.equipment.Prepare(self.settings, self.profile)
        self.frame("dysangelos phase1", player_hp=10)
        self.assertPair("fire sword", "stone sword -big +21")
        self.profile.dualWieldEnabled = False
        self.frame("dysangelos phase1")
        self.assertPair("fire sword", "FastGenShl")

    def test_ray_preempts_aac_and_transformations_hold_logical_pair(self):
        self.frame("dysangelos phase3", foe_state=32, hp=100, total=1)
        self.items.left.state = self.items.right.state = 3
        self.frame("dysangelos phase3", foe_state=115, foe_time=23, hp=90, total=2)
        self.assertPair("mind stone", "FastGenShl")
        self.assertEqual(self.items.equips, [])
        self.frame(total=3)
        self.assertPair("mind stone", "FastGenShl")
        self.frame(total=32)
        self.assertPair("fire sword", "stone sword -big +21")
        self.assertTrue(self.combat.travelBossSeen)
        self.frame("dysangelos phase3", armor=10, buffs="adaptive_defense_fire:1:9", total=33)
        self.assertPair("ice hammer", "vigor hammer")

    def test_unknown_enemy_keeps_shared_fallback_and_other_difficulty_is_untouched(self):
        self.assertFalse(self.frame("insect")); self.assertEqual(self.gear.calls, [])
        self.native["loc"].stars = 14
        self.assertFalse(self.frame("acronian_scout")); self.assertEqual(self.gear.calls, [])

    def test_clear_travel_stable_star_no_pickup_window_and_safe_triskelion_guards(self):
        self.native.update(pickup=SimpleNamespace(distance=1), boss=Text("boss"))
        self.combat = load_module(ROOT / "scripts/basic/combat/Generic.txt", self.native)
        self.frame("acronian_scout")
        self.assertTrue(self.frame(total=1))
        self.assertPair("triskelion", "star stone")
        self.assertFalse(self.combat.starWindowUsed)
        self.assertEqual(self.combat.starUntil, 0)
        self.frame(total=2, player_hp=99)
        self.assertNotEqual(self.gear.calls[0], "triskelion")
        self.native["ai"].walking = False
        self.frame(total=3)
        self.assertNotEqual(self.gear.calls[0], "triskelion")
        self.native["ai"].walking = True
        self.native["ai"].paused = True
        self.frame(total=4)
        self.assertEqual(self.gear.calls, [])
        self.native["ai"].paused = False
        self.frame("dysangelos phase1", total=5)
        self.frame(total=6)
        self.assertNotIn("triskelion", self.gear.calls)

    def aacFrame(self, total, hp, left=2, right=2):
        self.items.left.state = left
        self.items.right.state = right
        self.frame("dysangelos phase1", hp=hp, total=total)

    def test_aac_left_and_right_edges_with_same_frame_restoration(self):
        self.aacFrame(1, 100)
        self.aacFrame(2, 90, left=3)
        self.assertEqual([x[0] for x in self.items.equips], ["L"])
        self.assertPair("fire sword", "stone sword -big +21")
        self.aacFrame(3, 80, left=3)
        self.assertEqual(len(self.items.equips), 1)  # Stale recovery cannot repeat.
        self.aacFrame(4, 80)
        self.aacFrame(5, 70, right=3)
        self.assertEqual([x[0] for x in self.items.equips], ["L", "R"])
        self.assertEqual(self.attacks.cancelsL, 1)
        self.assertEqual(self.attacks.cancelsR, 1)
        self.assertEqual(self.items.activations, [])

    def test_aac_both_hands_distinct_dummies_and_no_premature_windup_cancel(self):
        self.aacFrame(1, 100)
        self.aacFrame(2, 90, left=1, right=2)
        self.assertEqual(self.items.equips, [])
        self.aacFrame(3, 80, left=3, right=3)
        self.assertEqual([x[0] for x in self.items.equips], ["L", "R"])
        self.assertNotEqual(self.items.equips[0][1], self.items.equips[1][1])
        self.assertNotIn("fire sword", [x[1] for x in self.items.equips])
        self.assertNotIn("stone sword -big +21", [x[1] for x in self.items.equips])
        self.assertPair("fire sword", "stone sword -big +21")

    def test_aac_requires_damage_corroboration_stable_pair_and_current_identity(self):
        self.aacFrame(1, 100)
        self.aacFrame(2, 100, left=3, right=3)
        self.assertEqual(self.items.equips, [])
        self.aacFrame(3, 100)
        self.items.left.id = Text("unknown_staff")
        self.aacFrame(4, 90, left=3)
        self.assertEqual(self.items.equips, [])
        self.items.left.id = Text("socketed_sword")
        self.aacFrame(5, 90)
        self.frame("dysangelos phase2 poison", hp=80, total=6)
        self.assertEqual(self.items.equips, [])  # New target/loadout cannot cancel from old state.

    def test_aac_missing_dummies_disable_and_no_inventory_scans_per_frame(self):
        queries = len(self.items.queries)
        self.profile.aacEnabled = False
        self.aacFrame(1, 100)
        self.aacFrame(2, 90, left=3, right=3)
        self.assertEqual(self.items.equips, [])
        self.profile.aacEnabled = True
        self.aacFrame(3, 90)
        self.equipment.swords = [Text(""), Text(""), Text(""), Text("fire sword"), Text("")]
        self.aacFrame(4, 80, left=3, right=3)
        self.assertEqual(self.items.equips, [])
        self.assertEqual(len(self.items.queries), queries)

    def configureRecoveryCopies(self, count, verified=False, nameA="", nameB="", overlap=0):
        base = str(self.profile.bearerRecoverySword)
        self.items.counts[base] = count
        self.items.counts["vigor sword"] = count
        self.profile.dualVigorVerified = verified
        self.profile.vigorRecoveryNameA = Text(nameA)
        self.profile.vigorRecoveryNameB = Text(nameB)
        if nameA:
            self.items.counts[base + " " + nameA] = 1
        if nameB:
            self.items.counts[base + " " + nameB] = 1
        if nameA or nameB:
            a = base + (" " + nameA if nameA else "")
            b = base + (" " + nameB if nameB else "")
            self.items.counts[a + " " + b] = overlap
        self.equipment.Prepare(self.settings, self.profile)
        return base

    def test_duplicate_count_without_native_independence_proof_uses_one_healer(self):
        base = self.configureRecoveryCopies(2)
        self.frame("dysangelos phase1", player_hp=30)
        self.assertPair("fire sword", base)
        self.assertFalse(self.equipment.distinctRecoveryPair)
        self.assertEqual(self.equipment.recoveryCount, 2)
        self.assertTrue(self.equipment.SameWeapon(base, base))

    def test_owner_verified_identical_names_can_use_two_separate_copies(self):
        base = self.configureRecoveryCopies(2, verified=True)
        for hp, dual in [(100, False), (60, True), (70, True), (84, True), (85, False), (70, False)]:
            self.frame("dysangelos phase1", player_hp=hp)
            self.assertEqual(self.handler.bearerRecoveryActive, dual)
            self.assertPair(base if dual else "fire sword", base if dual else "stone sword -big +21")
        self.assertTrue(self.equipment.distinctRecoveryPair)
        self.assertFalse(self.equipment.SameWeapon(base, base))  # Only this explicitly confirmed two-copy role.
        self.assertTrue(self.equipment.SameWeapon("vigor sword", base))  # Generic alias still conflicts.

    def test_unique_disjoint_named_copies_and_overlapping_sets(self):
        base = self.configureRecoveryCopies(2, verified=True, nameA="HealA", nameB="HealB", overlap=0)
        self.frame("dysangelos phase1", player_hp=30)
        self.assertPair(base + " HealA", base + " HealB")
        self.assertFalse(self.equipment.SameWeapon(base + " HealA", base + " HealB"))
        self.configureRecoveryCopies(2, verified=True, nameA="HealA", nameB="HealB", overlap=1)
        self.frame("dysangelos phase1", player_hp=30)
        self.assertPair("fire sword", base + " HealA")
        self.assertFalse(self.equipment.distinctRecoveryPair)
        self.assertIn("overlapping", str(self.equipment.recoveryPairStatus))
        self.assertTrue(self.equipment.SameWeapon(base + " HealA", base + " HealB"))

    def test_alias_subset_is_not_a_distinct_second_item_even_when_counts_are_one(self):
        base = self.configureRecoveryCopies(1, verified=True, nameA="", nameB="Alias", overlap=1)
        self.frame("dysangelos phase1", player_hp=30)
        self.assertPair("fire sword", base)
        self.assertFalse(self.equipment.distinctRecoveryPair)

    def test_crafting_or_renaming_reprepares_native_counts_without_fixed_positions(self):
        base = self.configureRecoveryCopies(1, verified=True)
        self.frame("dysangelos phase1", player_hp=30)
        self.assertPair("fire sword", base)
        self.configureRecoveryCopies(2, verified=True)
        self.frame("dysangelos phase1", player_hp=30)
        self.assertPair(base, base)
        self.items.counts[base] = 1
        self.equipment.Prepare(self.settings, self.profile)
        self.frame("dysangelos phase1", player_hp=30)
        self.assertPair("fire sword", base)
        self.configureRecoveryCopies(2, verified=True, nameA="HealA", nameB="HealB")
        self.items.counts[base + " HealB"] = 0
        self.equipment.Prepare(self.settings, self.profile)
        self.frame("dysangelos phase1", player_hp=30)
        self.assertPair("fire sword", base + " HealA")
        self.assertFalse(self.equipment.distinctRecoveryPair)

    def test_two_healers_still_yield_to_armor_resistance_and_ray(self):
        base = self.configureRecoveryCopies(2, verified=True)
        self.frame("dysangelos phase1", player_hp=30, armor=10)
        self.assertPair("fire hammer", "vigor hammer")
        self.frame("dysangelos phase3", player_hp=30, buffs="adaptive_defense_vigor:1:99")
        self.assertNotEqual(self.gear.lastShield, base)
        self.frame("dysangelos phase3", player_hp=30, foe_state=115, foe_time=23, total=10)
        self.assertPair("mind stone", "FastGenShl")
        self.assertEqual(self.items.equips, [])

    def test_frozen_ray_body_and_timing_are_preserved(self):
        body = (ROOT / "scripts/rocky/locations/RockyPlateau.txt").read_text().split("func TryPerfectedRay(", 1)[1].split("func Reset()", 1)[0]
        self.assertEqual(hashlib.sha256(body.encode()).hexdigest(), "cb7e55007f0396db68a72a5958fdf1e122388d0afc2fe69b545539ff0575ac20")
        self.assertEqual((self.profile.rayDodgeTriggerFrame, self.profile.rayDodgeHoldFrames, self.profile.rayDodgeTimeoutFrames), (23, 30, 90))


if __name__ == "__main__": unittest.main()
