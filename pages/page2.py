import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkintertable import TableCanvas
import customtkinter
ws = Tk()
ws.geometry('400x300')
ws.title('PythonGuides')
# ws['bg']='#ffbf00'
def submit():
    pass
f = ("Times bold", 14)
frame = Frame(ws)
frame.grid(row=1, column=1)

table = TableCanvas(frame)
table.show()
button = Button(frame, text ="Submit", command = submit).grid(row=2, column=1)
print(values)