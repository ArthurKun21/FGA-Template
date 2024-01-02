from pathlib import Path
from typing import Optional

import PySimpleGUI as sg
import toml


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
            sg.Image(filename=f"{image_path}"),
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
                disabled_readonly_background_color=sg.theme_text_element_background_color()
            ),
            sg.Button(
                "copy",
                key="NormalRegionCopy",
            )
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
                disabled_readonly_background_color=sg.theme_text_element_background_color()
            ),
            sg.Button(
                "copy",
                key="CenterRegionCopy",
            )
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
                disabled_readonly_background_color=sg.theme_text_element_background_color()
            ),
            sg.Button(
                "copy",
                key="RightRegionCopy",
            )
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
                disabled_readonly_background_color=sg.theme_text_element_background_color()
            ),
            sg.Button(
                "copy",
                key="NormalLocationCopy",
            )
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
                disabled_readonly_background_color=sg.theme_text_element_background_color()
            ),
            sg.Button(
                "copy",
                key="CenterLocationCopy",
            )
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
                disabled_readonly_background_color=sg.theme_text_element_background_color()
            ),
            sg.Button(
                "copy",
                key="RightLocationCopy",
            )
        ],
    ]
    window = sg.Window(f"{image_path.name}", layout, size=(800, 600))
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
