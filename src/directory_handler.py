from pathlib import Path
from typing import Literal
from datetime import datetime
from rich.console import Console
import shutil

console = Console()


def create_tmp_folder(
    image: Path,
    function: Literal["create", "match", "draw", "reverse"],
) -> Path:
    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    try:
        folder_name = f"{function}_{image.stem}_v{current_datetime}"
        tmp_folder = image.parent / "tmp" / folder_name
        tmp_folder.mkdir(exist_ok=True, parents=True)
    except FileNotFoundError:
        folder_name = f"{function}_v{current_datetime}"
        tmp_folder = image.parent / "tmp" / folder_name
        tmp_folder.mkdir(exist_ok=True, parents=True)

    console.print(f"Created temporary folder: [blue]{tmp_folder}[/blue]")
    return tmp_folder

def cleanup(
        *args
):
    console.print("Cleaning up...")
    for arg in args:
        if isinstance(arg, Path):
            if arg.is_dir():
                try:
                    shutil.rmtree(arg)
                    console.print(f"Removed directory: [blue]{arg}[/blue]")
                except FileNotFoundError:
                    console.print(f"Failed to remove directory: [red]{arg}[/red]")
            elif arg.is_file():
                try:
                    arg.unlink(missing_ok=True)
                    console.print(f"Removed file: [blue]{arg}[/blue]")
                except FileNotFoundError:
                    console.print(f"Failed to remove file: [red]{arg}[/red]")