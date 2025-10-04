import serial
import time

start=time.time()

class Photodiode_Ampli:
    def __init__(self,Port,Baudrate):
        self.PortCom=Port
        self.Baudrate=Baudrate
        self.AmpliCom=None

    def ChangePortSerie(self,NewPortName):
            self.PortCom=NewPortName

    def ChangeBaudrate(self,NewBaudrate):
            self.Baudrate=NewBaudrate

    def OpenCom(self):
        try:
            self.AmpliCom=serial.Serial(port=self.PortCom,baudrate=self.Baudrate)
            time.sleep(2)
            print(f"Connexion ouverte sur {self.PortCom} à {self.Baudrate} bauds.")
            self.AmpliCom.write(b'*mod0\n')
        except serial.SerialException as e:
            print(f"Erreur lors de l'ouverture de la connexion série : {e}")
    
    def CloseCom(self):
         if self.AmpliCom and self.AmpliCom.is_open :
             self.AmpliCom.close()
             print(f"connection port {self.PortCom} fermée")

    def Acquisition_Photodiode(self,Nb_mesure):
        Values=[]
        self.AmpliCom.write(b'*clr\n')
        while (self.AmpliCom.readline()[1:5]!=b'clr0'):
            1
        for i in range(Nb_mesure):
            res=self.AmpliCom.readline()
            Valeur=res[1:5]
            Valeur=Valeur.decode("utf-8")
            Valeur=str(Valeur)
            Valeur=int(Valeur,16)*5/32767
            Values.append(Valeur)
        Moyenne=0
        for j in range(Nb_mesure):
            Moyenne=Moyenne+Values[j]
        Moyenne=Moyenne/Nb_mesure
        return Moyenne
    

if __name__=='__main__':
    C9329=Photodiode_Ampli(Port='COM13',Baudrate=19200)
    C9329.OpenCom()
    Resultat=C9329.Acquisition_Photodiode(Nb_mesure=10)
    print(Resultat)
    C9329.CloseCom()