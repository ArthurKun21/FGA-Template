import PySimpleGUI as sg
from gui_components import text_input_validation


def template_create_layout():
    add_column = sg.Col(
        [
            [
                sg.Text(
                    "Left",
                ),
                sg.Push(),
                text_input_validation(
                    inputKey="LeftCreate",
                    default_text="0",
                ),
            ],
            [
                sg.Text("Top"),
                sg.Push(),
                text_input_validation(
                    inputKey="TopCreate",
                    default_text="0",
                ),
            ],
            [
                sg.Text("Right"),
                sg.Push(),
                text_input_validation(
                    inputKey="RightCreate",
                    default_text="0",
                ),
            ],
            [
                sg.Text("Bottom"),
                sg.Push(),
                text_input_validation(
                    inputKey="BottomCreate",
                    default_text="0",
                ),
            ],
        ],
        key="Add Column",
        expand_x=True,
        expand_y=True,
    )
    layout = [
        [sg.Frame("Values", [[add_column]])],
        [sg.Button("Submit", key="ButtonSubmitCreate", enable_events=True)],
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
            window["LeftCreateValidation"].update("Invalid value",text_color="red")
