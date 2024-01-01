"""
Create a template image from the original image given the borders from the original image of the would be template image.
"""
from rich.console import Console

from pathlib import Path
from typing import Optional
import directory_handler
import border_handler


console = Console()


def run(
    image_path: Path,
    left: Optional[int] = None,
    top: Optional[int] = None,
    right: Optional[int] = None,
    bottom: Optional[int] = None,
    **kwargs,
):
    console.print(f"Creating template from image: [blue]{image_path}[/blue]")
    tmp_folder = directory_handler.create_tmp_folder(image=image_path, function="create")

    left, top, right, bottom = border_handler.get_border(
        image_path=image_path,
        left=left,
        top=top,
        right=right,
        bottom=bottom,
    )