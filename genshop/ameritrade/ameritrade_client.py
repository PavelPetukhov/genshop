import time
import requests


class AmeritradeClient:
    def __init__(self, config):
        self.cfg = config
        self.client_id = self.cfg.client_id
        self.base_url = 'https://api.tdameritrade.com/v1/marketdata/'

    def get_ticker_daily_data(self, last_timestamp, ticker):
        url = f'{self.base_url}{ticker}/pricehistory'

        payload = {'apikey': self.client_id,
                   'periodType': 'day',
                   'frequencyType': 'minute',
                   'frequency': '1',
                   'period': '10',
                   'startDate': str(int(last_timestamp.timestamp())*1000),
                   'needExtendedHoursData': 'true'}

        content = requests.get(url=url, params=payload)

        if content.status_code != 200:
            raise Exception(f'Failed to get data {payload}, response {content.__dict__}')

        return content.json()

    def get_ticker_daily_data_all(self, ticker):
        curr_time = int(time.time())
        url = f'{self.base_url}{ticker}/pricehistory'

        payload = {'apikey': self.client_id,
                   'periodType': 'day',
                   'frequencyType': 'minute',
                   'frequency': '1',
                   'period': '10',
                   'needExtendedHoursData': 'true'}

        content = requests.get(url=url, params=payload)

        if content.status_code != 200:
            raise Exception(f'Failed to get data {payload}, response {content.__dict__}')

        return content.json()


if __name__ == "__main__":
    pass