from enum import StrEnum, auto
import math
from pathlib import Path
from typing import Optional

from PIL import Image
from rich.console import Console
from rich.prompt import IntPrompt

console = Console()


class MeasurementType(StrEnum):
    NORMAL = auto()
    CENTER = auto()
    RIGHT = auto()


height_reference = 1_440
width_reference = 2_560


def get_border_from_resize(
    left: Optional[int] = None,
    top: Optional[int] = None,
    template_width: Optional[int] = None,
    template_height: Optional[int] = None,
    measurement_type: MeasurementType = MeasurementType.NORMAL,
) -> tuple[int, int, int, int]:
    if (
        left is not None
        and top is not None
        and template_width is not None
        and template_height is not None
    ):
        return left, top, template_width + left, template_height + top

    left_input = left
    top_input = top
    width_input = template_width
    height_input = template_height

    match measurement_type:
        case MeasurementType.NORMAL:
            width_int_range_hint = f"0 ~ {width_reference}"
            width_int_range = range(0, width_reference)
        case MeasurementType.FROM_CENTER:
            half_size = math.floor(width_reference /2)
            width_int_range_hint = f"{-half_size} ~ {half_size}"
            width_int_range = range(-half_size, half_size)
        case MeasurementType.FROM_RIGHT:
            width_int_range_hint = f"0 ~ {width_reference}"
            width_int_range = range(-width_reference, 0)

    while left_input is None:
        left_input = IntPrompt.ask(
            prompt=f"How many pixels is the left border? [yellow]( {width_int_range_hint} )[/yellow]",
            show_choices=False,
            choices=[f"{x}" for x in width_int_range],
        )

    while top_input is None:
        top_input = IntPrompt.ask(
            prompt=f"How many pixels is the top border? [green]( 0 ~ {height_reference} )[/green]",
            show_choices=False,
            choices=[f"{x}" for x in range(0, height_reference)],
        )

    while width_input is None:
        width_input = IntPrompt.ask(
            prompt=f"How many pixels is the width of the template? [red]( 0 ~ {width_reference} )[/red]",
            show_choices=False,
            choices=[f"{x}" for x in range(1, width_reference)],
        )

    while height_input is None:
        height_input = IntPrompt.ask(
            prompt=f"How many pixels is the height of the template? [blue]( 1 ~ {height_reference} )[/blue]",
            show_choices=False,
            choices=[f"{x}" for x in range(1, height_reference)],
        )

    match measurement_type:
        case MeasurementType.NORMAL:
            left_input = left_input
        case MeasurementType.FROM_CENTER:
            left_input = math.floor(width_reference / 2) + left_input
        case MeasurementType.FROM_RIGHT:
            left_input = width_reference + left_input
        case _:
            left_input = left_input

    right_input = left_input + width_input
    bottom_input = top_input + height_input


    return left_input, top_input, right_input, bottom_input




def get_border(
    image_path: Path,
    left: Optional[int] = None,
    top: Optional[int] = None,
    right: Optional[int] = None,
    bottom: Optional[int] = None,
):
    if (
        left is not None
        and right is not None
        and top is not None
        and bottom is not None
    ):
        return left, top, right, bottom

    with Image.open(image_path) as img:
        width, height = img.size

    left_border = 0 if left is None else left
    top_border = 0 if top is None else top
    right_border = 0 if right is None else right
    bottom_border = 0 if bottom is None else bottom

    while True:
        if left_border != right_border and (right_border - left_border) > 1:
            break
        left_border = IntPrompt.ask(
            prompt=f"How many pixels is the left border? [yellow]( 0 ~ {width} )[/yellow]",
            show_choices=False,
            choices=[f"{x}" for x in range(0, width)],
        )
        right_border = IntPrompt.ask(
            prompt=f"How many pixels is the right border? [red]( {left_border} ~ {width} )[/red]",
            show_choices=False,
            choices=[f"{x}" for x in range(left_border, width)],
        )
        if left_border == right_border or (right_border - left_border) <= 1:
            console.print("[red]Invalid input![/red]")
            continue

    while True:
        if top_border != bottom_border and (bottom_border - top_border) > 1:
            break
        top_border = IntPrompt.ask(
            prompt=f"How many pixels is the top border? [green]( 0 ~ {height} )[/green]",
            show_choices=False,
            choices=[f"{x}" for x in range(0, height)],
        )
        bottom_border = IntPrompt.ask(
            prompt=f"How many pixels is the bottom border? [blue]( {top_border} ~ {height} )[/blue]",
            show_choices=False,
            choices=[f"{x}" for x in range(top_border, height)],
        )
        if top_border == bottom_border or (bottom_border - top_border) <= 1:
            console.print("[red]Invalid input![/red]")
            continue

    return left_border, top_border, right_border, bottom_border
