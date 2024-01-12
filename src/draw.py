from pathlib import Path
from typing import Optional

import border_handler
import directory_handler
import information_handler
from PIL import Image, ImageDraw
from rich.console import Console
from rich.prompt import Prompt

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

    region_image_name = f"{image_path.stem}_region.png"
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

    location_image_name = f"{image_path.stem}_location.png"
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
    image_path: Path,
    left: Optional[int] = None,
    top: Optional[int] = None,
    right: Optional[int] = None,
    bottom: Optional[int] = None,
    operations: Optional[str] = None,
    **kwargs,
):
    console.print(f"Creating Draw from image: [blue]{image_path}[/blue]")
    tmp_folder = directory_handler.create_tmp_folder(image=image_path, function="draw")

    left_border, top_border, right_border, bottom_border = border_handler.get_border(
        image_path=image_path,
        left=left,
        top=top,
        right=right,
        bottom=bottom,
    )
    operation_choices = ["normal", "reversed"]

    if operations is None or operations not in operation_choices:
        mode_of_operations = Prompt.ask(
            prompt="Normal or Reversed",
            choices=operation_choices,
            default="normal",
            show_default=True,
        )
        operations = mode_of_operations

    if operations == "normal":
        region(
            tmp_folder=tmp_folder,
            image_path=image_path,
            left=left_border,
            top=top_border,
            right=right_border,
            bottom=bottom_border,
        )
        location(
            tmp_folder=tmp_folder,
            image_path=image_path,
            x=left_border,
            y=top_border,
        )
    else:
        (
            resized_width,
            resized_height,
            orig_left,
            orig_top,
            orig_right,
            orig_bottom,
        ) = information_handler.get_border_information_from_resize(
            reference_image_path=image_path,
            resize_left=left_border,
            resize_top=top_border,
            resize_right=right_border,
            resize_bottom=bottom_border,
        )

        location_x = int(resized_width / 2) + orig_left
        location_y = int(resized_height / 2) + orig_top

        region(
            tmp_folder=tmp_folder,
            image_path=image_path,
            left=orig_left,
            top=orig_top,
            right=orig_right,
            bottom=orig_bottom,
        )
        location(
            tmp_folder=tmp_folder,
            image_path=image_path,
            x=location_x,
            y=location_y,
        )
