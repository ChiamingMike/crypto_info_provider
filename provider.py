import datetime
import requests
from bs4 import BeautifulSoup


class PriceProvider(object):

    def __init__(self) -> None:
        """
        """
        self.__url = 'https://www.google.com/finance/quote/SEARCH_TARGET'
        self.practical_url = str()

        return None

    def get_request_time(self) -> None:
        """
        """
        time = datetime.datetime.now(
            datetime.timezone(datetime.timedelta(hours=9)))
        request_time = time.strftime('%y-%m-%d %H:%M:%S')

        return request_time

    def get_price(self, crypto_name: str, currency_name: str) -> str:
        """
        """
        # getting the request from url
        search_target = f'{crypto_name}-{currency_name}'
        self.practical_url = self.__url.replace('SEARCH_TARGET', search_target)
        data = requests.get(self.practical_url)

        soup = BeautifulSoup(data.text, 'html.parser')

        price = soup.find("div", attrs={'class': 'YMlKec fxKbKc'}).text

        return price

    @property
    def url(self) -> str:
        return self.practical_url


if __name__ == '__main__':
    pass
