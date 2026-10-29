"""Synthetic fixtures only. Never discover or read the owner's private save."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "inventory_importer", Path(__file__).resolve().parents[1] / "tools/import_player_inventory.py")
IMPORTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(IMPORTER)


def item(type_id="socketed_sword", **detail):
    return {"id": type_id, "da": {"hI": True, "rng": 17, "lv": 8192,
            "el": "Fire", "abs": ["element_damage_sword_2"], **detail}}


def fixture(*items):
    return {"version": "4.35.2", "hero_settings": {"playerName": "PRIVATE-PROFILE"},
            "inventory_data": {"Stone": 3, "None": 0, "rightH": "PRIVATE-REF",
                               "itmsSeen": ["SEEN-ONLY"], "itms": list(items)}}


def encoded(data):
    return json.dumps(data).encode("utf-8")


class SchemaTests(unittest.TestCase):
    def test_variants_and_identical_duplicates_preserved(self):
        first = item(ra={"lv": 21, "ql": 12, "sSS": 18},
                     sra={"lv": 21, "ql": 13, "sSS": 19}, tag="PRIVATE-TAG")
        second = item(el="Ice", abs=["chill_onhit"])
        inventory, summary = IMPORTER.normalize(encoded(fixture(first, second, first)))
        rows = inventory["inventory_records"]
        self.assertEqual(len(rows), 3)
        self.assertEqual(summary["repeated_type_groups"], 1)
        self.assertEqual(summary["exact_duplicate_record_excess"], 1)
        self.assertEqual(sorted(r["identical_record_occurrence"] for r in rows), [1, 1, 2])
        self.assertTrue(all(r["upgrade_raw"] == 8192 for r in rows))
        self.assertEqual(sum(r["primary_enchantment_raw"] == first["da"]["ra"] for r in rows), 2)
        self.assertTrue(all("stars" not in r and "selector" not in r for r in rows))
        text = IMPORTER.canonical(summary).decode()
        for private_value in ("PRIVATE-TAG", "PRIVATE-PROFILE", "PRIVATE-REF", "SEEN-ONLY"):
            self.assertNotIn(private_value, text)
        self.assertNotIn("hero_settings", inventory)

    def test_resources_stacks_nested_contents_and_seen_are_separate(self):
        stack = item("sword")
        stack["co"] = 500000
        treasure = item("treasure_1", itms=[{"id": "sword", "t": 2, "st": 0}])
        inventory, summary = IMPORTER.normalize(encoded(fixture(stack, treasure)))
        self.assertEqual(summary["top_level_inventory_records"], 2)
        self.assertEqual(summary["stack_records"], 1)
        self.assertEqual(summary["unopened_content_records"], 1)
        self.assertEqual(summary["seen_history_entries"], 1)
        self.assertEqual(inventory["resource_buckets_raw"], {"None": 0, "Stone": 3})
        self.assertEqual(inventory["unopened_contents"][0]["raw_record"]["id"], "sword")
        rows = inventory["inventory_records"]
        self.assertTrue(any(r["quantity_raw"] == 500000 for r in rows))
        self.assertTrue(any(r["quantity_raw"] is None and not r["stack_count_field_present"] for r in rows))

    def test_malformed_and_duplicate_json_rejected_without_content_leak(self):
        for raw in (b'{"PRIVATE-TEXT":', b'{"a":1,"a":2}',
                    b'{"outer":{"a":1,"a":2}}', b'{} {}', b'\xff', b'NaN', b'1e999'):
            with self.subTest(raw=raw):
                with self.assertRaises(IMPORTER.ValidationError) as caught:
                    IMPORTER.normalize(raw)
                self.assertNotIn("PRIVATE-TEXT", str(caught.exception))

    def test_missing_fields_and_changed_known_types_rejected(self):
        baseline = fixture(item())
        variants = []
        for field in ("version", "inventory_data"):
            changed = copy.deepcopy(baseline)
            del changed[field]
            variants.append(changed)
        for field in ("itms", "itmsSeen", "rightH"):
            changed = copy.deepcopy(baseline)
            del changed["inventory_data"][field]
            variants.append(changed)
        for field in ("id", "da"):
            changed = copy.deepcopy(baseline)
            del changed["inventory_data"]["itms"][0][field]
            variants.append(changed)
        for field in ("hI", "rng"):
            changed = copy.deepcopy(baseline)
            del changed["inventory_data"]["itms"][0]["da"][field]
            variants.append(changed)
        for key, value in (("lv", "8192"), ("lv", True), ("abs", [1]), ("sh", 1),
                           ("ra", {"lv": 21}), ("ra", {"lv": True, "ql": 1, "sSS": 2})):
            changed = copy.deepcopy(baseline)
            changed["inventory_data"]["itms"][0]["da"][key] = value
            variants.append(changed)
        changed = copy.deepcopy(baseline)
        changed["inventory_data"]["itms"][0]["co"] = False
        variants.append(changed)
        for changed in variants:
            with self.subTest(changed=changed):
                with self.assertRaises(IMPORTER.ValidationError):
                    IMPORTER.normalize(encoded(changed))

    def test_new_version_fails_closed(self):
        changed = fixture(item())
        changed["version"] = "9.99.0"
        with self.assertRaisesRegex(IMPORTER.ValidationError, "schema review"):
            IMPORTER.normalize(encoded(changed))

    def test_invalid_nested_content_and_seen_schema_rejected(self):
        for contents in ({"id": "sword"}, [None], [{"id": ""}]):
            with self.subTest(contents=contents):
                with self.assertRaises(IMPORTER.ValidationError):
                    IMPORTER.normalize(encoded(fixture(item("treasure_1", itms=contents))))
        changed = fixture(item())
        changed["inventory_data"]["itmsSeen"] = [{"id": "sword"}]
        with self.assertRaises(IMPORTER.ValidationError):
            IMPORTER.normalize(encoded(changed))

    def test_nonfinite_unicode_and_size_limits(self):
        for raw in (b'Infinity', b'{"value":1e999}', b'{"value":"\\ud800"}'):
            with self.subTest(raw=raw):
                with self.assertRaises(IMPORTER.ValidationError):
                    IMPORTER.parse_save(raw)
        with patch.object(IMPORTER, "MAX_BYTES", 1):
            with self.assertRaisesRegex(IMPORTER.ValidationError, "size limit"):
                IMPORTER.parse_save(b'{}')

    def test_unknown_fields_and_types_preserved_but_sanitized(self):
        changed = fixture(item("PRIVATE-UNKNOWN-ID", unknown_future={"secret": "PRIVATE-UNKNOWN"},
                               el="PRIVATE-ELEMENT"))
        changed["inventory_data"]["future_inventory"] = {"secret": "PRIVATE-INVENTORY"}
        changed["inventory_data"]["itms"][0]["future_record"] = "PRIVATE-RECORD"
        inventory, summary = IMPORTER.normalize(encoded(changed))
        self.assertEqual(inventory["inventory_records"][0]["raw_record"], changed["inventory_data"]["itms"][0])
        self.assertEqual(summary["tentative_categories"], {"unclassified": 1})
        self.assertEqual(summary["elements"], {"unknown": 1})
        self.assertEqual(summary["warnings"]["unknown_item_data_field"], 1)
        self.assertNotIn("PRIVATE", IMPORTER.canonical(summary).decode())

    def test_output_deterministic_and_record_fingerprints_survive_reorder(self):
        baseline = fixture(item(), item(el="Ice"))
        raw = encoded(baseline)
        self.assertEqual(IMPORTER.canonical(IMPORTER.normalize(raw)[0]),
                         IMPORTER.canonical(IMPORTER.normalize(raw)[0]))
        other = copy.deepcopy(baseline)
        other["inventory_data"]["itms"].reverse()
        original = IMPORTER.normalize(raw)[0]["inventory_records"]
        reordered = IMPORTER.normalize(encoded(other))[0]["inventory_records"]
        self.assertEqual([r["content_sha256"] for r in original], [r["content_sha256"] for r in reordered])

    def test_empty_collection_does_not_invent_items(self):
        inventory, summary = IMPORTER.normalize(encoded(fixture()))
        self.assertEqual(inventory["inventory_records"], [])
        self.assertEqual(summary["top_level_inventory_records"], 0)


class FileBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.private = self.root / "data/raw/player_save"
        self.private.mkdir(parents=True)
        self.source = self.private / "synthetic.json"
        self.raw = encoded(fixture(item()))
        self.source.write_bytes(self.raw)

    def test_outside_or_generated_input_rejected(self):
        with self.assertRaises(IMPORTER.ValidationError):
            IMPORTER.private_paths(self.root, self.root / "active_game_save.json")
        derived = self.private / "derived/example.json"
        with self.assertRaises(IMPORTER.ValidationError):
            IMPORTER.private_paths(self.root, derived)

    @patch.object(IMPORTER, "ensure_git_private")
    def test_immutable_output_input_unchanged_and_repeat_noop(self, _):
        snapshot, first = IMPORTER.run_import(self.root, self.source)
        outputs = {p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in snapshot.iterdir()}
        second_path, second = IMPORTER.run_import(self.root, self.source)
        self.assertEqual(self.source.read_bytes(), self.raw)
        self.assertEqual((snapshot, first), (second_path, second))
        self.assertEqual(outputs, {p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in snapshot.iterdir()})
        (snapshot / "summary.json").write_text("DIFFERENT", encoding="utf-8")
        with self.assertRaisesRegex(IMPORTER.ValidationError, "differs or is incomplete"):
            IMPORTER.run_import(self.root, self.source)
        self.assertEqual((snapshot / "summary.json").read_text(), "DIFFERENT")

    @patch.object(IMPORTER.subprocess, "run")
    def test_tracked_private_input_is_rejected(self, run):
        run.return_value = subprocess.CompletedProcess([], 0, stdout=b"tracked.json\n")
        with self.assertRaisesRegex(IMPORTER.ValidationError, "tracked"):
            IMPORTER.ensure_git_private(self.root, [self.source])

    @patch.object(IMPORTER.subprocess, "run")
    def test_unignored_output_is_rejected(self, run):
        run.side_effect = [subprocess.CompletedProcess([], 0, stdout=b""),
                           subprocess.CompletedProcess([], 1)]
        with self.assertRaisesRegex(IMPORTER.ValidationError, "Git-ignored"):
            IMPORTER.ensure_git_private(self.root, [self.source])

    @patch.object(IMPORTER, "ensure_git_private", side_effect=IMPORTER.ValidationError("blocked"))
    def test_privacy_check_occurs_before_save_read(self, _):
        with patch.object(Path, "read_bytes", side_effect=AssertionError("must not read")):
            with self.assertRaisesRegex(IMPORTER.ValidationError, "blocked"):
                IMPORTER.run_import(self.root, self.source)


if __name__ == "__main__":
    unittest.main()
