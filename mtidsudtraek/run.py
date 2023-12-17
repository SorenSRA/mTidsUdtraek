from pathlib import Path  # core python module
from os.path import join, basename
import datetime

import pandas as pd  # pip install pandas openpyxl
import PySimpleGUI as sg  # pip install pysimplegui

# import af egne moduler
from windows_GUI.settingswindow import settings_window
from lav_mtidsudtraek import lav_tidsudtraek


def main_window():
    default_folder = settings["PROGRAM"]["outputfolder_default"]
    # ------ GUI Definition ------ #
    layout = [
        [sg.Text("", s=20)],
        [
            sg.T("Input File:", s=15, justification="r"),
            sg.I(s=60, key="-IN-"),
            sg.FileBrowse(
                initial_folder=default_folder, file_types=(("Excel Files", "*.xls*"),)
            ),
        ],
        [
            sg.T("Output Folder:", s=15, justification="r"),
            sg.I(s=60, default_text=default_folder, key="-OUT-"),
            sg.FolderBrowse(initial_folder=default_folder),
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
            window.disappear()
            file_name_indlaes = basename(values["-IN-"])
            current_date = datetime.date.today().strftime("%Y_%m_%d")
            file_name_newudtraek = current_date + file_name_indlaes
            file_path_newudtraek = join(values["-OUT-"], file_name_newudtraek)
            lav_tidsudtraek(values["-IN-"], file_path_newudtraek)

            sg.popup_no_titlebar(f"Nyt Tidsudtræk dannet: {file_name_newudtraek}")

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
