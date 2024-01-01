"""
Create a template image from the original image given the borders from the original image of the would be template image.
"""
from rich.console import Console

from pathlib import Path
from typing import Optional
import directory_handler

console = Console()


def run(
    image: Path,
    left: Optional[int] = None,
    top: Optional[int] = None,
    right: Optional[int] = None,
    bottom: Optional[int] = None,
    **kwargs,
):
    console.print(f"Creating template from image: [blue]{image}[/blue]")
    tmp_folder = directory_handler.create_tmp_folder(image=image, function="create")
