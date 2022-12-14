from lib2to3.pgen2.token import OP
from tkinter import *
from datetime import datetime, date
import mysql.connector
from mysql.connector import Error
from tkintertable import TableCanvas
from tkinter import ttk
import customtkinter


class Form:


    def __init__(self, master):
        self.frame = Frame(master)
        
        global name_entry
        global monomer_entry
        global cx_entry
        global temp_entry
        global volume_entry
        global cta_entry
        global device_entry

        name_label = Label(self.frame ,text = "Experiment Name").grid(row = 0,column = 0, sticky='e')
        
        name_entry = Entry(self.frame)
        name_entry.grid(row = 0,column = 1,sticky='e')

        monomer_label = Label(self.frame ,text = "Monomer Used").grid(row = 0,column = 2, sticky='e')
        monomer_entry = Entry(self.frame)
        monomer_entry.grid(row = 0,column = 3, sticky='e')

        cta_label = Label(self.frame ,text = "CTA used").grid(row = 1,column = 0,sticky='n')
        cta_entry = Entry(self.frame)
        cta_entry.grid(row = 1,column = 1, sticky='n')

        cx_label = Label(self.frame ,text = "Cx/Cm Ratio").grid(row = 1,column = 2, sticky='n')
        cx_entry= Entry(self.frame)
        cx_entry.grid(row = 1,column = 3, sticky='n')

        temp_label = Label(self.frame ,text = "Temperature").grid(row = 2,column = 0, sticky='n')
        temp_entry= Entry(self.frame)
        temp_entry.grid(row = 2,column = 1, sticky='n')

        volumn_label = Label(self.frame ,text = "Volume").grid(row = 2,column = 2, sticky='n')
        volume_entry= Entry(self.frame)
        volume_entry.grid(row = 2,column = 3, sticky='n')

        device_label = Label(self.frame, text="Select your device").grid(row=3 , column=0)
        global OPTIONS
        OPTIONS=[]
        mydb = mysql.connector.connect(host='localhost',
                                        database='momoda',
                                        user='root',
                                        password='')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT id, model, company FROM measurements_device")
        myresult = mycursor.fetchall()
        for x in myresult:
            OPTIONS.append(x)
        temp_array = []
        for i in OPTIONS:
            temp_array.append(i[1]+ ",  (Company: " +i[2] + " )")
        temp_array = tuple(temp_array)
        print(temp_array)
    


        variable = StringVar()
        device_entry = ttk.Combobox(self.frame, textvariable=variable)
        device_entry['values'] = temp_array
        device_entry['state'] = 'readonly'
        device_entry['state'] = 'normal'
        device_entry.grid(row=3 , column=1)
        self.frame.grid(row=0, column=0)


        Button(
        self.frame, 
        text="Submit",
        command=self.nextPage
        ).grid(row=3 ,column=3)

    def nextPage(self):
        device_array_id = device_entry.current()
        device_id = OPTIONS[device_array_id][0]
        mydb = mysql.connector.connect(host='localhost',
                                        database='momoda',
                                        user='root',
                                        password='')
        values = {"name":"", "monomer": "", "cta":"", "cx":"", "temp":"", "volume": ""}
        
        
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


        mycursor = mydb.cursor()
        sql = "INSERT INTO experiments_experiment (date, time, name, temperature, total_volume, monomer, CTA, cx_ratio, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (date_now, time_now, values['name'], values['temp'], values['volume'], values['monomer'], values['cta'], values['cx'], 1)
        mycursor.execute(sql, val)
        mydb.commit()


        # sql = "INSERT INTO measurements_measurement (date, time, name, temperature, total_volume, monomer, CTA, cx_ratio, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # val = (date_now, time_now, values['name'], values['temp'], values['volume'], values['monomer'], values['cta'], values['cx'], 1)
        # mycursor.execute(sql, val)
        # mydb.commit()
        print(mycursor.lastrowid)
        context ={"experiment_id" : mycursor.lastrowid, 'device_id':device_id}
        spreadsheet = Spreadsheet(context)

class Spreadsheet:
    def __init__(self, context):
        self.context=context
        self.measurement_id = None
        top = Toplevel()
        self.frame = Frame(top)
        self.table = TableCanvas(top)
        self.table.show()
        self.table.getModel().columnlabels = {'1': 'tres_GPC', '2': 'D', '3': 'Mn', '4': 'Mn theory', '5': 'Mw'}
        self.label_for_file = Label(self.frame, text="enter the file name (excluding .csv)")
        self.label_for_file.grid()
        self.file = Entry(self.frame)
        self.file.grid() 

        self.button = Button(self.frame, text="submit", command=self.getData).grid()
        self.button = Button(self.frame, text="clear", command=self.clearData).grid()
        self.frame.grid()
    def clearData(self):
        self.table.clearData()
    def getData(self):
        print(self.context['experiment_id'])
        mydb = mysql.connector.connect(host='localhost',
                                        database='momoda',
                                        user='root',
                                        password='')


        filename = self.file.get() + '.csv'
        mycursor = mydb.cursor()
        sql = "INSERT INTO measurements_measurement (file, is_approved, device_id, experiment_id) VALUES (%s, %s, %s, %s)"
        val = (filename, 1, self.context['device_id'], self.context['experiment_id'])
        mycursor.execute(sql, val)
        mydb.commit()
        self.measurement_id = mycursor.lastrowid
        print(self.measurement_id)
        print(mycursor.rowcount, "record inserted.")

        data = self.table.model.data
        for key in data:
           filled_column_per_row = len(data[key].keys())
           if filled_column_per_row != 5 :
                print("all of the 5 column needs to be filled")
                continue
           else: 
                row_data = data[key]
                tres_gpc = row_data["1"]
                d = row_data["2"]
                mn = row_data["3"]
                mn_theory = row_data["4"]
                mw = row_data["5"]

                
                mycursor = mydb.cursor()
                sql = "INSERT INTO measurements_gpc_data (tres_GPC, D, Mn, Mn_theory, Mw, measurement_id) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (tres_gpc, d, mn, mn_theory, mw, str(self.measurement_id))
                mycursor.execute(sql, val)
                mydb.commit()

                print(mycursor.rowcount, "record inserted.")
        
                



            
    
customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

root = Tk()
form = Form(root)
root.mainloop()


