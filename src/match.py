import shutil
from pathlib import Path
from typing import Optional, Tuple

import border_handler
import cv2
import directory_handler
import image_handler
import information_handler
import numpy as np
from PIL import Image
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

console = Console()


def prepare_based_image(
    image_path: Path,
    tmp_folder: Path,
    left_border: int,
    top_border: int,
    right_border: int,
    bottom_border: int,
) -> Tuple[Optional[Path], Optional[int], Optional[int], Optional[int], Optional[int]]:
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
        return None, None, None, None, None

    resized_template_path = image_handler.resize_template_to_reference(
        original_image_path=image_path,
        template_path=crop_image_path,
        tmp_folder=tmp_folder,
    )

    crop_image_path.unlink(missing_ok=True)
    if resized_template_path is not None:
        renamed_file = (
            resized_template_path.parent
            / f"{image_path.stem}_template_left_{left_border}_"
            f"top_{top_border}_right_{right_border}_bottom_{bottom_border}.png"
        )
        resized_template_path.rename(renamed_file)
        resized_template_path = renamed_file

    return resized_template_path, orig_left, orig_top, orig_right, orig_bottom


def load_based_image(
    image_path: Path,
) -> Image.Image:
    return Image.open(image_path)


def match_images(
    template: np.ndarray,
    input_image: Image.Image,
) -> float:
    # Convert image to np.array
    input_image_np = np.array(input_image)

    # Convert it to grayscale
    input_image_np_gray = cv2.cvtColor(input_image_np, cv2.COLOR_RGB2GRAY)

    result = cv2.matchTemplate(
        image=input_image_np_gray, templ=template, method=cv2.TM_CCOEFF_NORMED
    )
    _, max_val, _, _ = cv2.minMaxLoc(result)

    return max_val


def run(
    image_path: Path,
    template_path: Path,
    extra: str,
    retry: int,
    left: Optional[int] = None,
    top: Optional[int] = None,
    height: Optional[int] = None,
    width: Optional[int] = None,
    **kwargs,
):
    console.print(f"Creating template from image: [blue]{image_path}[/blue]")
    tmp_folder = directory_handler.create_tmp_folder(image=image_path, function="match")
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
        left=left,
        top=top,
        template_height=height,
        template_width=width,
        measurement_type=measurement_type,
    )

    template_image_read = cv2.imread(f"{template_path}", cv2.IMREAD_GRAYSCALE)

    highest_image_score = 0.0
    highest_image_score_path = None
    left_border_highest = 0
    top_border_highest = 0
    right_border_highest = 0
    bottom_border_highest = 0

    tmp_matching_folder = tmp_folder / "matching"
    tmp_matching_folder.mkdir(exist_ok=True, parents=True)

    with Progress() as progress:
        x_ranges_task = progress.add_task("[green]X Ranges...", total=retry * 2)
        y_ranges_task = progress.add_task(
            "[blue]Y Ranges...", total=(retry * 2) * (retry * 2)
        )

        for x in range(-retry, retry + 1):
            for y in range(-retry, retry + 1):
                if left_border + x < 0 or top_border + y < 0:
                    progress.advance(y_ranges_task)
                    progress.console.print(
                        f"Skipping {left_border + x}, {top_border + y} because it is out of bounds!"
                    )
                    continue
                (
                    based_image_path,
                    orig_left,
                    orig_top,
                    orig_right,
                    orig_bottom,
                ) = prepare_based_image(
                    image_path=image_path,
                    tmp_folder=tmp_matching_folder,
                    left_border=left_border + x,
                    top_border=top_border + y,
                    right_border=right_border + x,
                    bottom_border=bottom_border + y,
                )
                if based_image_path is None:
                    continue

                based_image = load_based_image(
                    image_path=based_image_path,
                )

                score = match_images(
                    template=template_image_read,
                    input_image=based_image,
                )
                if score > 0.8:
                    progress.console.print(
                        f"Score: [green]{score:.6}[/green]\t"
                        f"Left: [blue]{left_border + x}[/blue]\t"
                        f"Top: [blue]{top_border + y}[/blue]\t"
                        f"Right: [blue]{right_border + x}[/blue]\t"
                        f"Bottom: [blue]{bottom_border + y}[/blue]\t"
                    )
                    if score > highest_image_score:
                        highest_image_score_path = based_image_path
                        highest_image_score = score
                        left_border_highest = left_border + x
                        top_border_highest = top_border + y
                        right_border_highest = right_border + x
                        bottom_border_highest = bottom_border + y
                else:
                    progress.console.print(f"Score: [red]{score:.6f}[/red]\t")
                    based_image_path.unlink(missing_ok=True)
                progress.advance(y_ranges_task)
            progress.advance(x_ranges_task)

    if highest_image_score > 0:
        table = Table(title="Best Match", title_justify="center", show_lines=True)
        table.add_column("Left", justify="center")
        table.add_column("Top", justify="center")
        table.add_column("Right", justify="center")
        table.add_column("Bottom", justify="center")

        table.add_row(
            f"{left_border_highest}",
            f"{top_border_highest}",
            f"{right_border_highest}",
            f"{bottom_border_highest}",
        )

        console.print(table)
        if highest_image_score_path is not None:
            highest_path = tmp_folder / highest_image_score_path.name
            highest_image_score_path.rename(highest_path)

            highest_image_score_path = highest_path
            console.print(
                f"Path {highest_image_score_path.name} with score {highest_image_score:.6f}"
            )

            template_saved_path = (
                tmp_folder
                / f"{highest_image_score_path.stem}_template_{template_path.stem}{template_path.suffix}"
            )
            shutil.copy(template_path, template_saved_path)

            info_path = information_handler.print_table_of_information_resize(
                reference_image_path=image_path,
                template_image_path=highest_image_score_path,
                left_border=left_border_highest,
                top_border=top_border_highest,
                right_border=right_border_highest,
                bottom_border=bottom_border_highest,
                draw_information=True,
            )
    else:
        console.print(
            f"The highest found is [red]{highest_image_score:.6f}[/red] with borders: "
            f"left: {left_border_highest}, top: {top_border_highest}, "
            f"right: {right_border_highest}, bottom: {bottom_border_highest}"
        )
