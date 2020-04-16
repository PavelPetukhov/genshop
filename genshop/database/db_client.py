import datetime
import mysql.connector

from genshop.logger import logging

MINUTE_TABLE = 'Historical_Minute_Data'
EOD_TABLE = 'Historical_Eod_Data'


class DBClient:
    def __init__(self, config):
        self.logger = logging.getLogger()
        self.cfg = config
        self.db = mysql.connector.connect(
          host=self.cfg.host,
          user=self.cfg.user,
          passwd=self.cfg.passwd,
          database=self.cfg.database
        )
        self.cursor = self.db.cursor(buffered=True)

        # cursor.execute("CREATE TABLE tickers (name VARCHAR(255))")
        # cursor.execute("CREATE TABLE candles (sympol VARCHAR(20), type VARCHAR(20), open FLOAT, high FLOAT, low FLOAT, close FLOAT, timestame TIMESTAMP)")
        # self.cursor.execute("SHOW TABLES")
        # for x in self.cursor:
        #     print(x)
        # self.check_if_symbol_is_present('APPL')

    def store_eod_ticker_data(self, symbol, data):
        self.store_ticker_data(symbol, data, minute_data=False)

    def store_minute_ticker_data(self, symbol, data):
        self.store_ticker_data(symbol, data, minute_data=True)

    def check_if_transaction_is_recorded(self, table_name, symbol, timestamp):
        self.logger.debug(
            f'check_if_transaction_is_recorded started for {table_name}, {symbol}, {timestamp}')

        self.cursor.execute(
            f" select 1 from {table_name} where symbol = {symbol} and timestamp = '{timestamp}';")
        if self.cursor.rowcount == 0:
            return False
        return True

    def store_ticker_data(self, symbol, data, minute_data=True):
        self.logger.info(f'store_ticker_data started for {symbol}, minute_data {minute_data}')

        self.cursor.execute(f"SELECT * FROM Portfolio WHERE symbol = '{symbol}';")
        if self.cursor.rowcount == 0:
            self.logger.info(f'failed to find {symbol} in Portfolio')
            raise Exception(f'store_ticker_data. Symbol {symbol} was not found in portfolio table')

        try:
            key, symbol_ = self.cursor.fetchall()[0]
        except KeyError:
            raise Exception(f'Failed to parse cursor db data')

        is_present = True
        table_name = MINUTE_TABLE if minute_data else EOD_TABLE
        for elem in sorted(data['candles'], key=lambda elem: elem['datetime']):
            open, high, low, close, volume = elem['open'], elem['high'], \
                                             elem['low'], elem['close'], elem['volume']
            timestamp = datetime.datetime.fromtimestamp(int(elem['datetime'])/1000)

            if is_present:
                is_present = self.check_if_transaction_is_recorded(table_name, key, timestamp)
                if is_present:
                    continue

            self.cursor.execute(f"INSERT INTO {table_name} "
                                f"(symbol, open, high, low, close, volume, timestamp) "
                                f"VALUES "
                                f"({key}, '{open}', '{high}', "
                                f"'{low}', '{close}', '{volume}', '{timestamp}')")
        self.db.commit()

    def check_if_symbol_is_present(self, symbol, minute_data=True):
        self.logger.info(
            f'check_if_symbol_is_present started for {symbol}, minute_data {minute_data}')

        self.cursor.execute(f"SELECT * FROM Portfolio WHERE symbol = '{symbol}';")

        if self.cursor.rowcount == 0:
            raise Exception(f'Symbol {symbol} was not found in portfolio table')
        key, symbol_ = self.cursor.fetchall()[0]

        table_name = MINUTE_TABLE if minute_data else EOD_TABLE
        self.cursor.execute(f"SELECT * FROM {table_name} "
                            f"WHERE symbol = {key} ORDER BY timestamp DESC LIMIT 1;")
        if self.cursor.rowcount == 0:
            return None
        else:
            id, symbol, open, high, low, close, volume, timestamp = self.cursor.fetchall()[0]
            return timestamp

    def check_symbol(self, symbol):
        self.cursor.execute(f"SELECT 1 FROM Portfolio WHERE symbol = '{symbol}';")
        if self.cursor.rowcount == 0:
            return False
        return True

    def get_symbols(self):
        self.cursor.execute(f"SELECT symbol FROM Portfolio;")
        result = self.cursor.fetchall()
        return [elem[0] for elem in result]

    def add_symbol(self, symbol):
        self.cursor.execute(f"INSERT INTO Portfolio (symbol) VALUES ('{symbol}');")
        self.db.commit()

    def validate_db_schema(self):
        try:
            self.cursor.execute('SELECT 1 FROM Portfolio LIMIT 1;')
        except mysql.connector.errors.ProgrammingError as err:
            self.cursor.execute(
                "CREATE TABLE Portfolio (id INT NOT NULL AUTO_INCREMENT, "
                "PRIMARY KEY (id), symbol VARCHAR(20))")
            self.db.commit()

        try:
            self.cursor.execute('SELECT 1 FROM Daily_Trades LIMIT 1;')
        except mysql.connector.errors.ProgrammingError as err:
            self.cursor.execute(
                "CREATE TABLE Daily_Trades ("
                "id INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (id), symbol INT, "
                "FOREIGN KEY (symbol) REFERENCES Portfolio(id), "
                "open FLOAT, high FLOAT, low FLOAT, close FLOAT, "
                "volume FLOAT, timestamp TIMESTAMP)")
            self.db.commit()

        try:
            self.cursor.execute(f'SELECT 1 FROM {MINUTE_TABLE} LIMIT 1;')
        except mysql.connector.errors.ProgrammingError as err:
            self.cursor.execute(f"CREATE TABLE {MINUTE_TABLE} ("
                                "id INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (id), "
                                "symbol INT, FOREIGN KEY (symbol) REFERENCES Portfolio(id), "
                                "open FLOAT, high FLOAT, low FLOAT, close FLOAT, "
                                "volume FLOAT, timestamp TIMESTAMP)")
            self.db.commit()

        try:
            self.cursor.execute(f'SELECT 1 FROM {EOD_TABLE} LIMIT 1;')
        except mysql.connector.errors.ProgrammingError as err:
            self.cursor.execute(f"CREATE TABLE {EOD_TABLE} ("
                                "id INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (id), "
                                "symbol INT, FOREIGN KEY (symbol) REFERENCES Portfolio(id), "
                                "open FLOAT, high FLOAT, low FLOAT, close FLOAT, "
                                "volume FLOAT, timestamp TIMESTAMP)")
            self.db.commit()



