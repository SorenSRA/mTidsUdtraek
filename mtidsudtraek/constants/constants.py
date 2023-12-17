# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 12:18:25 2023

@author: B006207
"""
from os.path import join

from dataclasses import dataclass


@dataclass
class ColStruktur:
    col_name: str
    std_data: str


DRILL_SHEET = "Drill-through"
GRUNDDATA_SHEET = "SRATidGrunddata"
TIDSREG_SHEET = "TidsRegATD"
OPGAVE_SHEET = "Opgave"
LOKALOPGAVE_SHEET = "LokalOpgave"

SRAOPGAVE_COL = ColStruktur("SRA_Opgave", "")
SRAMEDARB_COL = ColStruktur("SRA_MedArb", "")
SRAMAANED_COL = ColStruktur("SRA_Maaned", "")
SRAACTION_COL = ColStruktur("SRA_Action", "")

# Kolonnenavne i LIS-mTidsudtræk
STED_COL = r"Sted Sted.Dim_Sted"
MEDARB_COL = "Medarbejder"
MEDARBTYPE_COL = "Medarbejdertype Medarbejdertypetekst"
MANED_COL = "Tid Tid.Måned"
TIMER_COL = "Timer"
LIS_LOKALOPGAVE_COL = "Lokalopgave LokalopgaveKey"
LIS_OPGAVE_COL = "Opgave Dim Opgave"

# Kolonnenavne i OpgaveNumre.excel arket, bruges til opslag
LOKALOPGAVE_COL = "Lokalopgave"
OPGAVE_COL = "Opgave"
ACTION_COL = "Action"
PROJEKT_COL = "Projekt"

GRUNDDATA_START_COL = 5
TIDSREG_START_COL = 0
TEXT_CONDITION = "LIFE|H2020"

GRUNDDATA_NEW_COL = [SRAMAANED_COL, SRAACTION_COL, SRAOPGAVE_COL]
TIDSREG_NEW_COL = [SRAOPGAVE_COL, SRAMEDARB_COL, SRAMAANED_COL, SRAACTION_COL]
TIDSREG_COL_RKFOLGE = [
    SRAOPGAVE_COL.col_name,
    SRAMEDARB_COL.col_name,
    STED_COL,
    SRAMAANED_COL.col_name,
    SRAACTION_COL.col_name,
    TIMER_COL,
    MEDARBTYPE_COL,
]

PATH_OPGAVE = r"F:\EUOkonomi\LIFE-Okonomi\Opfolgning\SystemFiler"  # Kan evt. flyttes til .ini-fil (setup)
PATH_SKABELON = r"F:\EUOkonomi\LIFE-Okonomi\Opfolgning\SystemFiler"  # Kan evt. flyttes til .ini-fil (setup)


FILE_NAME_OPGAVE = "OpgaveNumre.xlsx"
FILE_NAME_SKABELON = "SKABELON_TID_Dimensionsanalyse.xlsx"

FILE_PATH_OPGAVE = join(PATH_OPGAVE, FILE_NAME_OPGAVE)
FILE_PATH_SKABELON = join(PATH_SKABELON, FILE_NAME_SKABELON)
