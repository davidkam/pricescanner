import decimal
import json
import urllib
import re
from base_controller import BaseController


"""
Using json instead of parsing HTML
"""
class Adorama(BaseController):
    IN_STOCK = [
        "HTTPS://SCHEMA.ORG/INSTOCK",
    ]
    
    HEADERS = {
        "authority": "www.adorama.com",
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
    SITE_URL = "https://www.adorama.com"
    BASE_URL = SITE_URL + "/l/Computers/Computer-Components?sel=Item-Condition_New-Items&searchinfo="

    def get_status(self, item):
        try:
            status = None
            for offer in item["item"]["offers"]:
                if offer["itemCondition"] != "NewCondition":
                    continue

                status = offer["availability"]
                break
 
            if status is None:
                raise Exception("Unable to get status - offers")
          
        except Exception as e:
            raise Exception("Unable to get status")
        else:
            return status
        
    def get_price(self, item):
        try:
            price = None
            for offer in item["item"]["offers"]:
                if offer["itemCondition"] != "NewCondition":
                    continue

                price = decimal.Decimal(offer["price"])
                break

            if price is None:
                raise Exception("Unable to get price - offers")
        except Exception as e:
            raise Exception("Unable to get price")
        else:
            return price
            
    def get_sku(self, item):
        try:
            sku = item["item"]["sku"]
        except Exception as e:
            raise Exception("Unable to get sku")
        else:
            return sku
        
    def get_name(self, item):
        try:
            name = item["item"]["name"]
        except Exception as e:
            raise Exception("Unable to get name")
        else:
            return name
        
    def get_link(self, item):
        try:
            link = item["item"]["url"]
        except Exception as e:
            raise Exception("Unable to get link")
        else:
            return link
        
    def get_items(self, dom):
        try:
            script = dom.find("div", {"id": "productGridPlaceholder"}).findChild()
            listing = json.loads(script.text)
            items = listing["itemListElement"]
        except Exception as e:
            raise Exception("Unable to get items")
        else:
            return items
