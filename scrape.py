from bs4 import BeautifulSoup
import requests

card_info = "https://www.svenskamagic.com/kortparmen/index.php?cardid={}"

payload = {"loginusername": "",
           "password": ""}

class Card:
    def __init__(self):
        self.median = 0
        self.average_value = 0
        self.average_movement = 0
        self.sold = 0
        self.for_sale = []


class status:
    OK = 200


def get_for_sale(web_content):
    pass


def get_html_for_card(card_id):
    r = requests.get(card_info.format(card_id))
    if r.status_code == status.OK:
        return r.content


def _get_card(card_id):
    html_content = get_html_for_card(card_id)
    soup = BeautifulSoup(html_content, 'html.parser')
    result = soup.find_all("fieldset")
    print(result)

def get_card(name):
    pass

_get_card(36747)