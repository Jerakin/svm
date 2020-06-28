from pathlib import Path
import json
import csv

__all__ = ["SVM", "DEFAULT_HEADER", "SVM_HEADER"]

DEFAULT_HEADER = ("Antal", "Namn", "Exp", "Foil", "Skick", "Pris")
SVM_HEADER = ["SVM ID", "Antal", "Namn", "Exp", "Skick", "Språk", "Signerad", "Foil", "För Byte", "För Sälj", "Dold", "Pris", "Valuta", "Kommentar", "Bild"]


def __load(path):
    with path.open(encoding="utf-8") as fp:
        json_data = json.load(fp)
    return json_data


TRANSLATION_DATA = __load(Path(__file__).parent / "translation.json")


class HeaderList:
    def __init__(self, *args):
        self.list = list(*args)

    def index(self, item):
        for i, _item in enumerate(self.list):
            if item == _item:
                return i

        return None


class Card:
    def __init__(self, header=DEFAULT_HEADER):
        header = HeaderList(header)
        self.index_SVM_ID = header.index("SVM ID")
        self.index_antal = header.index("Antal")
        self.index_namn = header.index("Namn")
        self.index_exp = header.index("Exp")
        self.index_skick = header.index("Skick")
        self.index_sprak = header.index("Språk")
        self.index_signerad = header.index("Signerad")
        self.index_foil = header.index("Foil")
        self.index_for_byte = header.index("För_Byte")
        self.index_for_salj = header.index("För_Sälj")
        self.index_dold = header.index("Dold")
        self.index_pris = header.index("Pris")
        self.index_valuta = header.index("Valuta")
        self.index_kommentar = header.index("Kommentar")
        self.index_bild = header.index("Bild")

        self.SVM_ID = ""
        self.antal = None
        self.namn = None
        self.exp = None
        self.skick = "n/a"
        self.sprak = "n/a"
        self.signerad = "Nej"
        self.foil = "Nej"
        self.for_byte = "Nej"
        self.for_salj = "Nej"
        self.dold = "Ja"
        self.pris = "0"
        self.valuta = "SEK"
        self.kommentar = ""
        self.bild = ""

    @staticmethod
    def _get_item_from_row(csv_row, index, default):
        return csv_row[index] if index is not None else default

    def setup(self, csv_row):
        self.SVM_ID = self._get_item_from_row(csv_row, self.index_SVM_ID, self.SVM_ID)
        self.antal = int(self._get_item_from_row(csv_row, self.index_antal, self.antal).replace("x", ""))
        self.namn = self._get_item_from_row(csv_row, self.index_namn, self.namn)
        self.exp = self._get_item_from_row(csv_row, self.index_exp, self.exp)
        self.skick = self._get_item_from_row(csv_row, self.index_skick, self.skick)
        self.sprak = self._get_item_from_row(csv_row, self.index_sprak, self.sprak)
        self.signerad = self._get_item_from_row(csv_row, self.index_signerad, self.signerad)
        self.foil = self._get_item_from_row(csv_row, self.index_foil, self.foil)
        self.for_byte = self._get_item_from_row(csv_row, self.index_for_byte, self.for_byte)
        self.for_salj = self._get_item_from_row(csv_row, self.index_for_salj, self.for_salj)
        self.dold = self._get_item_from_row(csv_row, self.index_dold, self.dold)
        self.pris = self._get_item_from_row(csv_row, self.index_pris, self.pris)
        self.valuta = self._get_item_from_row(csv_row, self.index_valuta, self.valuta)
        self.kommentar = self._get_item_from_row(csv_row, self.index_kommentar, self.kommentar)
        self.bild = self._get_item_from_row(csv_row, self.index_bild, self.SVM_ID)

        self.skick = self.skick if self.skick else "n/a"
        self.sprak = self.sprak if self.sprak else "n/a"
        self.signerad = self.signerad if self.signerad else "Nej"
        self.foil = self.foil if self.foil else "Nej"
        self.for_byte = self.for_byte if self.for_byte else "Nej"
        self.for_salj = self.for_salj if self.for_salj else "Nej"
        self.dold = self.dold if self.dold else "Ja"
        self.pris = self.pris if self.pris else 0
        self.valuta = self.valuta if self.valuta else "SEK"

        self.validate()

    def validate(self):
        if self.skick not in ['n/a', 'Near Mint', 'Excellent', 'Good', 'Fine', 'Poor']:
            raise ValueError(f"Skick '{self.skick}' is not valid")

        if self.sprak not in ['n/a','Engelska','Italienska','Franska','Tyska','Spanska','Portugisiska','Ryska','Japanska','Koreanska','F. Kinesiska','T. Kinesiska']:
            raise ValueError(f"Språk '{self.sprak}' is not valid")

        if self.foil not in ['Ja', 'Nej']:
            raise ValueError(f"Foil '{self.foil}' is not valid")

        if self.for_byte not in ['Ja', 'Nej']:
            raise ValueError(f"För Byte '{self.for_byte}' is not valid")

        if self.for_salj not in ['Ja', 'Nej']:
            raise ValueError(f"För Sälj '{self.for_salj}' is not valid")

        if self.signerad not in ['Ja', 'Nej']:
            raise ValueError(f"Signerad '{self.signerad}' is not valid")

        if not float(self.pris).is_integer():
            raise ValueError(f"Pris måste vara i hela Kronor")

        if int(self.pris) < 0:
            raise ValueError(f"Pris måste vara mer eller lika med 0")

        if self.for_salj == 'Ja' and self.pris == 0:
            raise TypeError(f"För Sälj kan bara vara 'Ja' ifall 'Pris' är mer än 0")

        if self.valuta not in ['SEK', 'DKK', "NOK"]:
            raise ValueError(f"Valuta '{self.valuta}' is not valid")

        if self.namn is None:
            raise ValueError(f"Kortet måste ha ett namn")

        if self.exp is None:
            raise ValueError(f"Kortet måste ha ett expansion")

    def row(self, overwrite_antal=None):
        exp = TRANSLATION_DATA["expansion_name"][self.exp] if self.exp in TRANSLATION_DATA["expansion_name"] else self.exp
        namn = TRANSLATION_DATA["card_name"][self.namn] if self.namn in TRANSLATION_DATA["card_name"] else self.namn

        # Dual cards in Throne of Eldraine that by convention use // does not do so on SVM
        # But only uses the first of the cards name
        if exp in ["Throne of Eldraine"]:
            namn = namn.split("//")[0].strip()

        return [self.SVM_ID, overwrite_antal if overwrite_antal else self.antal, namn, exp, self.skick, self.sprak, self.signerad, self.foil,
                self.for_byte, self.for_salj, self.dold, int(self.pris), self.valuta, self.kommentar, self.bild]


class SVM:
    def __init__(self, input_csv, expand_antal=True, header=DEFAULT_HEADER, converters=()):
        self.cards = []
        self.expand = expand_antal

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
                        row[index] = con(row[index])
                card = Card(header)
                card.setup(row)
                self.cards.append(card)

    def save(self, file_path):
        with open(file_path, "w", newline="", encoding="utf-8") as fp:
            writer = csv.writer(fp, delimiter="\t")
            writer.writerow(SVM_HEADER)
            for card in self.cards:
                if self.expand:
                    for _ in range(card.antal):
                        writer.writerow(card.row(1))
                else:
                    writer.writerow(card.row())
