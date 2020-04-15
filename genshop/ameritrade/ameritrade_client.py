import datetime
import requests

from genshop.logger import logging


class AmeritradeClient:
    def __init__(self, config):
        self.logger = logging.getLogger()

        self.cfg = config
        self.max_dataset_in_days = self.cfg.max_dataset_in_days
        self.client_id = self.cfg.client_id
        self.base_url = 'https://api.tdameritrade.com/v1/marketdata/'

    def get_ticker_daily_data(self, last_timestamp, ticker):
        start = int(last_timestamp.timestamp())*1000
        return self._get_ticker_daily_data(before=None, after=start, ticker=ticker)

    def get_ticker_eod_data(self, last_timestamp, ticker):
        start = int(last_timestamp.timestamp())*1000
        return self._get_ticker_daily_data(before=None, after=start, ticker=ticker, eod=True)

    def _get_ticker_daily_data(self, before, after, ticker, eod=False):
        url = f'{self.base_url}{ticker}/pricehistory'

        payload = {'apikey': self.client_id,
                   'frequency': '1',
                   'period': '1',
                   'needExtendedHoursData': 'false'}
        if eod:
            payload['periodType'] = 'year'
            payload['frequencyType'] = 'daily'
        else:
            payload['periodType'] = 'day'
            payload['frequencyType'] = 'minute'
        if after:
            payload['startDate'] = str(after)
        if before:
            payload['endDate'] = str(before)

        self.logger.info(f'Sending request. ticker: {ticker}, payload: {payload}')

        content = requests.get(url=url, params=payload)

        if content.status_code != 200:
            raise Exception(f'Failed to get data {payload}, response {content.__dict__}')

        return content.json()

    def get_oldest_date(self, data):
        try:
            return data['candles'][0]['datetime']/1000
        except KeyError:
            return None

    def get_newest_date(self, data):
        try:
            return data['candles'][-1]['datetime']/1000
        except KeyError:
            return None

    def get_ticker_daily_data_all(self, ticker):
        response = {'candles': [], 'symbol': ticker, 'empty': False}
        current_time = datetime.datetime.now()
        required_start_time = current_time - datetime.timedelta(days=self.max_dataset_in_days)

        end_time = current_time
        start_time = current_time - datetime.timedelta(days=10)
        while start_time > required_start_time:
            data = self._get_ticker_daily_data(
                before=int(end_time.timestamp()*1000),
                after=int(start_time.timestamp()*1000),
                ticker=ticker)

            if data:
                try:
                    end_time = datetime.datetime.fromtimestamp(self.get_oldest_date(data))
                except IndexError as err:
                    import pdb; pdb.set_trace()
                    self.logger.info(f'failed to get get_oldest_date {err}')
                    break

                if start_time == end_time - datetime.timedelta(days=10):
                    break

                start_time = end_time - datetime.timedelta(days=10)
                response['candles'] += data['candles']
            else:
                break

        response['candles'] = sorted(response['candles'], key=lambda elem: elem['datetime'])

        return response

    def get_ticker_eod_data_all(self, ticker):
        current_time = datetime.datetime.now()
        start_time = current_time - datetime.timedelta(days=self.max_dataset_in_days)
        data = self._get_ticker_daily_data(
            before=None, after=int(start_time.timestamp()*1000),
            ticker=ticker, eod=True)
        return data

