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
import requests
import landingpage
from tkinter import messagebox



class Monomer(tk.Frame):  
  
    def __init__(self, parent, controller, width=500, height=400):  
        tk.Frame.__init__(self, parent) 
        self.controller = controller
        self.context = None
    
        self.user = self.controller.frames[login.Login].user
        self.user_fullname=None
        if(self.user):
            self.user_fullname = self.user[4]  

        global search_entry


        global mydb
        global mycursor

        mydb = Db().conn
        mycursor = mydb.cursor()

        Label(self, text="Search the Monomer name", font =("Helvetica",20)).pack()
        search_entry = CTkEntry(self, width=500)
        search_entry.pack(pady=20)

        search_button = CTkButton(self, text='Search', command=self.search)
        search_button.pack()


        back_button = CTkButton(self, text='landing page', command=self.back)
        back_button.place(relx=0.08, rely=0.05, anchor=CENTER)





    def search(self):

        global names_entry
        global mw_entry
        global iupac_entry
        global stdinchikey_entry
        global stdinchi_entry
        global cas_entry
        global smiles_entry

        keyword = search_entry.get()
        dict = {
         "stdinchi":"",
         "stdinchikey":"",
         "mw":"",
         "cas":"", 
         "smiles":"", 
         "iupac_name":"", 
         "Names":""
        }
        for key in dict:
            request = requests.get('https://cactus.nci.nih.gov/chemical/structure/{}/{}'.format(keyword, key))
            if request.status_code != 500:
                dict[key] = request.text
                print(request)
        # print(dict)
        self.form_frame = Frame(self)
       
        self.form_frame.pack()

        iupac_label = Label(self.form_frame, text="IUPAC")
        iupac_label.grid(row=0, column=0)
        iupac_entry = CTkEntry(self.form_frame, width=300)
        iupac_entry.grid(row=0, column=1, padx=20, pady=20)
        iupac_entry.insert(0, dict["iupac_name"])


        smiles_label = Label(self.form_frame, text="Smiles")
        smiles_label.grid(row=0, column=2)
        smiles_entry = CTkEntry(self.form_frame, width=300)
        smiles_entry.grid(row=0, column=3,  padx=(0, 20))
        smiles_entry.insert(0, dict["smiles"])


        cas_label = Label(self.form_frame, text="CAS")
        cas_label.grid(row=1, column=0)
        cas_entry = CTkEntry(self.form_frame, width=400)
        cas_entry.grid(row=1, column=1, padx=20, pady=20)
        cas_entry.insert(0, dict["cas"])


        mw_label = Label(self.form_frame, text="MW")
        mw_label.grid(row=1, column=2)
        mw_entry = CTkEntry(self.form_frame, width=100)
        mw_entry.grid(row=1, column=3, padx=(0, 100))
        mw_entry.insert(0, dict["mw"])
        
        stdinchikey_label = Label(self.form_frame, text="Stdinchi key")
        stdinchikey_label.grid(row=2, column=0)
        stdinchikey_entry = CTkEntry(self.form_frame, width=300)
        stdinchikey_entry.grid(row=2, column=1, padx=20, pady=20)
        stdinchikey_entry.insert(0, dict["stdinchikey"])

        stdinchi_label = Label(self.form_frame, text="Stdinchi")
        stdinchi_label.grid(row=2, column=2)
        stdinchi_entry = CTkEntry(self.form_frame, width=490)
        stdinchi_entry.grid(row=2, column=3, padx=20, pady=20)
        stdinchi_entry.insert(0, dict["stdinchi"])

        names = dict['Names'].split("\n")
        names_label = Label(self.form_frame, text="Names")
        names_label.grid(row=3, column=0)
        names_entry = CTkComboBox(self.form_frame, values = names, width=215)
        names_entry.grid(row=3, column=1, padx=20, pady=20)

        # names_entry.insert(0, dict["stdinchi"])


        
        submit_button = CTkButton(self, text="Submit", command=self.submit)
        submit_button.pack()

    def back(self):
        self.controller.show_frame(landingpage.LandingPage)

    def submit(self):

        msg_box = messagebox.askquestion('Exit Application', 'Are you sure you want to insert your?',
                                        icon='warning')
        if msg_box == "yes":
            try:
                inchi_id = self.insert_inchi_table()
                smiles_id = self.insert_smiles_table(inchi_id)
                cas_id = self.insert_cas_table(inchi_id)
                name_id = self.insert_name_table(inchi_id)
                sql = "INSERT INTO measurements_monomer (name_id, smiles_id, cas_id, inchi_id ) VALUES (%s, %s, %s, %s)"
                val = (name_id, smiles_id, cas_id, inchi_id)
                mycursor.execute(sql, val)
                mydb.commit()
                self.controller.show_frame(landingpage.LandingPage)
            except:
                print("the inchi has been added previously")
                self.controller.show_frame(landingpage.LandingPage)



    def insert_inchi_table(self):
        sql = "INSERT INTO chemicals_inchi (inchi, inchi_key, mw) VALUES (%s, %s, %s)"
        val = (stdinchi_entry.get(), stdinchikey_entry.get(), mw_entry.get())
        mycursor.execute(sql, val)
        mydb.commit()
        return mycursor.lastrowid

    def insert_smiles_table(self, inchi_id):
        sql = "INSERT INTO chemicals_smiles (smiles, inchi_id) VALUES (%s, %s)"
        val = (smiles_entry.get(), inchi_id)
        mycursor.execute(sql, val)
        mydb.commit()
        return mycursor.lastrowid
    def insert_cas_table(self, inchi_id):
        sql = "INSERT INTO chemicals_cas (cas, inchi_id) VALUES (%s, %s)"
        val = (cas_entry.get(), inchi_id)
        mycursor.execute(sql, val)
        mydb.commit()
        return mycursor.lastrowid
    def insert_name_table(self, inchi_id):
        sql = "INSERT INTO chemicals_name (name, iupac, inchi_id) VALUES (%s, %s, %s)"
        val = (names_entry.get(), iupac_entry.get(), inchi_id)
        mycursor.execute(sql, val)
        mydb.commit()
        return mycursor.lastrowid
        
   
        
        
customtkinter.set_appearance_mode("light")  
customtkinter.set_default_color_theme("dark-blue")




