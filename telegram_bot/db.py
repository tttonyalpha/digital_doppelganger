import sqlite3


class Database_handler:
    def __init__(self):
        self.conn = sqlite3.connect('/persistent/bot/request.db')
        self.cursor = self.conn.cursor()
        self.CreateRequestsTable()

    def __del__(self):
        self.conn.close()

    def CreateRequestsTable(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS requests (
        request_id INTEGER PRIMARY KEY,
        result TEXT CHECK( result IN ('S','F') ) NOT NULL,
        chat_id INTEGER NOT NULL,
        message TEXT NOT NULL,
        reply TEXT,
        time t_i DEFAULT (strftime('%s', 'now'))
    );''')

    def insert(self, chat_id: int, message: str, reply: str):
        if reply is not None:
            self.cursor.execute(
                "INSERT INTO requests(result, chat_id, message, reply) VALUES ('S', ?, ?, ?)", (chat_id, message, reply))
        else:
            self.cursor.execute(
                "INSERT INTO requests(result, chat_id, message) VALUES ('F', ?, ?)", (chat_id, message))

    def flush(self):
        self.conn.commit()
