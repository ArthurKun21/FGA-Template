from rich.console import Console
from rich.table import Table

import toml

console = Console()


def print_table_of_information():
    width_template = 0
    height_template = 0

    table_size = Table(show_header=False, show_lines=True)
    table_size.add_row("Width", width_template)
    table_size.add_row("Height", height_template)

    console.print(table_size)

    table_region = Table(title="Region", title_justify="center", show_lines=True)
    table_region.add_column("Transformations", justify="center")
    table_region.add_column("Area", justify="center")

    # ADD THE CALCULATIONS HERE

    region_normal = ""
    region_from_center = ""
    region_from_right = ""

    table_region.add_row("Normal", region_normal)
    table_region.add_row("From Center", region_from_center)
    table_region.add_row("From Right", region_from_right)

    console.print(table_region)

    table_location = Table(title="Location", title_justify="center", show_lines=True)
    table_location.add_column("Transformations", justify="center")
    table_location.add_column("Location", justify="center")

    # ADD THE CALCULATIONS HERE

    location_normal = ""
    location_from_center = ""
    location_from_right = ""

    table_location.add_row("Normal", location_normal)
    table_location.add_row("From Center", location_from_center)
    table_location.add_row("From Right", location_from_right)

    console.print(table_location)


def save_the_information():
    information_dict = {
        "Name": "name",
        "Region": {
            "Normal": "",
            "From Center": "",
            "From Right": "",
        },
        "Location": {
            "Normal": "",
            "From Center": "",
            "From Right": "",
        },
        "Border": {
            "Left": 0,
            "Right": 0,
            "Top": 0,
            "Bottom": 0,
        },
        "Resized Border": {
            "Left": 0,
            "Right": 0,
            "Top": 0,
            "Bottom": 0,
        },
        "Original Image Size": {
            "Width": "",
            "Height": "",
        },
        "Template Image Size": {
            "Width": "",
            "Height": "",
        },
    }

    try:
        with open("information.toml", "w", encoding="utf-8") as file:
            toml.dump(information_dict, file)
    except FileNotFoundError:
        console.print("[bold red]ERROR:[/bold red] File not found.")
