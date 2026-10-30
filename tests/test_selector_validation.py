"""Synthetic only: these checks do not run the game's Stonescript interpreter."""
import copy
import importlib.util
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build_selector_candidates as probes
from import_player_inventory import canonical, normalize, ValidationError


def inventory():
    sword = {"id": "socketed_sword", "da": {"hI": True, "rng": 1,
        "el": "Fire", "lv": 8192, "ra": {"lv": 21, "ql": 12, "sSS": 17},
        "sra": {"lv": 21, "ql": 7, "sSS": 8}, "abs": ["PRIVATE-CODE"],
        "tag": "PRIVATE-NAME", "sh": True}}
    other = copy.deepcopy(sword)
    other["da"]["abs"] = ["OTHER-CODE"]
    return normalize(canonical({"version": "4.35.2", "inventory_data": {
        "rightH": "PRIVATE-HAND", "itmsSeen": ["NOT-OWNED"], "itms": [sword, other,
        {"id": "treasure_1", "da": {"hI": True, "rng": 2, "itms": [
            {"id": "socketed_sword", "t": 5}]}},
        {"id": "Stone", "co": 999, "da": {"hI": True, "rng": 2}},
        {"id": "wand_hidden_fire", "da": {"hI": True, "rng": 2}}]}}))[0]


class CandidateTests(unittest.TestCase):
    def test_provenance_grouping_and_ambiguity(self):
        result, summary = probes.analyze(inventory())
        self.assertEqual(summary["inventory_records_analyzed"], 5)
        broad = next(p for p in result["candidates"] if p["selector"] == "fire sword -big")
        self.assertTrue(broad["ambiguous_saved_variants"])
        self.assertEqual(len(broad["profile_groups"]), 2)
        self.assertEqual(len(broad["source_pointers"]), 2)
        self.assertIsNone(broad["in_game_count"])
        self.assertEqual(summary["deferred_or_non_equipment_records"]["equipment_alias_deferred"], 1)

    def test_no_guessed_stars_or_private_text_in_stonescript(self):
        result, summary = probes.analyze(inventory())
        code = probes.stonescript(result["candidates"])
        for secret in (b"PRIVATE", b"OTHER-CODE", b"NOT-OWNED", b"8192"):
            # Header uses PRIVATE as a privacy label, not the fixture values.
            if secret != b"PRIVATE":
                self.assertNotIn(secret, code)
        self.assertNotIn(b"PRIVATE-NAME", code)
        self.assertNotIn(b"PRIVATE-CODE", code)
        self.assertNotIn(b"*", code)
        self.assertIn(b"+21", code)
        self.assertNotIn("PRIVATE", canonical(summary).decode())

    def test_deterministic_nonmutating_and_raw_profiles(self):
        source = inventory()
        before = canonical(source)
        first, _ = probes.analyze(source)
        self.assertEqual(before, canonical(source))
        self.assertEqual(canonical(first), canonical(probes.analyze(source)[0]))
        profiles = [p["profile"] for p in first["profiles"].values()]
        self.assertTrue(any(p["upgrade_raw"] == 8192 and p["secondary_enchantment_raw"]
                            for p in profiles))

    def test_schema_and_identity_fail_closed(self):
        mutations = [lambda x: x.update(schema_version=2),
                     lambda x: x.update(recorded_save_version="future"),
                     lambda x: x["inventory_records"][0].update(content_sha256="bad"),
                     lambda x: x["inventory_records"][0].update(source_pointer="bad"),
                     lambda x: x["inventory_records"][0].update(category_tentative="sword")]
        for change in mutations:
            with self.subTest(change=change):
                data = inventory()
                change(data)
                with self.assertRaises(ValidationError):
                    probes.analyze(data)

    def test_selector_injection_and_budget(self):
        for selector in ('sword\nequip hammer', 'sword @secret@', '"sword"',
                         'a b c d e f g h', ''):
            with self.assertRaises(ValidationError):
                probes.check_selector(selector)

    def test_paths_privacy_immutable_rerun(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "data/raw/player_save/derived/v1/example/inventory.json"
            source.parent.mkdir(parents=True)
            source.write_bytes(canonical(inventory()))
            with patch.object(probes, "ensure_git_private") as guard:
                target, _ = probes.run(root, source)
                guard.assert_called_once()
                times = {p.name: p.stat().st_mtime_ns for p in target.iterdir()}
                probes.run(root, source)
                self.assertEqual(times, {p.name: p.stat().st_mtime_ns for p in target.iterdir()})
                (target / "Candidates.txt").write_text("tampered")
                with self.assertRaises(ValidationError):
                    probes.run(root, source)
            with self.assertRaises(ValidationError):
                probes.run(root, root / "active_save.json")
            with patch.object(probes, "ensure_git_private", side_effect=ValidationError("private")):
                with self.assertRaises(ValidationError):
                    probes.run(root, source)

    def test_stonescript_safety_guards_and_isolation(self):
        text = (ROOT / "scripts/selector_validation/main.txt").read_text()
        self.assertIn("var allowEquip = false", text)
        self.assertIn("?allowEquip & probeArmed", text)
        self.assertIn("?key = primaryBegin", text)
        self.assertIn("?key = upBegin", text)
        self.assertIn("probeArmed = false", text)
        self.assertNotIn("SpeedRunBasic/", text)
        self.assertNotIn("activate ", text)
        self.assertNotIn("loadout ", text)
        self.assertNotIn("func Harvest", text)
        # Every equip command remains nested under input + opt-in + positive-count guards.
        for line in text.splitlines():
            if line.lstrip().startswith(("equip ", "equipL ", "equipR ")):
                self.assertTrue(line.startswith("        "))

    @unittest.skipUnless(sys.platform == "win32", "PowerShell installer runs on Windows")
    def test_installer_backup_hashes_and_unrelated_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "tools").mkdir()
            (root / "scripts/selector_validation").mkdir(parents=True)
            installer = root / "tools/Install-SelectorValidation.ps1"
            installer.write_bytes((ROOT / "tools/Install-SelectorValidation.ps1").read_bytes())
            (root / "scripts/selector_validation/main.txt").write_bytes(
                (ROOT / "scripts/selector_validation/main.txt").read_bytes())
            subprocess.run(["git", "init", "-q", str(root)], check=True, capture_output=True)
            (root / ".gitignore").write_text("data/raw/player_save/\nbackups/\n")
            candidates = root / "data/raw/player_save/selector_validation/v1/synthetic"
            candidates.mkdir(parents=True)
            (candidates / "Candidates.txt").write_bytes(probes.stonescript(
                [{"selector": "stone sword -big", "hand": "L"}]))
            game = root / "fake-game"
            target = game / "EquipmentSelectorTest"
            target.mkdir(parents=True)
            (target / "main.txt").write_text("OLD DIAGNOSTIC")
            (game / "MindStone.txt").write_text("DO NOT TOUCH")
            command = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                       str(installer), "-CandidatesDirectory", str(candidates),
                       "-StonescriptRoot", str(game)]
            completed = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual((game / "MindStone.txt").read_text(), "DO NOT TOUCH")
            self.assertEqual((target / "Candidates.txt").read_bytes(),
                             (candidates / "Candidates.txt").read_bytes())
            backups = list((root / "backups").glob("*/EquipmentSelectorTest/main.txt"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(), "OLD DIAGNOSTIC")


if __name__ == "__main__":
    unittest.main()
