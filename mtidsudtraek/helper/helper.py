import shutil
import pandas as pd


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
