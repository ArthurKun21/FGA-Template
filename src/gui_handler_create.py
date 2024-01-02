import textwrap
from pathlib import Path

import image_handler
import PySimpleGUI as sg
from gui_components import text_input_validation
from rich.console import Console

console = Console()

cwd = Path(__file__).cwd()
image_extensions = [".png", ".jpg"]


def create_directory_column():
    directory_column = sg.Col(
        [
            [
                sg.Text("Folder"),
                sg.Input(f"{cwd}", key="FolderCreate", enable_events=True),
                sg.FolderBrowse(key="FolderBrowseCreate", enable_events=True),
                sg.Button("Load", key="LoadCreate", enable_events=True),
            ],
        ],
        key="Add Column",
        expand_x=True,
        expand_y=True,
    )
    return directory_column


def load_images_from_directory(dir_path: Path):
    return [
        f"{x}"
        for x in dir_path.iterdir()
        if x.is_file() and x.suffix in image_extensions
    ]


def load_image_size_information(window, image_path: Path):
    image_width, image_height = image_handler.get_size(image_path)
    window["ImageWidthCreate"].update(f"{image_width}")
    window["ImageHeightCreate"].update(f"{image_height}")


def load_directory_images_column():
    images_column = [
        sg.Col(
            [
                [
                    sg.Listbox(
                        values=load_images_from_directory(cwd),
                        size=(40, 20),
                        key="ImageCreateListbox",
                        enable_events=True,
                    ),
                ]
            ],
            expand_x=True,
            justification="left",
        ),
        sg.Col(
            [
                [
                    sg.Text("File name"),
                ],
                [
                    sg.Text(
                        "",
                        key="SelectedImageCreate",
                        size=(20, None),
                    ),
                ],
                [
                    sg.Text("Width"),
                ],
                [
                    sg.Text("", key="ImageWidthCreate"),
                ],
                [
                    sg.Text("Height"),
                ],
                [
                    sg.Text("", key="ImageHeightCreate"),
                ],
            ],
            justification="center",
            expand_x=True,
        ),
    ]
    return images_column


def create_values_column():
    left_top_column = sg.Col(
        [
            [
                sg.Text(
                    "Left",
                ),
                sg.Push(),
                text_input_validation(
                    inputKey="LeftCreate",
                    default_text="0",
                    expand_x=False,
                    size=(25, 1),
                    justification="center",
                ),
                sg.Push(),
                sg.Text("Right"),
                sg.Push(),
                text_input_validation(
                    inputKey="RightCreate",
                    default_text="0",
                    expand_x=False,
                    size=(25, 1),
                    justification="center",
                ),
            ],
            [
                sg.Text("Top"),
                text_input_validation(
                    inputKey="TopCreate",
                    default_text="0",
                    expand_x=False,
                    size=(25, 1),
                    justification="center",
                ),
                sg.Text("Bottom"),
                sg.Push(),
                text_input_validation(
                    inputKey="BottomCreate",
                    default_text="0",
                    expand_x=False,
                    size=(25, 1),
                    justification="center",
                ),
            ],
        ]
    )
    return left_top_column


def template_create_layout():
    layout = [
        [
            sg.Frame(
                "File",
                [
                    [create_directory_column()],
                ],
                expand_x=True,
            )
        ],
        [
            sg.Frame(
                "Images",
                [
                    load_directory_images_column(),
                ],
                expand_x=True,
                size=(720, 250),
            )
        ],
        [
            sg.Frame(
                "Values",
                [
                    [create_values_column()],
                ],
                expand_x=True,
            )
        ],
        [
            sg.Button("Submit", key="ButtonSubmitCreate", enable_events=True),
        ],
    ]
    return layout


def template_create_events_handler(window, event, values):
    if event == "ButtonSubmitCreate":
        try:
            left_input = int(values["LeftCreate"])
        except ValueError:
            left_input = 0
        try:
            top_input = int(values["TopCreate"])
        except ValueError:
            top_input = 0
        try:
            right_input = int(values["RightCreate"])
        except ValueError:
            right_input = 0
        try:
            bottom_input = int(values["BottomCreate"])
        except ValueError:
            bottom_input = 0

    if event == "LeftCreate":
        try:
            int(values["LeftCreate"])
            window["LeftCreateValidation"].update(
                "",
            )
        except ValueError:
            window["LeftCreateValidation"].update("Invalid value", text_color="red")

    if event == "TopCreate":
        try:
            int(values["TopCreate"])
            window["TopCreateValidation"].update(
                "",
            )
        except ValueError:
            window["TopCreateValidation"].update("Invalid value", text_color="red")

    if event == "BottomCreate":
        try:
            int(values["BottomCreate"])
            window["BottomCreateValidation"].update(
                "",
            )
        except ValueError:
            window["BottomCreateValidation"].update("Invalid value", text_color="red")

    if event == "RightCreate":
        try:
            int(values["RightCreate"])
            window["RightCreateValidation"].update(
                "",
            )
        except ValueError:
            window["RightCreateValidation"].update("Invalid value", text_color="red")

    if event == "FolderCreate":
        console.print(f"Loading images from {values['FolderCreate']}")
        path = Path(f"{values["FolderCreate"]}")
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
            console.print(f"Loading images from {items}")
            window["ImageCreateListbox"].update(values=items)

    if event == "ImageCreateListbox":
        selected_image_name = values["ImageCreateListbox"][0]
        path = Path(selected_image_name)
        if path.exists():
            selected_image_text = textwrap.fill(f"{path.name}", 20)
            window["SelectedImageCreate"].update(selected_image_text)
        load_image_size_information(
            window=window,
            image_path=selected_image_name,
        )
    if event == "LoadCreate":
        path = Path(values["FolderCreate"])
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
            console.print(f"Loading images from {items}")
            window["ImageCreateListbox"].update(values=items)
