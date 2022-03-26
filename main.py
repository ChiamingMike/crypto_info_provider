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


def list_with_index(list):
    print('*'*12)
    for i, x in enumerate(list):
        print(f'{i}:{x}')
    print('*'*12)


if __name__ == '__main__':
    crypto_list = ['BTC', 'ETH']
    currency_list = ['USD', 'JPY']
    for one_list in [crypto_list, currency_list]:
        list_with_index(one_list)
    input_value = input('(i.e:01,10,11,00)\r\nPlease enter the number...')
    try:
        crypto_index = int(input_value[0])
        currency_index = int(input_value[-1])
    except Exception as e:
        # error
        print(e)

    if len(crypto_list) >= crypto_index and \
            len(currency_list) >= currency_index:
        price_provider = PriceProvider()
        time = price_provider.get_request_time()
        crypto_name = crypto_list[crypto_index]
        currency_name = currency_list[currency_index]
        price = price_provider.get_price(crypto_name, currency_name)
        url = price_provider.url
        print(
            f'{time}\r\n{crypto_name}:{price} {currency_name}\r\n{url}')
