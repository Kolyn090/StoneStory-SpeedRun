
from pathlib import Path
from PIL import Image

MATRIX_COLUMNS = 4
MATRIX_ROWS = 3


def split_matrix(image: Image.Image):
    """
    Split an inventory matrix into 12 cell images.

    Returns a list of (row, column, image).
    """
    width, height = image.size

    cells = []

    for row in range(MATRIX_ROWS):
        for col in range(MATRIX_COLUMNS):
            left = round(col * width / MATRIX_COLUMNS)
            top = round(row * height / MATRIX_ROWS)

            right = round(
                (col + 1) * width / MATRIX_COLUMNS
            )
            bottom = round(
                (row + 1) * height / MATRIX_ROWS
            )

            cell = image.crop(
                (left, top, right, bottom)
            )

            cells.append((row, col, cell))

    return cells


def process_matrix(image_path):
    """
    Read and process an inventory screenshot.
    """
    image_path = Path(image_path)

    with Image.open(image_path) as source:
        image = source.convert("RGB")

    cells = split_matrix(image)

    print(f"Matrix size: {image.width}x{image.height}")
    print(f"Detected cells: {len(cells)}")

    return cells


if __name__ == "__main__":
    input_path = (
        Path(__file__).resolve().parent
        / "screenshot"
        / "matrix.png"
    )

    cells = process_matrix(input_path)

    # Preview each cell's boundaries and dimensions.
    for row, col, cell in cells:
        print(
            f"Row {row + 1}, "
            f"Column {col + 1}: "
            f"{cell.width}x{cell.height}"
        )
