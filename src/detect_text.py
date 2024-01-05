from math import floor
from pathlib import Path
from typing import Optional

import border_handler
import cv2
import directory_handler
import image_handler
import information_handler
import numpy as np
import pytesseract
from PIL import Image
from pytesseract import TesseractError, TesseractNotFoundError
from rich.console import Console

console = Console()

cwd = Path(__file__).cwd()

tessdata = cwd / "tessdata"

tessdata_dir_config = f'--tessdata-dir "{tessdata}"'


def detect_text(
    image_np: np.ndarray,
) -> Optional[str]:
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )

    try:
        text = pytesseract.image_to_string(image_np, config=tessdata_dir_config)
        return text
    except TesseractNotFoundError:
        console.print_exception()
        return None
    except TesseractError:
        console.print_exception()
        return None
    except Exception:
        console.print_exception()
        return None


def set_image_threshold(
    image_path: Path,
    threshold: float = 0.5,
) -> Optional[np.ndarray]:
    try:
        with Image.open(image_path) as image:
            input_image_np = np.array(image)

            threshold_int = floor(threshold * 255)

            _, threshold_image_np = cv2.threshold(
                input_image_np, threshold_int, 255, cv2.THRESH_BINARY
            )
            return threshold_image_np
    except FileNotFoundError:
        console.print_exception()
        return None


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
        image=image_path, function="detect_text"
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

    based_image_np = set_image_threshold(
        image_path=resized_template_path,
    )
    if based_image_np is None:
        resized_template_path.unlink(missing_ok=True)
        return

    text = detect_text(
        image_np=based_image_np,
    )

    if text is None:
        console.print("[red]Failed to detect text![/red]")
        directory_handler.cleanup(crop_image_path)
        return ""
    else:
        console.print(f"Detected text: [blue]{text}[/blue]")
        directory_handler.cleanup(crop_image_path)

        detected_image_path = (
            resized_template_path.parent
            / f"{resized_template_path.stem}_detect_text{resized_template_path.suffix}"
        )
        resized_template_path.rename(detected_image_path)

        info_path = information_handler.print_table_of_information_resize(
            reference_image_path=image_path,
            template_image_path=detected_image_path,
            left_border=left_border,
            top_border=top_border,
            right_border=right_border,
            bottom_border=bottom_border,
            draw_information=True,
        )

        text_name = detected_image_path.parent / "Detected text.txt"
        with open(text_name, "w") as f:
            f.write(text)

        return text
