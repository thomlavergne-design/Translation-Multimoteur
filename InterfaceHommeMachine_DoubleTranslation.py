import tkinter as tk
from tkinter import ttk
from Essai_Discussion_Arduino import *
from Pilotage_motor import *

class IHM_DT(tk.Tk):
    def __init__(self):
        super().__init__()
         # Création des classes arduino et Ampli photodiode
        self.Pilote_Moteur=Arduino_Translation(Port="COM6",Baudrate="9600")
        
        # Paramètres gestion bouton
        self.com_arduino=False
        self.Enable=False
        self.Direction="0"

        self.Create_Widget()

        Moteurs=[0]*2
        for i in range(2):
            Moteurs[i] = ArduinoMoteurFrame(self,identity="M"+str(i+1))
            Moteurs[i].pack(padx=2,pady=10)

    def Create_Widget(self):
        #self.Title("Monochromateur Resort !")
        self.geometry("1000x800")

        # Frame pour les paramètres de communication
        self.com_frame = ttk.LabelFrame(self, text="Global parameters")
        self.com_frame.pack(padx=10, pady=10, fill="x")

        # Paramètres pour l'Arduino
            #Port com
        ttk.Label(self.com_frame, text="Port COM Arduino:").grid(row=0, column=0, padx=5, pady=5)
        self.arduino_port = tk.Entry(self.com_frame)
        self.arduino_port.insert(0,"COM6")
        self.arduino_port.grid(row=0, column=1, padx=5, pady=5)
            #Baudrate
        ttk.Label(self.com_frame, text="Baudrate Arduino:").grid(row=0, column=2, padx=5, pady=5)
        self.arduino_baudrate = tk.Entry(self.com_frame,textvariable="9600")
        self.arduino_baudrate.insert(0,"9600")
        self.arduino_baudrate.grid(row=0, column=3, padx=5, pady=5)
            #Bouton de démarage 
        self.open_com_arduino=tk.Button(self.com_frame,text="Com Arduino Eteint",bg='light pink', relief='raised', command=self.open_com_Arduino)
        self.open_com_arduino.grid(row=0, column=4, padx=5, pady=5)

    

    def open_com_Arduino(self):
        # Code pour démarrer ou éteindre la communication arduino pilote du moteur 
        # Modifie également l'aspect et l'effet du bouton
        if self.com_arduino==False :
            self.open_com_arduino.config(text="Com Arduino en cours",bg='light green',relief='sunken')
            self.com_arduino=True
            self.Pilote_Moteur.ChangePortSerie(NewPortName=self.arduino_port.get())
            self.Pilote_Moteur.ChangeBaudrate(NewBaudrate=self.arduino_baudrate.get())
            self.Pilote_Moteur.OpenCom()
        else :
            self.open_com_arduino.config(text="Com Arduino Eteint",bg='light pink',relief='raised')
            self.com_arduino=False
            self.Pilote_Moteur.CloseCom()




if __name__ == "__main__":
    app = IHM_DT()
    app.mainloop()
