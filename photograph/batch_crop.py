
from pathlib import Path
import csv

import cv2

from description_processor import find_description_bounds


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

INPUT_DIR = BASE_DIR / "captures"
OUTPUT_DIR = BASE_DIR / "cropped"
REPORT_PATH = OUTPUT_DIR / "crop_report.csv"

FILE_PATTERN = "item_*.png"

# Crop slightly inside the detected panel borders.
VERTICAL_INSET = 0

# Remove unnecessary space from the left and right.
HORIZONTAL_MARGIN = 0

# Set True to replace previously cropped images.
OVERWRITE_EXISTING = False


# ============================================================
# CROPPING
# ============================================================

def crop_image(image):
    """Detect and crop the equipment description panel."""

    top, bottom = find_description_bounds(image)

    height, width = image.shape[:2]

    crop_top = max(0, top + VERTICAL_INSET)
    crop_bottom = min(height, bottom - VERTICAL_INSET)

    crop_left = HORIZONTAL_MARGIN
    crop_right = width - HORIZONTAL_MARGIN

    if crop_bottom <= crop_top:
        raise ValueError("Invalid vertical crop boundaries")

    if crop_right <= crop_left:
        raise ValueError("Invalid horizontal crop boundaries")

    cropped = image[
        crop_top:crop_bottom,
        crop_left:crop_right
    ]

    return cropped, (crop_left, crop_top, crop_right, crop_bottom)


def process_file(input_path):
    """Crop one screenshot while preserving its relative path."""

    relative_path = input_path.relative_to(INPUT_DIR)
    output_path = OUTPUT_DIR / relative_path

    if output_path.exists() and not OVERWRITE_EXISTING:
        return "skipped", "Output already exists", ""

    image = cv2.imread(str(input_path))

    if image is None:
        raise ValueError("Could not read image")

    cropped, bounds = crop_image(image)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not cv2.imwrite(str(output_path), cropped):
        raise OSError(f"Failed to save {output_path}")

    return "success", "", str(bounds)


# ============================================================
# BATCH PROCESSING
# ============================================================

def batch_crop():
    """Crop all captured description screenshots."""

    if not INPUT_DIR.exists():
        raise FileNotFoundError(INPUT_DIR)

    files = sorted(INPUT_DIR.rglob(FILE_PATTERN))

    if not files:
        print("No screenshots found.")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    results = []

    success = 0
    failed = 0
    skipped = 0

    print(f"Found {len(files)} screenshots.\n")

    for index, input_path in enumerate(files, start=1):
        relative_path = input_path.relative_to(INPUT_DIR)

        try:
            status, error, bounds = process_file(input_path)

        except Exception as exc:
            status = "failed"
            error = str(exc)
            bounds = ""

        if status == "success":
            success += 1
        elif status == "skipped":
            skipped += 1
        else:
            failed += 1

        print(
            f"[{index}/{len(files)}] "
            f"{status.upper()}: {relative_path}"
        )

        if error and status == "failed":
            print(f"    Reason: {error}")

        results.append({
            "file": str(relative_path),
            "status": status,
            "bounds": bounds,
            "message": error,
        })

    with REPORT_PATH.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "file",
                "status",
                "bounds",
                "message",
            ],
        )
        writer.writeheader()
        writer.writerows(results)

    print("\n" + "=" * 40)
    print("BATCH CROP COMPLETE")
    print("=" * 40)

    print(f"Processed: {len(files)}")
    print(f"Successful: {success}")
    print(f"Skipped: {skipped}")
    print(f"Failed: {failed}")

    print(f"\nOutput: {OUTPUT_DIR}")
    print(f"Report: {REPORT_PATH}")


if __name__ == "__main__":
    batch_crop()
