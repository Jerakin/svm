import converter.converter as svm
from pathlib import Path


def pris(index, row):
    # My price is in Pound, from a different website. I want to use that price but lazily convert it to SEK and have a
    # minimum price of 2
    return round(max(float(row[index].replace(",", ".").replace("£", "")) * 10, 2))


def foil(index, row):
    # The website I export from have "Foil" as the text if it is a foil.
    return "Ja" if row[index] == "Foil" else "Nej"


# We want to overwrite some of the default values
salj_index = svm.SVM_HEADER.index("För Sälj")
byte_index = svm.SVM_HEADER.index("För Byte")
svm.SVM_DEFAULT[salj_index] = "Ja"
svm.SVM_DEFAULT[byte_index] = "Ja"

s = svm.SVM(Path(__file__).parent / "input_example.csv", converters=(None, None, None, foil, None, pris))
s.save(Path(__file__).parent / "output_example.csv")
