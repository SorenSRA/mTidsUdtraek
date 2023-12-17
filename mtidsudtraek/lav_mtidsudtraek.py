# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 07:18:19 2023

@author: B006207
"""
# import af egne moduler
import constants.constants as c
from ownfunc.ownfunc import find_ini
from ownfunc.ownfunc import find_maned
from helper.helper import indlaes_excelark
from helper.helper import kopi_fil

# import af standard moduler
import pandas as pd
from sys import exit
from os.path import join, basename
import datetime


def indsat_col(df, new_cols: list, pos: int):
    for col in new_cols:
        df.insert(loc=pos, column=col.col_name, value=col.std_data)
        pos += 1

    return df


def opdater_tidsreg(df, df_opgave, df_lokalopgave):
    for index, _ in df.iterrows():
        df.loc[index, c.SRAMAANED_COL.col_name] = find_maned(df.loc[index, c.MANED_COL])
        df.loc[index, c.SRAMEDARB_COL.col_name] = find_ini(df.loc[index, c.MEDARB_COL])
        df.loc[index, c.SRAACTION_COL.col_name] = find_action(
            df_opgave,
            df_lokalopgave,
            df.loc[index, c.LIS_OPGAVE_COL],
            df.loc[index, c.LIS_LOKALOPGAVE_COL],
        )

        df.loc[index, c.SRAOPGAVE_COL.col_name] = find_projekt(
            df_opgave, df.loc[index, c.LIS_OPGAVE_COL]
        )

    df = df[c.TIDSREG_COL_RKFOLGE]

    return df


def opdater_grunddata(df, df_opgave, df_lokalopgave):
    for index, _ in df.iterrows():
        df.loc[index, c.SRAMAANED_COL.col_name] = find_maned(df.loc[index, c.MANED_COL])
        df.loc[index, c.SRAACTION_COL.col_name] = find_action(
            df_opgave,
            df_lokalopgave,
            df.loc[index, c.LIS_OPGAVE_COL],
            df.loc[index, c.LIS_LOKALOPGAVE_COL],
        )

        df.loc[index, c.SRAOPGAVE_COL.col_name] = find_projekt(
            df_opgave, df.loc[index, c.LIS_OPGAVE_COL]
        )

    return df


def lav_df_fra_excel(file_path: str, sheetname: str):
    df = indlaes_excelark(file_path, sheetname)
    if isinstance(df, pd.DataFrame):
        print(f"OK - {file_path} - {sheetname}")
        return df
    else:
        print(df)
        exit(99)


def find_projekt(df_opgave, opgave: str) -> str:
    if opgave[:6].isdigit():
        opg = int(opgave[:6])
    else:
        return "???"

    if opg in df_opgave.index:
        return df_opgave.loc[opg, c.PROJEKT_COL]
    else:
        return "IR"


def find_action(df_opgave, df_lokalopgave, opgave: str, lokalopgave: str) -> str:
    if opgave[:6].isdigit():
        opg = int(opgave[:6])
    else:
        return "???"

    if opg in df_opgave.index:
        if df_opgave.loc[opg, c.ACTION_COL] != "Bev":
            return df_opgave.loc[opg, c.ACTION_COL]
        else:
            if lokalopgave[:6].isdigit():
                lok = int(lokalopgave[:6])
                if lok in df_lokalopgave.index:
                    return df_lokalopgave.loc[lok, c.ACTION_COL]
                else:
                    return "???"

            else:
                return "???"

    else:
        return "IR"


def slet_rk(df):
    rk_behold = df[c.LIS_OPGAVE_COL].str.upper().str.contains(c.TEXT_CONDITION)
    return df[rk_behold]


def lav_tidsudtraek(file_path_indlaes, file_path_newudtraek):
    # Opret dataframes der skal gemmes i Excel-opfølgningsarket
    df_drill = lav_df_fra_excel(file_path_indlaes, c.DRILL_SHEET)
    df_grunddata = slet_rk(df_drill)
    df_tidsreg = df_grunddata.copy()

    # Opret dataframes der bruges til diverse opslag.
    df_opgave = lav_df_fra_excel(c.FILE_PATH_OPGAVE, c.OPGAVE_SHEET)
    df_lokalopgave = lav_df_fra_excel(c.FILE_PATH_OPGAVE, c.LOKALOPGAVE_SHEET)

    # set index til at være opgaveNr og LokalopgaveNr, lettere at lave opslag df.loc[index]
    df_opgave.set_index(c.OPGAVE_COL, inplace=True)
    df_lokalopgave.set_index(c.LOKALOPGAVE_COL, inplace=True)

    # indsæt de manglende kolonner, basisoplysninger hentes fra Constants
    df_grunddata = indsat_col(df_grunddata, c.GRUNDDATA_NEW_COL, c.GRUNDDATA_START_COL)
    df_tidsreg = indsat_col(df_tidsreg, c.TIDSREG_NEW_COL, c.TIDSREG_START_COL)

    # Opdater tidsreg-dataframe
    df_tidsreg = opdater_tidsreg(df_tidsreg, df_opgave, df_lokalopgave)

    # Opdater grunddata-dataframe
    df_grunddata = opdater_grunddata(df_grunddata, df_opgave, df_lokalopgave)

    # kopier skabelon-filen til den nye udtræksfil bør udviddes således at det ikke er nødvendigt at angive
    # destination fil navnet -bør autogenereres udestår
    kopi_fil(c.FILE_PATH_SKABELON, file_path_newudtraek)

    #
    with pd.ExcelWriter(
        file_path_newudtraek, mode="a", if_sheet_exists="replace"
    ) as writer:
        # Insert the DataFrame into an Excel sheet
        df_drill.to_excel(writer, sheet_name=c.DRILL_SHEET, index=False)
        df_grunddata.to_excel(writer, sheet_name=c.GRUNDDATA_SHEET, index=False)
        df_tidsreg.to_excel(writer, sheet_name=c.TIDSREG_SHEET, index=False)


if __name__ == "__main__":
    file_path_indlaes = r"C:\Filkassen\LIFE-Systemudvikling Mm\Python\mTidsUdtraek\Data\Gammel20231023TID_Dimensionsanalyse.xlsx"
    file_name_indlaes = basename(file_path_indlaes)
    path_newudtraek = r"C:\Filkassen\LIFE-Systemudvikling Mm\Python\mTidsUdtraek\Data"
    current_date = datetime.date.today().strftime("%Y_%m_%d")
    file_name_newudtraek = current_date + file_name_indlaes
    file_path_newudtraek = join(path_newudtraek, file_name_newudtraek)

    print(file_path_indlaes)
    print(file_path_newudtraek)

    lav_tidsudtraek(file_path_indlaes, file_path_newudtraek)
