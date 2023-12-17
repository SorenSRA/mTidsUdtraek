import re


# returnere de initialer der findes i parentes i en medarbejder-tekststreng
# ala "Rasmussen, Søren (SRA)" -> "sra"
def find_ini(navn: str) -> str:
    pattern = r"\(([a-zA-Z]+)\)"
    matches = re.findall(pattern, navn)
    if not len(matches) == 0:
        return matches[0].lower()
    else:
        return "Ukendt"


# returnere de første 3 tegn i en tekst-streng måned
# ala "December" -> "Dec"
def find_maned(maned: str) -> str:
    if len(maned) >= 3:
        return maned[:3]
    else:
        return "???"
