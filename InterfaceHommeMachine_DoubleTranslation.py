import tkinter as tk
from tkinter import ttk
from Essai_Discussion_Arduino import *
from Pilotage_motor import *

class IHM_DT(tk.Tk):
    def __init__(self,Nombre_Moteurs:int):
        super().__init__()
         # Création des classes arduino et Ampli photodiode
        self.Pilote_Moteur=Arduino_Translation(Port="COM6",Baudrate="9600")
        
        # Paramètres gestion bouton
        self.com_arduino=False
        self.Enable=False
        self.Direction="0"

        self.Create_Widget_Global()
        self.Create_Widget_Coupling(Nb_moteur=Nombre_Moteurs)

        self.Moteurs=[0]*Nombre_Moteurs
        for i in range(Nombre_Moteurs):
            self.Moteurs[i] = ArduinoMoteurFrame(self,identity="M"+str(i+1))
            self.Moteurs[i].grid(row=i+1,column=0,columnspan=2,padx=2,pady=10)

        self.bind('<Control-B>',self.Envoi_Message)

    def Create_Widget_Global(self):
        #self.Title("Monochromateur Resort !")
        self.geometry("1050x900")

        # Frame pour les paramètres de communication
        self.com_frame = ttk.LabelFrame(self, text="Global parameters")
        self.com_frame.grid(row=0, column=0, padx=10, pady=10)

        # Paramètres pour l'Arduino
            #Port com
        ttk.Label(self.com_frame, text="Port COM Arduino:").grid(row=0, column=0, padx=5, pady=5)
        self.arduino_port = tk.Entry(self.com_frame)
        self.arduino_port.insert(0,"COM6")
        self.arduino_port.grid(row=0, column=1, padx=5, pady=5)
            #Baudrate
        ttk.Label(self.com_frame, text="Baudrate Arduino:").grid(row=1, column=0, padx=5, pady=5)
        self.arduino_baudrate = tk.Entry(self.com_frame,textvariable="9600")
        self.arduino_baudrate.insert(0,"9600")
        self.arduino_baudrate.grid(row=1, column=1, padx=5, pady=5)
            #Bouton de démarage 
        self.open_com_arduino=tk.Button(self.com_frame,text="Com Arduino Eteint",bg='light pink', relief='raised', command=self.open_com_Arduino)
        self.open_com_arduino.grid(row=2, column=0, padx=5, pady=5,columnspan=2)

        
    def Create_Widget_Coupling (self, Nb_moteur):
        self.coupling_frame = ttk.LabelFrame(self, text="Couplage :")
        self.coupling_frame.grid(row=0, column=1, padx=10, pady=10)
        
        self.coche_moteur=[tk.BooleanVar() for _ in range(Nb_moteur)]
        self.case_moteur=[0]*Nb_moteur
        for i in range(Nb_moteur):
            self.case_moteur[i]=tk.Checkbutton(self.coupling_frame,text="M"+str(i+1),variable=self.coche_moteur[i],command=self.Moteurs_couples)
            self.case_moteur[i].grid(row=i, column=0, padx=5, pady=5)

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

    def Moteurs_couples (self):
        for i in range(self.Nombre_Moteurs) :
            Etat=self.coche_moteur[i].get() 
            print("Case cochée" if Etat else "Case décochée")

    def Envoi_Message (self,event=None):
        Coupler=[]*self.Nombre_Moteurs
        for i in range(self.Nombre_Moteurs):
            if self.coche_moteur[i].get() and self.Moteurs[i].command=="":
                Coupler[i]=self.Moteurs[i].identity
            else : 
                if self.Moteurs[i].command !="":
                    print(self.Moteurs[i].Command)
                    self.Pilote_Moteur.Discussion(Message=self.Moteurs[i].Command)
                    self.Moteurs[i].Command =""
        for i in range(Coupler):
                self.plop

        for i in range(self.Nombre_Moteurs):
            if self.Moteurs[i].Command != "" :
                
                print(self.Moteurs[i].Command)
                self.Pilote_Moteur.Discussion(Message=self.Moteurs[i].Command)
                self.Moteurs[i].Command =""
                




if __name__ == "__main__":
    app = IHM_DT(Nombre_Moteurs=2)
    app.mainloop()
