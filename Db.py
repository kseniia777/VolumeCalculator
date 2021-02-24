class Db:

    def __init__(self, db):
        self.db = db


    def create_table_api(self):  # создаем таблицу, если ее нет
        cursor = self.db.cursor( )
        cursor.execute('''CREATE TABLE IF NOT EXISTS userAPI (
                               "id"    INTEGER PRIMARY KEY AUTOINCREMENT,
                               user_id INTEGER,
                               API     TEXT,
                               SECRET  TEXT
                        )''')
        self.db.commit( )

    def insert_user_id(self, user_id):
        cursor = self.db.cursor( )
        cursor.execute("INSERT INTO userAPI (user_id) VALUES (?)",
                       (user_id,))
        self.db.commit( )

    def insert_api_key(self, ApiKey, user_id):
        cursor = self.db.cursor( )
        cursor.execute("UPDATE userAPI SET API = ? WHERE user_id = ? ",
                       (ApiKey, user_id))
        self.db.commit( )

    def insert_secret_key(self, SecretKey, user_id):
        cursor = self.db.cursor( )
        cursor.execute("UPDATE userAPI SET SECRET = ? WHERE user_id = ? ",
                       (SecretKey, user_id))
        self.db.commit( )

    def destroy(self, user_id):  # clear a table
        cursor = self.db.cursor( )
        cursor.execute("DELETE FROM userAPI WHERE user_id = ? ", (user_id,))
        self.db.commit( )


class VolDb:

    def __init__(self, db):
        self.db = db


    def create_table_volume(self):  # создаем таблицу, если ее нет
        cursor = self.db.cursor( )
        cursor.execute('''CREATE TABLE IF NOT EXISTS Volume(
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        ticker VARCHAR,
                        price DECIMAL(30, 10),
                        percent DECIMAL(5, 3),
                        dollar DECIMAL(5, 3),
                        comission DECIMAL(3, 2) DEFAULT (0.08)
                        );''')
        self.db.commit( )

    def insert_user_id_vol(self, user_id):
        cursor = self.db.cursor( )
        cursor.execute("INSERT INTO Volume (user_id) VALUES (?)",
                       (user_id,))
        self.db.commit( )

    def insert_ticker(self, ticker, user_id):
        cursor = self.db.cursor( )
        cursor.execute("UPDATE Volume SET ticker = ? WHERE user_id = ? ",
                       (ticker, user_id))
        self.db.commit( )

    def insert_price(self, price, user_id):
        cursor = self.db.cursor( )
        cursor.execute("UPDATE Volume SET price = ? WHERE user_id = ? ",
                       (price, user_id))
        self.db.commit( )
        return price

    def insert_percent(self, percent, user_id):
        cursor = self.db.cursor( )
        cursor.execute("UPDATE Volume SET percent = ? WHERE user_id = ? ",
                       (percent, user_id))
        self.db.commit( )
        return percent

    def insert_dollar(self, dollar, user_id):
        cursor = self.db.cursor( )
        cursor.execute("UPDATE Volume SET dollar = ? WHERE user_id = ? ",
                       (dollar, user_id))
        self.db.commit( )
        return dollar

    def destroy(self, user_id):  # clear a table
        cursor = self.db.cursor( )
        cursor.execute("DELETE FROM Volume WHERE user_id = ? ", (user_id,))
        self.db.commit( )

    # доразобраться
    def commis(self, user_id):
        cursor = self.db.cursor( )
        cursor.execute("SELECT comission FROM Volume WHERE user_id = ? LIMIT 1",
                       (user_id,))  # изменила звёздочку на ранкс
        coms = cursor.fetchone( )[0]
        return coms


    def all(self, user_id):
        cursor = self.db.cursor( )
        cursor.execute("SELECT * FROM Volume WHERE user_id = ? LIMIT 1",
                       (user_id,))
        data = cursor.fetchall( )
        # print(coms) - [(1, 933693522, 'NEARUSDT', 4.1398, 1, 3, 0.08)]
        dollar = data[0][5]
        percent = data[0][4]
        coms = data[0][6]
        price = data[0][3]
        volume = (100 * dollar / (percent + coms) / price)
        vol = round(volume, 2)
        return vol
######работа с открытием ордера
