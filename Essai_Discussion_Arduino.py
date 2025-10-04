import serial
import time
import tkinter as tk
from tkinter import ttk

class Arduino_Translation:
    def __init__(self,Port,Baudrate):
        self.PortSerie=Port
        self.Baudrate=Baudrate
        self.Serie_Arduino=None

    def ChangePortSerie(self,NewPortName):
            self.PortSerie=NewPortName

    def ChangeBaudrate(self,NewBaudrate):
            self.Baudrate=int(NewBaudrate)

    def OpenCom(self):
        try:
            self.Serie_Arduino=serial.Serial(port=self.PortSerie,baudrate=self.Baudrate,timeout=self.Baudrate)
            time.sleep(2)
            print(f"Connexion ouverte sur {self.PortSerie} à {self.Baudrate} bauds.")
        except serial.SerialException as e:
            print(f"Erreur lors de l'ouverture de la connexion série : {e}")
    
    def CloseCom(self):
         if self.Serie_Arduino and self.Serie_Arduino.is_open :
             self.Serie_Arduino.close()
             print(f"connection port {self.PortSerie} fermée")

    def MoveTo(self,Moteur,Nb_pas, Direction):
        if self.Serie_Arduino and self.Serie_Arduino.is_open :
            try : 
                #Envoi de la direction
                Envoi=Moteur+"DIREC_"+Direction+'\n'
                self.Serie_Arduino.write(Envoi.encode())        
                response=""
                TempsTimeout=time.time()
                while(time.time()-TempsTimeout < 5):
                    if self.Serie_Arduino.in_waiting > 0:
                        response = "Direction: "+ self.Serie_Arduino.readline().decode().strip()
                        print(response)
                        break
                else : 
                    print("Timeout atteinds, pas de réponse")
                #Envoi du nombre de pas 
                Envoi=Moteur+"DRIVE_"+Nb_pas+'\n'
                self.Serie_Arduino.write(Envoi.encode())        
                response=""
                TempsTimeout=time.time()
                while(time.time()-TempsTimeout < 5):
                    if self.Serie_Arduino.in_waiting > 0:
                        response = "Nombre de pas: "+self.Serie_Arduino.readline().decode().strip()
                        print(response)
                        break
                else : 
                    print("Timeout atteinds, pas de réponse")
            except serial.SerialException as e:
                self.Message=f"Erreur connection : {e}"  
    
    def Speed(self,Moteur, Vitesse):
        if self.Serie_Arduino and self.Serie_Arduino.is_open :
            try : 
                #Envoi de la direction
                Envoi=Moteur+"SPEED_"+Vitesse+'\n'
                self.Serie_Arduino.write(Envoi.encode())        
                response=""
                TempsTimeout=time.time()
                while(time.time()-TempsTimeout < 5):
                    if self.Serie_Arduino.in_waiting > 0:
                        response = "Direction: "+ self.Serie_Arduino.readline().decode().strip()
                        print(response)
                        break
                else : 
                    print("Timeout atteinds, pas de réponse")
            except serial.SerialException as e:
                self.Message=f"Erreur connection : {e}"  
    
    def RampUp(self,Moteur, Acceleration):
        if self.Serie_Arduino and self.Serie_Arduino.is_open :
            try : 
                #Envoi de la direction
                Envoi=Moteur+"ACCEL_"+Acceleration+'\n'
                self.Serie_Arduino.write(Envoi.encode())        
                response=""
                TempsTimeout=time.time()
                while(time.time()-TempsTimeout < 5):
                    if self.Serie_Arduino.in_waiting > 0:
                        response = "Acceleration: "+ self.Serie_Arduino.readline().decode().strip()
                        print(response)
                        break
                else : 
                    print("Timeout atteinds, pas de réponse")
            except serial.SerialException as e:
                self.Message=f"Erreur connection : {e}"  

    def Enable(self, Moteur, OnOFF):
        if self.Serie_Arduino and self.Serie_Arduino.is_open :
            try : 
                #Envoi de la direction
                Envoi=Moteur+"ENABL_"+OnOFF+'\n'
                self.Serie_Arduino.write(Envoi.encode())        
                response=""
                TempsTimeout=time.time()
                while(time.time()-TempsTimeout < 5):
                    if self.Serie_Arduino.in_waiting > 0:
                        response = "ENABLE: "+ self.Serie_Arduino.readline().decode().strip()
                        print(response)
                        break
                else : 
                    print("Timeout atteinds, pas de réponse")
            except serial.SerialException as e:
                self.Message=f"Erreur connection : {e}"  

    def Stop(self,Moteur):
        if self.Serie_Arduino and self.Serie_Arduino.is_open :
            try : 
                #Envoi de la direction
                Envoi=Moteur+"STOP"+'\n'
                self.Serie_Arduino.write(Envoi.encode())        
                response=""
                TempsTimeout=time.time()
                while(time.time()-TempsTimeout < 5):
                    if self.Serie_Arduino.in_waiting > 0:
                        response = "Stop: "+ self.Serie_Arduino.readline().decode().strip()
                        print(response)
                        break
                else : 
                    print("Timeout atteinds, pas de réponse")
            except serial.SerialException as e:
                self.Message=f"Erreur connection : {e}"

    def Home(self,Moteur):
        if self.Serie_Arduino and self.Serie_Arduino.is_open :
            try : 
                #Envoi de la direction
                Envoi=Moteur+"HOME"+'\n'
                self.Serie_Arduino.write(Envoi.encode())        
                response=""
                TempsTimeout=time.time()
                while(time.time()-TempsTimeout < 500):
                    if self.Serie_Arduino.in_waiting > 0:
                        response = "Home: "+ self.Serie_Arduino.readline().decode().strip()
                        print(response)
                        break
                else : 
                    print("Timeout atteinds home, pas de réponse")
            except serial.SerialException as e:
                self.Message=f"Erreur connection : {e}"


class IHM_Arduino_Translation:
    def __init__(self, root):
        self.Arduino=Arduino_Translation(Port='COM1',Baudrate='9600')
        self.Arduino.__init__
        
        self.root = root
        self.root.title("Module de pilotage translation arduino")

        # Cadre arduino 
        self.CadreArduino=tk.LabelFrame(self.root, text="Port série :",padx=10,pady=10)
        self.CadreArduino.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Port COM
        self.com_port_label = ttk.Label(self.CadreArduino, text="Port COM:")
        self.com_port_label.grid(column=0, row=0, padx=10, pady=10)

        self.com_port_var = tk.StringVar()
        self.com_port_dropdown = ttk.Combobox(self.CadreArduino, textvariable=self.com_port_var)
        self.com_port_dropdown['values'] = ['COM1', 'COM2', 'COM3', 'COM4','COM5','COM6','COM7']
        self.com_port_dropdown.grid(column=1, row=0, columnspan=2,padx=10, pady=10)
        self.com_port_dropdown.current(0)


        # Baudrate
        self.baudrate_label = ttk.Label(self.CadreArduino, text="Baudrate:")
        self.baudrate_label.grid(column=0, row=1, padx=10, pady=10)

        self.baudrate_var = tk.StringVar()
        self.baudrate_dropdown = ttk.Combobox(self.CadreArduino, textvariable=self.baudrate_var)
        self.baudrate_dropdown['values'] = ['9600', '19200', '38400', '57600', '115200']
        self.baudrate_dropdown.grid(column=1, row=1, columnspan=2,padx=10, pady=10)
        self.baudrate_dropdown.current(0)

        # Démarrage dicussion
        self.Démarrage_button = ttk.Button(self.CadreArduino, text="Demarrer Communication", command=self.demarrage)
        self.Démarrage_button.grid(column=0, row=3, columnspan=2, pady=10)
        
        # Fermeture dicussion
        self.Fermeture_button = ttk.Button(self.CadreArduino, text="Fermer Communication", command=self.fermeture)
        self.Fermeture_button.grid(column=3, row=3, columnspan=2, pady=10)
        
        # Cadre arduino 
        self.CadreM1=tk.LabelFrame(self.root, text="Moteur M1:",padx=10,pady=10)
        self.CadreM1.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        ligne=0

        # Réduction
        self.Reduction_label = ttk.Label(self.CadreM1, text="Réduction du driver :")
        self.Reduction_label.grid(column=0, row=ligne, padx=10, pady=10)

        self.Reduction_var = tk.StringVar()
        self.Reduction_dropdown = ttk.Combobox(self.CadreM1, textvariable=self.Reduction_var,width=10)
        self.Reduction_dropdown['values'] = ['1/1', '1/2', '1/4', '1/16', '1/32', '1/64']
        self.Reduction_dropdown.grid(column=1, row=ligne, padx=10, pady=10)
        self.Reduction_dropdown.current(0)

        ligne=ligne+1
        
        self.ReductionVis_label = ttk.Label(self.CadreM1, text="Pas de la vis (si nécessaire):")
        self.ReductionVis_label.grid(column=0, row=ligne, padx=10, pady=10)
        
        self.ReductionVis_entry = tk.Entry(self.CadreM1,width=40)
        self.ReductionVis_entry.grid(column=1, row=ligne, padx=10, pady=10)
        
        ligne =ligne+1
        #Enable
        self.EnableM1_button = ttk.Button(self.CadreM1, text="Alimenter Moteur M1", command=self.Enable_M1)
        self.EnableM1_button.grid(column=0, row=ligne, columnspan=3, pady=0)

        # Vitesse
        self.speed_label = ttk.Label(self.CadreM1, text="Vitesse:")
        self.speed_label.grid(column=0, row=3, padx=10, pady=10)

        self.speed_scale = ttk.Scale(self.CadreM1, from_=0, to=100, orient='horizontal')
        self.speed_scale.grid(column=1, row=4,columnspan=2, padx=10, pady=10)
        
        self.speed_entry = tk.Entry(self.CadreM1,width=10)
        self.speed_entry.grid(column=1, row=3, padx=10, pady=10)

        self.Vitesse_var = tk.StringVar()
        self.Vitesse_dropdown = ttk.Combobox(self.CadreM1, textvariable=self.Vitesse_var,width=10)
        self.Vitesse_dropdown['values'] = ['RPM', 'mm/s', 'µs/pas']
        self.Vitesse_dropdown.grid(column=2, row=3, padx=10, pady=10)
        self.Vitesse_dropdown.current(0)

        #Acceleration
        self.Accel_label = ttk.Label(self.CadreM1, text="Acceleration :")
        self.Accel_label.grid(column=0, row=5, padx=10, pady=10)

        self.Accel_entry = tk.Entry(self.CadreM1,width=10)
        self.Accel_entry.grid(column=1, row=5, padx=10, pady=10)

        self.Accel_var = tk.StringVar()
        self.Accel_dropdown = ttk.Combobox(self.CadreM1, textvariable=self.Accel_var,width=10)
        self.Accel_dropdown['values'] = ['pas','%','mm/s²']
        self.Accel_dropdown.grid(column=2, row=5, padx=10, pady=10)
        self.Accel_dropdown.current(0)
        
        # direction
        self.Direction_label=ttk.Label(self.CadreM1,text="Direction:")
        self.Direction_label.grid(column=0,row=6,padx=10,pady=10)

        self.Direction_Var = tk.StringVar()
        self.Direction_Radio_A = ttk.Radiobutton(self.CadreM1,text="Avance",variable=self.Direction_Var,value="Avance")
        self.Direction_Radio_A.grid(column=10,row=6,padx=10,pady=10)
        self.Direction_Radio_B = ttk.Radiobutton(self.CadreM1,text="Recule",variable=self.Direction_Var,value="Recule")
        self.Direction_Radio_B.grid(column=2,row=6,padx=10,pady=10)
        
        #pas
        self.Pas_label = ttk.Label(self.CadreM1, text="Avance / recule :")
        self.Pas_label.grid(column=0, row=7, padx=10, pady=10)

        self.Pas_entry = tk.Entry(self.CadreM1,width=10)
        self.Pas_entry.grid(column=1, row=7, padx=10, pady=10)

        self.Pas_var = tk.StringVar()
        self.Pas_dropdown = ttk.Combobox(self.CadreM1, textvariable=self.Pas_var,width=10)
        self.Pas_dropdown['values'] = ['µpas [Relatif]', 'pas [Relatif]', 'mm [Relatif]']
        self.Pas_dropdown.grid(column=3, row=7, padx=10, pady=10)
        self.Pas_dropdown.current(0)
        
        # Démarrage avance
        self.Démarrage_button = ttk.Button(self.CadreM1, text="Deplacement discret", command=lambda:self.deplace(MoteurName="M1"))
        self.Démarrage_button.grid(column=0, row=8, columnspan=2, pady=10)
        
        # démarrage avance continue
        self.Fermeture_button = ttk.Button(self.CadreM1, text="Deplacement continu", command=lambda:self.deplace_continu(MoteurName="M1"))
        self.Fermeture_button.grid(column=3, row=8, columnspan=2, pady=10)

    def demarrage(self):
        self.Arduino.ChangePortSerie(NewPortName=self.com_port_dropdown.get())
        self.Arduino.ChangeBaudrate(NewBaudrate=self.baudrate_dropdown.get())
        self.Arduino.OpenCom()
        print (self.Arduino.Baudrate)

    def fermeture(self):
        
        self.Arduino.CloseCom()
        print("Fin '\n'")

    def Enable_M1(self):
        self.Arduino.Enable(Moteur="M1",OnOFF=0)

    def deplace(self, MoteurName):
        print ("bla")

    def deplace_continu(self,MoteurName):
        print ("pli")


if __name__ == "__main__":
    root = tk.Tk()
    app = IHM_Arduino_Translation(root)
    root.mainloop()

    
       


