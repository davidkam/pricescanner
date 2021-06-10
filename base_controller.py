import pycurl_requests as requests
import os
from bs4 import BeautifulSoup


class BaseController:

    def process(self):
        self.process_items("RTX+3090", 1000)
        self.process_items("RTX+3080", 500)

    def process_items(self, search_string, min_price):
        url = "%s%s"%(self.BASE_URL,search_string)
        response = self.get_contents(url, self.HEADERS)
        dom = self.to_dom(response)
        items = self.get_items(dom)
        for item in items:
            self.process_item(item, min_price)

    def process_item(self, item, min_price):
        status = self.get_status(item)
        if status.upper() not in self.IN_STOCK:
            return

        price = self.get_price(item)
        if price < min_price:
            return

        sku = self.get_sku(item)
        name = self.get_name(item)
        link = self.get_link(item)

        url = link if link.startswith("http") else "%s%s"%(self.SITE_URL, link)

        notification = "%s - %s back in stock (%s)"%(type(self).__name__, name, str(price))
        message = "*%s* - %s back in stock (%s)\n\n<%s|%s>"%(type(self).__name__, sku, str(price), url, name)
        print(message)

        # self.send_alert(notification, message)

    def get_contents(self, url, headers = None):
        try:
            r = requests.get(url, headers=headers)
        except Exception as e:
            raise
        else:
            return r.text
    
    @staticmethod
    def to_dom(text):
        try:
            soup = BeautifulSoup(text, "html5lib")
        except Exception as e:
            raise
        else:
            return soup

    @staticmethod
    def send_alert(notification, message):
        slack_url = os.getenv("SLACK_URL")
        data = {
            "text": notification,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": message
                    }
                }
            ]
        }
        requests.post(slack_url, json=data)

    def get_status(self, item):
        # implement in child class
        pass

    def get_price(self, item):
        # implement in child class
        pass

    def get_sku(self, item):
        # implement in child class
        pass

    def get_name(self, item):
        # implement in child class
        pass

    def get_link(self, item):
        # implement in child class
        pass

    def get_items(self, dom = None):
        # implement in child class
        pass
