from tkinter import *
from customtkinter import *
import login
import customtkinter
import landingpage
app = Tk()
frame = Frame(app)
def callbackFunc(company):
    print(company)
    if company=="add":
        landingpage.LandingPage()

frame.pack()
# combobox_var = customtkinter.StringVar()
array=["one", "two", "three", "add"]
company_entry = CTkComboBox(frame, values=array, command=callbackFunc)
company_entry.pack()
if(company_entry.get()=="add"):
    print("add")
app.mainloop()


