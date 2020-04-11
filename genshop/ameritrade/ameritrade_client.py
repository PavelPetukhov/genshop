import requests


class AmeritradeClient:
    def __init__(self, client_id):
        self.client_id = client_id
        self.base_url = 'https://api.tdameritrade.com/v1/marketdata/'

    def get_ticker_daily_data(self, ticker):
        url = f'{self.base_url}{ticker}/pricehistory'

        payload = {'apikey': self.client_id,
                   'periodType': 'month',
                   'frequencyType': 'daily',
                   'frequency': '1',
                   'period': '1',
                   'endDate': '1586161925000',
                   'needExtendedHoursData': 'true'}

        content = requests.get(url=url, params=payload)

        if content.status_code != 200:
            raise Exception(f'Failed to get data {payload}, response {content.__dict__}')

        return content.json()


if __name__ == "__main__":
    pass