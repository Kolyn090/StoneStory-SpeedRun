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
                relative, appended = mutation
                target = fixture / "scripts/basic" / relative
                with target.open("a", encoding="utf-8") as handle:
                    handle.write(appended)
            return subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                "-File", str(ROOT / "tools/Test-BasicStatic.ps1"), "-ProjectRoot", str(fixture)],
                capture_output=True, text=True)

    def test_current_source_passes(self):
        result = self.run_checker()
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


if __name__ == "__main__":
    unittest.main()
