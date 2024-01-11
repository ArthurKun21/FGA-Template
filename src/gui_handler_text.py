import os
import textwrap
from pathlib import Path

import detect_text
import PySimpleGUI as sg
from gui_components import (
    create_directory_column,
    load_directory_images_column,
    load_image_size_information,
    load_images_from_directory,
    save_directory_settings,
)
from rich.console import Console

console = Console()


def template_text_layout():
    layout = [
        [
            sg.Frame(
                "Directory",
                [
                    [create_directory_column("Text")],
                ],
                expand_x=True,
            )
        ],
        [
            sg.Frame(
                "Images",
                [
                    load_directory_images_column(function="Text"),
                ],
                expand_x=True,
                size=(720, 250),
            )
        ],
        [
            sg.Button("Submit", key="ButtonSubmitText", enable_events=True),
        ],
        [
            sg.Frame(
                "Detect Text",
                [
                    [
                        sg.Push(),
                        sg.Image(filename=None, key="ImageTextDisplay"),
                        sg.Push(),
                    ],
                    [
                        sg.Frame(
                            "Output Text",
                            layout=[
                                [
                                    sg.Multiline(
                                        "",
                                        expand_x=True,
                                        expand_y=True,
                                        key="ImageTextMultiLine"
                                    )
                                ]
                            ],
                            key="ImageTextFrame",
                            expand_x=True,
                            expand_y=True,
                        )
                    ],
                ],
                expand_x=True,
                expand_y=True,
            )
        ],
    ]
    return layout


def template_text_events_handler(window, event, values):
    if event == "ImageTextListbox":
        selected_image_name = values["ImageTextListbox"][0]
        path = Path(selected_image_name)
        if path.exists():
            selected_image_text = textwrap.fill(f"{path.name}", 20)
            window["SelectedImageText"].update(selected_image_text)
            load_image_size_information(
                window=window, image_path=selected_image_name, function="Text"
            )
            window["OpenImageText"].update(visible=True)
    if event == "OpenImageText":
        selected_image_name = values["ImageTextListbox"][0]
        path = Path(selected_image_name)
        if path.exists():
            os.startfile(f"{path}")
    if event == "LoadText":
        path = Path(values["FolderText"])
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
            window["ImageTextListbox"].update(values=items)

    if event == "FolderText":
        path = Path(f"{values["FolderText"]}")
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
            window["ImageTextListbox"].update(values=items)
            save_directory_settings("Text", path)

    if event == "ButtonSubmitText":
        try:
            selected_image_name = values["ImageTextListbox"][0]
            path = Path(selected_image_name)
            if path.exists():
                based_image_np = detect_text.set_image_threshold(
                    image_path=path,
                )
                if based_image_np is not None:
                    output_text = detect_text.detect_text(
                        image_np=based_image_np,
                    )
                    window["ImageTextDisplay"].update(filename=path)
                    window["ImageTextMultiLine"].update(value=output_text)

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
