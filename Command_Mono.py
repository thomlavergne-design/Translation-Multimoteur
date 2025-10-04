from Essai_Discussion_Arduino import *
from Photodiode_C9329 import *
import time


fileName=input("Nom du fichier d'enregistrement :")


for j in range(1):

    UnoR3=Arduino_Translation(Port="COM6",Baudrate=9600)
    C9329=Photodiode_Ampli(Port='COM13',Baudrate=19200)
    
   
   
    fichier=open(fileName+"_"+str(j)+".txt",'a')

    UnoR3.OpenCom()
    C9329.OpenCom()

    UnoR3.Enable(Moteur="M1",OnOFF="0")
    UnoR3.Home(Moteur="M1")
    UnoR3.Speed(Moteur="M1",Vitesse="200")
    UnoR3.MoveTo(Moteur="M1",Nb_pas="200",Direction="0")
    time.sleep(10)
    i=0 
    while i<750:
        Resultat=C9329.Acquisition_Photodiode(Nb_mesure=10)
        fichier.write(str(i)+" "+str(Resultat) + '\n')
        UnoR3.MoveTo(Moteur="M1",Nb_pas="4",Direction="0")
        i=i+1

    UnoR3.Enable(Moteur="M1",OnOFF="1")

    C9329.CloseCom()
    UnoR3.CloseCom()