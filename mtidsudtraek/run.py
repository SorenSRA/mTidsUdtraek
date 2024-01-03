from pathlib import Path  # core python module

import pandas as pd  # pip install pandas openpyxl
import PySimpleGUI as sg  # pip install pysimplegui

# import af egne moduler
from windows_GUI.settingswindow import settings_window
from lav_mtidsudtraek import lav_tidsudtraek
from helper.helper import file_exists, folder_exists, create_file_path_name


def main_window():
    input_default_folder = settings["PROGRAM"]["inputfolder_default"]
    output_default_folder = settings["PROGRAM"]["outputfolder_default"]
    # ------ GUI Definition ------ #
    layout = [
        [sg.Text("", s=20)],
        [
            sg.T("Input File:", s=15, justification="r"),
            sg.I(s=60, key="-IN-"),
            sg.FileBrowse(
                initial_folder=input_default_folder,
                file_types=(("Excel Files", "*.xls*"),),
            ),
        ],
        [
            sg.T("Output Folder:", s=15, justification="r"),
            sg.I(s=60, default_text=output_default_folder, key="-OUT-"),
            sg.FolderBrowse(initial_folder=output_default_folder),
        ],
        [sg.Text("", s=20)],
        [
            sg.Text("", s=20),
            sg.Exit(s=15, button_color="tomato"),
            sg.B("Settings", s=15),
            sg.B("Lav nyt Tidsudtræk", s=15),
            sg.Text("", s=20),
        ],
    ]

    window_title = " " * 80 + settings["GUI"]["title"] + " " * 80
    window = sg.Window(window_title, layout, use_custom_titlebar=True)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break
        if event == "Settings":
            window.disappear()
            sg.popup_no_titlebar("Settings Ikke implementeret!")
            # settings_window(settings)
            window.reappear()
            window.bring_to_front()

        if event == "Lav nyt Tidsudtræk":
            if file_exists(values["-IN-"]) and folder_exists(values["-OUT-"]):
                file_path_newudtraek = create_file_path_name(
                    values["-OUT-"], settings["PROGRAM"]["basis_file_name"]
                )
                lav_tidsudtraek(values["-IN-"], file_path_newudtraek)
                window.disappear()
                sg.popup_no_titlebar(f"Nyt Tidsudtræk dannet: {file_path_newudtraek}")
            else:
                window.disappear()
                sg.popup_no_titlebar(
                    f'Fejl i filnavn: {values["-IN-"]} \neller \nmappenavn: {values["-OUT-"]}'
                )
            window.reappear()
            window.bring_to_front()

    window.close()


if __name__ == "__main__":
    SETTINGS_PATH = Path.cwd()
    # create the settings object and use ini format
    settings = sg.UserSettings(
        path=SETTINGS_PATH,
        filename="tidudtraek.ini",
        use_config_file=True,
        convert_bools_and_none=True,
    )
    theme = settings["GUI"]["theme"]
    font_family = settings["GUI"]["font_family"]
    font_size = int(settings["GUI"]["font_size"])
    sg.theme(theme)
    sg.set_options(font=(font_family, font_size))
    main_window()
