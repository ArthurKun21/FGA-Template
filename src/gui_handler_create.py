import textwrap
from pathlib import Path

import create
import image_handler
import information_handler
import PySimpleGUI as sg
from gui_components import load_image_window, text_input_validation
from rich.console import Console

console = Console()

cwd = Path(__file__).cwd()
image_extensions = [".png", ".jpg"]


def create_directory_column():
    directory_column = sg.Col(
        [
            [
                sg.Text("Folder"),
                sg.Input(f"{cwd}", key="FolderCreate", enable_events=True),
                sg.FolderBrowse(key="FolderBrowseCreate", enable_events=True),
                sg.Button("Load", key="LoadCreate", enable_events=True),
            ],
        ],
        key="Add Column",
        expand_x=True,
        expand_y=True,
    )
    return directory_column


def load_images_from_directory(dir_path: Path):
    return [
        f"{x}"
        for x in dir_path.iterdir()
        if x.is_file() and x.suffix in image_extensions
    ]


def load_image_size_information(window, image_path: Path):
    image_width, image_height = image_handler.get_size(image_path)
    window["ImageWidthCreate"].update(f"{image_width}")
    window["ImageHeightCreate"].update(f"{image_height}")


def load_directory_images_column():
    images_column = [
        sg.Col(
            [
                [
                    sg.Listbox(
                        values=load_images_from_directory(cwd),
                        size=(40, 20),
                        key="ImageCreateListbox",
                        enable_events=True,
                    ),
                ]
            ],
            expand_x=True,
            justification="left",
        ),
        sg.Col(
            [
                [
                    sg.Text("File name"),
                ],
                [
                    sg.Text(
                        "",
                        key="SelectedImageCreate",
                        size=(20, None),
                    ),
                ],
                [
                    sg.Text("Width"),
                ],
                [
                    sg.Text("", key="ImageWidthCreate"),
                ],
                [
                    sg.Text("Height"),
                ],
                [
                    sg.Text("", key="ImageHeightCreate"),
                ],
            ],
            justification="center",
            expand_x=True,
        ),
    ]
    return images_column


def create_values_column():
    left_top_column = sg.Col(
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
    return left_top_column


def template_create_layout():
    layout = [
        [
            sg.Frame(
                "File",
                [
                    [create_directory_column()],
                ],
                expand_x=True,
            )
        ],
        [
            sg.Frame(
                "Images",
                [
                    load_directory_images_column(),
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
                create_information_layout(),
            )
        ],
    ]
    return layout

def create_information_layout():
    layout = [
        [
            sg.Text("Left Border"),
            sg.Push(),
            sg.Text("", key="LeftBorderInformation"),
            sg.Push(),
            sg.Text("Top Border"),
            sg.Push(),
            sg.Text("", key="TopBorderInformation"),
        ],
        [
            sg.Text("Right Border"),
            sg.Push(),
            sg.Text("", key="RightBorderInformation"),
            sg.Push(),
            sg.Text("Bottom Border"),
            sg.Push(),
            sg.Text("", key="BottomBorderInformation"),
        ],
        [
            sg.Text("Template Width"),
            sg.Push(),
            sg.Text("", key="WidthInformation"),
            sg.Push(),
            sg.Text("Template Height"),
            sg.Push(),
            sg.Text("", key="HeightInformation"),
        ]
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
            window["LeftBorderInformation"].update(f"{left_border}")
            window["TopBorderInformation"].update(f"{top_border}")
            window["RightBorderInformation"].update(f"{right_border}")
            window["BottomBorderInformation"].update(f"{bottom_border}")
            window["WidthInformation"].update(f"{width_template}")
            window["HeightInformation"].update(f"{height_template}")
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
        console.print(f"Loading images from {values['FolderCreate']}")
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
            console.print(f"Loading images from {items}")
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
            console.print(f"Loading images from {items}")
            window["ImageCreateListbox"].update(values=items)
