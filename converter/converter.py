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
        self.antal = "1"
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

    def setup(self, csv_row):
        self.SVM_ID = csv_row[self.index_SVM_ID] if self.index_SVM_ID else self.SVM_ID
        self.antal = csv_row[self.index_antal] if self.index_antal else self.antal
        self.namn = csv_row[self.index_namn] if self.index_namn else self.namn
        self.exp = csv_row[self.index_exp] if self.index_exp else self.exp
        self.skick = csv_row[self.index_skick] if self.index_skick else self.skick
        self.sprak = csv_row[self.index_sprak] if self.index_sprak else self.sprak
        self.signerad = csv_row[self.index_signerad] if self.index_signerad else self.signerad
        self.foil = csv_row[self.index_foil] if self.index_foil else self.foil
        self.for_byte = csv_row[self.index_for_byte] if self.index_for_byte else self.for_byte
        self.for_salj = csv_row[self.index_for_salj] if self.index_for_salj else self.for_salj
        self.dold = csv_row[self.index_dold] if self.index_dold else self.dold
        self.pris = float(csv_row[self.index_pris]) if self.index_pris else self.pris
        self.valuta = csv_row[self.index_valuta] if self.index_valuta else self.valuta
        self.kommentar = csv_row[self.index_kommentar] if self.index_kommentar else self.kommentar
        self.bild = csv_row[self.index_bild] if self.index_bild else self.bild

        self.antal = int(self.antal.replace("x", "")) if self.antal else "1"
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

    def row(self, antal=None):
        exp = TRANSLATION_DATA["expansion_name"][self.exp] if self.exp in TRANSLATION_DATA["expansion_name"] else self.exp
        namn = TRANSLATION_DATA["card_name"][self.namn] if self.namn in TRANSLATION_DATA["card_name"] else self.namn

        # Dual cards in Throne of Eldraine that by convention use // does not do so on SVM
        # But only uses the first of the cards name
        if exp in ["Throne of Eldraine"]:
            namn = namn.split("//")[0].strip()

        return [self.SVM_ID, antal if antal else self.antal, namn, exp, self.skick, self.sprak, self.signerad, self.foil,
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
                        writer.writerow(card.row(antal=1))
                else:
                    writer.writerow(card.row())
