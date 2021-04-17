import re
import colored
import requests
from bs4 import BeautifulSoup, Tag
from .notifier import Notifier


class Scrapper:

    # url: str = "https://www.amazon.com.br/PlayStation-3006297-Demons-Souls-5/dp/B08QTLJDD2"
    url: str = "https://www.amazon.com.br/PlayStation-Console-PlayStation®5/dp/B088GNRX3J"

    soup: BeautifulSoup
    notifier: Notifier

    def __init__(self, notifier: Notifier):
        self.notifier = notifier

    def process(self) -> None:
        self._request()
        element_target_container: Tag = self.soup.find(id="centerCol")

        print("%sScrapping product page...%s" %
              (colored.fg(11), colored.attr(0)))
        if (self._evalute(element_target_container)):
            print("%sAVAILABLE! Sending notification.%s" %
                  (colored.fg(10), colored.attr(0)))
            self._notify(element_target_container)

    def _request(self) -> None:
        has_response = False
        while has_response == False:
            response = requests.get(self.url)
            has_response = True if response.status_code == 200 else False

        self.soup = BeautifulSoup(response.content, "html.parser")

    def _evalute(self, container: Tag) -> bool:
        points: int = 0

        if self._check_price(container):
            points += 1

        if self._check_availability(container):
            points += 1

        if points > 0:
            return True

        print("%sProduct Unavailable :(%s" %
              (colored.fg(1), colored.attr(0)))
        return False

    def _notify(self, container: Tag) -> bool:
        product_title = container.find(id="productTitle").get_text()
        self.notifier.set_message_values(product=product_title, link=self.url)
        self.notifier.notify()

    def _check_price(self, container: Tag) -> bool:
        # If empty means that the product is no available in stock
        element_unified_price: Tag = container.find(
            id="unifiedPrice_feature_div")

        if not element_unified_price.find_all():
            return False

        return True

    def _check_availability(self, container: Tag) -> bool:
        # If "Não disponível." means that isn't available yet.
        element_availability_info: Tag = container.find(
            id="availability_feature_div")

        element_availability_info.string = self._sanitize_text(
            element_availability_info.get_text())

        if element_availability_info.get_text().startswith("Não disponível"):
            return False

        return True

    def _sanitize_text(self, text: str) -> str:
        return re.sub(r"[\n][\W]+[^\w]", "\n", text.strip())
