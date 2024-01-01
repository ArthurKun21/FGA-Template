from pathlib import Path
from typing import Literal
from datetime import datetime
from rich.console import Console

console = Console()


def create_tmp_folder(
    image: Path,
    function: Literal["create", "match", "draw", "reverse"],
) -> Path:
    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    try:
        folder_name = f"{function}_v{image.stem}_{current_datetime}"
        tmp_folder = image.parent / "tmp" / folder_name
        tmp_folder.mkdir(exist_ok=True, parents=True)
    except FileNotFoundError:
        folder_name = f"{function}_v{current_datetime}"
        tmp_folder = image.parent / "tmp" / folder_name
        tmp_folder.mkdir(exist_ok=True, parents=True)

    console.print(f"Created temporary folder: [blue]{tmp_folder}[/blue]")
    return tmp_folder
