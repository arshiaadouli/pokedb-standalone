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
import form
import monomer
import image_handler as handler
import deviceForm
class LandingPage(tk.Frame):  
  
    def __init__(self, parent, controller, width=500, height=400):  
        tk.Frame.__init__(self, parent) 
        self.controller = controller
        self.context = None
    
        self.user = self.controller.frames[login.Login].user
        self.user_fullname=None
        if(self.user):
            self.user_fullname = self.user[4]
        if(self.user_fullname):
            user_label = Label(self ,text = "Welcome "+self.user_fullname, font=("Arial", 25)).grid(row = 0,column = 0, pady=(10, 30), padx=40)
            CTkButton(
            self, 
            text="Logout",fg_color="red",
            command=lambda:self.controller.show_frame(login.Login)
            ).place(relx=0.8, rely=0.03)
        self.frame_monomer=Frame(self, bd=0)

        self.monomer_icon = Image.open(handler.resource_path('image/monomer-icon.jpg'))
        self.monomer_icon = self.monomer_icon.resize((150, 150))
        photo = ImageTk.PhotoImage(self.monomer_icon)
        self.monomer_label = Label(self.frame_monomer, image=photo, bg='#f3ece9', fg='#040405')
        self.monomer_label.image = photo
        self.monomer_label.pack()
        self.monomer_label.bind('<Button-1>', self.monomer_redirect)
        Label(self.frame_monomer, text="Add Monomer").pack()
        self.frame_monomer.bind("<Button-1>", self.monomer_redirect)
        self.frame_monomer.place(relx=0.2, rely=0.5, anchor=CENTER)
        




        self.frame_exp=Frame(self, bd=0)
        self.exp_icon = Image.open(handler.resource_path('image/add-exp.png'))
        self.exp_icon = self.exp_icon.resize((150, 150))
        photo = ImageTk.PhotoImage(self.exp_icon)
        self.exp_label = Label(self.frame_exp, image=photo, bg='#f3ece9', fg='#040405')
        self.exp_label.image = photo
        self.exp_label.pack()
        self.exp_label.bind('<Button-1>', self.exp_redirect)
        Label(self.frame_exp, text="Add Experiment").pack()
        self.frame_exp.bind("<Button-1>", self.exp_redirect)
        self.frame_exp.place(relx=0.5, rely=0.5, anchor=CENTER)



        self.frame_device=Frame(self, bd=0)
        self.device_icon = Image.open(handler.resource_path('image/device.jpg'))
        self.device_icon = self.device_icon.resize((150, 150))
        photo = ImageTk.PhotoImage(self.device_icon)
        self.device_label = Label(self.frame_device, image=photo, bg='#f3ece9', fg='#040405')
        self.device_label.image = photo
        self.device_label.pack()
        self.device_label.bind('<Button-1>', self.device_redirect)
        Label(self.frame_device, text="Add Devices").pack()
        self.frame_device.bind("<Button-1>", self.device_redirect)
        self.frame_device.place(relx=0.80, rely=0.5, anchor=CENTER)


    def monomer_redirect(self, event):
        self.controller.show_frame(monomer.Monomer)
    def exp_redirect(self, event):
        self.controller.show_frame(form.MyForm)
    def csv_redirect(self, event):
        self.controller.show_frame(spreadsheet.Spreadsheet)
    def device_redirect(self, event):
        self.controller.show_frame(deviceForm.DeviceForm)
        

        
customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
# customtkinter.set_default_color_theme("./dark-blue.json")




