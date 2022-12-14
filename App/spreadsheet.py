from lib2to3.pgen2.token import OP
from tkinter import *
from datetime import datetime, date
import mysql.connector
from mysql.connector import Error
from tkintertable import TableCanvas
from tkinter import ttk
import customtkinter
from customtkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import pandas as pd
from tkinter.filedialog import askopenfilename
from database import DatabaseInterface as Db
import image_handler as handler


class Spreadsheet:
    def __init__(self, context):
        customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
        # customtkinter.set_default_color_theme("./dark-blue.json")
        
        self.context=context
        self.measurement_id = None
        top = Toplevel()

        top.geometry('1166x718')
        self.bg_frame = Image.open(handler.resource_path('image/background.jpg'))
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(top, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.place(x=0, y=0, relwidth=1, relheight=1)
        self.frame = CTkFrame(top, width=400)
        self.table = TableCanvas(top)
        self.table.show()
        self.table.getModel().columnlabels = {'1': 'tres_GPC', '2': 'Mw', '3':'Mn', '4':'Time', '5':'Conversion'}            
        self.label_for_file = CTkLabel(self.frame, text="enter the file name (excluding .csv)")
        self.label_for_file.grid(row=0, column=0, padx=(45, 5))
        self.file = CTkEntry(self.frame)
        self.file.grid(row=0, column=1, padx=(5, 45)) 
        self.button = CTkButton(self.frame, text="submit", command=self.getData, fg_color="green").grid(row=1, column=0, pady=(20, 10), padx=(20, 0))
        self.button1 = CTkButton(self.frame, text="clear", command=self.clearData, fg_color="red").grid(row=1, column=1,  pady=(20, 10), padx=(0, 20))
        
        self.excel_error = Label(self.frame, text="for each written row all five column should be filled", fg='red')
        self.filename_error = Label(self.frame, text="file name cannot be empty", fg='red')
        self.entry_type_error = Label(self.frame, text="the entry type of all cells should either be integer or decimal", fg='red')
        
        self.frame.grid(row=1, column=5)

    def import_csv(self):
            csv_file_path = askopenfilename()
            data = self.table.model.data
            df = pd.read_csv(csv_file_path)
            COLUMNS = len(df.columns)
            ROWS = len(df)
            for row in range(ROWS):
                for column in range(COLUMNS):
                    data[row][column] = 5
                    
    def clearData(self):
        self.table.clearData()

    def getData(self):
        mydb = Db().conn
        data = self.table.model.data
        is_input_null = self.check_input_null(data)
        is_input_type= self.check_input_type(data)
        is_empty_sheet = self.check_empty_sheet(data)
        print(is_input_null, is_input_type, is_empty_sheet)
        print(data)
        insert_result = []
        if is_input_null and is_input_type and is_empty_sheet:
            print("hello")
            for key in data:
                if not data[key]:
                    continue
            
                filled_column_per_row = len(data[key].keys())
                if self.file.get():
                    filename = self.file.get() + '.csv'
                    mycursor = mydb.cursor()
                    for device_id in self.context['device_ids']:
                        sql = "INSERT INTO measurements_measurement (file, is_approved, device_id, experiment_id) VALUES (%s, %s, %s, %s)"
                        val = (filename, 1, device_id, self.context['experiment_id'])
                        mycursor.execute(sql, val)
                    mydb.commit()
                    self.measurement_id = mycursor.lastrowid
                    self.file.configure(fg_color='white')
                    self.file.configure(bg_color='white')


                else:
                    self.excel_error.grid_forget()
                    self.file.configure(fg_color='red')
                    self.file.configure(bg_color='red')
                    self.filename_error.grid(row=3, column=0)
                    return

                if not self.check_input_null(data) :
                        print("error #1")
                        self.filename_error.grid_forget()
                        self.entry_type_error.grid_forget()
                        self.excel_error.grid(row=3, column=0)
                        break

                elif not self.check_input_type(data) :
                        print("error #2")
                        self.filename_error.grid_forget()
                        self.excel_error.grid_forget()
                        self.entry_type_error.grid(row=3, column=0)
                        break
                
                elif not self.check_empty_sheet(data):
                     print("error #3")
                     self.filename_error.grid_forget()
                     self.excel_error.grid_forget()
                     self.excel_error.grid(row=3, column=0)
                     break

                        
                else: 
                        
                        row_data = data[key]
                    
                        # print(True)

                        tres_gpc = row_data["1"] if "1" in row_data else None
                        mw = row_data["2"] if "2" in row_data else None
                        mn = row_data["3"] if "3" in row_data else None
                        res_time = row_data["4"] if "4" in row_data else None
                        conversion = row_data["5"] if "5" in row_data else None
                        mycursor = mydb.cursor()
                        sql = "INSERT INTO measurements_gpc_data (tres_GPC, Mw, Mn, measurement_id) VALUES (%s, %s, %s, %s)"
                        val = (tres_gpc, mw, mn, str(self.measurement_id))
                        mycursor.execute(sql, val)
                        measurement_gpc_id = mycursor.lastrowid
                        mydb.commit()


                        sql = "INSERT INTO measurements_data (res_time, result, measurement_id) VALUES (%s, %s, %s)"
                        val = (res_time, conversion, str(self.measurement_id))
                        mycursor.execute(sql, val)
                        measurement_gpc_data_id = mycursor.lastrowid
                        mydb.commit()
                        insert_result.append("true")

                        # messagebox.showinfo(title=None, message="File has been added successfully")

            messagebox.showinfo(title=None, message="File has been added successfully")  
        else:
             
                if not self.check_input_null(data) :
                        print("error #1")
                        self.filename_error.grid_forget()
                        self.excel_error.grid(row=3, column=0)
                        insert_result.append(False)

                elif not self.check_input_type(data) :
                        print("error #2")
                        self.filename_error.grid_forget()
                        self.entry_type_error.grid(row=3, column=0)
                        insert_result.append(False)
   


    def check_input_null(self, dict):
        result = True
        for key in dict:
            array = list(dict[key].values())
            non_null_elems=self.count_not_null_elem(array)
            print(non_null_elems)
            print(array)
            if len(array)==0: 
                continue
            if (non_null_elems > 5  or non_null_elems < 2) and non_null_elems !=0:
                result = False
                break


        return result

    def check_input_type(self, dict):
        result = True
        try:
            for key in dict:
                
                array = list(dict[key].values())
                non_null_elems=self.count_not_null_elem(array)
                if non_null_elems >= 2 and non_null_elems <= 5:
                    for elem in array:
                        if elem !='':
                            if isinstance(int(elem), int) or isinstance(float(elem), elem):
                                result = True
                            else:
                                result=False
                                break

            return result

        except:
            result = False
            return result

    
    
    def count_not_null_elem(self, array):
        count =0
        for i in array:
            if i!='':
                count+=1
        return count

    
    def check_empty_sheet(self, dict):
        result = 0

        for key in dict:
            
            array = list(dict[key].values())
            null_items_count=0
            for i in array:
                if i != '':
                    null_items_count += 1
                if null_items_count == 2:
                    result+=1
        print("result: " + str(result))
        if result < 1:
            return False
        else:
             return True

            



            
                    



            
    
