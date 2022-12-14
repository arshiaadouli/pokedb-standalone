import tkinter as tk  
import form
import login
from PIL import Image, ImageTk
import landingpage
import monomer
import os, sys
import image_handler as handler

  
LARGE_FONT= ("Verdana", 12)  
  
  
class Main(tk.Tk):  
  
    def __init__(self, *args, **kwargs):  
          
        tk.Tk.__init__(self, *args, **kwargs)  
        self.geometry('1166x718')
        self.state('zoomed')
        
        self.bg_frame = Image.open(handler.resource_path('image/background.jpg'))
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = tk.Label(self, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')
        
        global container
        container = tk.Frame(self, bg="#e0e0d1", width=950, height=600)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER) 
        self.frames = {} 
        self.user = None
        self.experiment_id="asdasde" 
        self.device_id=None
        
        for F in (login.Login, landingpage.LandingPage, form.MyForm, monomer.Monomer):
  
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
        self.show_frame(login.Login)


# Logo = resource_path("Logo.png")    
  
    def show_frame(self, cont): 
        
        self.frames[cont] = cont(container, self)
        frame = self.frames[cont] 
        frame.grid(row = 0, column = 0, sticky ="nsew")
        frame.tkraise()

app = Main()  
app.mainloop()  
