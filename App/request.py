# # # # import requests

# # # # x = requests.get('https://cactus.nci.nih.gov/chemical/structure/1-dodecanethiol/mw')

# # # # print(x.text)


# # # from tkinter import *

    
# # # root = Tk()
# # # frame = Frame(root)
# # # frame.pack()
# # # scrollbar = Scrollbar(frame)
# # # scrollbar.pack( side = RIGHT, fill = Y )

# # # mylist = Listbox(frame, yscrollcommand = scrollbar.set, selectmode=MULTIPLE )
# # # for line in range(100):
# # #    mylist.insert(END, "This is line number " + str(line))

# # # mylist.pack( side = LEFT, fill = BOTH )
# # # scrollbar.config( command = mylist.yview )
# # # var1=StringVar()
# # # def submit():
# # #     for i in mylist.curselection():

# # #         value = mylist.get(i)
# # #         print(value)

# # # button = Button(root, text="submit", command=submit)
# # # button.pack()

# # # mainloop()


# # import customtkinter, tkinter

# # app = customtkinter.CTk()
# # app.grid_rowconfigure(0, weight=1)
# # app.grid_columnconfigure(0, weight=1)

# # # create scrollable textbox
# # tk_textbox = tkinter.Text(app, highlightthickness=0)
# # tk_textbox.grid(row=0, column=0, sticky="nsew")

# # # create CTk scrollbar
# # ctk_textbox_scrollbar = customtkinter.CTkScrollbar(app, command=tk_textbox.yview)
# # ctk_textbox_scrollbar.grid(row=0, column=1, sticky="ns")

# # # connect textbox scroll event to CTk scrollbar
# # tk_textbox.configure(yscrollcommand=ctk_textbox_scrollbar.set)

# # app.mainloop()
# from database import DatabaseInterface as Db
# def find_id_by_name(table, name):
#     global mydb
#     mydb = Db().conn
#     mycursor = mydb.cursor()
#     query = "select id from {table_value} where name = '{name_value}'".format(table_value=table, name_value=name)
#     print(query)
#     mycursor.execute(query)
#     id = mycursor.fetchone()[0]
#     return id

# def get_model_id(arr):
    
#     for item in arr:
#         details = item.split(',')
#         model = details[0]
#         company = details[1].split(':')[1][1:-2]
#         print(model, company)

#         mydb = Db().conn
#         mycursor = mydb.cursor()
#         query = "select id from measurements_device where company = '{company}' and model = '{model}'".format(company=company, model=model)
#         print(query)
#         mycursor.execute(query)
#         id = mycursor.fetchone()
#         return id
    
# def count_not_null_elem(array):
#         count =0
#         for i in array:
#             if i!='':
#                 count+=1
#         return count

# print(count_not_null_elem(['', '']))

# dict={0: {'1': '12', '2': '12', '3': '12', '4': '12', '5': '12'}, 1: {}, 2: {'2': ''}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}, 8: {}, 9: {}}

# def check_atleast_two():
#     pass
a="""hi

dsf

dsf"""
print(repr(a))
