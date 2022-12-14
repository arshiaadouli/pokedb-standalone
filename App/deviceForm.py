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
import image_handler as handlers
import landingpage
import deviceForm
from tkinter import messagebox



class DeviceForm(tk.Frame):  
  
    def __init__(self, parent, controller, width=500, height=400):  
        tk.Frame.__init__(self, parent) 
        self.controller = controller
        self.context = None
    
        self.user = self.controller.frames[login.Login].user
        self.user_fullname=None
        if(self.user):
            self.user_fullname = self.user[4] 
        
        Label(self, text="Add New Device", font =("Helvetica",20)).pack()
        
        self.frame=Frame(self)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        

        CTkButton(self, text='landing page', command= lambda:self.controller.show_frame(landingpage.LandingPage)).place(x=15, y=15)
        global mydb
        mydb = Db().conn


        self.empty_entry_error = Label(self.frame, text="All of the inputs need to be filled", fg="red")
        self.wrong_type_entry = Label(self.frame, text="Wrong input type for highlighted inputs", fg="red")

        self.new_conv_label = Label(self.frame, text="new conversion")
        self.new_mn_label = Label(self.frame, text="new Mn")
        
        self.new_conv_entry = CTkEntry(self.frame)
        self.new_mn_entry = CTkEntry(self.frame)

        self.btn_conv = CTkButton(self.frame, text="Submit", command=self.submit_conv)
        self.btn_mn = CTkButton(self.frame, text="Submit", command=self.submit_mn)
  

        global company_entry
        global mn_entry
        global details_entry
        global conversion_entry


        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM measurements_conversion")
        myresult = mycursor.fetchall()  
        array = []
        for item in myresult:
            array.append(item[1])
        array.append("add new conversion")

        conversion_label = CTkLabel(self.frame,text = "Conversion").grid(row = 0,column = 0, pady=(10, 30))
        conversion_entry = CTkComboBox(self.frame, values=array, command=self.conversion_callback)
        conversion_entry.set(array[0])
        conversion_entry.grid(row = 0,column = 1, pady=(10, 30), padx=20)


        # mycursor.execute("SELECT * FROM experiments_company")
        # myresult = mycursor.fetchall()  
        # array = []
        # for item in myresult:
        #     array.append(item[1])
        # company_label = CTkLabel(self.frame,text = "Company").grid(row = 0,column = 2, pady=(10, 30))
        # company_entry = CTkComboBox(self.frame, values=array)
        # company_entry.set(array[0])
        # company_entry.grid(row = 0,column = 3, pady=(10, 30))


        company_label = CTkLabel(self.frame ,text = "Company Details").grid(row = 0,column = 2, pady=(10, 30))
        company_entry = CTkTextbox(self.frame, height=80)
        company_entry.grid(row = 0,column = 3,sticky='e', pady=(10, 30), padx=(30, 30) )


        mycursor.execute("SELECT * FROM measurements_mn")
        myresult = mycursor.fetchall()  
        array = []
        for item in myresult:
            array.append(item[1])
        array.append("add new Mn")
        mn_label = CTkLabel(self.frame,text = "Mn").grid(row = 4,column = 0, pady=(10, 30))
        mn_entry = CTkComboBox(self.frame, values=array, command=self.mn_callback)
        mn_entry.set(array[0])
        mn_entry.grid(row = 4,column = 1, pady=(10, 30), padx=20)


        details_label = CTkLabel(self.frame ,text = "Calibration Details").grid(row = 4,column = 2, pady=(10, 30))
        details_entry = CTkTextbox(self.frame, height=80)
        details_entry.grid(row = 4,column = 3,sticky='e', pady=(10, 30), padx=(30, 30) )

        CTkButton(
        self.frame, 
        text="Submit",
        command=self.nextPage
        ).grid(row=6 ,column=3, pady=(40, 15), padx=(0, 10))

        # CTkButton(
        # self.frame, 
        # text="Logout",fg_color="red",
        # command=lambda:self.controller.show_frame(login.Login)
        # ).grid(row=7 ,column=3, pady=(20, 8), padx=(0, 10))
    
        
        
    def get_id_by_name(self, table, name):
        global mydb
        mydb = Db().conn
        mycursor = mydb.cursor()
        query = "select id from {table_value} where title = '{name_value}'".format(table_value=table, name_value=name)
        print(query)
        mycursor.execute(query)
        id = mycursor.fetchone()[0]
        return id

    def get_id_by_name_company(self, table, name):
        global mydb
        mydb = Db().conn
        mycursor = mydb.cursor()
        query = "select id from {table_value} where name = '{name_value}'".format(table_value=table, name_value=name)
        print(query)
        mycursor.execute(query)
        id = mycursor.fetchone()[0]
        return id

    def nextPage(self):


        msg_box = messagebox.askquestion('Exit Application', 'Are you sure you want to insert your?',
                                        icon='warning')
        if msg_box == "yes":
            mydb = Db().conn
            mycursor = mydb.cursor()
            sql = "INSERT INTO measurements_device (company_details, conversion_id, mn_id, calibration_details) VALUES (%s, %s, %s, %s)"
            val = (company_entry.get("1.0", END), self.get_id_by_name('measurements_conversion', conversion_entry.get()), self.get_id_by_name('measurements_mn', mn_entry.get()), details_entry.get("1.0", END))
            mycursor.execute(sql, val)
            mydb.commit()
            self.controller.show_frame(landingpage.LandingPage)




    def go_back(self):
        self.controller.show_frame()

    def conversion_callback(self, choice):
        if choice == 'add new conversion':
            self.new_conv_label.grid(row=2, column=0)
            self.new_conv_entry.grid(row=2, column=1)
            self.btn_conv.grid(row=2, column=2)

    def mn_callback(self, choice):
        if choice == 'add new Mn':
            self.new_mn_label.grid(row=5, column=0)
            self.new_mn_entry.grid(row=5, column=1)
            self.btn_mn.grid(row=5, column=2)

    def submit_conv(self):
        mycursor = mydb.cursor()
        query = "insert into measurements_conversion (title) values ('{title}')".format(title=self.new_conv_entry.get())
        print(query)
        mycursor.execute(query)
        mydb.commit()
        self.controller.show_frame(deviceForm.DeviceForm)

    def submit_mn(self):
        mycursor = mydb.cursor()
        query = "insert into measurements_mn (title) values ('{title}')".format(title=self.new_mn_entry.get())
        print(query)
        mycursor.execute(query)
        mydb.commit()
        self.controller.show_frame(deviceForm.DeviceForm)
        

        

        
   
        
        
customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
# customtkinter.set_default_color_theme("./dark-blue.json")




