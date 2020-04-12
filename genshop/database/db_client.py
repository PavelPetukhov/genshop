import datetime
import mysql.connector


class DBClient:
    def __init__(self, config):
        self.cfg = config
        self.db = mysql.connector.connect(
          host=self.cfg.host,
          user=self.cfg.user,
          passwd=self.cfg.passwd,
          database=self.cfg.database
        )
        self.cursor = self.db.cursor(buffered=True)

    def store_ticker_data(self, symbol, data):
        self.cursor.execute(f"SELECT * FROM Portfolio WHERE symbol = '{symbol}';")
        if self.cursor.rowcount == 0:
            raise Exception(f'store_ticker_data. Symbol {symbol} was not found in portfolio table')

        try:
            key, symbol_ = self.cursor.fetchall()[0]
        except KeyError:
            raise Exception(f'Failed to parse cursor db data')

        # Assuming
        for elem in sorted(data['candles'], key=lambda elem: elem['datetime']):
            open, high, low, close, volume = elem['open'], elem['high'], \
                                             elem['low'], elem['close'], elem['volume']
            timestamp = datetime.datetime.fromtimestamp( int(elem['datetime'])/1000)
            self.cursor.execute(f"INSERT INTO Daily_Trades "
                                f"(symbol, open, high, low, close, volume, timestamp) "
                                f"VALUES "
                                f"({key}, '{open}', '{high}', "
                                f"'{low}', '{close}', '{volume}', '{timestamp}')")
        self.db.commit()

    def check_if_symbol_is_present(self, symbol):
        self.cursor.execute(f"SELECT * FROM Portfolio WHERE symbol = '{symbol}';")

        if self.cursor.rowcount == 0:
            raise Exception(f'Symbol {symbol} was not found in portfolio table')
        key, symbol_ = self.cursor.fetchall()[0]

        self.cursor.execute(f"SELECT * FROM Daily_Trades "
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
        if self.cursor.rowcount == 0:
            return None
        result = self.cursor.fetchall()
        return [elem[0] for elem in result]

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
            self.cursor.execute('SELECT 1 FROM Historical_Data LIMIT 1;')
        except mysql.connector.errors.ProgrammingError as err:
            self.cursor.execute("CREATE TABLE Historical_Data ("
                                "id INT NOT NULL AUTO_INCREMENT, PRIMARY KEY (id), "
                                "symbol INT, FOREIGN KEY (symbol) REFERENCES Portfolio(id), "
                                "open FLOAT, high FLOAT, low FLOAT, close FLOAT, "
                                "volume FLOAT, timestamp TIMESTAMP)")
            self.db.commit()



