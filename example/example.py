import converter.converter as svm
from pathlib import Path


def pris(value):
    # My price is in Pound, from a different website. I want to use that price but lazily convert it to SEK and have a
    # minimum price of 2
    return round(max(float(value.replace(",", ".").replace("£", "")) * 10, 2))


def foil(value):
    # The website I export from have "Foil" as the text if it is a foil.
    return "Ja" if value else "Nej"


s = svm.SVM(Path(__file__).parent / "input_example.csv", converters=(None, None, None, foil, None, pris))
s.save(Path(__file__).parent / "output_example.csv")
