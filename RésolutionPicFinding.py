import pandas as pd

Name_Fichier_Excel='SN2203/2025-07-23_Répétabilité\Repetability mesure SN2203.xlsx'
Fichier_Excel=pd.read_excel(Name_Fichier_Excel,sheet_name="SN2203-Repetability-24-07")
Wavelength=Fichier_Excel["Pas Moteur [5]" ].iloc[2:].tolist()

Tension=Fichier_Excel["Signal [5]"].iloc[2:].tolist()




def Bruit_Dark(Liste):
    dark=Liste[0]
    K=1
    for i in range(1,len(Liste)):
        if abs(Liste[i])<1.05*abs(dark):
            dark=(K*dark+Liste[i])/(K+1)
            K=K+1
    return dark

def FindMax(ListeTension,ListeWl,marge):
    Maximas=[]
    for i in range(1,len(ListeTension)-1) :
        if ListeTension[i]-ListeTension[i-1]>0 and ListeTension[i+1]-ListeTension[i]<0 and ListeTension[i]>marge:
            Limit_50Pourcent=(ListeTension[i])/2            
            j=0
            while(ListeTension[i-j]>Limit_50Pourcent):
                j=j+1
            #ResBas=ListeWl[i-j]
            Resolutionbas=(ListeWl[i-j]-ListeWl[i-j+1])/(ListeTension[i-j]-ListeTension[i-j+1])*(ListeTension[i]*0.5-(ListeWl[i-j]*ListeTension[i-j+1]-ListeWl[i-j+1]*ListeTension[i-j])/(ListeWl[i-j]-ListeWl[i-j+1]))
            j=0
            while(ListeTension[i+j]>Limit_50Pourcent):
               j=j+1
            #ResHaut=ListeWl[i+j]
            #Resolutionshaut=ListeWl[i+j]    
            Resolutionhaut=(ListeWl[i+j-1]-ListeWl[i+j])/(ListeTension[i+j-1]-ListeTension[i+j])*(ListeTension[i]*0.5-(ListeWl[i+j-1]*ListeTension[i+j]-ListeWl[i+j]*ListeTension[i+j-1])/(ListeWl[i+j-1]-ListeWl[i+j]))
            Maximas.append([(Resolutionbas+Resolutionhaut)/2,ListeTension[i],(Resolutionhaut-Resolutionbas)])
            #Maximas.append([ListeWl[i],ListeTension[i]])
    return Maximas


Bruit=Bruit_Dark(Tension)

Tension2=[]
for i in range(0, len(Tension)):
    Tension2.append(Tension[i]-Bruit*1.3)
Bruit2=Bruit_Dark(Tension2)
Maxima=FindMax(Tension,Wavelength,abs(Bruit)*2)
print(Maxima)