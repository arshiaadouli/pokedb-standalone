import mysql.connector
from mysql.connector import Error

class DatabaseInterface:
    def __init__(self):
        self.conn = mysql.connector.connect(host='mysql.ocio.monash.edu',
                                        database='pokedb',
                                        user='pokedb',
                                        password='Po*l6K12e-220815')
        self.mycursor =self.conn.cursor()
    def fetchAll(self, table):
        self.mycursor.execute("SELECT * FROM " + table)
        return self.mycursor.fetchall()
        
    # def action(self):
    #     self.mycursor.execute("SELECT * FROM " + table)
    #     return self.mycursor.fetchall()
# db = DatabaseInterface()
# print(db)
# print(db.action())