from pathlib import Path
import json
import requests
import csv

json_folder = Path(__file__).parent / "json"


class SVM:
    CACHE = []

    def create_cache(self):
        self.CACHE = []
        for x in json_folder.iterdir():
            with x.open("r") as fp:
                json_data = json.load(fp)

                for card in json_data:
                    c = {"name": card["name"], "exp": card["exp"], "id": card["id"]}
                    self.CACHE.append(c)

    def get_id(self, name, exp):
        if len(self.CACHE) == 0:
            self.create_cache()
        for c in self.CACHE:
            if name == c["name"] and exp == c["exp"]:
                return c["id"]


def download_card_data():
    offset = 0
    LIMIT = 2000
    url = "https://www.svenskamagic.com/svmapp_cardfinder.php?type=cards&limit={limit}&offset={offset}"
    output_folder = Path(__file__).parent / "json"

    while True:
        r = requests.get(url.format(limit=LIMIT, offset=offset))
        if r.status_code == 200:
            json_data = json.loads(r.content)

            output = output_folder / "svm_{}-{}.json".format(offset, offset + LIMIT)

            with output.open("w") as fp:
                json.dump(json_data, fp, indent=4)

            if len(json_data) < LIMIT:
                break
            offset += LIMIT

import random
def convert_rnd(input_file, output_file):
    #             0         1       2       3       4       5              6        7        8           9          10       11       12          13
    header =  ["SVM ID", "Antal", "Namn", "Exp", "Skick", "Språk"   , "Signerad", "Foil", "För Byte", "För Sälj" , "Dold", "Pris", "Kommentar", "Bild"]
    default = [""      , ""     , ""    , ""   , ""     , "Engelska", "Nej"     , "Nej" , "Ja"      , "Ja"       , "Nej" , 2     , ""         , ""]

    output = []
    with input_file.open("r") as fp:
        reader = csv.reader(fp)
        next(reader)

        for row in reader:
            SVM_ID = ""
            antal = 1
            namn = '{}'.format(row[1]) if " " in row[1] else row[1]
            exp = '{}'.format(row[2]) if " " in row[2] else row[2]
            skick = ['n/a', 'Near Mint', 'Excellent', 'Good', 'Fine', 'Poor'][random.randint(0, 5)]
            sprak = ['n/a','Engelska','Italienska','Franska','Tyska','Spanska','Portugisiska','Ryska','Japanska','Koreanska','F. Kinesiska','T. Kinesiska'][random.randint(0, 11)]
            signerad = default[6]
            foil = row[3] if row[3] else default[7]
            byte = default[8]
            dold = "Ja" if random.randint(0, 4) > 3 else "Nej"
            pris = random.randint(0, 200)
            salj = "Nej" if pris == 0 else "Ja"
            kommentar = default[12]
            bild = default[13]
            for n in range(antal):
                output.append(
                    ["", 1, namn, exp, skick, sprak, signerad, foil, byte, salj, dold,
                     pris, kommentar, bild])
    print(len(output))
    with output_file.open("w", newline="") as fp:
        writer = csv.writer(fp, delimiter="\t")
        writer.writerow(header)
        for i, row in enumerate(output):
            if i % 50 == 0:
                writer.writerow(row)


def convert(input_file, output_file):
    #             0         1       2       3       4       5              6        7        8           9          10       11       12          13
    header =  ["SVM ID", "Antal", "Namn", "Exp", "Skick", "Språk"   , "Signerad", "Foil", "För Byte", "För Sälj" , "Dold", "Pris", "Kommentar", "Bild"]
    default = [""      , ""     , ""    , ""   , ""     , "Engelska", "Nej"     , "Nej" , "Ja"      , "Ja"       , "Nej" , 2     , ""         , ""]

    output = []
    with input_file.open("r") as fp:
        reader = csv.reader(fp)
        next(reader)

        for row in reader:
            SVM_ID = ""
            antal = int(row[0].replace("x", ""))
            namn = '{}'.format(row[1]) if " " in row[1] else row[1]
            exp = '{}'.format(row[2]) if " " in row[2] else row[2]
            skick = row[4] if row[4] else default[4]
            skick = '{}'.format(skick) if " " in skick else skick
            sprak = default[5]
            signerad = default[6]
            foil = row[3] if row[3] else default[7]
            byte = default[8]
            salj = default[9]
            dold = default[10]
            pris = round(max(float(row[5].replace(",", ".").replace("£", "")) * 10, 2))
            kommentar = default[12]
            bild = default[13]
            for n in range(antal):
                output.append(
                    ["", 1, namn, exp, skick, sprak, signerad, foil, byte, salj, dold,
                     pris, kommentar, bild])
    print(len(output))
    with output_file.open("w", newline="") as fp:
        writer = csv.writer(fp, delimiter="\t")
        writer.writerow(header)
        for row in output:
            writer.writerow(row)


f_input = Path(__file__).parent / "Cards - Commons.csv"
f_output = Path(__file__).parent / "random.csv"
convert_rnd(f_input, f_output)

# f_input = Path(__file__).parent / "Cards - Special.csv"
# f_output = Path(__file__).parent / "special.csv"
# convert(f_input, f_output)
