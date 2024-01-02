import PySimpleGUI as sg


def template_create_layout():
    add_column = sg.Col(
        [
            [
                sg.Text("Left", key="LeftCreateText"),
            ],
            [
                sg.Text("Top"),
            ],
            [
                sg.Text("Right"),
            ],
            [
                sg.Text("Bottom"),
            ],
        ],
        key="Add Column",
        expand_x=True,
    )
    add_value_col = sg.Col(
        [
            [
                sg.Input("0", key="LeftCreate", expand_x=True, enable_events=True),
            ],
            [
                sg.Input("0", key="TopCreate", expand_x=True),
            ],
            [
                sg.Input("0", key="RightCreate", expand_x=True),
            ],
            [
                sg.Input("0", key="BottomCreate", expand_x=True),
            ]
        ],
        expand_x=True,
    )
    layout = [
        [
            sg.Frame(
                "Values",
                [[
                    add_column,
                    add_value_col
                ]]
            )
        ],
        [
            sg.Button("Submit", key="ButtonSubmitCreate", enable_events=True)
        ]
    ]
    return layout


def template_create_events_handler(window, event, values):
    if event == "LeftCreate":
        window["LeftCreateText"].update(values["LeftCreate"])
    if event == "ButtonSubmitCreate":
        sg.popup("test")