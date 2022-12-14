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


class FirstPage(tk.Frame):  
  
    def __init__(self, parent, controller, width=500, height=400):  
        tk.Frame.__init__(self, parent) 
        self.controller = controller
        self.context = None

        

        self.login_frame=Frame(self)
        self.frame.grid(1, 0)


        self.contact_frame=Frame(self)
        self.frame.grid(1, 0)






        
   
        
        
customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
# customtkinter.set_default_color_theme("./dark-blue.json")




