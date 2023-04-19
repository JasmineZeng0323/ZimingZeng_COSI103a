import sqlite3


class Transaction:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS transactions
                            (id INTEGER PRIMARY KEY,
                            item TEXT,
                            amount REAL,
                            category TEXT,
                            date TEXT,
                            description TEXT)''')
        self.conn.commit()

    def create_transaction(self, item, amount, category, date, description):
        self.cur.execute("INSERT INTO transactions (item, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
                         (item, amount, category, date, description))
        self.conn.commit()

    def read_transaction(self, transaction_id):
        self.cur.execute("SELECT * FROM transactions WHERE id=?", (transaction_id,))
        return self.cur.fetchone()

    def read_all_transactions(self):
        self.cur.execute("SELECT * FROM transactions")
        return self.cur.fetchall()

    def update_transaction(self, transaction_id, item=None, amount=None, category=None, date=None, description=None):
        update_query = "UPDATE transactions SET "
        update_params = []
        if item:
            update_query += "item=?, "
            update_params.append(item)
        if amount:
            update_query += "amount=?, "
            update_params.append(amount)
        if category:
            update_query += "category=?, "
            update_params.append(category)
        if date:
            update_query += "date=?, "
            update_params.append(date)
        if description:
            update_query += "description=?, "
            update_params.append(description)
        update_query = update_query[:-2] + " WHERE id=?"
        update_params.append(transaction_id)
        self.cur.execute(update_query, tuple(update_params))
        self.conn.commit()

    def delete_transaction(self, transaction_id):
        self.cur.execute("DELETE FROM transactions WHERE id=?", (transaction_id,))
        self.conn.commit()

    def aggregate_by_category(self):
        self.cur.execute("SELECT category, SUM(amount) FROM transactions GROUP BY category")
        return self.cur.fetchall()

    def aggregate_by_date(self):
        self.cur.execute("SELECT date, SUM(amount) FROM transactions GROUP BY date")
        return self.cur.fetchall()

    def aggregate_by_month(self):
        self.cur.execute("SELECT strftime('%Y-%m', date) AS month, SUM(amount) FROM transactions GROUP BY month")
        return self.cur.fetchall()

    def aggregate_by_year(self):
        self.cur.execute("SELECT strftime('%Y', date) AS year, SUM(amount) FROM transactions GROUP BY year")
        return self.cur.fetchall()

    def close(self):
        self.conn.close()
