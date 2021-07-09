import decimal
import json
import urllib
import re
from base_controller import BaseController


"""
Using json instead of parsing HTML
"""
class BHPhoto(BaseController):
    IN_STOCK = [
        "ADD_TO_CART",
    ]
    
    HEADERS = {
        "authority": "www.bhphotovideo.com",
        "pragma": "no-cache",
        "cache-control": "no-cache",
        "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "dnt": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "sec-fetch-site": "none",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "accept-language": "en-US,en;q=0.9",
    }
    SITE_URL = "https://www.bhphotovideo.com"
    BASE_URL = SITE_URL + "/c/search?sort=PRICE_HIGH_TO_LOW&filters=fct_category%3Agraphic_cards_6567&q="

    def get_status(self, item):
        try:
            status = item["priceInfo"]["addToCartButton"]
            if item["priceInfo"]["showNotifyWhenAvailable"]:
                return 'NOTIFY'
        except Exception as e:
            raise Exception("Unable to get status")
        else:
            return status
        
    def get_price(self, item):
        try:
            price = decimal.Decimal(str(item["priceInfo"]["price"]))
        except Exception as e:
            raise Exception("Unable to get price")
        else:
            return price
            
    def get_sku(self, item):
        try:
            sku = item["itemKey"]["skuNo"]
        except Exception as e:
            raise Exception("Unable to get sku")
        else:
            return sku
        
    def get_name(self, item):
        try:
            name = item["core"]["shortDescription"]
        except Exception as e:
            raise Exception("Unable to get name")
        else:
            return name
        
    def get_link(self, item):
        try:
            link = item["core"]["detailsUrl"]
        except Exception as e:
            raise Exception("Unable to get link")
        else:
            return link
        
    def get_items(self, dom):
        try:
            script = dom.find("div", {"id": "bh-portal"}).next_element
            if script.name == "script":
                listing = json.loads(script.text.split("__PRELOADED_DATA = ")[1].split(";window.__SERVER_RENDER_TIME")[0])
            if script.name == "div":
                listing = json.loads(script["data-data"])
            items = listing["ListingStore"]["response"]["data"]["items"]
        except Exception as e:
            raise Exception("Unable to get items")
        else:
            return items
