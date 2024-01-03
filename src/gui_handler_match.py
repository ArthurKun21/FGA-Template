import os
import textwrap
from pathlib import Path

import match
import PySimpleGUI as sg
from gui_components import (
    create_directory_column,
    create_information_layout,
    create_operations_layout,
    load_directory_images_column,
    load_image_size_information,
    load_image_window,
    load_images_from_directory,
    text_input_validation,
)
from rich.console import Console

console = Console()


def match_values_column():
    values_column = sg.Col(
        [
            [
                sg.Text(
                    "Left",
                    tooltip="Left value of the template",
                ),
                sg.Push(),
                text_input_validation(
                    inputKey="LeftMatch",
                    default_text="0",
                    expand_x=False,
                    size=(25, 1),
                    justification="center",
                ),
                sg.Push(),
                sg.Text(
                    "Top",
                    tooltip="Top value of the template",
                ),
                text_input_validation(
                    inputKey="TopMatch",
                    default_text="0",
                    expand_x=False,
                    size=(25, 1),
                    justification="center",
                ),
            ],
            [
                sg.Text(
                    "Width",
                    tooltip="Width value of the template",
                ),
                sg.Push(),
                text_input_validation(
                    inputKey="WidthMatch",
                    default_text="0",
                    expand_x=False,
                    size=(25, 1),
                    justification="center",
                ),
                sg.Push(),
                sg.Text(
                    "Height",
                    tooltip="Height value of the template",
                ),
                sg.Push(),
                text_input_validation(
                    inputKey="HeightMatch",
                    default_text="0",
                    expand_x=False,
                    size=(25, 1),
                    justification="center",
                ),
            ],
        ]
    )
    return values_column


def template_match_layout():
    layout = [
        [
            sg.Frame(
                "Directory",
                [
                    [create_directory_column("Match")],
                ],
                expand_x=True,
            )
        ],
        [
            sg.Frame(
                "Reference Images",
                [
                    load_directory_images_column(function="Match"),
                ],
                expand_x=True,
                size=(720, 175),
            )
        ],
        [
            sg.Frame(
                "Template Images",
                [
                    load_directory_images_column(function="MatchTemplate"),
                ],
                expand_x=True,
                size=(720, 175),
            )
        ],
        [
            sg.Frame(
                "Values",
                [
                    [match_values_column()],
                ],
                expand_x=True,
            )
        ],
        [
            sg.Frame(
                "Mode",
                create_operations_layout(function="Match"),
                expand_x=True,
            )
        ],
        [
            sg.Button("Submit", key="ButtonSubmitMatch", enable_events=True),
            sg.Push(),
            sg.Text(
                "Offset",
                tooltip="Range of pixels to offset for the Image matching",
            ),
            text_input_validation(
                inputKey="OffsetMatch",
                default_text="0",
                expand_x=False,
                size=(25, 1),
                justification="center",
            ),
        ],
    ]
    return layout


def template_match_events_handler(window, event, values):
    function = "Match"

    operations = [
        "NORMALMatch",
        "CENTERMatch",
        "RIGHTMatch",
    ]
    selected_color = ("red", "white")

    if event in operations:
        for operation in operations:
            window[operation].update(button_color=sg.theme_button_color())
        window[event].update(button_color=selected_color)
    if event == "ImageMatchListbox":
        selected_image_name = values["ImageMatchListbox"][0]
        path = Path(selected_image_name)
        if path.exists():
            selected_image_text = textwrap.fill(f"{path.name}", 20)
            window["SelectedImageMatch"].update(selected_image_text)
            load_image_size_information(
                window=window, image_path=selected_image_name, function="Match"
            )
            window["OpenImageMatch"].update(visible=True)
    if event == "OpenImageMatch":
        selected_image_name = values["ImageMatchListbox"][0]
        path = Path(selected_image_name)
        if path.exists():
            os.startfile(f"{path}")
    if event == "LoadMatch":
        path = Path(values["FolderMatch"])
        if not path.exists():
            sg.popup(
                f"Invalid Path {path}",
                text_color="red",
                auto_close_duration=2,
                auto_close=True,
                no_titlebar=True,
            )
        else:
            items = load_images_from_directory(path)
            window["ImageMatchListbox"].update(values=items)
    if event == "FolderMatch":
        path = Path(f"{values["FolderMatch"]}")
        if not path.exists():
            sg.popup(
                f"Invalid Path {path}",
                text_color="red",
                auto_close_duration=2,
                auto_close=True,
                no_titlebar=True,
            )
        else:
            items = load_images_from_directory(path)
            window["ImageMatchListbox"].update(values=items)
    if event == "ButtonSubmitMatch":
        try:
            left_input = int(values["LeftMatch"])
            top_input = int(values["TopMatch"])
            width_input = int(values["WidthMatch"])
            height_input = int(values["HeightMatch"])

            offset_input = int(values["OffsetMatch"])

            if (left_input + width_input) < left_input or (
                left_input + width_input
            ) == left_input:
                raise ValueError("Right value is less than or equal to left value")
            if (top_input + height_input) < top_input or (
                top_input + height_input
            ) == top_input:
                raise ValueError("Bottom value is less than or equal to top value")

            selected_operation = operations[0]
            for operation in operations:
                color = window[operation].ButtonColor
                console.print(
                    f"Operation: [blue]{operation}[/blue] Color: [blue]{color}[/blue]"
                )

                if color == selected_color:
                    selected_operation = operation.replace("Match", "")

            selected_image_name = values["ImageMatchListbox"][0]
            path = Path(selected_image_name)
            if path.exists():
                template_path, info_path = match.run(
                    image_path=path,
                    template_path=path,
                    offset=offset_input,
                    left=left_input,
                    top=top_input,
                    width=width_input,
                    height=height_input,
                    extra=selected_operation,
                )
                if template_path is not None and info_path is not None:
                    load_image_window(template_path, info_path)
        except ValueError:
            console.print_exception()
            sg.popup(
                "Value error/s",
                text_color="red",
                auto_close_duration=2,
                auto_close=True,
                no_titlebar=True,
            )
        except FileNotFoundError:
            console.print_exception()
            sg.popup(
                "FileNotFoundError",
                text_color="red",
                auto_close_duration=2,
                auto_close=True,
                no_titlebar=True,
            )
        except IndexError:
            console.print_exception()
            sg.popup(
                "No selected item",
                text_color="red",
                auto_close_duration=2,
                auto_close=True,
            )

    if event == "LeftMatch":
        try:
            int(values["LeftMatch"])
            window["LeftMatchValidation"].update(
                "",
            )
        except ValueError:
            window["LeftMatchValidation"].update("Invalid value", text_color="red")

    if event == "OffsetMatch":
        try:
            int(values["OffsetMatch"])
            window["OffsetMatchValidation"].update(
                "",
            )
        except ValueError:
            window["OffsetMatchValidation"].update("Invalid value", text_color="red")

    if event == "WidthMatch":
        try:
            int(values["WidthMatch"])
            window["WidthMatchValidation"].update(
                "",
            )
        except ValueError:
            window["WidthMatchValidation"].update("Invalid value", text_color="red")

    if event == "TopMatch":
        try:
            int(values["TopMatch"])
            window["TopMatchValidation"].update(
                "",
            )
        except ValueError:
            window["TopMatchValidation"].update("Invalid value", text_color="red")

    if event == "HeightMatch":
        try:
            int(values[f"Height{function}"])
            window["HeightMatchValidation"].update(
                "",
            )
        except ValueError:
            window["HeightMatchValidation"].update("Invalid value", text_color="red")
