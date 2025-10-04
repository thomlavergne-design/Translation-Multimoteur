import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial
import time
from Essai_Discussion_Arduino import *
from Photodiode_C9329 import *


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
         # Création des classes arduino et Ampli photodiode
        self.Pilote_Moteur=Arduino_Translation(Port="COM6",Baudrate="9600")
        self.Pilote_Photodiode=Photodiode_Ampli(Port="COM11",Baudrate="19200")
        # Paramètres gestion bouton
        self.com_arduino=False
        self.com_photo=False
        self.Enregiste=False
        self.Enable=False
        self.Direction="0"

        self.Create_Widget()

    def Create_Widget(self):
        #self.Title("Monochromateur Resort !")
        self.geometry("800x600")

        # Frame pour les paramètres de communication
        self.com_frame = ttk.LabelFrame(self, text="Global parameters")
        self.com_frame.pack(padx=10, pady=10, fill="x")

        # Paramètres pour l'Arduino
        ttk.Label(self.com_frame, text="Port COM Arduino:").grid(row=0, column=0, padx=5, pady=5)
        self.arduino_port = tk.Entry(self.com_frame)
        self.arduino_port.insert(0,"COM6")
        self.arduino_port.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.com_frame, text="Baudrate Arduino:").grid(row=0, column=2, padx=5, pady=5)
        self.arduino_baudrate = tk.Entry(self.com_frame,textvariable="9600")
        self.arduino_baudrate.insert(0,"9600")
        self.arduino_baudrate.grid(row=0, column=3, padx=5, pady=5)

        self.open_com_arduino=tk.Button(self.com_frame,text="Com Arduino Eteint",bg='light pink', relief='raised', command=self.open_com_Arduino)
        self.open_com_arduino.grid(row=0, column=4, padx=5, pady=5)

        # Paramètres pour la Photodiode
        ttk.Label(self.com_frame, text="Port COM Photodiode:").grid(row=1, column=0, padx=5, pady=5)
        self.photodiode_port = tk.Entry(self.com_frame)
        self.photodiode_port.insert(0,"COM13")
        self.photodiode_port.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.com_frame, text="Baudrate Photodiode:").grid(row=1, column=2, padx=5, pady=5)
        self.photodiode_baudrate = tk.Entry(self.com_frame)
        self.photodiode_baudrate.insert(0,"19200")
        self.photodiode_baudrate.grid(row=1, column=3, padx=5, pady=5)

        self.open_com_photodiode=tk.Button(self.com_frame,text="Com Photodiode Eteint",bg='light pink', relief='raised', command=self.open_com_Photodiode)
        self.open_com_photodiode.grid(row=1, column=4, padx=5, pady=5,columnspan=3);

        # Paramètres fichier d'enregistement
        ttk.Label(self.com_frame, text="Nom du fichier d'enregistrement:").grid(row=2, column=0, padx=5, pady=5)
        self.filename_Register=ttk.Entry(self.com_frame)
        self.filename_Register.grid(row=2, column=1, padx=5, pady=5)

        # Frame pour le contrôle du moteur
        self.control_frame = ttk.LabelFrame(self, text="Contrôle du Moteur")
        self.control_frame.pack(padx=10, pady=10, fill="x")

        # Bouton pour allumer le moteur
        self.on_button = tk.Button(self.control_frame, text="Moteur Non alimneté",bg='light pink', relief='raised', command=self.allumer_moteur)
        self.on_button.grid(row=0, column=0, padx=5, pady=5)

        # Bouton Home
        self.home_button = ttk.Button(self.control_frame, text="Home", command=self.home)
        self.home_button.grid(row=0, column=1, padx=5, pady=5)

        # Scale pour régler la vitesse
        ttk.Label(self.control_frame, text="Vitesse:").grid(row=0, column=2, padx=5, pady=5)
        self.vitesse_scale = ttk.Scale(self.control_frame, from_=0, to=1000, orient="horizontal")
        self.vitesse_scale.grid(row=0, column=3, padx=5, pady=5)

        # Boutons pour régler le sens de rotation
        self.sens_horaire_button = tk.Button(self.control_frame, text="Sens Horaire", bg='light yellow', relief='raised', command=self.sens_Rotation)
        self.sens_horaire_button.grid(row=1, column=0, padx=5, pady=5)

        # Texte et bouton pour avancer le moteur d'un certain nombre de pas
        ttk.Label(self.control_frame, text="Nombre de pas:").grid(row=1, column=2, padx=5, pady=5)
        self.nb_pas = ttk.Entry(self.control_frame)
        self.nb_pas.grid(row=1, column=3, padx=5, pady=5)

        self.avancer_button = ttk.Button(self.control_frame, text="Avancer", command=self.avancer)
        self.avancer_button.grid(row=1, column=4, padx=5, pady=5)

        # Texte et bouton pour déclencher le scan
        ttk.Label(self.control_frame, text="Nombre de points du scan:").grid(row=2, column=0, padx=5, pady=5)
        self.nb_points_scan = ttk.Entry(self.control_frame)
        self.nb_points_scan.grid(row=2, column=1, padx=5, pady=5)

        self.scan_button = ttk.Button(self.control_frame, text="Déclencher le Scan", command=self.declencher_scan)
        self.scan_button.grid(row=2, column=2, padx=5, pady=5)

        # Frame pour le graphique
        self.graph_frame = ttk.LabelFrame(self, text="Graphique")
        self.graph_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)


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

    def open_com_Photodiode(self):
        # Code pour démarrer ou éteindre la communication photodiode 
        # Modifie également l'aspect et l'effet du bouton
        if self.com_photo==False :
            self.open_com_photodiode.config(text="Com Photodiode en cours",bg='light green',relief='sunken')
            self.com_photo=True
            self.Pilote_Photodiode.ChangePortSerie(NewPortName=self.photodiode_port.get())
            self.Pilote_Photodiode.ChangeBaudrate(NewBaudrate=self.photodiode_baudrate.get())
            self.Pilote_Photodiode.OpenCom()
        else :
            self.open_com_photodiode.config(text="Com Photodiode Eteint",bg='light pink',relief='raised')
            self.com_photo=False
            self.Pilote_Photodiode.CloseCom()

    def allumer_moteur(self):
        if self.Enable==False :
            self.on_button.config(text="Moteur alimenté",bg='light green',relief='sunken')
            self.Enable=True
            self.Pilote_Moteur.Enable(Moteur="M1",OnOFF="0")# Code pour allumer le moteur
        else :
            self.on_button.config(text="Moteur Désengagé",bg='light pink',relief='raised')
            self.Enable=False
            self.Pilote_Moteur.Enable(Moteur="M1",OnOFF="1")# Code pour couper le moteur

    def home(self):
        if self.Enable==True :
            self.Pilote_Moteur.Home(Moteur="M1")

    def sens_Rotation(self):
        if self.Direction=="0" :
            self.sens_horaire_button.config(text="Sens Anti-horaire",bg='light blue',relief='sunken')
            self.Direction="1"
        else :
            self.sens_horaire_button.config(text="Sens horaire",bg='light yellow',relief='raised')
            self.Direction="0"



    def avancer(self):
        if self.Enable==True :
            self.Pilote_Moteur.Speed(Moteur="M1",Vitesse=str(self.vitesse_scale.get()))
            self.Pilote_Moteur.MoveTo(Moteur="M1",Nb_pas=self.nb_pas.get(),Direction=self.Direction)

    def declencher_scan(self):
        if self.Enable==True:
            self.ax.clear()
        
            if self.filename_Register.get()!="":
                self.Enregiste=True
                self.filename=self.filename_Register.get()
                fichier=open(self.filename+".txt",'a')

            nb_points_Scan = int(self.nb_points_scan.get())
            data = []

            for i in range(nb_points_Scan):
                Resultat=self.Pilote_Photodiode.Acquisition_Photodiode(Nb_mesure=10)
                data.append(Resultat)
                self.ax.plot(data)
                self.canvas.draw()
                if self.Enregiste==True:
                    fichier.write(str(i)+" "+str(Resultat) + '\n')
                self.Pilote_Moteur.MoveTo(Moteur="M1",Nb_pas="4",Direction=self.Direction)
                # Mise à jour le graphique
                
                
        
            self.Enregiste=False


       
if __name__ == "__main__":
    app = Application()
    app.mainloop()
