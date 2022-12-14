import mysql.connector
from mysql.connector import Error

mydb = mysql.connector.connect(host='localhost',
                                        database='momoda',
                                        user='root',
                                        password='')

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM experiments_experiment")
myresult = mycursor.fetchall()
for x in myresult:
  print(x[0])

