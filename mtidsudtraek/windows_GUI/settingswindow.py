import PySimpleGUI as sg  # pip install pysimplegui


def settings_window(settings):
    # ------ GUI Definition ------ #
    layout = [
        [sg.T("Opsætning", s=11, justification="r")],
        [
            sg.T("Title:", s=11, justification="r"),
            sg.I(settings["GUI"]["title"], s=20, key="-TITLE-"),
        ],
        [
            sg.T("Sheet Name:", s=11, justification="r"),
            sg.I(settings["EXCEL"]["sheet_name"], s=20, key="-SHEET_NAME-"),
        ],
        [sg.Exit(s=20, button_color="tomato"), sg.B("Gem Settings", s=20)],
    ]

    window = sg.Window("Opsætning", layout, modal=True, use_custom_titlebar=True)
    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break
        if event == "Gem Settings":
            # Write to ini file
            settings["GUI"]["title"] = values["-TITLE-"]
            settings["EXCEL"]["sheet_name"] = values["-SHEET_NAME-"]

            # Display success message & close window
            window.disappear()
            sg.popup_no_titlebar("Settings saved!")
            break
    window.close()
