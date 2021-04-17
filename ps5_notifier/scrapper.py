import re
import colored
import requests
from bs4 import BeautifulSoup, Tag
from .notifier import Notifier


class Scrapper:
    # url: str = "https://www.amazon.com.br/PlayStation-3006297-Demons-Souls-5/dp/B08QTLJDD2"
    # TODO: provide this value with cli argument
    url: str = "https://www.amazon.com.br/PlayStation-Console-PlayStation®5/dp/B088GNRX3J"

    soup: BeautifulSoup
    notifier: Notifier

    def __init__(self, notifier: Notifier):
        """Inits Scrapper class.

        Args:
            notifier (Notifier): receive a notifier instance.
        """
        self.notifier = notifier

    def process(self) -> None:
        """Control all scrapper flow."""
        self._request()
        element_target_container: Tag = self.soup.find(id="centerCol")

        print("%sScrapping product page...%s" %
              (colored.fg(11), colored.attr(0)))
        if (self._evalute(element_target_container)):
            print("%sAVAILABLE! Sending notification.%s" %
                  (colored.fg(10), colored.attr(0)))
            self._notify(element_target_container)

    def _request(self) -> None:
        """Make a request.
           Sometimes the site will reject the request,
           then this function will try again, until getting done.
        """
        has_response = False
        while has_response == False:
            response = requests.get(self.url)
            has_response = True if response.status_code == 200 else False

        self.soup = BeautifulSoup(response.content, "html.parser")

    def _evalute(self, container: Tag) -> bool:
        """Evalute if the target product is available or not.

        Args:
            container (Tag): Receives a Tag instance as parameter.

        Returns:
            bool: Returns true if product available, false if not.
        """
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

    def _notify(self, container: Tag) -> None:
        """Prepare data and call Notifier.notify method.

        Args:
            container (Tag): Receives a Tag instance as parameter.
        """
        product_title = container.find(id="productTitle").get_text()
        self.notifier.set_message_values(product=product_title, link=self.url)
        self.notifier.notify()

    def _check_price(self, container: Tag) -> bool:
        """Check if product has a price, if empty means that product is not
        available for sale.

        Args:
            container (Tag): Receives a Tag instance as parameter.

        Returns:
            bool: Returns True if product price exists, False if not.
        """
        element_unified_price: Tag = container.find(
            id="unifiedPrice_feature_div")

        if not element_unified_price.find_all():
            return False

        return True

    def _check_availability(self, container: Tag) -> bool:
        """Check if product has a description different of 'Não disponivel'.

        Args:
            container (Tag): Receives a Tag instance as parameter.

        Returns:
            bool: Returns True if product description has not 'Não disponível' in your description, False if not.
        """
        # If "Não disponível." means that isn't available yet.
        element_availability_info: Tag = container.find(
            id="availability_feature_div")

        element_text = element_availability_info.get_text()
        element_availability_info.string = re.sub(
            r"[\n][\W]+[^\w]", "\n", element_text.strip())

        if element_availability_info.get_text().startswith("Não disponível"):
            return False

        return True
