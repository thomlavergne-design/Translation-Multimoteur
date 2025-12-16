import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog,ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os 


class IHM_Traitement_M158():
    def __init__(self,root):
        self.root=root
        self.figure, self.ax = plt.subplots()
        self.Moyennes=[]
        

        self.canvasFigure = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvasFigure.draw()
        self.canvasFigure.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.bouton_quitter = tk.Button(self.root, text="Quitter", command=root.destroy)
        self.bouton_quitter.pack()
        
        self.bouton_selectionner = tk.Button(self.root, text="Selectionner Fichier", command=self.Selection_Fichier)
        self.bouton_selectionner.pack()

        self.bouton_clear_graphe= tk.Button(self.root, text="clear graphe", command=self.Clear_Graphe)
        self.bouton_clear_graphe.pack()

        # Treeview pour afficher les maxima
        self.tree = ttk.Treeview(self.root, columns=("Position", "Intensité", "Largeur"), show="headings")
        self.tree.heading("Position", text="Position (nm)")
        self.tree.heading("Intensité", text="Intensité")
        self.tree.heading("Largeur", text="Largeur (nm)")
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # Barre de défilement pour le tableau
        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

    def Selection_Fichier(self):
        chemin=filedialog.askopenfilename(title="Sélectionner les fichiers brutes", filetypes=[("Fichiers texte", "*.txt")])
        colonnes = []

        colonnes=self.Lecture_Fichier(Chemin=chemin)
        resultat=0
        Moyenne=[]
        nom_legende = os.path.basename(chemin)
        for i in range(len(colonnes[0])):
            for j in range(len(colonnes)):
                if j%2==1 :
                    resultat=resultat+colonnes[j][i]
            Moyenne.append(resultat/10)
            resultat=0
        
        ligne, = self.ax.plot(colonnes[0], Moyenne,label=nom_legende)
        self.ax.legend()
        self.Moyennes.append(ligne)
        self.canvasFigure.draw()
        Resolution=self.FindMax(ListeTension=Moyenne,ListeWl=colonnes[0],marge=float(0.05))
        self.afficher_maxima(Resolution)
    
    def Clear_Graphe(self):
        for ligne in self.Moyennes:
            ligne.remove()
        self.Moyennes = []
        self.ax.clear()
        self.canvasFigure.draw()

    def Lecture_Fichier(self,Chemin):
        colonnes = []
        with open(Chemin, 'r', encoding='latin-1') as fichier:
            next(fichier)
            for ligne in fichier:
                mots = ligne.strip().split('\t')
                for i, mot in enumerate(mots):
                    if i >= len(colonnes):
                        colonnes.append([])
                    mot = mot.replace(',' , '.')
                    colonnes[i].append(float(mot))
        return colonnes

    def FindMax(self,ListeTension,ListeWl,marge):
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
    
    def afficher_maxima(self, maxima):
        # Effacer les anciennes données
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Ajouter les nouvelles données
        for maxi in maxima:
            self.tree.insert("", tk.END, values=(f"{maxi[0]:.3f}", f"{maxi[1]:.3f}", f"{maxi[2]:.3f}"))

    def Enregistrement_Valeur(self,chemin):
        fefdmo

if __name__ == "__main__":
    root = tk.Tk()
    app = IHM_Traitement_M158(root)
    root.mainloop()
