from pathlib import Path
from typing import Dict
from PIL import Image, ImageDraw, ImageFont


def resize_image(
        image: Image.Image,
        width: int,
        height: int
) -> Image.Image:
    """Resize and return the resized image"""

    return image.resize((width, height))


def crop_image(
        image: Image.Image,
        left: float,
        upper: float,
        right: float,
        lower: float
) -> Image.Image:
    """Crop and return cropped image."""

    box = (left, upper, right, lower)
    return image.crop(box)


def rotate_image (
        image: Image.Image,
        degree: float
) -> Image.Image:
    """rotate and return rotated image."""

    return image.rotate(degree, expand=True)


def filter_image(
        image: Image.Image,
        filters: dict[str, bool]
) -> Image.Image:
    """Apply filters and return filtered image"""

    if filters.get("grayscale"):
        image = image.convert("L")

    if filters.get("sepia"):
        pixels = image.load()
        for y in range(image.height):
            for x in range(image.width):
                r, g, b = pixels[x, y]
                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                pixels[x, y] = (min(255, tr), min(255, tg), min(255, tb))

    return image


def change_image_format(
        image: Image.Image,
        fmt: str
) -> Image.Image:
    """change image format"""

    acceptable_fmts = set(Image.SAVE.keys())

    if fmt.upper() not in acceptable_fmts:
        raise ValueError(f"{fmt} is not a recognisable image format.")
    image.format = fmt.upper()
    return image


def compress_image_file(
        image:Image.Image
) -> Image.Image:
    """compress image file"""

    pass


def flip_image(
        image: Image.Image
) -> Image.Image:
    """Flip the image vertically (top to bottom)."""

    return image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)


def apply_water_mask_to_image(
        image: Image.Image,
        text: str
) -> Image.Image:
    """Apply watermark text to image file."""

    draw = ImageDraw.Draw(image)
    font_size = 100
    font = ImageFont.truetype("arial.ttf", font_size)

    draw.text((100, 100), text, font=font, fill=100) # Draw text

    return image

def apply_mirror_to_image(
        image: Image.Image
) -> Image.Image:
    """Flip image horizontally (left to right)."""

    return image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)


def transform_image(
        image: Image.Image,
        transformations: Dict[str, dict | str | int | bool]
) -> tuple[Image.Image, bool]:
    """Perform different transformation on the image object"""

    compress = False

    # Resize
    resize = transformations.get("resize")
    if resize:
        width = resize.get("width")
        height = resize.get("height")
        image = resize_image(image, width, height)

    # Crop
    crop = transformations.get("crop")
    if crop:
        left = float(crop.get("x"))
        upper = float(crop.get("y"))
        right = left + float(crop.get("width"))
        lower = upper + float(crop.get("height"))

        image = crop_image(image, left, upper, right, lower)

    # Rotate
    rotate = transformations.get("rotate")
    if rotate:
        degree = float(rotate)
        image = rotate_image(image, degree)

    # Filters
    filters = transformations.get("filters", {})
    if filters:
        image = filter_image(image, filters)


    # Watermark
    watermark = transformations.get("watermark")
    if watermark:
        image = apply_water_mask_to_image(image, watermark)

    # Mirror
    if transformations.get("mirror"):
        image = apply_mirror_to_image(image)

    # compress
    if transformations.get("compress"):
        # Apply compress to image
        compress = True

    # flip
    if transformations.get("flip"):
        image = flip_image(image)

    # Format
    fmt = transformations.get("format")
    if fmt:
        image = change_image_format(image, fmt)

    return image, compress


def delete_image_duplicate(old_path: str, new_path: str) -> None:
    """Delete old image if format change"""

    if old_path != new_path:
        path = Path(old_path)
        if path.exists():
            path.unlink() #delete the image located in old_path