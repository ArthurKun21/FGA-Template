"""
Create a template image from the original image given the borders from the original image of the would be template image.
"""
from rich.console import Console

from pathlib import Path
from typing import Optional
import directory_handler
import border_handler
import image_handler


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

    left_border, top_border, right_border, bottom_border = border_handler.get_border(
        image_path=image_path,
        left=left,
        top=top,
        right=right,
        bottom=bottom,
    )

    crop_image_path = image_handler.crop_image(
        image_path=image_path,
        tmp_folder=tmp_folder,
        left=left_border,
        top=top_border,
        right=right_border,
        bottom=bottom_border,
    )
    if crop_image_path is None:
        console.print("[red]Failed to create template![/red]")
        return

    resized_template_path = image_handler.resize_template_to_reference(
        original_image_path=image_path,
        template_path=crop_image_path,
        tmp_folder=tmp_folder,
    )
    if resized_template_path is None:
        console.print("[red]Failed to create template![/red]")
        crop_image_path.unlink(missing_ok=True)
        return
