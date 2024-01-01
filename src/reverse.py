from pathlib import Path
from typing import Optional

import border_handler
import directory_handler
import image_handler
import information_handler
from rich.console import Console

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
    tmp_folder = directory_handler.create_tmp_folder(
        image=image_path, function="reverse"
    )

    left_border, top_border, right_border, bottom_border = border_handler.get_border(
        image_path=image_path,
        left=left,
        top=top,
        right=right,
        bottom=bottom,
    )

    (
        _,
        _,
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

    crop_image_path = image_handler.crop_image(
        image_path=image_path,
        tmp_folder=tmp_folder,
        left=orig_left,
        top=orig_top,
        right=orig_right,
        bottom=orig_bottom,
    )

    if crop_image_path is None:
        console.print("[red]Failed to create template![/red]")
        directory_handler.cleanup(tmp_folder)
        return

    resized_template_path = image_handler.resize_template_to_reference(
        original_image_path=image_path,
        template_path=crop_image_path,
        tmp_folder=tmp_folder,
    )

    if resized_template_path is None:
        console.print("[red]Failed to create template![/red]")
        directory_handler.cleanup(tmp_folder, crop_image_path)
        return

    information_handler.print_table_of_information(
        reference_image_path=image_path,
        template_image_path=resized_template_path,
        left=orig_left,
        top=orig_top,
        right=orig_right,
        bottom=orig_bottom,
        draw_information=True,
    )

    # Perform cleanup
    directory_handler.cleanup(crop_image_path)
