from pathlib import Path
from typing import Optional

from PIL import Image
from rich.console import Console
from rich.prompt import IntPrompt

console = Console()


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
