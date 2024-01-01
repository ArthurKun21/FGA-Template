from pathlib import Path

from PIL import Image, ImageDraw
from rich.console import Console

console = Console()


def region(
    tmp_folder: Path,
    image_path: Path,
    left: int,
    top: int,
    right: int,
    bottom: int,
):
    console.print(f"Drawing region on image: [blue]{image_path}[/blue]")

    region_image_name = f"{image_path.stem}_region{image_path.suffix}"
    region_image_path = tmp_folder / region_image_name
    try:
        with Image.open(image_path) as img:
            im_width, im_height = img.size
            draw = ImageDraw.Draw(img)
            # Left
            draw.line((left, 0, left, im_height), fill="red", width=1)
            # Top
            draw.line((0, top, im_width, top), fill="red", width=1)
            # Right
            draw.line((right, 0, right, im_height), fill="red", width=1)
            # Bottom
            draw.line((0, bottom, im_width, bottom), fill="red", width=1)

            img.save(region_image_path, "PNG")
    except FileNotFoundError:
        console.print("[red]Image not found![/red]")
        return None


def location(
    tmp_folder: Path,
    image_path: Path,
    x: int,
    y: int,
):
    console.print(f"Drawing location on image: [blue]{image_path}[/blue]")
    
    location_image_name = f"{image_path.stem}_location{image_path.suffix}"
    location_image_path = tmp_folder / location_image_name
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            draw = ImageDraw.Draw(img)
            # X
            draw.line((x, 0, x, height), fill="red", width=1)
            # Y
            draw.line((0, y, width, y), fill="red", width=1)
            img.save(location_image_path, "PNG")
    except FileNotFoundError:
        console.print("[red]Image not found![/red]")
        return None


def run(
    **kwargs,
):
    pass
