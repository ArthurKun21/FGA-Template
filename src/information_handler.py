import math
from pathlib import Path
from typing import Literal

import draw
import image_handler
import toml
from PIL import Image
from rich.console import Console
from rich.table import Table

from border_handler import MeasurementType

console = Console()

height_reference = 1_440
width_reference = 2_560


def get_border_information(
    reference_image_path: Path,
    left: int,
    top: int,
    right: int,
    bottom: int,
):
    try:
        with Image.open(reference_image_path) as img:
            width, height = img.size
    except FileNotFoundError:
        console.print("[red]Image not found![/red]")
        exit(0)

    reference_image_resize_height = height_reference
    reference_image_resize_width = math.floor(
        (width / height) * reference_image_resize_height
    )

    left_border = math.floor((left / width) * reference_image_resize_width)
    top_border = math.floor((top / height) * reference_image_resize_height)
    right_border = math.floor((right / width) * reference_image_resize_width)
    bottom_border = math.floor((bottom / height) * reference_image_resize_height)

    return (
        reference_image_resize_width,
        reference_image_resize_height,
        left_border,
        top_border,
        right_border,
        bottom_border,
    )


def get_border_information_from_resize(
    reference_image_path: Path,
    resize_left: int,
    resize_top: int,
    resize_right: int,
    resize_bottom: int,
):
    try:
        with Image.open(reference_image_path) as img:
            width, height = img.size
    except FileNotFoundError:
        console.print("[red]Image not found![/red]")
        exit(0)

    reference_image_resize_height = height_reference
    reference_image_resize_width = math.floor(
        (width / height) * reference_image_resize_height
    )

    left_border = math.floor((resize_left / reference_image_resize_width) * width)
    top_border = math.floor((resize_top / reference_image_resize_height) * height)
    right_border = math.floor((resize_right / reference_image_resize_width) * width)
    bottom_border = math.floor((resize_bottom / reference_image_resize_height) * height)

    return (
        reference_image_resize_width,
        reference_image_resize_height,
        left_border,
        top_border,
        right_border,
        bottom_border,
    )


def create_region(
    left_border: int,
    top_border: int,
    width_template: int,
    height_template: int,
    mode: Literal["normal", "center", "right"],
):
    match mode:
        case "normal":
            suffix = ""
        case "center":
            suffix = ".xFromCenter()"
        case "right":
            suffix = ".xFromRight()"
        case _:
            suffix = ""
    return f"Region({left_border}, {top_border}, {width_template}, {height_template}){suffix}"


def create_location(
    x: int,
    y: int,
    mode: Literal["normal", "center", "right"],
):
    match mode:
        case "normal":
            suffix = ""
        case "center":
            suffix = ".xFromCenter()"
        case "right":
            suffix = ".xFromRight()"
        case _:
            suffix = ""
    return f"Location({x}, {y}){suffix}"

def print_table_of_information_resize(
    reference_image_path: Path,
    template_image_path: Path,
    left: int,
    top: int,
    right: int,
    bottom: int,
    draw_information: bool = False,
):
    (
        left_border,
        top_border,
        right_border,
        bottom_border,
        width_template,
        height_template,
        left_border_from_center,
        left_border_from_right,
        template_center_x,
        template_center_y,
        template_center_x_from_center,
        template_center_x_from_right,
    ) = fetch_image_manipulation_information(
        reference_image_path, left, top, right, bottom
    )

    table_size = Table(show_header=False, show_lines=True)
    table_size.add_row("Width", f"{width_template}")
    table_size.add_row("Height", f"{height_template}")

    console.print(table_size)

    table_region = Table(title="Region", title_justify="center", show_lines=True)
    table_region.add_column("Transformations", justify="center")
    table_region.add_column("Area", justify="center")

    region_normal = create_region(
        left_border, top_border, width_template, height_template, "normal"
    )
    region_from_center = create_region(
        left_border_from_center, top_border, width_template, height_template, "center"
    )
    region_from_right = create_region(
        left_border_from_right, top_border, width_template, height_template, "right"
    )

    table_region.add_row("Normal", region_normal)
    table_region.add_row("From Center", region_from_center)
    table_region.add_row("From Right", region_from_right)

    console.print(table_region)

    table_location = Table(title="Location", title_justify="center", show_lines=True)
    table_location.add_column("Transformations", justify="center")
    table_location.add_column("Location", justify="center")

    location_normal = create_location(template_center_x, template_center_y, "normal")
    location_from_center = create_location(
        template_center_x_from_center, template_center_y, "center"
    )
    location_from_right = create_location(
        template_center_x_from_right, template_center_y, "right"
    )

    table_location.add_row("Normal", location_normal)
    table_location.add_row("From Center", location_from_center)
    table_location.add_row("From Right", location_from_right)

    console.print(table_location)

    information_path = save_the_information(
        reference_image_path=reference_image_path,
        template_image_path=template_image_path,
        region_normal=region_normal,
        region_from_center=region_from_center,
        region_from_right=region_from_right,
        location_normal=location_normal,
        location_from_center=location_from_center,
        location_from_right=location_from_right,
        left=left,
        top=top,
        right=right,
        bottom=bottom,
        resized_left=left_border,
        resized_top=top_border,
        resized_right=right_border,
        resized_bottom=bottom_border,
    )

    if draw_information:
        draw.region(
            tmp_folder=template_image_path.parent,
            image_path=reference_image_path,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
        )

        template_center_x_orig = left + math.floor((right - left) / 2)
        template_center_y_orig = top + math.floor((bottom - top) / 2)

        draw.location(
            tmp_folder=template_image_path.parent,
            image_path=reference_image_path,
            x=template_center_x_orig,
            y=template_center_y_orig,
        )

    return information_path

def print_table_of_information(
    reference_image_path: Path,
    template_image_path: Path,
    left: int,
    top: int,
    right: int,
    bottom: int,
    draw_information: bool = False,
):
    (
        left_border,
        top_border,
        right_border,
        bottom_border,
        width_template,
        height_template,
        left_border_from_center,
        left_border_from_right,
        template_center_x,
        template_center_y,
        template_center_x_from_center,
        template_center_x_from_right,
    ) = fetch_image_manipulation_information(
        reference_image_path, left, top, right, bottom
    )

    table_size = Table(show_header=False, show_lines=True)
    table_size.add_row("Width", f"{width_template}")
    table_size.add_row("Height", f"{height_template}")

    console.print(table_size)

    table_region = Table(title="Region", title_justify="center", show_lines=True)
    table_region.add_column("Transformations", justify="center")
    table_region.add_column("Area", justify="center")

    region_normal = create_region(
        left_border, top_border, width_template, height_template, "normal"
    )
    region_from_center = create_region(
        left_border_from_center, top_border, width_template, height_template, "center"
    )
    region_from_right = create_region(
        left_border_from_right, top_border, width_template, height_template, "right"
    )

    table_region.add_row("Normal", region_normal)
    table_region.add_row("From Center", region_from_center)
    table_region.add_row("From Right", region_from_right)

    console.print(table_region)

    table_location = Table(title="Location", title_justify="center", show_lines=True)
    table_location.add_column("Transformations", justify="center")
    table_location.add_column("Location", justify="center")

    location_normal = create_location(template_center_x, template_center_y, "normal")
    location_from_center = create_location(
        template_center_x_from_center, template_center_y, "center"
    )
    location_from_right = create_location(
        template_center_x_from_right, template_center_y, "right"
    )

    table_location.add_row("Normal", location_normal)
    table_location.add_row("From Center", location_from_center)
    table_location.add_row("From Right", location_from_right)

    console.print(table_location)

    information_path = save_the_information(
        reference_image_path=reference_image_path,
        template_image_path=template_image_path,
        region_normal=region_normal,
        region_from_center=region_from_center,
        region_from_right=region_from_right,
        location_normal=location_normal,
        location_from_center=location_from_center,
        location_from_right=location_from_right,
        left=left,
        top=top,
        right=right,
        bottom=bottom,
        resized_left=left_border,
        resized_top=top_border,
        resized_right=right_border,
        resized_bottom=bottom_border,
    )

    if draw_information:
        draw.region(
            tmp_folder=template_image_path.parent,
            image_path=reference_image_path,
            left=left_border,
            top=top_border,
            right=right_border,
            bottom=bottom_border,
        )

        draw.location(
            tmp_folder=template_image_path.parent,
            image_path=reference_image_path,
            x=template_center_x,
            y=template_center_y,
        )

    return information_path


def fetch_image_manipulation_information_reverse(
    reference_image_path: Path,
    left: int,
    top: int,
    width: int,
    height: int,
    selected_measurement_type: str,
):
    if selected_measurement_type in MeasurementType.__members__:  # type: ignore
        measurement_type = MeasurementType[selected_measurement_type]
    else:
        measurement_type = MeasurementType.NORMAL

    match measurement_type:
        case MeasurementType.NORMAL:
            left = left
        case MeasurementType.CENTER:
            left = math.floor(width_reference / 2) + left
        case MeasurementType.RIGHT:
            left = width_reference + left
        case _:
            left = left

    return left, top, left + width, top + height, width, height


def fetch_image_manipulation_information(
    reference_image_path:Path,
    left: int,
    top: int,
    right: int,
    bottom: int
):
    (
        resize_width,
        _,
        left_border,
        top_border,
        right_border,
        bottom_border,
    ) = get_border_information(
        reference_image_path=reference_image_path,
        left=left,
        top=top,
        right=right,
        bottom=bottom,
    )
    width_template = right_border - left_border
    height_template = bottom_border - top_border

    left_border_from_center = left_border - math.floor(resize_width / 2)
    left_border_from_right = left_border - resize_width

    template_center_x = left_border + math.floor(width_template / 2)
    template_center_y = top_border + math.floor(height_template / 2)

    template_center_x_from_center = template_center_x - math.floor(resize_width / 2)
    template_center_x_from_right = template_center_x - resize_width
    return (
        left_border,
        top_border,
        right_border,
        bottom_border,
        width_template,
        height_template,
        left_border_from_center,
        left_border_from_right,
        template_center_x,
        template_center_y,
        template_center_x_from_center,
        template_center_x_from_right,
    )


def save_the_information(
    reference_image_path: Path,
    template_image_path: Path,
    region_normal: str,
    region_from_center: str,
    region_from_right: str,
    location_normal: str,
    location_from_center: str,
    location_from_right: str,
    left: int,
    top: int,
    right: int,
    bottom: int,
    resized_left: int,
    resized_top: int,
    resized_right: int,
    resized_bottom: int,
):
    width, height = image_handler.get_size(image_path=reference_image_path)
    information_dict = {
        "Name": reference_image_path.stem,
        "Template": template_image_path.name,
        "Region": {
            "Normal": region_normal,
            "From Center": region_from_center,
            "From Right": region_from_right,
        },
        "Location": {
            "Normal": location_normal,
            "From Center": location_from_center,
            "From Right": location_from_right,
        },
        "Border": {
            "Left": left,
            "Right": right,
            "Top": top,
            "Bottom": bottom,
        },
        "Resized Border": {
            "Left": resized_left,
            "Right": resized_right,
            "Top": resized_top,
            "Bottom": resized_bottom,
        },
        "Original Image Size": {
            "Width": width,
            "Height": height,
        },
        "Template Image Size": {
            "Width": resized_right - resized_left,
            "Height": resized_bottom - resized_top,
        },
    }
    information_name = f"{reference_image_path.stem}_information.toml"
    information_path = template_image_path.parent / information_name
    try:
        with open(information_path, "w", encoding="utf-8") as file:
            toml.dump(information_dict, file)

        return information_path
    except FileNotFoundError:
        console.print("[bold red]ERROR:[/bold red] File not found.")
