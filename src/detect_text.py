from math import floor
from pathlib import Path
from typing import Optional

import border_handler
import cv2
import directory_handler
import image_handler
import information_handler
import numpy as np
from PIL import Image
from rich.console import Console

console = Console()


def set_image_threshold(
    image_path: Path,
    threshold: float = 0.5,
):
    with Image.open(image_path) as image:
        input_image_np = np.array(image)

        # input_image_np_gray = cv2.cvtColor(input_image_np, cv2.COLOR_RGB2GRAY)
        threshold_int = floor(threshold * 255)

        _, threshold_image_np = cv2.threshold(
            input_image_np, threshold_int, 255, cv2.THRESH_BINARY
        )


def run(
    image_path: Path,
    extra: str,
    left: Optional[int] = None,
    top: Optional[int] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    **kwargs,
):
    console.print(f"Creating template from image: [blue]{image_path}[/blue]")
    tmp_folder = directory_handler.create_tmp_folder(
        image=image_path, function="reverse"
    )
    if extra in border_handler.MeasurementType.__members__:  # type: ignore
        measurement_type = border_handler.MeasurementType[extra]
    else:
        measurement_type = border_handler.MeasurementType.NORMAL

    (
        left_border,
        top_border,
        right_border,
        bottom_border,
    ) = border_handler.get_border_from_resize(
        image_path=image_path,
        left=left,
        top=top,
        template_height=height,
        template_width=width,
        measurement_type=measurement_type,
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
