import mysql.connector

class DB:

    def __init__(self):
        dbconfig = {
            'host': '10.0.1.146',
            'user': 'darren',
            'password': 'password',
            'database': 'cin_xyz',

        }
        self.conn = mysql.connector.connect(**dbconfig)
        self.cursor = self.conn.cursor()
    
    def do_insert(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor.lastrowid

    def do_fetch_all(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def do_fetch_one(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def do_update(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
    
    def close(self):
        self.cursor.close()
        self.conn.close()