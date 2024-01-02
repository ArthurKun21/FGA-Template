import PySimpleGUI as sg


def template_reverse_layout():
    layout = [
        [
            sg.Text("Reverse Template"),
        ]
    ]
    return layout


def template_reverse_events_handler(window, event, values):
    if event == "LeftCreate":
        window["LeftCreateText"].update(values["LeftCreate"])