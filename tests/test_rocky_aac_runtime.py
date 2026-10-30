"""AAC assignment and config regressions; native parser check is a separate PS tool."""
from pathlib import Path
import shutil
import tempfile
import unittest
import test_rocky_candidate as baseline

ROOT = Path(__file__).resolve().parents[1]

class RuntimeGateTests(unittest.TestCase):
    frame = baseline.PolicyTests.frame

    def setUp(self):
        baseline.PolicyTests.setUp(self)
        self.profile.dualWieldEnabled = True

    def test_aac_flag_does_not_disable_dual_combat(self):
        original = self.equipment.CancelDummy
        calls = []
        def counted(*args):
            calls.append(args)
            return original(*args)
        self.equipment.CancelDummy = counted
        self.frame("acronian_scout")
        self.assertEqual(len(calls), 2)
        self.assertEqual(self.gear.calls, ["fire sword"])
        self.profile.aacEnabled = False
        calls.clear()
        self.frame("acronian_scout")
        self.assertEqual(calls, [])
        self.assertEqual(self.gear.calls, ["fire sword"])
        self.assertEqual(self.gear.lastShield, "stone sword -big +21")

    def test_uninitialized_config_is_not_silently_converted_to_aac_false(self):
        with self.assertRaises(AttributeError):
            self.handler.Tick(self.gear, self.settings, self.equipment, None,
                              self.combat, self.attacks)
        self.assertEqual(self.gear.calls, [])

    def test_missing_aac_config_field_is_a_configuration_error(self):
        del self.profile.aacEnabled
        with self.assertRaisesRegex(AttributeError, "aacEnabled"):
            self.frame("acronian_scout")
        self.assertEqual(self.gear.calls, [])

    def test_missing_offhand_selects_shield_without_aac(self):
        for name in list(self.items.counts):
            if "sword" in name and name != "fire sword": self.items.counts[name] = 0
        self.equipment.Prepare(self.settings, self.profile)
        self.equipment.CancelDummy = lambda *args: self.fail("shield cannot enter AAC")
        self.frame("acronian_scout")
        self.assertEqual(self.gear.calls, ["fire sword"])
        self.assertEqual(self.gear.lastShield, "FastGenShl")

    def test_packager_rejects_original_native_assignment_trap(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            shutil.copytree(ROOT / "scripts", root / "scripts")
            path = root / "scripts/rocky/locations/RockyPlateau.txt"
            text = path.read_text()
            fixed = 'allowAAC = (rockyConfig.aacEnabled & (equipment.pickedKind = "sword") & (equipment.offhandKind = "sword") & !physicalOnly)'
            old = 'allowAAC = rockyConfig.aacEnabled & equipment.pickedKind = "sword" & equipment.offhandKind = "sword" & !physicalOnly'
            self.assertIn(fixed, text)
            path.write_text(text.replace(fixed, old))
            with self.assertRaisesRegex(ValueError, "AAC assignment must group"):
                baseline.PACKAGE.inspect(root)

    def test_quiet_default_keeps_native_errors_measurement_and_initialization(self):
        self.assertFalse(self.profile.showDiagnostics)
        main = (ROOT / "scripts/rocky/main.txt").read_text()
        self.assertIn('?config.showDiagnostics & rockyConfig.showDiagnostics', main)
        self.assertEqual(main.count('metrics.Observe()'), 1)
        self.assertNotIn('disable diagnostics', main)
        self.assertLess(main.index('var rockyConfig = new '), main.index('equipment.Prepare('))
        self.assertLess(main.index('var equipment = new '), main.index('rocky.Tick('))
        self.assertIn('var showDiagnostics = true', (ROOT / "scripts/basic/config/Settings.txt").read_text())
