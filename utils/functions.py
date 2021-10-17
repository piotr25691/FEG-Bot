import datetime

from dateutil import parser
from epicstore_api import EpicGamesStoreAPI

api = EpicGamesStoreAPI()


def get_curr_free():
    json = [g for g in api.get_free_games()["data"]["Catalog"]["searchStore"]["elements"]]
    for e in json:
        try:
            if datetime.datetime.now().date() >= parser.parse(e["promotions"]["promotionalOffers"][0]
                                                              ["promotionalOffers"][0]["startDate"]).date() and \
                    e["price"]["totalPrice"]["fmtPrice"]["discountPrice"] == "0":
                return e
        except (TypeError, IndexError):
            pass
    return


def get_next_free():
    json = [g for g in api.get_free_games()["data"]["Catalog"]["searchStore"]["elements"]]
    for e in reversed(json[:-1]):
        return e


def find_dict(li, k, v):
    for i, d in enumerate(li):
        if d[k] == v:
            return i
    return -1
