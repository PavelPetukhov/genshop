import mysql.connector


class DBClient:
    def __init__(self):
        self.db = mysql.connector.connect(
          host="localhost",
          user="demouser",
          passwd="Password_123",
          database="demodb"
        )
        cursor = self.db.cursor()

        # cursor.execute("CREATE TABLE tickers (name VARCHAR(255))")
        # cursor.execute("CREATE TABLE candles (sympol VARCHAR(20), type VARCHAR(20), open FLOAT, high FLOAT, low FLOAT, close FLOAT, timestame TIMESTAMP)")

        cursor.execute("SHOW TABLES")

        for x in cursor:
            print(x)


if __name__ == '__main__':
    cl = DBClient()
