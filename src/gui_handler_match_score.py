from enum import auto
import os
import textwrap
from pathlib import Path

import match
import PySimpleGUI as sg
from gui_components import (
    create_directory_column,
    create_operations_layout,
    load_directory_images_column,
    load_image_size_information,
    load_image_window,
    load_images_from_directory,
    text_input_validation,
    save_directory_settings,
)
from rich.console import Console

console = Console()


def MatchScore_values_column():
    values_column = sg.Col(
        [
            [
                sg.Text(
                    "Left",
                    tooltip="Left value of the template",
                ),
                sg.Push(),
                text_input_validation(
                    inputKey="LeftMatchScore",
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
                    inputKey="TopMatchScore",
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
                    inputKey="WidthMatchScore",
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
                    inputKey="HeightMatchScore",
                    default_text="0",
                    expand_x=False,
                    size=(25, 1),
                    justification="center",
                ),
            ],
        ]
    )
    return values_column


def template_match_score_layout():
    layout = [
        [
            sg.Frame(
                "Directory",
                [
                    [create_directory_column("MatchScore")],
                ],
                expand_x=True,
            )
        ],
        [
            sg.Frame(
                "Reference Images",
                [
                    load_directory_images_column(function="MatchScore"),
                ],
                expand_x=True,
                size=(720, 165),
            )
        ],
        [
            sg.Frame(
                "Template Images",
                [
                    load_directory_images_column(function="MatchScoreTemplate"),
                ],
                expand_x=True,
                size=(720, 165),
            )
        ],
        [
            sg.Frame(
                "Values",
                [
                    [MatchScore_values_column()],
                ],
                expand_x=True,
            )
        ],
        [
            sg.Frame(
                "Mode",
                create_operations_layout(function="MatchScore"),
                expand_x=True,
            )
        ],
        [
            sg.Button("Submit", key="ButtonSubmitMatchScore", enable_events=True),
            sg.Push(),
            sg.Text(
                "Offset X",
                tooltip="Range of pixels to offset in x for the Image MatchScoreing",
            ),
            text_input_validation(
                inputKey="OffsetXMatchScore",
                default_text="10",
                expand_x=False,
                size=(15, 1),
                justification="center",
            ),
            sg.Text(
                "Offset Y",
                tooltip="Range of pixels to offset in y for the Image MatchScoreing",
            ),
            text_input_validation(
                inputKey="OffsetYMatchScore",
                default_text="10",
                expand_x=False,
                size=(15, 1),
                justification="center",
            ),
        ],
    ]
    return layout


def template_match_score_events_handler(window, event, values):
    function = "MatchScore"

    operations = [
        "NORMALMatchScore",
        "CENTERMatchScore",
        "RIGHTMatchScore",
    ]
    selected_color = ("red", "white")

    if event in operations:
        for operation in operations:
            window[operation].update(button_color=sg.theme_button_color())
        window[event].update(button_color=selected_color)

    if event == "ImageMatchScoreListbox":
        selected_image_name = values["ImageMatchScoreListbox"][0]
        path = Path(selected_image_name)
        if path.exists():
            selected_image_text = textwrap.fill(f"{path.name}", 20)
            window["SelectedImageMatchScore"].update(selected_image_text)
            load_image_size_information(
                window=window, image_path=selected_image_name, function="MatchScore"
            )
            window["OpenImageMatchScore"].update(visible=True)

    if event == "ImageMatchScoreTemplateListbox":
        selected_image_name = values["ImageMatchScoreTemplateListbox"][0]
        path = Path(selected_image_name)
        if path.exists():
            selected_image_text = textwrap.fill(f"{path.name}", 20)
            window["SelectedImageMatchScoreTemplate"].update(selected_image_text)
            load_image_size_information(
                window=window, image_path=selected_image_name, function="MatchScoreTemplate"
            )
            window["OpenImageMatchScoreTemplate"].update(visible=True)

    if event == "OpenImageMatchScore":
        selected_image_name = values["ImageMatchScoreListbox"][0]
        path = Path(selected_image_name)
        if path.exists():
            os.startfile(f"{path}")

    if event == "OpenImageMatchScoreTemplate":
        selected_image_name = values["ImageMatchScoreTemplateListbox"][0]
        path = Path(selected_image_name)
        if path.exists():
            os.startfile(f"{path}")

    if event == "LoadMatchScore":
        path = Path(values["FolderMatchScore"])
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
            window["ImageMatchScoreListbox"].update(values=items)
            window["ImageMatchScoreTemplateListbox"].update(values=items)

    if event == "FolderMatchScore":
        path = Path(f"{values["FolderMatchScore"]}")
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
            window["ImageMatchScoreListbox"].update(values=items)
            window["ImageMatchScoreTemplateListbox"].update(values=items)
            save_directory_settings("MatchScore", path)

    if event == "ButtonSubmitMatchScore":
        try:
            left_input = int(values["LeftMatchScore"])
            top_input = int(values["TopMatchScore"])
            width_input = int(values["WidthMatchScore"])
            height_input = int(values["HeightMatchScore"])

            offset_x_input = int(values["OffsetXMatchScore"])
            offset_y_input = int(values["OffsetYMatchScore"])

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
                    selected_operation = operation.replace("MatchScore", "")

            selected_image_name = values["ImageMatchScoreListbox"][0]

            selected_template_name = values["ImageMatchScoreTemplateListbox"][0]

            path = Path(selected_image_name)

            template_path = Path(selected_template_name)
            if path.exists() and template_path.exists():
                sg.popup(
                    "Wait for the process to finish",
                    auto_close_duration=2,
                    auto_close=True,
                    no_titlebar=True,
                    non_blocking=True
                )
                template_path, info_path, score = match.score(
                    image_path=path,
                    template_path=template_path,
                    offset_x=offset_x_input,
                    offset_y=offset_y_input,
                    left=left_input,
                    top=top_input,
                    width=width_input,
                    height=height_input,
                    extra=selected_operation,
                )
                if template_path is not None and info_path is not None:
                    load_image_window(template_path, info_path, output_text=f"Score: {score}")
                else:
                    sg.popup(
                        "No Match Score found",
                        text_color="red",
                        no_titlebar=True,
                    )
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

    if event == "LeftMatchScore":
        try:
            int(values["LeftMatchScore"])
            window["LeftMatchScoreValidation"].update(
                "",
            )
        except ValueError:
            window["LeftMatchScoreValidation"].update("Invalid value", text_color="red")

    if event == "OffsetXMatchScore":
        try:
            int(values["OffsetXMatchScore"])
            window["OffsetXMatchScoreValidation"].update(
                "",
            )
        except ValueError:
            window["OffsetXMatchScoreValidation"].update("Invalid value", text_color="red")

    if event == "OffsetYMatchScore":
        try:
            int(values["OffsetYMatchScore"])
            window["OffsetYMatchScoreValidation"].update(
                "",
            )
        except ValueError:
            window["OffsetYMatchScoreValidation"].update("Invalid value", text_color="red")

    if event == "WidthMatchScore":
        try:
            int(values["WidthMatchScore"])
            window["WidthMatchScoreValidation"].update(
                "",
            )
        except ValueError:
            window["WidthMatchScoreValidation"].update("Invalid value", text_color="red")

    if event == "TopMatchScore":
        try:
            int(values["TopMatchScore"])
            window["TopMatchScoreValidation"].update(
                "",
            )
        except ValueError:
            window["TopMatchScoreValidation"].update("Invalid value", text_color="red")

    if event == "HeightMatchScore":
        try:
            int(values[f"Height{function}"])
            window["HeightMatchScoreValidation"].update(
                "",
            )
        except ValueError:
            window["HeightMatchScoreValidation"].update("Invalid value", text_color="red")
