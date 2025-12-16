import tkinter as tk
from tkinter import ttk


class ArduinoMoteurFrame(tk.LabelFrame):
    def __init__(self, master=None, identity="M1",**Kwargs):
        super().__init__(master,**Kwargs)
        # Création des classes arduino et Ampli photodiode
     
        
        # Configuration de la communication série
        self.identity=identity
        self.configure(borderwidth=2, relief="groove",text=self.identity,font=('helvetica',10,'italic'), padx=10, pady=10)
        self.nb_µpas=0
        self.Command=""

        # Création des widgets
        self.pad=5
        self.create_widgets_paramètres(Pad=self.pad)
        self.create_widgets_speeds_accel(Pad=self.pad)
        self.create_widgets_avance(Pad=self.pad)
        self.create_widget_command(Pad=self.pad)

    def create_widgets_paramètres(self,Pad:int):
        self.parametres_frame=tk.Frame(self)
        self.parametres_frame.grid(row=0,column=0,padx=Pad,pady=Pad)
        
        # Avant premiere:
        self.Reglage_Micropas = tk.Label(self.parametres_frame, text="Driver µPas/tour :")
        self.Reglage_Micropas.grid(row=0, column=0, padx=Pad, pady=Pad)

        self.Reglage_µPas = tk.StringVar()
        self.Reglage_μPas.set("200")
        self.Reglage_μPas_menu = tk.OptionMenu(self.parametres_frame, self.Reglage_μPas, "200", "400","800","1600","3200","6400","12800","25600")
        self.Reglage_μPas_menu.config(width=15,height=2)
        self.Reglage_μPas_menu.grid(row=0, column=1, padx=Pad, pady=Pad)
        

        self.Reglage_AvanceVis = tk.Label(self.parametres_frame, text= "Avance de vis [mm/tour] :")
        self.Reglage_AvanceVis.grid(row=1,column=0,padx=Pad,pady=Pad)

        self.Reglage_Vis=tk.Entry(self.parametres_frame)
        self.Reglage_Vis.grid(row=1,column=1,padx=Pad,ipady=Pad)
    
    def create_widgets_speeds_accel(self,Pad:int):
        self.VitesseAccel_frame = tk.Frame(self)
        self.VitesseAccel_frame.grid(row=0,column=1,padx=Pad,pady=Pad)

        # Première ligne : Variateurs pour la vitesse 
        self.speed_label = tk.Label(self.VitesseAccel_frame, text="Vitesse:")
        self.speed_label.grid(row=0, column=0, padx=Pad, pady=Pad)

        self.speed_Value=tk.Entry(self.VitesseAccel_frame)
        self.speed_Value.grid(row=0,column=1,padx=Pad,ipady=Pad)

        self.speed_unit = tk.StringVar()
        self.speed_unit.set("Tour/min")
        self.speed_unit_menu = tk.OptionMenu(self.VitesseAccel_frame, self.speed_unit, "pas/s", "Tour/min","µ-pas/s")
        self.speed_unit_menu.grid(row=0, column=2, padx=Pad, pady=Pad)

        self.set_speed_button = tk.Button(self.VitesseAccel_frame, text="Set", width=5, height=2, bg='light green', command=self.send_speed_command)
        self.set_speed_button.grid(row=0, column=3, padx=Pad, pady=Pad)

        # Deuxième ligne : Variateurs pour l'accélération
        self.accel_label = tk.Label(self.VitesseAccel_frame, text="Accélération:")
        self.accel_label.grid(row=1, column=0, padx=Pad, pady=Pad)

        self.accel_Value = tk.Entry(self.VitesseAccel_frame)
        self.accel_Value.grid(row=1, column=1, padx=Pad, pady=Pad)

        self.accel_unit = tk.StringVar()
        self.accel_unit.set("pas/s²")
        self.accel_unit_menu = tk.OptionMenu(self.VitesseAccel_frame, self.accel_unit, "pas/s²", "Tour/min²")
        self.accel_unit_menu.grid(row=1, column=2, padx=Pad, pady=Pad)

        self.set_accel_button = tk.Button(self.VitesseAccel_frame, text="Set", width=5, height=2, bg='light green', command=self.send_accel_command)
        self.set_accel_button.grid(row=1, column=3, padx=Pad, pady=Pad)


    def create_widgets_avance(self,Pad:int):
        self.Avance_frame=tk.Frame(self)
        self.Avance_frame.grid(row=1,column=0,padx=Pad,pady=Pad)
        #Première ligne : Nombre de pas 
        self.step_label = tk.Label(self.Avance_frame, text="Quantité de mouvement:")
        self.step_label.grid(row=0, column=0, padx=Pad, pady=Pad)

        self.step_entry = tk.Entry(self.Avance_frame)
        self.step_entry.grid(row=0, column=1, padx=Pad, pady=Pad)

        self.step_unit = tk.StringVar()
        self.step_unit.set("µ-pas")
        self.step_unit_menu = tk.OptionMenu(self.Avance_frame, self.step_unit,  "µ-pas", "pas","tour","mm","Lambda")
        self.step_unit_menu.grid(row=0, column=2, padx=Pad, pady=Pad)
        
        #Deuxième ligne : Boutons avance recule et stop
        self.Avance_button = tk.Button(self.Avance_frame, text="AVANCE !", width=25, bg='light green', command=self.send_Avance_command)
        self.Avance_button.grid(row=1, column=0, padx=Pad, pady=Pad)

        self.Recule_button = tk.Button(self.Avance_frame, text="RECULE !", bg='light blue', width=25, command=self.send_Recule_command)
        self.Recule_button.grid(row=1, column=1, padx=Pad, pady=Pad)
        
        self.stop_button = tk.Button(self.Avance_frame, text="STOP !", bg='dark red', fg='white', width=25, command=self.send_Stop_command)
        self.stop_button.grid(row=1, column=2, padx=Pad, pady=Pad)

    def create_widget_command(self,Pad:int):
        self.Command_frame=tk.Frame(self)
        self.Command_frame.grid(row=1,column=1,padx=Pad,pady=Pad)

        # Première ligne : Boutons d'alimentation et Home
        self.power_button = tk.Button(self.Command_frame, text="Moteur Eteins", width=25, bg='light pink', relief='raised', command=self.send_power_command)
        self.power_button.grid(row=0, column=0, padx=Pad, pady=Pad)
        self.Allume=False

        self.home_button = tk.Button(self.Command_frame, text="Home Switch", width=25, command=self.Go_Home)
        self.home_button.grid(row=1, column=0,padx=Pad, pady=Pad)

        self.Def_Zero_button = tk.Button(self.Command_frame, text="Définir position Zero", width=25, command=self.Def_Zero)
        self.Def_Zero_button.grid(row=0, column=1, padx=Pad, pady=Pad)
        
        self.Go_Zero_button = tk.Button(self.Command_frame,text="Zéro",width=25,command=self.Go_Zero)
        self.Go_Zero_button.grid(row=1,column=1,padx=Pad,pady=Pad)
       
    def Def_Zero(self):
        self.nb_μpas=0
        print("Position zero définie")
    
    def Go_Zero(self):
        self.Command=self.identity+"DRIVE_"+str(self.nb_μpas*(-1))+"\n"        
        self.nb_µpas=0 

    def Go_Home(self):
        self.Command=self.identity+"HOME\n"
        self.nb_µpas=0
    
    def calcul_du_nombre_de_µpas(self):
        match self.step_unit.get() :
            case "µ-pas":
                return int(self.step_entry.get())
            case "pas":
                return int(self.step_entry.get())*float(self.Reglage_μPas.get())/200
            case "tour":
                return int(self.step_entry.get())*float(self.Reglage_μPas.get())
            case "mm":
                return int(self.step_entry.get())*float(self.Reglage_μPas.get())*float(self.Reglage_Vis.get())

    def send_speed_command(self):
        Ajoute=int(self.speed_Value)
        self.Command = self.identity+"SPEED_"+str(Ajoute)+"\n"
        print(self.Command)
        self.event_generate('<Control-B>')

    def send_accel_command(self):
        Ajoute=int(self.accel_Value)
        self.Command = self.identity+"ACCEL_"+str(Ajoute)+"\n"
        print(self.Command)
        self.event_generate('<Control-B>')

    def send_Avance_command(self):
        Ajoute=self.calcul_du_nombre_de_µpas()
        self.nb_μpas=self.nb_μpas+int(Ajoute)
        self.Command = self.identity+"DRIVE_"+str(Ajoute)+"\n"
        self.event_generate('<Control-B>')

    def send_Recule_command(self):
        Ajoute=self.calcul_du_nombre_de_µpas()
        self.nb_μpas=self.nb_μpas+int(Ajoute)
        self.Command = self.identity+"DRIVE_"+str(Ajoute*(-1))+"\n"
        self.event_generate('<Control-B>')

    def send_Stop_command(self):
        self.Command=self.identity+"STOP\n"
        print(self.Command)
        self.event_generate('<Control-B>')


    def send_power_command(self):
        if self.Allume==False :
            self.power_button.config(text="Moteur Allumé",bg='light green',relief='sunken')
            self.Allume=True
            self.Command = self.identity+"ENABL_0\n"
        else :
            self.power_button.config(text="Moteur Eteins",bg='light pink',relief='raised')
            self.Allume=False
            self.Command = self.identity+"ENABL_1\n"
        self.event_generate('<Control-B>')
        print(self.Command)

    def send_home_command(self):
        self.Command = self.identity+"HOME\n"
        self.event_generate('<Control-B>')

   


if __name__ == "__main__":
    root=tk.Tk()
    # Remplacez 'COM3' par le port série de votre Arduino
    app=[0]*3
    for i in range(3):
        app[i] = ArduinoMoteurFrame(master=root,identity="M"+str(i))
        app[i].pack(padx=2,pady=10)
#    tk.Button(root,text="KILL",command=Buton_Kill(app)).pack()
    
    root.mainloop()
