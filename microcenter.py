import decimal
import urllib
import re
from base_controller import BaseController


class MicroCenter(BaseController):
    IN_STOCK = [
        "IN STOCK",
        "LIMITED AVAILABILITY",
    ]
    
    HEADERS = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36"
    }
    SITE_URL = "https://www.microcenter.com"
    BASE_URL = SITE_URL + "/search/search_results.aspx?Ntk=all&sortby=match&N=4294966938&myStore=false&Ntt="

    def get_status(self, item):
        try:
            status = item.find("div", class_="stock").find("span").text
        except Exception as e:
            raise Exception("Unable to get status")
        else:
            return status
        
    def get_price(self, item):
        try:
            price = decimal.Decimal(re.sub("[,\$]","",item.find("div", class_="price").text.strip()))
        except Exception as e:
            raise Exception("Unable to get price")
        else:
            return price
            
    def get_sku(self, item):
        try:
            sku = item.find("p", class_="sku").text.split(" ")[1]
        except Exception as e:
            raise Exception("Unable to get sku")
        else:
            return sku
        
    def get_name(self, item):
        try:
            name = item.find("div", class_="pDescription").find("a")["data-name"]
        except Exception as e:
            raise Exception("Unable to get name")
        else:
            return name
        
    def get_link(self, item):
        try:
            link = item.find("div", class_="pDescription").find("a")["href"]
        except Exception as e:
            raise Exception("Unable to get link")
        else:
            return link
        
    def get_items(self, dom):
        try:
            items = dom.find_all("li", class_="product_wrapper")
        except Exception as e:
            raise Exception("Unable to get items")
        else:
            return items
