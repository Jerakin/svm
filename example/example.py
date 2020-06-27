import converter.converter as svm
from pathlib import Path


def pris(value):
    return round(max(float(value.replace(",", ".").replace("£", "")) * 10, 2))


def foil(value):
    return "Ja" if value else "Nej"


s = svm.SVM(Path(__file__).parent / "input_example.csv", converters=(None, None, None, foil, None, pris))
s.save(Path(__file__).parent / "output_example.csv")
