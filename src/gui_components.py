from typing import Optional

import PySimpleGUI as sg


def text_input_validation(
    inputKey: str,
    default_text: str = "",
    key: Optional[str] = None,
    expand_x: bool = True,
):
    if key is None:
        key = inputKey + "Validation"
    return sg.Col(
        [
            [
                sg.Input(default_text=default_text, key=inputKey, enable_events=True, expand_x=expand_x),
            ],
            [
                sg.Text("", key=key, enable_events=True),
            ],
        ],
        element_justification='centered'
    )
