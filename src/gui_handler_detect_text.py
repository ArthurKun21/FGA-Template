import os
import textwrap
from pathlib import Path

import detect_text
import information_handler
import PySimpleGUI as sg
from gui_components import (
    create_directory_column,
    create_information_layout,
    create_operations_layout,
    load_directory_images_column,
    load_image_size_information,
    load_image_window,
    load_images_from_directory,
    text_input_validation,
    save_directory_settings
)
from rich.console import Console

console = Console()


def DetectText_values_column():
    values_column = sg.Col(
        [
            [
                sg.Text(
                    "Left",
                    tooltip="Left value of the template",
                ),
                sg.Push(),
                text_input_validation(
                    inputKey="LeftDetectText",
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
                    inputKey="TopDetectText",
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
                    inputKey="WidthDetectText",
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
                    inputKey="HeightDetectText",
                    default_text="0",
                    expand_x=False,
                    size=(25, 1),
                    justification="center",
                ),
            ],
        ]
    )
    return values_column


def show_template_DetectText_calculations(window, values):
    try:
        left_input = int(values["LeftDetectText"])
        top_input = int(values["TopDetectText"])
        width_input = int(values["WidthDetectText"])
        height_input = int(values["HeightDetectText"])

        if (left_input + width_input) < left_input or (
            left_input + width_input
        ) == left_input:
            raise ValueError("Right value is less than or equal to left value")
        if (top_input + height_input) < top_input or (
            top_input + height_input
        ) == top_input:
            raise ValueError("Bottom value is less than or equal to top value")

        operations = [
            "NORMALDetectText",
            "CENTERDetectText",
            "RIGHTDetectText",
        ]
        selected_color = ("red", "white")

        selected_operation = operations[0]
        for operation in operations:
            color = window[operation].ButtonColor
            console.print(
                f"Operation: [blue]{operation}[/blue] Color: [blue]{color}[/blue]"
            )

            if color == selected_color:
                selected_operation = operation.replace("DetectText", "")

        selected_image_name = values["ImageDetectTextListbox"][0]
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
            window["LeftBorderDetectTextInformation"].update(f"{left_border}")
            window["TopBorderDetectTextInformation"].update(f"{top_border}")
            window["RightBorderDetectTextInformation"].update(f"{right_border}")
            window["BottomBorderDetectTextInformation"].update(f"{bottom_border}")
            window["WidthDetectTextInformation"].update(f"{width_template}")
            window["HeightDetectTextInformation"].update(f"{height_template}")
    except ValueError:
        pass
    except FileNotFoundError:
        pass
    except IndexError:
        pass


def template_detect_text_layout():
    layout = [
        [
            sg.Frame(
                "Directory",
                [
                    [create_directory_column("DetectText")],
                ],
                expand_x=True,
            )
        ],
        [
            sg.Frame(
                "Images",
                [
                    load_directory_images_column(function="DetectText"),
                ],
                expand_x=True,
                size=(720, 250),
            )
        ],
        [
            sg.Frame(
                "Values",
                [
                    [DetectText_values_column()],
                ],
                expand_x=True,
            )
        ],
        [
            sg.Frame(
                "Mode",
                create_operations_layout(function="DetectText"),
                expand_x=True,
            )
        ],
        [
            sg.Button("Submit", key="ButtonSubmitDetectText", enable_events=True),
        ],
        [
            sg.Frame(
                "Information",
                create_information_layout(function="DetectText"),
                expand_x=True,
            )
        ],
    ]
    return layout


def template_detect_text_events_handler(window, event, values):
    operations = [
        "NORMALDetectText",
        "CENTERDetectText",
        "RIGHTDetectText",
    ]
    selected_color = ("red", "white")
    if event in operations:
        for operation in operations:
            window[operation].update(button_color=sg.theme_button_color())
        window[event].update(button_color=selected_color)
    if event == "ImageDetectTextListbox":
        selected_image_name = values["ImageDetectTextListbox"][0]
        path = Path(selected_image_name)
        if path.exists():
            selected_image_text = textwrap.fill(f"{path.name}", 20)
            window["SelectedImageDetectText"].update(selected_image_text)
            load_image_size_information(
                window=window, image_path=selected_image_name, function="DetectText"
            )
            window["OpenImageDetectText"].update(visible=True)
    if event == "OpenImageDetectText":
        selected_image_name = values["ImageDetectTextListbox"][0]
        path = Path(selected_image_name)
        if path.exists():
            os.startfile(f"{path}")
            
    if event == "LoadDetectText":
        path = Path(values["FolderDetectText"])
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
            window["ImageDetectTextListbox"].update(values=items)
            save_directory_settings("DetectText", path)

    if event == "FolderDetectText":
        path = Path(f"{values["FolderDetectText"]}")
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
            window["ImageDetectTextListbox"].update(values=items)
    if event == "ButtonSubmitDetectText":
        try:
            left_input = int(values["LeftDetectText"])
            top_input = int(values["TopDetectText"])
            width_input = int(values["WidthDetectText"])
            height_input = int(values["HeightDetectText"])

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
                    selected_operation = operation.replace("DetectText", "")

            selected_image_name = values["ImageDetectTextListbox"][0]
            path = Path(selected_image_name)
            if path.exists():
                template_path, info_path, output_text = detect_text.run(
                    image_path=path,
                    left=left_input,
                    top=top_input,
                    width=width_input,
                    height=height_input,
                    extra=selected_operation,
                )
                if template_path is not None and info_path is not None:
                    load_image_window(template_path, info_path, output_text=output_text)
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

    if event == "LeftDetectText":
        try:
            int(values["LeftDetectText"])
            window["LeftDetectTextValidation"].update(
                "",
            )
            show_template_DetectText_calculations(window, values)
        except ValueError:
            window["LeftDetectTextValidation"].update("Invalid value", text_color="red")

    if event == "WidthDetectText":
        try:
            int(values["WidthDetectText"])
            window["WidthDetectTextValidation"].update(
                "",
            )
            show_template_DetectText_calculations(window, values)
        except ValueError:
            window["WidthDetectTextValidation"].update(
                "Invalid value", text_color="red"
            )

    if event == "TopDetectText":
        try:
            int(values["TopDetectText"])
            window["TopDetectTextValidation"].update(
                "",
            )
            show_template_DetectText_calculations(window, values)
        except ValueError:
            window["TopDetectTextValidation"].update("Invalid value", text_color="red")

    if event == "HeightDetectText":
        try:
            int(values["HeightDetectText"])
            window["HeightDetectTextValidation"].update(
                "",
            )
            show_template_DetectText_calculations(window, values)
        except ValueError:
            window["HeightDetectTextValidation"].update(
                "Invalid value", text_color="red"
            )
