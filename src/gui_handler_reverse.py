import os
import textwrap
from pathlib import Path

import information_handler
import PySimpleGUI as sg
import reverse
from gui_components import (
    create_directory_column,
    create_information_layout,
    create_operations_layout,
    load_directory_images_column,
    load_image_size_information,
    load_image_window,
    load_images_from_directory,
    text_input_validation,
)
from rich.console import Console

console = Console()


def reverse_values_column():
    values_column = sg.Col(
        [
            [
                sg.Text(
                    "Left",
                    tooltip="Left value of the template",
                ),
                sg.Push(),
                text_input_validation(
                    inputKey="LeftReverse",
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
                    inputKey="TopReverse",
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
                    inputKey="WidthReverse",
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
                    inputKey="HeightReverse",
                    default_text="0",
                    expand_x=False,
                    size=(25, 1),
                    justification="center",
                ),
            ],
        ]
    )
    return values_column


def show_template_reverse_calculations(window, values):
    try:
        left_input = int(values["LeftReverse"])
        top_input = int(values["TopReverse"])
        width_input = int(values["WidthReverse"])
        height_input = int(values["HeightReverse"])

        if (left_input + width_input) < left_input or (
            left_input + width_input
        ) == left_input:
            raise ValueError("Right value is less than or equal to left value")
        if (top_input + height_input) < top_input or (
            top_input + height_input
        ) == top_input:
            raise ValueError("Bottom value is less than or equal to top value")

        operations = [
            "NORMALReverse",
            "CENTERReverse",
            "RIGHTReverse",
        ]
        selected_color = ("red", "white")

        selected_operation = operations[0]
        for operation in operations:
            color = window[operation].ButtonColor
            console.print(
                f"Operation: [blue]{operation}[/blue] Color: [blue]{color}[/blue]"
            )

            if color == selected_color:
                selected_operation = operation.replace("Reverse", "")

        selected_image_name = values["ImageReverseListbox"][0]
        path = Path(selected_image_name)
        if path.exists():
            (
                left_border,
                top_border,
                right_border,
                bottom_border,
                width_template,
                height_template,
            ) = information_handler.fetch_image_manipulation_information_reverse(
                path,
                left_input,
                top_input,
                width=width_input,
                height=height_input,
                selected_measurement_type=selected_operation,
            )
            window["LeftBorderReverseInformation"].update(f"{left_border}")
            window["TopBorderReverseInformation"].update(f"{top_border}")
            window["RightBorderReverseInformation"].update(f"{right_border}")
            window["BottomBorderReverseInformation"].update(f"{bottom_border}")
            window["WidthReverseInformation"].update(f"{width_template}")
            window["HeightReverseInformation"].update(f"{height_template}")
    except ValueError:
        pass
    except FileNotFoundError:
        pass
    except IndexError:
        pass


def template_reverse_layout():
    layout = [
        [
            sg.Frame(
                "Directory",
                [
                    [create_directory_column("Reverse")],
                ],
                expand_x=True,
            )
        ],
        [
            sg.Frame(
                "Images",
                [
                    load_directory_images_column(function="Reverse"),
                ],
                expand_x=True,
                size=(720, 250),
            )
        ],
        [
            sg.Frame(
                "Values",
                [
                    [reverse_values_column()],
                ],
                expand_x=True,
            )
        ],
        [
            sg.Frame(
                "Mode",
                create_operations_layout(function="Reverse"),
                expand_x=True,
            )
        ],
        [
            sg.Button("Submit", key="ButtonSubmitReverse", enable_events=True),
        ],
        [
            sg.Frame(
                "Information",
                create_information_layout(function="Reverse"),
                expand_x=True,
            )
        ],
    ]
    return layout


def template_reverse_events_handler(window, event, values):
    operations = [
        "NORMALReverse",
        "CENTERReverse",
        "RIGHTReverse",
    ]
    selected_color = ("red", "white")
    if event in operations:
        for operation in operations:
            window[operation].update(button_color=sg.theme_button_color())
        window[event].update(button_color=selected_color)
    if event == "ImageReverseListbox":
        selected_image_name = values["ImageReverseListbox"][0]
        path = Path(selected_image_name)
        if path.exists():
            selected_image_text = textwrap.fill(f"{path.name}", 20)
            window["SelectedImageReverse"].update(selected_image_text)
            load_image_size_information(
                window=window, image_path=selected_image_name, function="Reverse"
            )
            window["OpenImageReverse"].update(visible=True)
    if event == "OpenImageReverse":
        selected_image_name = values["ImageReverseListbox"][0]
        path = Path(selected_image_name)
        if path.exists():
            os.startfile(f"{path}")
    if event == "LoadReverse":
        path = Path(values["FolderReverse"])
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
            window["ImageReverseListbox"].update(values=items)
    if event == "FolderReverse":
        path = Path(f"{values["FolderReverse"]}")
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
            window["ImageReverseListbox"].update(values=items)
    if event == "ButtonSubmitReverse":
        try:
            left_input = int(values["LeftReverse"])
            top_input = int(values["TopReverse"])
            width_input = int(values["WidthReverse"])
            height_input = int(values["HeightReverse"])

            if (left_input + width_input) < left_input or (
                left_input + width_input
            ) == left_input:
                raise ValueError("Right value is less than or equal to left value")
            if (top_input + height_input) < top_input or (
                top_input + height_input
            ) == top_input:
                raise ValueError("Bottom value is less than or equal to top value")

            selected_operation = operations[0]
            for operation in operations:
                color = window[operation].ButtonColor
                console.print(
                    f"Operation: [blue]{operation}[/blue] Color: [blue]{color}[/blue]"
                )

                if color == selected_color:
                    selected_operation = operation.replace("Reverse", "")

            selected_image_name = values["ImageReverseListbox"][0]
            path = Path(selected_image_name)
            if path.exists():
                template_path, info_path = reverse.run(
                    image_path=path,
                    left=left_input,
                    top=top_input,
                    width=width_input,
                    height=height_input,
                    extra=selected_operation,
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
            )

    if event == "LeftReverse":
        try:
            int(values["LeftReverse"])
            window["LeftReverseValidation"].update(
                "",
            )
            show_template_reverse_calculations(window, values)
        except ValueError:
            window["LeftReverseValidation"].update("Invalid value", text_color="red")

    if event == "WidthReverse":
        try:
            int(values["WidthReverse"])
            window["WidthReverseValidation"].update(
                "",
            )
            show_template_reverse_calculations(window, values)
        except ValueError:
            window["WidthReverseValidation"].update("Invalid value", text_color="red")

    if event == "TopReverse":
        try:
            int(values["TopReverse"])
            window["TopReverseValidation"].update(
                "",
            )
            show_template_reverse_calculations(window, values)
        except ValueError:
            window["TopReverseValidation"].update("Invalid value", text_color="red")

    if event == "HeightReverse":
        try:
            int(values["HeightReverse"])
            window["HeightReverseValidation"].update(
                "",
            )
            show_template_reverse_calculations(window, values)
        except ValueError:
            window["HeightReverseValidation"].update("Invalid value", text_color="red")
