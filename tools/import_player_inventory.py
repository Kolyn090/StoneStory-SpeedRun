"""Offline save importer. Private output only; no Stonescript selectors or game IO."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

IMPORTER_VERSION = 1
SUPPORTED_SAVE_VERSION = "4.35.2"
MAX_BYTES = 64 * 1024 * 1024
RESOURCE_KEYS = {"Stone", "Wood", "Tar", "Xi", "Bronze", "None"}
DATA_TYPES = {
    "hI": bool, "rng": int, "rS": str, "itms": list, "lv": int,
    "ra": dict, "sra": dict, "sh": bool, "tag": str, "sig": str,
    "el": str, "abs": list, "lC": int, "lBU": int, "c": str,
    "hidAb": bool, "potion_type": str, "last_type": str,
    "auto_refill": bool, "costs": list,
}
ELEMENTS = {"Poison": "poison", "Vigor": "vigor", "AEther": "aether",
            "Fire": "fire", "Ice": "ice"}
# Category labels are reviewed, tentative type classifications, not native selectors.
FAMILIES = {
    "sword": {"sword", "socketed_sword", "socketed_long_sword"},
    "wand": {"wand", "lollipop_wand"} | {"wand_hidden_" + e for e in ELEMENTS.values()},
    "crossbow": {"crossbow", "socketed_crossbow", "repeating_crossbow"},
    "hammer": {"socketed_hammer", "heavy_hammer"},
    "shield": {"shield", "socketed_shield", "compound_shield", "bashing_shield",
               "dashing_shield", "tower_shield"},
    "staff": {"quarterstaff", "socketed_staff"} | {
        "socketed_staff_hidden_" + e for e in ELEMENTS.values()},
    "special_equipment": {"bardiche", "blade_of_god", "cult_mask", "skeleton_arm",
                          "aether_talisman", "fire_talisman"},
    "tool": {"shovel_lv1", "hatchet_lv1", "grappling_hook_lv2", "fishing_rod", "torch_lv1"},
    "utility": {"potion", "craft_book", "foe_book", "goal_book", "utility_belt",
                "canoe_lv1", "bronze_key", "moon_stone", "mind_stone", "triskelion_stone",
                "fissure_stone", "quest_stone", "ouroboros_stone", "xp_stone", "xi_stone",
                "star_stone", "sight_stone"},
    "material_or_consumable": {"moonbloom", "moonbloom_petal", "event_ticket", "ki_crystal",
        "resonant_clay", "crystal_powder", "shiny", "hourglass", "name_tag", "enchantment",
        "runestone", "vigor_talisman_voucher", "balloon", "candy", "mug", "warm_stone", "stones"},
    "unopened_treasure": {"treasure_1"},
}


class ValidationError(Exception):
    """Messages are fixed/sanitized: never echo untrusted keys or scalar values."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def canonical(value) -> bytes:
    return (json.dumps(value, ensure_ascii=True, allow_nan=False, sort_keys=True,
                       indent=2) + "\n").encode("utf-8")


def digest(value) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def parse_save(raw: bytes) -> dict:
    require(len(raw) <= MAX_BYTES, "Input exceeds size limit.")

    def pairs_hook(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "Duplicate JSON object key.")
            result[key] = value
        return result

    def reject_constant(_):
        raise ValidationError("Non-finite JSON number.")

    try:
        text = raw.decode("utf-8-sig", errors="strict")
        data = json.loads(text, object_pairs_hook=pairs_hook, parse_constant=reject_constant)
    except UnicodeDecodeError:
        raise ValidationError("Input is not valid UTF-8.") from None
    except json.JSONDecodeError as error:
        raise ValidationError(f"Malformed JSON at line {error.lineno}, column {error.colno}.") from None
    except (RecursionError, ValueError):
        raise ValidationError("JSON nesting or numeric representation exceeds limits.") from None

    def check(value, depth=0):
        require(depth <= 64, "JSON nesting exceeds limit.")
        if isinstance(value, float):
            require(math.isfinite(value), "Non-finite JSON number.")
        elif isinstance(value, str):
            require(not any(0xD800 <= ord(c) <= 0xDFFF for c in value), "Invalid Unicode scalar.")
        elif isinstance(value, dict):
            for key, child in value.items():
                check(key, depth + 1)
                check(child, depth + 1)
        elif isinstance(value, list):
            for child in value:
                check(child, depth + 1)
    check(data)
    require(type(data) is dict, "Save root must be an object.")
    return data


def classify(type_id: str) -> str:
    return next((family for family, ids in FAMILIES.items() if type_id in ids), "unclassified")


def normalize(raw: bytes) -> tuple[dict, dict]:
    data = parse_save(raw)
    require(data.get("version") == SUPPORTED_SAVE_VERSION, "Save version requires schema review.")
    inv = data.get("inventory_data")
    require(type(inv) is dict, "Missing or malformed inventory_data.")
    require(type(inv.get("itms")) is list, "Missing or malformed inventory item collection.")
    require(type(inv.get("itmsSeen")) is list and all(type(x) is str for x in inv["itmsSeen"]),
            "Missing or malformed seen-item history.")
    require(type(inv.get("rightH")) is str, "Missing or malformed right-hand reference.")
    if "leftH" in inv:
        require(type(inv["leftH"]) is str, "Malformed left-hand reference.")
    for key in RESOURCE_KEYS:
        if key in inv:
            require(type(inv[key]) is int and inv[key] >= 0, "Resource bucket schema changed.")

    warnings = Counter()
    records = []
    contents = []

    def content_records(items, parent_pointer):
        require(type(items) is list, "Treasure contents must be an array.")
        for index, item in enumerate(items):
            require(type(item) is dict and type(item.get("id")) is str and bool(item["id"]),
                    "Malformed nested item record.")
            pointer = f"{parent_pointer}/da/itms/{index}"
            contents.append({"source_pointer": pointer, "classification": "unopened_content",
                             "parent_pointer": parent_pointer, "raw_record": item})
            nested = item.get("da", {}).get("itms") if type(item.get("da")) is dict else None
            if nested is not None:
                content_records(nested, pointer)

    for index, item in enumerate(inv["itms"]):
        require(type(item) is dict, "Inventory record must be an object.")
        require(type(item.get("id")) is str and bool(item["id"]), "Missing or malformed item type ID.")
        require(type(item.get("da")) is dict, "Missing or malformed item data.")
        detail = item["da"]
        require(type(detail.get("hI")) is bool and type(detail.get("rng")) is int,
                "Missing or malformed required raw item fields.")
        if "co" in item:
            require(type(item["co"]) is int and item["co"] > 0, "Malformed item quantity.")
        for key, value in detail.items():
            if key not in DATA_TYPES:
                warnings["unknown_item_data_field"] += 1
                continue
            require(type(value) is DATA_TYPES[key], "Known item field changed type.")
        warnings["unknown_item_record_field"] += len(set(item) - {"id", "da", "co"})
        if "lv" in detail:
            require(detail["lv"] > 0, "Raw upgrade value must be positive.")
        for key in ("ra", "sra"):
            if key in detail:
                affix = detail[key]
                require(all(type(affix.get(k)) is int for k in ("lv", "ql", "sSS")),
                        "Enchantment structure schema changed.")
                require(affix["lv"] > 0, "Raw enchantment level must be positive.")
                warnings["unknown_enchantment_field"] += len(set(affix) - {"lv", "ql", "sSS"})
        if "abs" in detail:
            require(all(type(x) is str for x in detail["abs"]), "Ability codes must be strings.")
        if "el" in detail and detail["el"] not in ELEMENTS:
            warnings["unknown_element"] += 1
        category = classify(item["id"])
        if category == "unclassified":
            warnings["unclassified_type"] += 1
        pointer = f"/inventory_data/itms/{index}"
        # A content fingerprint is not an item-instance ID. Keep exact duplicates too.
        record = {
            "source_pointer": pointer, "content_sha256": digest(item),
            "type_id": item["id"], "category_tentative": category,
            "stack_count_field_present": "co" in item,
            "quantity_raw": item.get("co"),
            "element_raw": detail.get("el"), "ability_codes_raw": detail.get("abs"),
            "upgrade_raw": detail.get("lv"),
            "primary_enchantment_raw": detail.get("ra"),
            "secondary_enchantment_raw": detail.get("sra"),
            "unknown_data_fields": {k: v for k, v in detail.items() if k not in DATA_TYPES},
            "raw_record": item,
        }
        records.append(record)
        if "itms" in detail:
            if category != "unopened_treasure":
                warnings["contents_of_unclassified_container"] += 1
            content_records(detail["itms"], pointer)

    records.sort(key=lambda r: (r["type_id"], r["content_sha256"], r["source_pointer"]))
    occurrences = Counter()
    for record in records:
        occurrences[record["content_sha256"]] += 1
        record["identical_record_occurrence"] = occurrences[record["content_sha256"]]
    known_inv = RESOURCE_KEYS | {"itms", "itmsSeen", "rightH", "leftH"}
    unknown_inv = {k: v for k, v in inv.items() if k not in known_inv}
    warnings["unknown_inventory_field"] += len(unknown_inv)
    warnings = {k: v for k, v in sorted(warnings.items()) if v}
    inventory = {
        "schema_version": IMPORTER_VERSION, "recorded_save_version": data["version"],
        "source": {"sha256": hashlib.sha256(raw).hexdigest(), "byte_count": len(raw)},
        "semantics": "Observed raw values; categories tentative; no stars, stats, rarity or selectors derived.",
        "inventory_records": records,
        "resource_buckets_raw": {k: inv[k] for k in sorted(RESOURCE_KEYS) if k in inv},
        "unopened_contents": contents,
        "seen_item_history_raw": inv["itmsSeen"],
        "equipment_references_raw": {k: inv[k] for k in ("rightH", "leftH") if k in inv},
        "unmapped_inventory_fields": unknown_inv,
        "warnings": warnings,
    }
    return inventory, sanitized_summary(inventory)


def sanitized_summary(inventory: dict) -> dict:
    """Only fixed category labels and aggregate counts; never echo arbitrary IDs/codes/tags."""
    records = inventory["inventory_records"]
    types = Counter(r["type_id"] for r in records)
    variants = Counter((r["type_id"], r["element_raw"]) for r in records)
    element_counts = Counter(ELEMENTS.get(r["element_raw"], "absent" if r["element_raw"] is None
                                        else "unknown") for r in records)
    modifier_counts = Counter()
    for record in records:
        detail = record["raw_record"]["da"]
        for name, key in (("primary_enchantment", "ra"), ("secondary_enchantment", "sra"),
                          ("raw_upgrade", "lv"), ("ability_codes", "abs"), ("signature", "sig"),
                          ("custom_tag", "tag"), ("appearance", "c")):
            modifier_counts[name + "_present"] += key in detail
        modifier_counts["shiny_flag_true"] += detail.get("sh") is True
        modifier_counts["hidden_ability_flag_true"] += detail.get("hidAb") is True
        modifier_counts["both_raw_enchantment_levels_21"] += (
            detail.get("ra", {}).get("lv") == 21 and detail.get("sra", {}).get("lv") == 21)
    return {
        "summary_schema_version": 1, "top_level_inventory_records": len(records),
        "distinct_type_ids": len(types),
        "tentative_categories": dict(sorted(Counter(r["category_tentative"] for r in records).items())),
        "elements": dict(sorted(element_counts.items())),
        "modifier_presence_counts": dict(sorted(modifier_counts.items())),
        "stack_records": sum(r["stack_count_field_present"] for r in records),
        "resource_bucket_count": len(inventory["resource_buckets_raw"]),
        "unopened_content_records": len(inventory["unopened_contents"]),
        "seen_history_entries": len(inventory["seen_item_history_raw"]),
        "repeated_type_groups": sum(n > 1 for n in types.values()),
        "repeated_type_element_groups": sum(n > 1 for n in variants.values()),
        "exact_duplicate_record_excess": len(records) - len({r["content_sha256"] for r in records}),
        "warnings": inventory["warnings"],
    }


def private_paths(project_root: Path, input_path: Path) -> tuple[Path, Path]:
    root = project_root.resolve()
    private = (root / "data/raw/player_save").resolve()
    derived = (private / "derived").resolve()
    source = input_path.resolve()
    require(private.is_relative_to(root), "Private root escapes project.")
    require(derived.is_relative_to(private), "Derived root escapes private area.")
    require(source.is_relative_to(private) and not source.is_relative_to(derived),
            "Input must be an offline JSON export inside data/raw/player_save, outside derived.")
    require(source.is_file() and source.suffix.lower() == ".json", "Input must be a JSON export file.")
    return source, derived


def ensure_git_private(root: Path, paths: list[Path]) -> None:
    """Fail before save IO if Git privacy cannot be established. Never changes the index."""
    try:
        tracked = subprocess.run(["git", "-C", str(root), "ls-files", "--", "data/raw/player_save"],
                                 capture_output=True, check=True).stdout
        require(not tracked.strip(), "Private save files are tracked; remove from index before importing.")
        for path in paths:
            result = subprocess.run(["git", "-C", str(root), "check-ignore", "-q", "--", str(path)],
                                    capture_output=True)
            require(result.returncode == 0, "Private input/output must be Git-ignored.")
    except (OSError, subprocess.CalledProcessError):
        raise ValidationError("Could not verify Git privacy; no save was read.") from None


def run_import(project_root: Path, input_path: Path) -> tuple[Path, dict]:
    source, derived = private_paths(project_root, input_path)
    ensure_git_private(project_root, [source, derived / "privacy-check.json"])
    require(source.stat().st_size <= MAX_BYTES, "Input exceeds size limit.")
    raw = source.read_bytes()  # The only save read; never search for or open an active game save.
    inventory, summary = normalize(raw)
    snapshot = derived / f"v{IMPORTER_VERSION}" / inventory["source"]["sha256"]
    require(snapshot.resolve().is_relative_to(derived), "Snapshot path escapes private area.")
    require(not snapshot.is_symlink(), "Snapshot directory must not be a symlink.")
    payloads = {"inventory.json": canonical(inventory), "summary.json": canonical(summary)}
    # Immutable snapshots: repeat import is a no-op; differing existing files are not overwritten.
    if snapshot.exists():
        require(snapshot.is_dir(), "Snapshot destination is not a directory.")
        for name, payload in payloads.items():
            target = snapshot / name
            require(not target.is_symlink() and target.is_file() and target.read_bytes() == payload,
                    "Existing snapshot differs or is incomplete; preserve it and investigate.")
        return snapshot, summary
    snapshot.mkdir(parents=True)
    for name, payload in payloads.items():
        with (snapshot / name).open("xb") as output:
            output.write(payload)
    return snapshot, summary


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Explicit offline export under data/raw/player_save")
    args = parser.parse_args(argv)
    try:
        root = Path(__file__).resolve().parents[1]
        _, summary = run_import(root, args.input)
    except (ValidationError, OSError) as error:
        # Never print OS exceptions: they can contain private filenames or payload fragments.
        message = str(error) if isinstance(error, ValidationError) else "Private file operation failed."
        print("Import rejected: " + message, file=sys.stderr)
        return 1
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
