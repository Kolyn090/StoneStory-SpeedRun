"""Build PRIVATE, unverified selector probes from an offline normalized snapshot."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

from import_player_inventory import (ELEMENTS, ValidationError, canonical, digest,
                                     ensure_git_private, normalize, parse_save, require)

# Explicit reviewed hypotheses, NOT an internal-ID -> native-ID conversion rule.
# hand: L/R are one-handed probes; auto uses equip (required for two-handed gear).
ALIASES = {
    "sword": ("stone sword -big -socket", "L"),
    "socketed_sword": ("sword -big", "L"),
    "socketed_long_sword": ("sword big", "auto"),
    "wand": ("wand", "L"),
    "crossbow": ("stone crossbow", "auto"),
    "socketed_crossbow": ("crossbow", "auto"),
    "repeating_crossbow": ("repeating crossbow", "auto"),
    "socketed_hammer": ("hammer -heavy", "L"),
    "heavy_hammer": ("heavy hammer", "auto"),
    "shield": ("stone shield -socket", "R"),
    "socketed_shield": ("shield", "R"),
    "compound_shield": ("compound shield", "R"),
    "bashing_shield": ("bashing shield", "R"),
    "dashing_shield": ("dashing shield", "R"),
    "tower_shield": ("towering shield", "R"),
    "quarterstaff": ("quarterstaff", "auto"),
    "socketed_staff": ("staff", "auto"),
    "shovel_lv1": ("shovel", "auto"),
}
EQUIPMENT_FAMILIES = {"sword", "wand", "crossbow", "hammer", "shield", "staff",
                      "special_equipment", "tool"}


def check_selector(selector):
    # Generated code contains ONLY fixed dictionary words + fixed element labels/numbers.
    require(type(selector) is str and bool(re.fullmatch(r"[A-Za-z0-9 *+\-]+", selector)),
            "Unsafe selector text.")
    require(0 < len(selector.split()) <= 7, "Selector exceeds criteria budget.")


def analyze(inventory):
    require(inventory.get("schema_version") == 1, "Normalized schema requires review.")
    require(inventory.get("recorded_save_version") == "4.35.2", "Save version requires review.")
    records = inventory.get("inventory_records")
    require(type(records) is list and bool(records), "Normalized records missing or empty.")
    # Revalidate authoritative raw records through the existing strict importer.
    rebuilt, _ = normalize(canonical({"version": "4.35.2", "inventory_data": {
        "itms": [r.get("raw_record") for r in records if type(r) is dict],
        "itmsSeen": [], "rightH": ""}}))
    require(len(rebuilt["inventory_records"]) == len(records), "Malformed normalized record.")
    groups, probes, excluded = {}, {}, Counter()
    pointers = set()
    for r in records:
        raw = r["raw_record"]
        da = raw["da"]
        require(r.get("type_id") == raw["id"] and r.get("content_sha256") == digest(raw),
                "Normalized identity mismatch.")
        pointer = r.get("source_pointer")
        require(type(pointer) is str and bool(re.fullmatch(r"/inventory_data/itms/\d+", pointer))
                and pointer not in pointers, "Invalid or repeated source reference.")
        pointers.add(pointer)
        family = next(x["category_tentative"] for x in rebuilt["inventory_records"]
                      if x["content_sha256"] == r["content_sha256"])
        require(r.get("category_tentative") == family, "Normalized category mismatch.")
        profile = {"type_id": raw["id"], "family_tentative": family,
                   "element_raw": da.get("el"), "upgrade_raw": da.get("lv"),
                   "primary_enchantment_raw": da.get("ra"),
                   "secondary_enchantment_raw": da.get("sra"),
                   "ability_codes_raw": da.get("abs"), "shiny_flag_raw": da.get("sh"),
                   "appearance_raw": da.get("c")}
        key = digest(profile)
        group = groups.setdefault(key, {"profile": profile, "source_records": []})
        group["source_records"].append({"pointer": pointer,
            "content_sha256": r["content_sha256"], "quantity_raw": raw.get("co")})
        if family not in EQUIPMENT_FAMILIES:
            excluded[family] += 1
            group["disposition"] = "non-equipment category; no probe"
            continue
        if raw["id"] not in ALIASES or (da.get("el") is not None and da["el"] not in ELEMENTS):
            excluded["equipment_alias_deferred"] += 1
            group["disposition"] = "alias/element unresolved; no probe"
            continue
        base, hand = ALIASES[raw["id"]]
        if "el" in da:
            base = ELEMENTS[da["el"]] + " " + base
        variants = [(base, "broad-family hypothesis")]
        # Native +N syntax is documented; mapping ra.lv -> N is NOT established.
        if "ra" in da:
            variants.append((base + " +" + str(da["ra"]["lv"]), "raw-primary-level hypothesis"))
        if da.get("sh") is True:
            variants.append((base + " shiny", "raw-shiny-flag hypothesis"))
        group["disposition"] = "candidate only; equippability unverified"
        for selector, hypothesis in variants:
            check_selector(selector)
            probe = probes.setdefault((selector, hand), {"selector": selector, "hand": hand,
                "hypothesis": hypothesis, "profile_groups": set(), "source_pointers": set(),
                "static_status": "documented form; alias/property mapping unverified",
                "in_game_count": None, "exact_item_confirmed": None})
            probe["profile_groups"].add(key)
            probe["source_pointers"].add(pointer)
    ordered = []
    for index, (_, probe) in enumerate(sorted(probes.items())):
        probe = dict(probe, case=f"S{index + 1:03d}")
        for field in ("profile_groups", "source_pointers"):
            probe[field] = sorted(probe[field])
        probe["saved_record_count_not_game_count"] = len(probe["source_pointers"])
        probe["ambiguous_saved_variants"] = len(probe["profile_groups"]) > 1
        ordered.append(probe)
    require(bool(ordered), "No reviewed selector hypotheses available.")
    private = {"candidate_schema_version": 1, "normalized_input_sha256": digest(inventory),
               "profiles": dict(sorted(groups.items())), "candidates": ordered,
               "semantics": "Provenance is private; record counts are not runtime copy counts."}
    summary = {"inventory_records_analyzed": len(records), "profile_groups": len(groups),
               "candidate_queries": len(ordered), "saved_ambiguous_queries": sum(
                   p["ambiguous_saved_variants"] for p in ordered),
               "deferred_or_non_equipment_records": dict(sorted(excluded.items()))}
    return private, summary


def stonescript(probes):
    selectors, hands = [], []
    for probe in probes:
        check_selector(probe["selector"])
        require(probe["hand"] in ("L", "R", "auto"), "Invalid hand mode.")
        selectors.append(probe["selector"])
        hands.append(probe["hand"])
    return ("// PRIVATE generated hypotheses. No IDs, tags or save text embedded.\n"
            + "var selectors = " + json.dumps(selectors) + "\n"
            + "var hands = " + json.dumps(hands) + "\n").encode("ascii")


def run(root, source):
    root = root.resolve()
    private = (root / "data/raw/player_save").resolve()
    source = source.resolve()
    output = (private / "selector_validation/v1").resolve()
    require(private.is_relative_to(root) and output.is_relative_to(private), "Private output escapes project.")
    require(source.is_relative_to(private / "derived/v1") and source.name == "inventory.json",
            "Select an offline normalized snapshot, not a save file.")
    ensure_git_private(root, [source, output / "probe"])
    source_bytes = source.read_bytes()
    inventory = parse_save(source_bytes)
    result, summary = analyze(inventory)
    target = output / hashlib.sha256(source_bytes).hexdigest()
    files = {"candidates.json": canonical(result), "summary.json": canonical(summary),
             "Candidates.txt": stonescript(result["candidates"]),
             "results-template.json": canonical({"build": None, "script_commit": None,
                 "location_difficulty": None, "results": [{"case": p["case"],
                    "selector": p["selector"], "count": None, "actual_left": None,
                    "actual_right": None, "displayed_stars": None,
                    "displayed_enchantments": None, "exact_item_confirmed": None,
                    "errors_or_notes": ""} for p in result["candidates"]]})}
    if target.exists():
        require(all((target / name).is_file() and (target / name).read_bytes() == value
                    for name, value in files.items()), "Existing output differs; preserve and review it.")
    else:
        target.mkdir(parents=True)
        for name, value in files.items():
            with (target / name).open("xb") as handle:
                handle.write(value)
    return target, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", required=True, type=Path)
    args = parser.parse_args()
    try:
        _, summary = run(Path(__file__).resolve().parents[1], args.inventory)
        print(canonical(summary).decode(), end="")
        return 0
    except (ValidationError, OSError, KeyError, TypeError, ValueError, StopIteration):
        print("Candidate build rejected: invalid schema, unsafe path, privacy check or output conflict.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
