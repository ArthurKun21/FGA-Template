import PySimpleGUI as sg
from gui_handler_create import template_create_events_handler, template_create_layout
from gui_handler_match import template_match_events_handler, template_match_layout
from gui_handler_reverse import template_reverse_events_handler, template_reverse_layout
from gui_handler_detect_text import template_detect_text_events_handler, template_detect_text_layout
from gui_handler_text import template_text_events_handler, template_text_layout
from gui_handler_match_score import template_match_score_events_handler, template_match_score_layout

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
            sg.Tab(
                "Score",
                key="Tab Match",
                layout=template_match_score_layout(),
                expand_x=True,
                expand_y=True,
            ),
            sg.Tab(
                "Text Detection",
                key="Tab Detect Text",
                layout=template_detect_text_layout(),
                expand_x=True,
                expand_y=True,
            ),
            sg.Tab(
                "Text Only",
                key="Tab Text",
                layout=template_text_layout(),
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
        return_keyboard_events=True,
        finalize=True,
        resizable=False,
    )
    window.move_to_center()

    while True:
        event, values = window.read(timeout=None)
        template_create_events_handler(window, event, values)
        template_reverse_events_handler(window, event, values)
        template_match_events_handler(window, event, values)
        template_detect_text_events_handler(window, event, values)
        template_text_events_handler(window, event, values)
        template_match_score_events_handler(window, event, values)
        if event == sg.WIN_CLOSED:
            break
        if event == sg.WINDOW_CLOSED:
            break
        if event in (None, "Exit"):
            break

    window.close()


if __name__ == "__main__":
    main()
