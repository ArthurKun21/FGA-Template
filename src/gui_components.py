import os
from pathlib import Path
from typing import Optional

import image_handler
import PySimpleGUI as sg
import toml

cwd = Path(__file__).cwd()
image_extensions = [".png", ".jpg"]


def copy_to_clipboard(text: str):
    sg.clipboard_set(text)


def load_image_window(image_path: Path, info_path: Path):
    with open(info_path) as f:
        info = toml.load(f)

    normal_region = info["Region"]["Normal"]
    center_region = info["Region"]["From Center"]
    right_region = info["Region"]["From Right"]

    normal_location = info["Location"]["Normal"]
    center_location = info["Location"]["From Center"]
    right_location = info["Location"]["From Right"]

    layout = [
        [
            sg.Push(),
            sg.Image(filename=f"{image_path}"),
            sg.Push(),
        ],
        [
            sg.Button("Load Directory", key="LoadDirectoryButton"),
            sg.Text(f"{image_path.parent}", key="LoadDirectoryText"),
        ],
        [
            sg.Text("Normal Region"),
            sg.Push(),
            sg.Input(
                f"{normal_region}",
                key="NormalRegion",
                disabled=True,
                justification="center",
                text_color=sg.theme_text_color(),
                disabled_readonly_background_color=sg.theme_text_element_background_color(),
            ),
            sg.Button(
                "copy",
                key="NormalRegionCopy",
            ),
        ],
        [
            sg.Text("Center Region"),
            sg.Push(),
            sg.Input(
                f"{center_region}",
                key="CenterRegion",
                disabled=True,
                justification="center",
                text_color=sg.theme_text_color(),
                disabled_readonly_background_color=sg.theme_text_element_background_color(),
            ),
            sg.Button(
                "copy",
                key="CenterRegionCopy",
            ),
        ],
        [
            sg.Text("Right Region"),
            sg.Push(),
            sg.Input(
                f"{right_region}",
                key="RightRegion",
                disabled=True,
                justification="center",
                text_color=sg.theme_text_color(),
                disabled_readonly_background_color=sg.theme_text_element_background_color(),
            ),
            sg.Button(
                "copy",
                key="RightRegionCopy",
            ),
        ],
        [
            sg.Text("Normal Location"),
            sg.Push(),
            sg.Input(
                f"{normal_location}",
                disabled=True,
                key="NormalLocation",
                justification="center",
                text_color=sg.theme_text_color(),
                disabled_readonly_background_color=sg.theme_text_element_background_color(),
            ),
            sg.Button(
                "copy",
                key="NormalLocationCopy",
            ),
        ],
        [
            sg.Text("Center Location"),
            sg.Push(),
            sg.Input(
                f"{center_location}",
                key="CenterLocation",
                disabled=True,
                justification="center",
                text_color=sg.theme_text_color(),
                disabled_readonly_background_color=sg.theme_text_element_background_color(),
            ),
            sg.Button(
                "copy",
                key="CenterLocationCopy",
            ),
        ],
        [
            sg.Text("Right Location"),
            sg.Push(),
            sg.Input(
                f"{right_location}",
                key="RightLocation",
                disabled=True,
                justification="center",
                text_color=sg.theme_text_color(),
                disabled_readonly_background_color=sg.theme_text_element_background_color(),
            ),
            sg.Button(
                "copy",
                key="RightLocationCopy",
            ),
        ],
    ]
    window = sg.Window(f"{image_path.name}", layout, size=(800, 400))
    while True:
        event, _ = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "NormalRegionCopy":
            copy_to_clipboard(text=normal_region)
        if event == "CenterRegionCopy":
            copy_to_clipboard(text=center_region)
        if event == "RightRegionCopy":
            copy_to_clipboard(text=right_region)
        if event == "NormalLocationCopy":
            copy_to_clipboard(text=normal_location)
        if event == "CenterLocationCopy":
            copy_to_clipboard(text=center_location)
        if event == "RightLocationCopy":
            copy_to_clipboard(text=right_location)
        if event == "LoadDirectoryButton":
            os.startfile(image_path.parent)
    window.close()


def text_input_validation(
    inputKey: str,
    default_text: str = "",
    key: Optional[str] = None,
    expand_x: bool = True,
    size: tuple[Optional[int], Optional[int]] = (None, None),
    justification: Optional[str] = None,
):
    if key is None:
        key = inputKey + "Validation"
    return sg.Col(
        [
            [
                sg.Input(
                    default_text=default_text,
                    key=inputKey,
                    enable_events=True,
                    expand_x=expand_x,
                    size=size,
                    justification=justification,
                ),
            ],
            [
                sg.Text("", key=key, enable_events=True),
            ],
        ],
        element_justification="centered",
    )


def load_images_from_directory(dir_path: Path):
    return [
        f"{x}"
        for x in dir_path.iterdir()
        if x.is_file() and x.suffix in image_extensions
    ]


def load_image_size_information(window, image_path: Path, function: str):
    image_width, image_height = image_handler.get_size(image_path)
    window[f"ImageWidth{function}"].update(f"{image_width}")
    window[f"ImageHeight{function}"].update(f"{image_height}")


def create_operations_layout(
    function: str,
):
    active = f"NORMAL{function}"
    operations = [
        "NORMAL",
        "CENTER",
        "RIGHT",
    ]
    selected_color = ("red", "white")
    layout = [
        [
            sg.Button(
                name,
                key=f"{name}{function}",
                button_color=selected_color
                if f"{name}{function}" == active
                else sg.theme_button_color(),
            )
            for name in operations
        ]
    ]
    return layout


def create_information_layout(function: str):
    layout = [
        [
            sg.Text("Left Border"),
            sg.Push(),
            sg.Text("", key=f"LeftBorder{function}Information"),
            sg.Push(),
            sg.Text("Top Border"),
            sg.Push(),
            sg.Text("", key=f"TopBorder{function}Information"),
        ],
        [
            sg.Text("Right Border"),
            sg.Push(),
            sg.Text("", key=f"RightBorder{function}Information"),
            sg.Push(),
            sg.Text("Bottom Border"),
            sg.Push(),
            sg.Text("", key=f"BottomBorder{function}Information"),
        ],
        [
            sg.Text("Template Width"),
            sg.Push(),
            sg.Text("", key=f"Width{function}Information"),
            sg.Push(),
            sg.Text("Template Height"),
            sg.Push(),
            sg.Text("", key=f"Height{function}Information"),
        ],
    ]
    return layout


def load_directory_images_column(function: str):
    images_column = [
        sg.Col(
            [
                [
                    sg.Listbox(
                        values=load_images_from_directory(cwd),
                        size=(40, 20),
                        key=f"Image{function}Listbox",
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
                        key=f"SelectedImage{function}",
                        size=(20, None),
                    ),
                ],
                [
                    sg.Text("Width"),
                ],
                [
                    sg.Text("", key=f"ImageWidth{function}"),
                ],
                [
                    sg.Text("Height"),
                ],
                [
                    sg.Text("", key=f"ImageHeight{function}"),
                ],
                [
                    sg.Button(
                        "Open Image",
                        key=f"OpenImage{function}",
                        enable_events=True,
                        visible=False,
                    ),
                ],
            ],
            justification="center",
            expand_x=True,
        ),
    ]
    return images_column


def create_directory_column(function: str):
    directory_column = sg.Col(
        [
            [
                sg.Text("Folder"),
                sg.Input(f"{cwd}", key=f"Folder{function}", enable_events=True),
                sg.FolderBrowse(key=f"FolderBrowse{function}", enable_events=True),
                sg.Button("Load", key=f"Load{function}", enable_events=True),
            ],
        ],
        expand_x=True,
        expand_y=True,
    )
    return directory_column
