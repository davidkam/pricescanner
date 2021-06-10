import decimal
import urllib
import re
from base_controller import BaseController


class BestBuy(BaseController):
    IN_STOCK = [
        "ADD TO CART",
        "SEE DETAILS",
    ]
    
    HEADERS = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36"
    }
    SITE_URL = "https://www.bestbuy.com"
    BASE_URL = SITE_URL + "/site/searchpage.jsp?sp=-currentprice%20skuidsaas&st="

    def get_status(self, item):
        try:
            status = item.find(class_="add-to-cart-button").text
        except Exception as e:
            raise Exception("Unable to get status")
        else:
            return status
        
    def get_price(self, item):
        try:
            price = decimal.Decimal(re.sub("[,\$]","",item.find("div", class_="priceView-customer-price").find("span").text))
        except Exception as e:
            raise Exception("Unable to get price")
        else:
            return price
            
    def get_sku(self, item):
        try:
            sku = item["data-sku-id"]
        except Exception as e:
            raise Exception("Unable to get sku")
        else:
            return sku
        
    def get_name(self, item):
        try:
            name = item.find("h4", class_="sku-header").text
        except Exception as e:
            raise Exception("Unable to get name")
        else:
            return name
        
    def get_link(self, item):
        try:
            link = item.find("a", class_="image-link")["href"]
        except Exception as e:
            raise Exception("Unable to get link")
        else:
            return link
        
    def get_items(self, dom):
        try:
            items = dom.find_all("li", class_="sku-item")
        except Exception as e:
            raise Exception("Unable to get items")
        else:
            return items
