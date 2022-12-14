from tkinter import *
from datetime import datetime, date
import mysql.connector
from mysql.connector import Error

mydb = mysql.connector.connect(host='localhost',
                                        database='momoda',
                                        user='root',
                                        password='')



ws = Tk()
ws.geometry('400x300')
ws.title('PythonGuides')
# ws['bg']='#5d8a82'

f = ("Times bold", 10)
values = {"name":"", "monomer": "", "cta":"", "cx":"", "temp":"", "volume": ""}
def nextPage():
    now = datetime.now()
    time_now=now.strftime("%H:%M:%S")
    today = date.today()
    date_now= today.strftime("%Y-%m-%d")
    values['name'] = name_entry.get()
    values['monomer'] = monomer_entry.get()
    values['cta'] = cta_entry.get()
    values['cx'] = cx_entry.get()
    values['temp'] = temp_entry.get()
    values['volume'] = volume_entry.get()

    # mycursor = mydb.cursor()
    # mycursor.execute("SELECT * FROM experiments_experiment")
    # myresult = mycursor.fetchall()
    mycursor = mydb.cursor()
    sql = "INSERT INTO experiments_experiment (date, time, name, temperature, total_volume, monomer, CTA, cx_ratio, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (date_now, time_now, values['name'], values['temp'], values['volume'], values['monomer'], values['cta'], values['cx'], 1)
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")


    ws.destroy()
    import page2

tframe = Frame(ws).grid(row=0, column=1)
ws.columnconfigure(tuple(range(120)), weight=1)
ws.rowconfigure(tuple(range(30)), weight=1)

name_label = Label(ws ,text = "Experiment Name").grid(row = 0,column = 0, sticky='e')
name_entry = Entry(ws)
name_entry.grid(row = 0,column = 1,sticky='e')

monomer_label = Label(ws ,text = "Monomer Used").grid(row = 0,column = 2, sticky='e')
monomer_entry = Entry(ws)
monomer_entry.grid(row = 0,column = 3, sticky='e')

cta_label = Label(ws ,text = "CTA used").grid(row = 1,column = 0,sticky='n')
cta_entry = Entry(ws)
cta_entry.grid(row = 1,column = 1, sticky='n')

cx_label = Label(ws ,text = "Cx/Cm Ratio").grid(row = 1,column = 2, sticky='n')
cx_entry= Entry(ws)
cx_entry.grid(row = 1,column = 3, sticky='n')

temp_label = Label(ws ,text = "Temperature").grid(row = 2,column = 0, sticky='n')
temp_entry= Entry(ws)
temp_entry.grid(row = 2,column = 1, sticky='n')

volumn_label = Label(ws ,text = "Volume").grid(row = 2,column = 2, sticky='n')
volume_entry= Entry(ws)
volume_entry.grid(row = 2,column = 3, sticky='n')






Button(
    ws, 
    text="Submit", 
    font=f,
    command=nextPage
    ).grid(row=3 ,column=3)

# Button(
#     ws, 
#     text="Next Page", 
#     font=f,
#     command=prevPage
#     ).pack(fill=X, expand=TRUE, side=LEFT)

ws.mainloop()
