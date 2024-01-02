import textwrap
from pathlib import Path

import create
import information_handler
import PySimpleGUI as sg
from gui_components import (
    create_directory_column,
    load_image_window,
    load_images_from_directory,
    text_input_validation,
    load_image_size_information,
    load_directory_images_column,
    create_information_layout
)
from rich.console import Console

console = Console()

cwd = Path(__file__).cwd()
image_extensions = [".png", ".jpg"]





def create_values_column():
    values_column = sg.Col(
        [
            [
                sg.Text(
                    "Left",
                ),
                sg.Push(),
                text_input_validation(
                    inputKey="LeftCreate",
                    default_text="0",
                    expand_x=False,
                    size=(25, 1),
                    justification="center",
                ),
                sg.Push(),
                sg.Text("Right"),
                sg.Push(),
                text_input_validation(
                    inputKey="RightCreate",
                    default_text="0",
                    expand_x=False,
                    size=(25, 1),
                    justification="center",
                ),
            ],
            [
                sg.Text("Top"),
                text_input_validation(
                    inputKey="TopCreate",
                    default_text="0",
                    expand_x=False,
                    size=(25, 1),
                    justification="center",
                ),
                sg.Text("Bottom"),
                sg.Push(),
                text_input_validation(
                    inputKey="BottomCreate",
                    default_text="0",
                    expand_x=False,
                    size=(25, 1),
                    justification="center",
                ),
            ],
        ]
    )
    return values_column


def template_create_layout():
    layout = [
        [
            sg.Frame(
                "Directory",
                [
                    [create_directory_column(function="Create")],
                ],
                expand_x=True,
            )
        ],
        [
            sg.Frame(
                "Images",
                [
                    load_directory_images_column(function="Create"),
                ],
                expand_x=True,
                size=(720, 250),
            )
        ],
        [
            sg.Frame(
                "Values",
                [
                    [create_values_column()],
                ],
                expand_x=True,
            )
        ],
        [
            sg.Button("Submit", key="ButtonSubmitCreate", enable_events=True),
        ],
        [
            sg.Frame(
                "Information",
                create_information_layout(function="Create"),
            )
        ],
    ]
    return layout


def show_template_create_calculations(window, values):
    try:
        left_input = int(values["LeftCreate"])
        top_input = int(values["TopCreate"])
        right_input = int(values["RightCreate"])
        bottom_input = int(values["BottomCreate"])

        if right_input < left_input or right_input == left_input:
            raise ValueError("Right value is less than or equal to left value")
        if bottom_input < top_input or bottom_input == top_input:
            raise ValueError("Bottom value is less than or equal to top value")

        selected_image_name = values["ImageCreateListbox"][0]
        path = Path(selected_image_name)
        if path.exists():
            (
                left_border,
                top_border,
                right_border,
                bottom_border,
                width_template,
                height_template,
                _,
                _,
                _,
                _,
                _,
                _,
            ) = information_handler.fetch_image_manipulation_information(
                path, left_input, top_input, right_input, bottom_input
            )
            window["LeftBorderCreateInformation"].update(f"{left_border}")
            window["TopBorderCreateInformation"].update(f"{top_border}")
            window["RightBorderCreateInformation"].update(f"{right_border}")
            window["BottomBorderCreateInformation"].update(f"{bottom_border}")
            window["WidthCreateInformation"].update(f"{width_template}")
            window["HeightCreateInformation"].update(f"{height_template}")
    except ValueError:
        pass
    except FileNotFoundError:
        pass
    except IndexError:
        pass


def template_create_events_handler(window, event, values):
    if event == "ButtonSubmitCreate":
        try:
            left_input = int(values["LeftCreate"])
            top_input = int(values["TopCreate"])
            right_input = int(values["RightCreate"])
            bottom_input = int(values["BottomCreate"])

            if right_input < left_input or right_input == left_input:
                raise ValueError("Right value is less than or equal to left value")
            if bottom_input < top_input or bottom_input == top_input:
                raise ValueError("Bottom value is less than or equal to top value")

            selected_image_name = values["ImageCreateListbox"][0]
            path = Path(selected_image_name)
            if path.exists():
                template_path, info_path = create.run(
                    image_path=path,
                    left=left_input,
                    top=top_input,
                    right=right_input,
                    bottom=bottom_input,
                )
                if template_path is not None and info_path is not None:
                    load_image_window(template_path, info_path)
        except ValueError:
            console.print_exception()
            sg.popup(
                "Value error/s",
                text_color="red",
                auto_close_duration=2,
                auto_close=True,
                no_titlebar=True,
            )
        except FileNotFoundError:
            console.print_exception()
            sg.popup(
                "FileNotFoundError",
                text_color="red",
                auto_close_duration=2,
                auto_close=True,
                no_titlebar=True,
            )
        except IndexError:
            console.print_exception()
            sg.popup(
                "No selected item",
                text_color="red",
                auto_close_duration=2,
                auto_close=True,
                no_titlebar=True,
            )

    if event == "LeftCreate":
        try:
            int(values["LeftCreate"])
            window["LeftCreateValidation"].update(
                "",
            )
            show_template_create_calculations(window, values)
        except ValueError:
            window["LeftCreateValidation"].update("Invalid value", text_color="red")

    if event == "TopCreate":
        try:
            int(values["TopCreate"])
            window["TopCreateValidation"].update(
                "",
            )
            show_template_create_calculations(window, values)
        except ValueError:
            window["TopCreateValidation"].update("Invalid value", text_color="red")

    if event == "BottomCreate":
        try:
            int(values["BottomCreate"])
            window["BottomCreateValidation"].update(
                "",
            )
            show_template_create_calculations(window, values)
        except ValueError:
            window["BottomCreateValidation"].update("Invalid value", text_color="red")

    if event == "RightCreate":
        try:
            int(values["RightCreate"])
            window["RightCreateValidation"].update(
                "",
            )
            show_template_create_calculations(window, values)
        except ValueError:
            window["RightCreateValidation"].update("Invalid value", text_color="red")

    if event == "FolderCreate":
        path = Path(f"{values["FolderCreate"]}")
        if not path.exists():
            sg.popup(
                f"Invalid Path {path}",
                text_color="red",
                auto_close_duration=2,
                auto_close=True,
                no_titlebar=True,
            )
        else:
            items = load_images_from_directory(path)
            window["ImageCreateListbox"].update(values=items)

    if event == "ImageCreateListbox":
        selected_image_name = values["ImageCreateListbox"][0]
        path = Path(selected_image_name)
        if path.exists():
            selected_image_text = textwrap.fill(f"{path.name}", 20)
            window["SelectedImageCreate"].update(selected_image_text)
        load_image_size_information(
            window=window,
            image_path=selected_image_name,
            function="Create"
        )
    if event == "LoadCreate":
        path = Path(values["FolderCreate"])
        if not path.exists():
            sg.popup(
                f"Invalid Path {path}",
                text_color="red",
                auto_close_duration=2,
                auto_close=True,
                no_titlebar=True,
            )
        else:
            items = load_images_from_directory(path)
            window["ImageCreateListbox"].update(values=items)
