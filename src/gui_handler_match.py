import PySimpleGUI as sg
from gui_components import (
    text_input_validation,
    create_directory_column,
    load_directory_images_column,
    create_operations_layout,
    create_information_layout
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
                "Images",
                [
                    load_directory_images_column(function="Match"),
                ],
                expand_x=True,
                size=(720, 250),
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
        [
            sg.Frame(
                "Information",
                create_information_layout(function="Match"),
                expand_x=True,
            )
        ],
    ]
    return layout


def template_match_events_handler(window, event, values):
    operations = [
        "NORMALMatch",
        "CENTERMatch",
        "RIGHTMatch",
    ]
    selected_color = ("red", "white")
