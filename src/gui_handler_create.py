from pathlib import Path

import PySimpleGUI as sg
from gui_components import text_input_validation

cwd = Path(__file__).cwd()
image_extensions = [".png", ".jpg"]


def create_directory_column():
    directory_column = sg.Col(
        [
            [
                sg.Text("Folder"),
                sg.Push(),
                sg.Input(f"{cwd}", key="FolderCreate", enable_events=True),
                sg.FolderBrowse(key="FolderBrowseCreate", enable_events=True),
            ],
        ],
        key="Add Column",
        expand_x=True,
        expand_y=True,
    )
    return directory_column


def load_images_from_directory(dir_path: Path):
    return [
        f"{x.name}"
        for x in cwd.iterdir()
        if x.is_file() and x.suffix in image_extensions
    ]


def load_directory_images_column():
    images_column = [
        sg.Col(
            [
                [
                    sg.Listbox(
                        values=load_images_from_directory(dir_path=cwd),
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
                    sg.Text("Width"),
                ],
                [
                    sg.Text("Image Width"),
                ],
                [
                    sg.Text("Height"),
                ],
                [
                    sg.Text("Image Height"),
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
            print(path)
            items = load_images_from_directory(path)
            print(items)
            window["ImageCreateListbox"].update(values=items)
