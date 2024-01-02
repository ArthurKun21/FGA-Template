import textwrap
from pathlib import Path

import information_handler
import PySimpleGUI as sg
from gui_components import (
    create_directory_column,
    create_information_layout,
    load_directory_images_column,
    load_image_size_information,
    load_images_from_directory,
    text_input_validation,
    create_operations_layout,
)


def reverse_values_column():
    values_column = sg.Col(
        [
            [
                sg.Text(
                    "Left",
                ),
                sg.Push(),
                text_input_validation(
                    inputKey="LeftReverse",
                    default_text="0",
                    expand_x=False,
                    size=(25, 1),
                    justification="center",
                ),
                sg.Push(),
                sg.Text("Width"),
                sg.Push(),
                text_input_validation(
                    inputKey="WidthReverse",
                    default_text="0",
                    expand_x=False,
                    size=(25, 1),
                    justification="center",
                ),
            ],
            [
                sg.Text("Top"),
                text_input_validation(
                    inputKey="TopReverse",
                    default_text="0",
                    expand_x=False,
                    size=(25, 1),
                    justification="center",
                ),
                sg.Text("Height"),
                sg.Push(),
                text_input_validation(
                    inputKey="HeightReverse",
                    default_text="0",
                    expand_x=False,
                    size=(25, 1),
                    justification="center",
                ),
            ],
        ]
    )
    return values_column

def show_template_create_calculations(window, values):
    try:
        left_input = int(values["LeftReverse"])
        top_input = int(values["TopReverse"])
        right_input = int(values["RightReverse"])
        bottom_input = int(values["BottomReverse"])

        if right_input < left_input or right_input == left_input:
            raise ValueError("Right value is less than or equal to left value")
        if bottom_input < top_input or bottom_input == top_input:
            raise ValueError("Bottom value is less than or equal to top value")

        selected_image_name = values["ImageReverseListbox"][0]
        path = Path(selected_image_name)
        if path.exists():
            (
                left_border,
                top_border,
                right_border,
                bottom_border,
                width_template,
                height_template,
                _,
                _,
                _,
                _,
                _,
                _,
            ) = information_handler.fetch_image_manipulation_information(
                path, left_input, top_input, right_input, bottom_input
            )
            window["LeftBorderInformation"].update(f"{left_border}")
            window["TopBorderInformation"].update(f"{top_border}")
            window["RightBorderInformation"].update(f"{right_border}")
            window["BottomBorderInformation"].update(f"{bottom_border}")
            window["WidthInformation"].update(f"{width_template}")
            window["HeightInformation"].update(f"{height_template}")
    except ValueError:
        pass
    except FileNotFoundError:
        pass
    except IndexError:
        pass


def template_reverse_layout():
    layout = [
        [
            sg.Frame(
                "Directory",
                [
                    [create_directory_column("Reverse")],
                ],
                expand_x=True,
            )
        ],
        [
            sg.Frame(
                "Images",
                [
                    load_directory_images_column(function="Reverse"),
                ],
                expand_x=True,
                size=(720, 250),
            )
        ],
        [
            sg.Frame(
                "Values",
                [
                    [reverse_values_column()],
                ],
                expand_x=True,
            )
        ],
        [
            sg.Button("Submit", key="ButtonSubmitReverse", enable_events=True),
        ],
        [
            sg.Frame(
                "Mode",
                create_operations_layout(function="Reverse"),
            )
        ],
        [
            sg.Frame(
                "Information",
                create_information_layout(function="Reverse"),
            )
        ],
    ]
    return layout


def template_reverse_events_handler(window, event, values):
    operations = [
        f"NORMALReverse",
        f"CENTERReverse",
        f"RIGHTReverse",
    ]
    selected_color = ("red", "white")
    if event in operations:
        for operation in operations:
            window[operation].update(button_color=sg.theme_button_color())
        window[event].update(button_color=selected_color)
    if event == "ImageReverseListbox":
        selected_image_name = values["ImageReverseListbox"][0]
        path = Path(selected_image_name)
        if path.exists():
            selected_image_text = textwrap.fill(f"{path.name}", 20)
            window["SelectedImageReverse"].update(selected_image_text)
        load_image_size_information(
            window=window,
            image_path=selected_image_name,
            function="Reverse"
        )
    if event == "LoadReverse":
        path = Path(values["FolderReverse"])
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
            window["ImageReverseListbox"].update(values=items)
    if event == "FolderReverse":
        path = Path(f"{values["FolderReverse"]}")
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
            window["ImageReverseListbox"].update(values=items)
    if event == "ButtonSubmitReverse":
        pass

    if event == "LeftReverse":
        try:
            int(values["LeftReverse"])
            window["LeftReverseValidation"].update(
                "",
            )
        except ValueError:
            window["LeftReverseValidation"].update("Invalid value", text_color="red")

    if event == "WidthReverse":
        try:
            int(values["WidthReverse"])
            window["WidthReverseValidation"].update(
                "",
            )
        except ValueError:
            window["WidthReverseValidation"].update("Invalid value", text_color="red")

    if event == "TopReverse":
        try:
            int(values["TopReverse"])
            window["TopReverseValidation"].update(
                "",
            )
        except ValueError:
            window["TopReverseValidation"].update("Invalid value", text_color="red")

    if event == "HeightReverse":
        try:
            int(values["HeightReverse"])
            window["HeightReverseValidation"].update(
                "",
            )
        except ValueError:
            window["HeightReverseValidation"].update("Invalid value", text_color="red")
