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

    def Discussion(self,Message):
        if self.Serie_Arduino and self.Serie_Arduino.is_open :
            try:
                self.Serie_Arduino.write(Message.encode())
                response=""
                TempsTimeout=time.time()
                while(time.time()-TempsTimeout < 5):
                    if self.Serie_Arduino.in_waiting > 0:
                        response = "Réponse: "+ self.Serie_Arduino.readline().decode().strip()
                        print(response)
                        break
                else : 
                    print("Timeout atteinds, pas de réponse")
            except serial.SerialException as e:
                self.Message=f"Erreur connection : {e}"

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




if __name__ == "__main__":
    DUO=Arduino_Translation(Port="COM6",Baudrate=9600)

    
       


