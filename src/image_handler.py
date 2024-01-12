from PIL import Image
from pathlib import Path
from typing import Optional
from rich.console import Console

console = Console()

height_reference = 1_440
width_reference = 2_560


def crop_image(
    image_path: Path,
    tmp_folder: Path,
    left: int,
    top: int,
    right: int,
    bottom: int,
) -> Optional[Path]:
    try:
        crop_image_path_name = f"{image_path.stem}_crop.png"
        crop_image_path = tmp_folder / crop_image_path_name
        with Image.open(image_path) as img:
            img = img.crop((left, top, right, bottom))
            img.save(crop_image_path, "PNG")
        return crop_image_path
    except FileNotFoundError:
        console.print("[red]Image not found![/red]")
        return None


def resize_template_to_reference(
    original_image_path: Path,
    template_path: Path,
    tmp_folder: Path,
) -> Optional[Path]:
    try:
        resize_image_path_name = (
            f"{original_image_path.stem}_resize.png"
        )
        resize_image_path = tmp_folder / resize_image_path_name
        with Image.open(original_image_path) as img:
            width_original, height_original = img.size

            height_original_resize = height_reference
            width_original_resize = int(
                (width_original / height_original) * height_original_resize
            )


            with Image.open(template_path) as template:
                template_width, template_height = template.size

                # Fetch the size of the template and then
                # resize it to 1440p
                # afterwards, divided by 2 because of FGA
                # needs 720p for Image matching
                template_resize_height = (
                    (template_height * height_original_resize) / height_original
                ) / 2
                template_resize_width = (
                    (template_width * width_original_resize) / width_original
                ) / 2


                template_img = template.resize(
                    (int(template_resize_width), int(template_resize_height)),
                    Image.Resampling.LANCZOS,
                )
                template_img.save(resize_image_path, "PNG")
        return resize_image_path
    except FileNotFoundError:
        console.print("[red]Image not found![/red]")
        return None

def get_size(
        image_path: Path,
):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
    except FileNotFoundError:
        console.print("[red]Image not found![/red]")
        exit(0)
    return width, height