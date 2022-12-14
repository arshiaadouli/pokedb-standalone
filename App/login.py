from tkinter import *
from PIL import Image, ImageTk
from customtkinter import *
import form
import mysql.connector
from mysql.connector import Error
from passlib.hash import django_pbkdf2_sha256 as handler
# from form import getFrame
import tkinter as tk
from database import DatabaseInterface as Db
import landingpage
import image_handler as handlers


class Login(tk.Frame):  
  
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent, width=950, height=600)  
        self.controller = controller
        self.empty_entry_error = Label(self,text = "Please fill username and password input", fg="red")
        self.user=None
        self.side_image = Image.open(handlers.resource_path('image/vector-login.webp'))
        self.side_image = self.side_image.resize((400, 500))
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self, image=photo, bg='#f3ece9', fg='white')
        self.side_image_label.image = photo
        self.side_image_label.place(x=30, y=40)


        self.avatar = Image.open(handlers.resource_path('image/avatar.png'))
        self.avatar = self.avatar.resize((150, 150))
        photo = ImageTk.PhotoImage(self.avatar)
        self.avatar_label = Label(self, image=photo, bg='#f3ece9', fg='#040405')
        self.avatar_label.image = photo
        self.avatar_label.place(x=600, y=40)


        self.sign_in_label = Label(self, text='Sign In', bg="#f3ece9", fg="black", font = ('yu gothic ui', 17, 'bold'))
        self.sign_in_label.place(x=640, y= 205)

        self.username_label = Label(self, text='Username', bg="#f3ece9", fg="#6b6a69", font = ('yu gothic ui', 13, 'bold'))
        self.username_label.place(x=640, y= 270)

        self.username_entry = CTkEntry(self, width=350, height=40)
        self.username_entry.place(x=520, y=300)

        self.password_label = Label(self, text='password', bg="#f3ece9", fg="#6b6a69", font = ('yu gothic ui', 13, 'bold'))
        self.password_label.place(x=640, y= 355)
        
        self.password_entry = CTkEntry(self, show="*", width=350, height=40)
        self.password_entry.place(x=520, y=385)

        self.submit = CTkButton(self, text="LOG IN", width=350, height=35, command=self.login)
        self.submit.place(x=520, y=435)



    def login(self):
        email = self.username_entry.get()
        self.is_user_valid(email)

    def is_user_valid(self, email):
        if self.form_validation():

            mydb = Db().conn
            mycursor = mydb.cursor()

            query = ("SELECT * FROM users_user where email = %s")
            mycursor.execute(query, (email,))
            
            result = mycursor.fetchone()
            self.user = result
            self.controller.user = result
            raw_pwd = ''
            if result:
                hash_pwd = result[1]
                entered_pwd = self.password_entry.get()
                if handler.verify(entered_pwd, hash_pwd):
                    self.controller.show_frame(landingpage.LandingPage)

                else:
                    Label(self ,text="wrong username or password", fg='red').place(x=520, y=470)  
            else:
                    Label(self ,text="wrong username or password", fg='red').place(x=520, y=470)


            
    def form_validation(self):
        validations=[]
        username_validation = self.input_field_validation(self.username_entry, str)
        password_validation = self.input_field_validation(self.password_entry, str)
        validations.append(username_validation)
        validations.append(password_validation)
        return all(validations)

    def input_field_validation(self, entry, type):


        text = entry.get()

        
        if len(text) < 1:
            entry.configure(fg_color='red')
            entry.configure(bg='red')
            self.empty_entry_error.place(x=520, y=490) 
            return False
        entry.configure(fg_color='white')
        entry.configure(bg_color='white')
        self.empty_entry_error.forget()
        return True