from gui_handler_create import template_create_layout, template_create_events_handler
from gui_handler_reverse import template_reverse_layout, template_reverse_events_handler
from gui_handler_match import template_match_layout, template_match_events_handler
import PySimpleGUI as sg

sg.theme("Dark")


def layout_tab_group():
    layout = [
        [
            sg.Tab(
                "Create",
                key="Tab Create",
                layout=template_create_layout(),
                expand_x=True,
                expand_y=True,
            ),
            sg.Tab(
                "Reverse",
                key="Tab Reverse",
                layout=template_reverse_layout(),
                expand_x=True,
                expand_y=True,
            ),
            sg.Tab(
                "Match",
                key="Tab Match",
                layout=template_match_layout(),
                expand_x=True,
                expand_y=True,
            ),
        ]
    ]
    return layout


def main():
    layout = [
        [
            sg.TabGroup(
                key="-TABGROUP-",
                layout=layout_tab_group(),
                expand_x=True,
                expand_y=True,
                size=(540, 720),
            )
        ],
    ]
    window = sg.Window(
        "FGA Template",
        layout=layout,
        size=(540, 720),
        location=(0, 0),
        return_keyboard_events=True,
        finalize=True,
        resizable=False,
    )

    while True:
        event, values = window.read(timeout=None)
        template_create_events_handler(window, event, values)
        template_reverse_events_handler(window, event, values)
        template_match_events_handler(window, event, values)
        if event == sg.WIN_CLOSED:
            break
        if event == sg.WINDOW_CLOSED:
            break
        if event in (None, "Exit"):
            break

    window.close()


if __name__ == "__main__":
    main()
