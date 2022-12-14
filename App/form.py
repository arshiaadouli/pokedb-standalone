from lib2to3.pgen2.token import OP
from tkinter import *
from datetime import datetime, date
import mysql.connector
from mysql.connector import Error
from tkintertable import TableCanvas
from tkinter import ttk
import customtkinter
from customtkinter import *
import spreadsheet
from PIL import Image, ImageTk
import tkinter as tk
import login
from database import DatabaseInterface as Db
import landingpage


class MyForm(tk.Frame):  
  
    def __init__(self, parent, controller, width=500, height=400):  
        tk.Frame.__init__(self, parent) 
        self.controller = controller
        self.context = None
    
        self.user = self.controller.frames[login.Login].user
        self.user_fullname=None
        if(self.user):
            self.user_fullname = self.user[4] 

        Label(self, text="Add New Experiment ", font =("Helvetica",20)).pack()
        

        self.frame=Frame(self)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        global name_entry
        global monomer_entry
        global cta_entry
        global monomer_conc_entry
        global temp_entry
        global volume_entry
        global cta_entry
        global device_entry 
        global init_entry
        global cta_conc_entry
        global init_conc_entry
        global mydb

        mydb = Db().conn


        self.empty_entry_error = Label(self.frame, text="All of the inputs need to be filled", fg="red")
        self.wrong_type_entry = Label(self.frame, text="Wrong input type for highlighted inputs", fg="red")
  
        back_button = CTkButton(self, text='Landing Page', command=self.back)
        back_button.place(relx=0.08, rely=0.05, anchor=CENTER)

        name_label = CTkLabel(self.frame ,text = "Experiment Name").grid(row = 0,column = 0, pady=(10, 30))
        name_entry = CTkEntry(self.frame)
        name_entry.grid(row = 0,column = 1,sticky='e', pady=(10, 30) )


        mycursor = mydb.cursor()
        mycursor.execute("SELECT name_id FROM measurements_monomer")
        myresult = mycursor.fetchall()  
        array = []
        for id in myresult:
            sql = "SELECT name FROM chemicals_name where id = %s"
            val = (id)
            mycursor.execute(sql, val)
            name = mycursor.fetchone()  
            print(name)
            array.append(name[0])


        monomer_label = CTkLabel(self.frame,text = "Monomer Used").grid(row = 0,column = 2, pady=(10, 30))
        monomer_entry = CTkComboBox(self.frame, values=array)
        monomer_entry.set(array[0])
        monomer_entry.grid(row = 0,column = 3, pady=(10, 30), padx=(0, 10))

        mycursor = mydb.cursor()
        mycursor.execute("SELECT name FROM measurements_cta")
        myresult = mycursor.fetchall()  
        array = []
        for item in myresult:
            array.append(item[0])

        cta_label = CTkLabel(self.frame ,text = "CTA used").grid(row = 1,column = 0 , pady=(0, 30))
        cta_entry = CTkComboBox(self.frame, values=array)
        cta_entry.set(myresult[0])
        cta_entry.grid(row = 1,column = 1 , pady=(0, 30))

        monomer_conc_label = CTkLabel(self.frame ,text = "Monomer Concentration").grid(row = 1,column = 2 , pady=(0, 30))
        monomer_conc_entry= CTkEntry(self.frame)
        monomer_conc_entry.grid(row = 1,column = 3, pady=(0, 30), padx=(0, 10))

        temp_label = CTkLabel(self.frame,text = "Temperature").grid(row = 2,column = 0 , pady=(0, 30))
        temp_entry= CTkEntry(self.frame)
        temp_entry.grid(row = 2,column = 1 , pady=(0, 30))

        volumn_label = CTkLabel(self.frame,text = "Volume").grid(row = 2,column = 2 , pady=(0, 30))
        volume_entry= CTkEntry(self.frame)
        volume_entry.grid(row = 2,column = 3 , pady=(0, 30), padx=(0, 10))

        device_label = CTkLabel(self.frame, text="Select your device").grid(row=3 , column=0 , pady=(0, 30))
        global OPTIONS
        global temp_array
        
        device_entry = Listbox(self.frame, height=3, selectmode="multiple")
        device_entry.grid(row=3 , column=1, pady=(0, 30))
        OPTIONS=[]
        mycursor = mydb.cursor()
        mycursor.execute("SELECT id, calibration_details, company_details FROM measurements_device")
        myresult = mycursor.fetchall()
        for x in myresult:
            OPTIONS.append(x)
        temp_array = []
        for i in OPTIONS:
            temp_array.append(i[2])

        for i in temp_array:
            device_entry.insert(END, i)



            

        device_entry.select_set(0) #This only sets focus on the first item.
        device_entry.event_generate("<<ListboxSelect>>")


    
        mycursor = mydb.cursor()
        mycursor.execute("SELECT name FROM measurements_initiator")
        myresult = mycursor.fetchall()  
        array = []
        for item in myresult:
            array.append(item[0])

        init_label = CTkLabel(self.frame ,text = "Initiator used").grid(row = 3,column = 2 , pady=(0, 30))
        init_entry = CTkComboBox(self.frame, values=array)
        init_entry.set(myresult[0])
        init_entry.grid(row = 3,column = 3 , pady=(0, 30))


        cta_conc_label = CTkLabel(self.frame ,text = "CTA Concentration").grid(row = 4,column = 0 , pady=(0, 30))
        cta_conc_entry= CTkEntry(self.frame)
        cta_conc_entry.grid(row = 4,column = 1, pady=(0, 30), padx=(0, 10))


        init_conc_label = CTkLabel(self.frame ,text = "Initiator Concentration").grid(row = 4,column = 2 , pady=(0, 30))
        init_conc_entry= CTkEntry(self.frame)
        init_conc_entry.grid(row = 4,column = 3, pady=(0, 30), padx=(0, 10))
        
        CTkButton(
        self.frame, 
        text="Submit",
        command=self.nextPage
        ).grid(row=5 ,column=3, pady=(40, 15), padx=(0, 10))

        CTkButton(
        self.frame, 
        text="Logout",fg_color="red",
        command=lambda:self.controller.show_frame(login.Login)
        ).grid(row=6 ,column=3, pady=(20, 8), padx=(0, 10))

        # if(self.user_fullname):
        #     user_label = Label(self ,text = "Welcome "+self.user_fullname, font=("Arial", 25)).grid(row = 0,column = 0, pady=(10, 30), padx=40)
    
    def nextPage(self):
        if self.form_validation():

            # device_array_id = device_entry.get()
            # device_id = temp_array.index(device_array_id)
            # device_id = OPTIONS[device_id][0]
            values = {"name":"", "monomer": "", "cta":"", "monomer_conc":"", "temp":"", "volume": "", "device":[], "init":"", "cta_conc":"", "init_conc":""}
            
            
            now = datetime.now()
            time_now=now.strftime("%H:%M:%S")
            today = date.today()
            date_now= today.strftime("%Y-%m-%d")

            values['name'] = name_entry.get()
            values['monomer'] = self.get_id_by_name("chemicals_name", monomer_entry.get())
            values['cta'] = self.get_id_by_name("measurements_cta", cta_entry.get())
            values['monomer_conc'] = monomer_conc_entry.get()
            values['temp'] = temp_entry.get()
            values['volume'] = volume_entry.get()
            values['device'] = []
            for i in device_entry.curselection():
                values['device'].append(device_entry.get(i))
            values['device'] = self.get_model_id(values['device'])
            values['init'] = self.get_id_by_name("measurements_initiator", init_entry.get())
            values['cta_conc'] = cta_conc_entry.get()
            values["init_conc"]= init_conc_entry.get()

            print(values)

            mycursor = mydb.cursor()
            sql = "INSERT INTO experiments_experiment (date, time, name, temperature, total_volume, monomer_concentration, cta_concentration, initiator_concentration, monomer_id, cta_id, initiator_id, user_id, reactor_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (date_now, time_now, values['name'], values['temp'], values['volume'], values['monomer_conc'], values['cta_conc'], values['init_conc'], values['monomer'], values['cta'], values['init'], self.user[0], 12)
            mycursor.execute(sql, val)
            mydb.commit()
            experiment_id = mycursor.lastrowid
            context = {}
            context['device_ids'] = values['device']
            context['experiment_id'] = experiment_id
            spreadsheet.Spreadsheet(context)



    def form_validation(self):

        name_validation = self.input_field_validation(name_entry, str)
        monomer_validation = self.input_field_validation(monomer_entry, str)
        cta_validation = self.input_field_validation(cta_entry, str)
        temp_validation = self.input_field_validation(temp_entry, float)
        volume_validation = self.input_field_validation(volume_entry, float)
        init_validation = self.input_field_validation(init_entry, str)
        cta_conc_validation = self.input_field_validation(cta_conc_entry, float)
        monomer_conc_validation = self.input_field_validation(monomer_conc_entry, float)
        init_conc_validation = self.input_field_validation(init_conc_entry, float)
        validations=[]
        validations.append(name_validation)
        validations.append(monomer_validation)
        validations.append(temp_validation)
        validations.append(volume_validation)
        validations.append(cta_validation)
        validations.append(init_validation)
        validations.append(cta_conc_validation)
        validations.append(monomer_conc_validation)
        validations.append(init_conc_validation)
        validations.append(self.device_validation())
        return all(validations)

    
    def device_validation(self):

        devices = []
        for i in device_entry.curselection():
                devices.append(device_entry.get(i))
        if len(devices)==0:
            self.wrong_type_entry.grid(column=0 , row=7)
            return False
        return True


    def input_field_validation(self, entry, type):


        text = entry.get()

        
        if len(text) < 1:
            self.wrong_type_entry.grid_remove()
            entry.configure(fg_color='red')
            entry.configure(bg_color='red')
            return False
        else:

            try:
                if(isinstance(type(text), type)):
                    self.empty_entry_error.grid_remove()
                    entry.configure(fg_color='white')
                    entry.configure(bg_color='white')         
                    return True
            except:
                entry.configure(fg_color='red')
                entry.configure(bg_color='red')
                self.wrong_type_entry.grid(column=0 , row=7)
                return False


        return True
    


    def get_id_by_name(self, table, name):
        global mydb
        mydb = Db().conn
        mycursor = mydb.cursor()
        query = "select id from {table_value} where name = '{name_value}'".format(table_value=table, name_value=name)
        print(query)
        mycursor.execute(query)
        id = mycursor.fetchone()[0]
        return id


    
    def get_model_id(self, arr):
        ids=[]

        print("array", arr)
        for item in arr:
            # details = item.split(',')
            # model = details[0]
            # company = details[1].split(': ')[1][1:-2]
            # print(model, company)
            print(item)
            mydb = Db().conn
            mycursor = mydb.cursor()
            query = "select id from measurements_device where company_details = {company_details}".format(company_details=repr(item))
            print(query)
            mycursor.execute(query)
            id = mycursor.fetchone()
            # print("id: ", id)
            ids.append(id[0])
            print(id)
        return ids


        
    def back(self):
        self.controller.show_frame(landingpage.LandingPage)
        
   
        
        
customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
# customtkinter.set_default_color_theme("./dark-blue.json")




