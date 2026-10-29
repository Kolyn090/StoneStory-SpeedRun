"""Exercise static policy guards on synthetic source copies, never live deployment."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(sys.platform == "win32", "Static checker requires PowerShell")
class NoResourcePolicyTests(unittest.TestCase):
    def run_checker(self, mutation=None):
        with tempfile.TemporaryDirectory() as temp:
            fixture = Path(temp)
            shutil.copytree(ROOT / "scripts/basic", fixture / "scripts/basic")
            shutil.copytree(ROOT / "scripts/metrics", fixture / "scripts/metrics")
            if mutation:
                relative, *changes = mutation
                target = fixture / "scripts/basic" / relative
                if len(changes) == 1:
                    with target.open("a", encoding="utf-8") as handle:
                        handle.write(changes[0])
                else:
                    original = target.read_text(encoding="utf-8")
                    self.assertIn(changes[0], original)
                    target.write_text(original.replace(*changes), encoding="utf-8")
            return subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                "-File", str(ROOT / "tools/Test-BasicStatic.ps1"), "-ProjectRoot", str(fixture)],
                capture_output=True, text=True)

    def test_current_source_passes(self):
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_benchmark_off_configuration_passes(self):
        result = self.run_checker(("config/Settings.txt", "var passiveStarEnabled = true",
                                   "var passiveStarEnabled = false"))
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_collection_queries_settings_and_helper_are_rejected(self):
        for mutation in [
            ("combat/Generic.txt", "\n?harvest\n  equip shovel\n"),
            ("config/Settings.txt", "\nvar harvestEnabled = true\n"),
            ("equipment/Catalog.txt", '\nvar shovel = "shovel"\n'),
            ("equipment/Catalog.txt", "\nfunc Harvest()\n  return\n"),
        ]:
            with self.subTest(file=mutation[0], code=mutation[1]):
                result = self.run_checker(mutation)
                self.assertNotEqual(result.returncode, 0)
                self.assertTrue("Optional resource harvesting" in result.stderr or
                                "reserved name" in result.stderr, result.stderr)

    def test_passive_star_safety_contract_mutations_are_rejected(self):
        for before, after in [
            ("foe.count > 0", "foe.count < 0"),
            ("starWindowUsed = true", "starWindowUsed = false"),
            ("starUntil = totaltime + settings.passiveStarHoldFrames", "starUntil = 999999"),
            ("?TryPassiveStar(gear, settings)", "?true"),
            ("!ai.walking", "ai.walking"),
            ("starBossSeen = true", "starBossSeen = false"),
        ]:
            with self.subTest(contract=before):
                result = self.run_checker(("combat/Generic.txt", before, after))
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Passive Star", result.stderr)

    def test_passive_star_unconditional_lookup_and_invented_api_are_rejected(self):
        for mutation in [
            ("equipment/Catalog.txt", "?settings.passiveStarEnabled", "?true"),
            ("combat/Generic.txt", "\n?pickup.id = unknown\n  activate star\n"),
        ]:
            with self.subTest(mutation=mutation):
                result = self.run_checker(mutation)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Passive Star", result.stderr)


if __name__ == "__main__":
    unittest.main()
