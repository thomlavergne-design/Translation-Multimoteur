import tkinter as tk
from tkinter import ttk
from Essai_Discussion_Arduino import *
from Photodiode_C9329 import *

class ArduinoMoteurFrame(tk.LabelFrame):
    def __init__(self, master=None, identity="M1",**Kwargs):
        super().__init__(master,**Kwargs)
        # Création des classes arduino et Ampli photodiode
     
        
        # Configuration de la communication série
        self.identity=identity
        self.configure(borderwidth=2, relief="groove",text=self.identity,font=('helvetica',10,'italic'), padx=10, pady=10)
        
        # Création des widgets
        self.create_widgets()

    def create_widgets(self):
        # Première ligne : Boutons d'alimentation et Home
        self.power_button = tk.Button(self, text="Moteur Eteins", width=50, bg='light pink', relief='raised', command=self.send_power_command)
        self.power_button.grid(row=0, column=0, columnspan=3, padx=50, ipady=10)
        self.Allume=False

        self.home_button = tk.Button(self, text="Home", width=50, command=self.send_home_command)
        self.home_button.grid(row=0, column=3, columnspan=3,padx=10, ipady=10)

        # Deuxième ligne : Variateurs pour la vitesse et l'accélération
        self.speed_label = tk.Label(self, text="Vitesse:")
        self.speed_label.grid(row=1, column=0, padx=2, pady=10)

        self.speed_scale = tk.Scale(self, from_=0, to=1000, length=200, orient=tk.HORIZONTAL)
        self.speed_scale.grid(row=1, column=1, padx=0, pady=10)

        self.speed_unit = tk.StringVar()
        self.speed_unit.set("Tour/min")
        self.speed_unit_menu = tk.OptionMenu(self, self.speed_unit, "pas/s", "Tour/min")
        self.speed_unit_menu.grid(row=1, column=2, padx=2, pady=10)

        self.accel_label = tk.Label(self, text="Accélération:")
        self.accel_label.grid(row=1, column=3, padx=20, pady=10)

        self.accel_scale = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL)
        self.accel_scale.grid(row=1, column=4, padx=10, pady=10)

        self.accel_unit = tk.StringVar()
        self.accel_unit.set("pas/s²")
        self.accel_unit_menu = tk.OptionMenu(self, self.accel_unit, "pas/s²", "Tour/min²")
        self.accel_unit_menu.grid(row=1, column=5, padx=0, pady=10)

        # Troisième ligne : Boutons pour la direction
        self.direction_var = tk.StringVar()
        self.direction_var.set("none")

        self.direction_forward_button = tk.Radiobutton(self, text="Avant", variable=self.direction_var, value="forward", command=self.send_direction_command)
        self.direction_forward_button.grid(row=3, column=0, padx=10, pady=10)

        self.direction_backward_button = tk.Radiobutton(self, text="Arrière", variable=self.direction_var, value="backward", command=self.send_direction_command)
        self.direction_backward_button.grid(row=3, column=1, padx=10, pady=10)

        
        self.step_label = tk.Label(self, text="Nombre:")
        self.step_label.grid(row=3, column=3, padx=10, pady=10)

        self.step_entry = tk.Entry(self)
        self.step_entry.grid(row=3, column=4, padx=10, pady=10)

        self.step_unit = tk.StringVar()
        self.step_unit.set("pas")
        self.step_unit_menu = tk.OptionMenu(self, self.step_unit, "pas", "tour", "micropas")
        self.step_unit_menu.grid(row=3, column=5, padx=10, pady=10)
        
        # Quatrième ligne : Champ de texte et liste déroulante pour l'unité
        self.Move_button = tk.Button(self, text="Bouge de là !", width=50, bg='light green', command=self.send_power_command)
        self.Move_button.grid(row=4, column=0, columnspan=3, padx=10, ipady=10,pady=10)

        self.stop_button = tk.Button(self, text="STOP !", bg='dark red', fg='white', width=50, command=self.send_power_command)
        self.stop_button.grid(row=4, column=3, columnspan=3, padx=10, ipady=10,pady=10)

    def send_power_command(self):
        if self.Allume==False :
            self.power_button.config(text="Moteur Allumé",bg='light green',relief='sunken')
            self.Allume=True
        else :
            self.power_button.config(text="Moteur Eteins",bg='light pink',relief='raised')
            self.Allume=False
        command = "POWER_ON\n"
       

    def send_home_command(self):
        command = "HOME\n"
      

    def send_direction_command(self):
        direction = self.direction_var.get()
        if direction == "forward":
            command = "DIR_FORWARD\n"
        elif direction == "backward":
            command = "DIR_BACKWARD\n"
        else:
            return
        
    def send_speed_command(self):
        speed = self.speed_scale.get()
        unit = self.speed_unit.get()
        command = f"SPEED {speed} {unit}\n"
    

    def send_accel_command(self):
        accel = self.accel_scale.get()
        unit = self.accel_unit.get()
        command = f"ACCEL {accel} {unit}\n"
       

    def send_step_command(self):
        steps = self.step_entry.get()
        unit = self.step_unit.get()
        command = f"STEPS {steps} {unit}\n"
    
#def Buton_Kill(appli):
#   appli.destroy(-1)
#   del appli[-1]


if __name__ == "__main__":
    root=tk.Tk()
    # Remplacez 'COM3' par le port série de votre Arduino
    app=[0]*3
    for i in range(3):
        app[i] = ArduinoMoteurFrame(master=root,identity="M"+str(i))
        app[i].pack(padx=2,pady=10)
#    tk.Button(root,text="KILL",command=Buton_Kill(app)).pack()
    
    root.mainloop()
