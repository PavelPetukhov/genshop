import requests

functions = {
    'intraday': 'TIME_SERIES_INTRADAY'
}

intervals = {
    1: '1min',
    5: '5min',
    15: '15min',
    30: '30min',
    60: '60min',
}


class Client:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = 'https://www.alphavantage.co'

    def get_ticker_time_series(self, ticker):
        func = functions['intraday']
        interval = intervals[1]
        endpoint = f'{self.url}/query?function={func}&symbol={ticker}' \
                   f'&interval={interval}&outputsize=full&apikey={self.api_key}'
        content = requests.get(url=endpoint)
        return content.json()
