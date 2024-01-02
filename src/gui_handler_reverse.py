import PySimpleGUI as sg
from pathlib import Path
import textwrap
from gui_components import (
    create_directory_column,
    load_directory_images_column,
    text_input_validation,
    load_image_size_information,
    load_images_from_directory,
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
    ]
    return layout


def template_reverse_events_handler(window, event, values):

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
