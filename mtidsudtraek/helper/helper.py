import shutil
import pandas as pd
from os.path import exists
from os.path import join
import datetime


def indlaes_excelark(file_path, sheetname):
    try:
        return pd.read_excel(file_path, sheet_name=sheetname)
    except FileNotFoundError:
        return f"Indlæsningsfilen {file_path} findes ikke!"
    except ValueError:
        return f"Arket {sheetname} findes ikke i indlæsningsfilen!"


def kopi_fil(source, destination):
    try:
        shutil.copy(source, destination)
        return (0, f"{destination} er nu dannet")
    except FileNotFoundError:
        return (99, f"Indlæsningsfilen {source} findes ikke!")


def file_exists(file_name: str) -> bool:
    if exists(file_name):
        return True
    else:
        return False


def folder_exists(folder_name: str) -> bool:
    if exists(folder_name):
        return True
    else:
        return False


def create_file_path_name(path_name: str, file_name_basis: str) -> str:
    current_date = datetime.date.today().strftime("%Y%m%d")
    file_name = current_date + "_" + file_name_basis
    return join(path_name, file_name)
