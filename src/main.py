import sys
from pathlib import Path
from typing import Optional

import click
import create
import draw
import match
import reverse
from click.exceptions import Abort, BadParameter, Exit, FileError, NoSuchOption
from rich.console import Console
from rich.table import Table
from rich.prompt import IntPrompt

debug_mode = (
    False if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS") else True
)
console = Console()

cwd = Path(__file__).cwd() if debug_mode else Path.cwd()

console = Console()

image_extensions = [".png", ".jpg"]


task_list = [create, match, draw, reverse]


def get_image() -> Optional[Path]:
    image_files = [
        x for x in cwd.iterdir() if x.is_file() and x.suffix in image_extensions
    ]
    if len(image_files) > 1:
        images_table = Table(show_lines=True)
        images_table.add_column("Index", justify="center")
        images_table.add_column("Image name", justify="left")
        for index, x in enumerate(image_files):
            images_table.add_row(f"{index + 1}", f"{x.name}")
        console.print(images_table)
        index_to_process = IntPrompt.ask(
            prompt="Which of the following screenshot would be processed? "
            "Enter the Index number",
            choices=[f"{x}" for x in range(1, len(image_files) + 1)],
            show_choices=False,
        )
        chosen_image = image_files[index_to_process - 1]
    elif len(image_files) == 1:
        chosen_image = image_files[0]
    else:
        console.print("[red]There are no images found.")
        return None

    return chosen_image


@click.command()
@click.option(
    "--task",
    default=None,
    help="Select which task to use",
    type=click.Choice(
        case_sensitive=False, choices=[x.__name__.upper() for x in task_list]
    ),
    required=False,
)
@click.option(
    "--image",
    "-i",
    required=False,
    default=None,
    type=click.Path(exists=True, path_type=Path),
    help="This is the image to be processed",
)
@click.option(
    "--template",
    required=False,
    default=None,
    type=click.Path(exists=True, path_type=Path),
    help="This is the image to be processed with the image",
)
@click.option(
    "--left",
    required=False,
    default=None,
    type=int,
    help="Left Border",
)
@click.option(
    "--right",
    required=False,
    default=None,
    type=int,
    help="Right",
)
@click.option(
    "--top",
    required=False,
    default=None,
    type=int,
    help="Top Border",
)
@click.option(
    "--bottom",
    required=False,
    default=None,
    type=int,
    help="Bottom Border",
)
@click.option(
    "--height",
    required=False,
    default=None,
    type=int,
    help="Height of the template",
)
@click.option(
    "--width",
    required=False,
    default=None,
    type=int,
    help="Width of the template",
)
def main(
    task: Optional[str],
    image: Optional[Path],
    template: Optional[Path],
    left: Optional[int],
    right: Optional[int],
    top: Optional[int],
    bottom: Optional[int],
    height: Optional[int],
    width: Optional[int],
):
    console.print(f"Current Working Directory:\t[yellow]{cwd}")

    if image is None:
        image = get_image()
        if image is None:
            console.print("[red]No image found![/red]")
            return

    if task is None:
        table_task = Table(title="Tasks", title_justify="center", show_lines=True)
        table_task.add_column("Index", justify="center")
        table_task.add_column("Task", justify="center")

        for index, task_name in enumerate(task_list):
            table_task.add_row(
                f"{index+1}",
                f"[yellow]{task_name.__name__.upper()}[/yellow]",
            )

        console.print(table_task)

        prompt_task = IntPrompt.ask(
            "Select a task",
            choices=[f"{x}" for x in range(1, len(task_list) + 1)],
        )
        task_to_perform = task_list[prompt_task - 1]
    else:
        check_list = [x for x in task_list if x.__name__.lower() == task.lower()]
        if len(check_list) == 0:
            console.print(f"[bold red]Task {task} not found![/bold red]")
            return
        task_to_perform = check_list[0]

    if hasattr(task_to_perform, "run"):
        task_to_perform.run(
            image=image,
            template=template,
            left=left,
            right=right,
            top=top,
            bottom=bottom,
            height=height,
            width=width,
        )


if __name__ == "__main__":
    try:
        main()
    except Abort:
        console.print_exception()
    except BadParameter:
        console.print_exception()
    except FileError:
        console.print_exception()
    except Exit:
        console.print_exception()
    except NoSuchOption:
        console.print_exception()
    except KeyboardInterrupt:
        console.print("\n[bold red]Program stopped![/bold red]")
        exit(0)
