import csv
import json
from pathlib import Path
from . import converter


def __load(path):
    with path.open(encoding="utf-8") as fp:
        json_data = json.load(fp)
    return json_data


SET_DATA = __load(Path(__file__).parent / "sets.json")


class MoxfieldCard(converter.Card):
    def __init__(self):
        super(MoxfieldCard, self).__init__(converter.SVM_HEADER)

    def row(self, **kwargs):
        exp = SET_DATA[self.exp] if self.exp in SET_DATA else None
        if not exp:
            if self.exp != "-":
                print(f"Could not find {self.exp} in sets.json")
            return [1, self.namn]
        return [1, self.namn, f"({exp})"]

    @staticmethod
    def _get_item_from_row(csv_row, index, default):
        try:
            return csv_row[index] if index is not None else default
        except IndexError:  # We are trying to access something that the exported format doesn't use/have
            return ""


def _bool_converter(index, row):
    return "Nej" if row[index] == "-" else row[index]


def _expand_converter(_converters, index):
    if len(_converters) < index:
        _converters = list(_converters)
        _converters.extend([None]*(index-1-len(_converters)))
        _converters.append(_bool_converter)
    return _converters


class Moxfield:
    def __init__(self, input_csv, converters=()):
        self.cards = []

        # Add "singed" and "foil" converter
        converters = _expand_converter(converters, 7)
        converters = _expand_converter(converters, 8)

        with open(input_csv, "r", encoding="utf-8") as fp:
            # Try to sniff the dialect
            dialect = csv.Sniffer().sniff(fp.read(1024))

            # Seek to beginning
            fp.seek(0)

            reader = csv.reader(fp, dialect)
            next(reader)
            for row in reader:
                for index, con in enumerate(converters):
                    if con:
                        row[index] = con(index, row)
                card = MoxfieldCard()
                card.setup(row)
                self.cards.append(card)

    def save(self, file_path):
        with open(file_path, "w", newline="", encoding="utf-8") as fp:
            writer = csv.writer(fp, delimiter="\t", quoting=csv.QUOTE_NONE)
            for card in self.cards:
                writer.writerow(card.row())
