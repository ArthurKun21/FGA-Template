from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import PySimpleGUI as sg


@dataclass
class ItemPath:
    path: Path
    name: Optional[str] = None

    def __post__init__(self):
        self.name = self.path.name


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
