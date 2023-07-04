# -*- coding: utf-8 -*-
"""
@authors: adnane sennoune
"""

from tkinter import *
from random import randint
from formes import *
import sqlite3
from tkinter.colorchooser import askcolor
       
        
        
class ZoneAffichage(Canvas):
    def __init__(self,parent,w,h,c):
        Canvas.__init__(self,master=parent,width=w, height=h, bg=c)
        self.listeshape=[]
        #Les composants du Pendu, dans l'ordre du dessin
        # Base, Poteau, Traverse, Corde
        self.listeshape.append(Rectangle(self, 50,  270, 200,  26, "black"))
        self.listeshape.append(Rectangle(self, 87,   83,  26, 200, "black"))
        self.listeshape.append(Rectangle(self, 87,   70, 150,  26, "black"))
        self.listeshape.append(Rectangle(self, 183,  70,  10,  70, "black"))
        # Tete, Tronc
        self.listeshape.append(Ellipse(self, 188, 122,  20,  20, "white"))
        self.listeshape.append(Rectangle(self, 175, 143,  26,  60, "white"))
        # Bras gauche et droit
        self.listeshape.append(Rectangle(self, 164, 150,  10,  40, "white"))
        self.listeshape.append(Rectangle(self, 203, 150,  10,  40, "white"))
        # Jambes gauche et droite
        self.listeshape.append(Rectangle(self, 175, 205,  10,  40, "white"))
        self.listeshape.append(Rectangle(self, 191, 205,  10,  40, "white"))
        
class MonBoutonLettre(Button):
    def __init__(self,parent,lettre,traittement):
        Button.__init__(self,parent,text=lettre,state="disabled",command=self.cliquer,borderwidth=1)
        self.__traittement=traittement
        self.__lettre =lettre
    def cliquer(self):
        self.config(state=DISABLED)
        self.__traittement(self.__lettre)


class FenPrincipale(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title('Jeu du Pendu')
        self.geometry('700x520+400+400')
        self.bg="#2687bc"
        self.fond_fenetre="#2687bc"
        self.configure(bg=self.fond_fenetre)
        
        #Tableau Classement        
        self.Cadre4 = Frame(self, borderwidth=1, relief=GROOVE)
        self.Cadre4.pack(side=RIGHT, padx=0, pady=0)
        self.label1=Label(self.Cadre4, text="classement")
        self.label1.grid(row=0, column=0)
        self.label2=Label(self.Cadre4, text="pseudo")
        self.label2.grid(row=0, column=1)
        self.label3=Label(self.Cadre4, text="score")
        self.label3.grid(row=0, column=2)
        self.label4=Label(self.Cadre4, text="nombre parties")
        self.label4.grid(row=0, column=3)

        #Importation des données du tableau classement    
        conn = sqlite3.connect('Pendu.db')
        curseur = conn.cursor()
        curseur.execute("SELECT pseudo, SUM(score) ,COUNT(Partie.idjoueur) FROM Joueur,Partie WHERE \
                        Joueur.idjoueur = Partie.idjoueur GROUP BY pseudo ORDER BY SUM(score) DESC LIMIT 3;") 
                        
        C = curseur.fetchall()
        for i in range (len(C)):
            self.label=Label(self.Cadre4, text="{}".format(i+1))
            self.label.grid(row=i+1, column=0)
            self.label=Label(self.Cadre4, text="{}".format(C[i][0]))
            self.label.grid(row=i+1, column=1)
            self.label=Label(self.Cadre4, text="{}".format(C[i][1]))
            self.label.grid(row=i+1, column=2)
            self.label=Label(self.Cadre4, text="{}".format(C[i][2]))
            self.label.grid(row=i+1, column=3)
            
        #
        Cadre1 = Frame(self, borderwidth=1, relief=GROOVE)
        Cadre1.pack(side=TOP, padx=0, pady=5)
        

        self.Cadre2 = Frame(self, borderwidth=1, relief=GROOVE)
        self.Cadre2.pack(side=TOP, padx=0, pady=0)
        
        #Zone pour saisir le pseudo
        self.pseudoLabel = Label(self.Cadre2, text="Pseudo").grid(row=0, column=0)
        self.pseudo = StringVar()
        self.pseudoEntry = Entry(self.Cadre2, textvariable=self.pseudo).grid(row=0, column=1)
        self.EntrerButton = Button(self.Cadre2, text="Entrer",command=self.Entrer ).grid(row=0, column=5)
        
        self.labelm=Label(self, text="Mot : ")
        self.labelm.pack(padx=0, pady=0)       
      
        Cadre3 = Frame(self, borderwidth=2, relief=GROOVE)
        Cadre3.pack(side=BOTTOM, padx=0, pady=0)
        
        #Les boutons de la barre d'outil           #command indique les commandes associées aux boutons
        boutonNP = Button(Cadre1 , text='Nouvelle partie',command=self.NouvellePartie)
        boutonNP.pack(side=LEFT, padx=0, pady=0)
        
        boutonQuitter = Button(Cadre1, text='Quitter',command=self.destroy)
        boutonQuitter.pack(side=RIGHT, padx=0, pady=0)
        
        boutonUndo = Button(Cadre1, text='Undo',command=self.Undo)
        boutonUndo.pack(side=RIGHT, padx=0, pady=0)
        
        #Barre menu
        menubar = Menu()
        menuu = Menu(menubar, tearoff=0)
        menuu.add_command(label="Fond pendu", command=self.couleurArrierePendu)
        menuu.add_command(label="Fenêtre", command=self.couleurFondFenetre)
        menubar.add_cascade(label="Couleur", menu=menuu)
        
        FenPrincipale.config(self,menu=menubar)
        # Le canvas pour le dessin du pendu
        self.__canevas_pendu=ZoneAffichage(self,300,300,self.bg)
        self.__canevas_pendu.pack(side=TOP)

        
        #les boutons du clavier
        self.__lettre=[]
        for i in range(26):
            self.__lettre.append(MonBoutonLettre(Cadre3,chr(ord('A')+i),self.traittement))
            
        for i in range(7):
            self.__lettre[i].grid(row=0, column=i)
        for i in range(7):
            self.__lettre[7+i].grid(row=1, column=i)
        for i in range(7):
            self.__lettre[14+i].grid(row=2, column=i)
        for i in range(5):
            self.__lettre[21+i].grid(row=3, column=i+1)
       


    def NouvellePartie(self):
        self.__nbManques=0
        self.trouve=''
        self.chargeMots()
        self.__mot=self.__mots[randint(0,len(self.__mots))]
        self.__MotCaché='*'*len(self.__mot)
        self.labelm.config(text="Mot : {}".format(self.__MotCaché))
        for lettre in self.__lettre : lettre.config(state = NORMAL)
        for i in self.__canevas_pendu.listeshape :   #on cache le pendu quand on lance une nouvelle partie
            i.setState("hidden")
        
   
    def chargeMots(self):
        f =open('mots.txt', 'r')
        s =f.read()
        self.__mots = s.split('\n')
        f.close()
 
    def traittement(self,lettre):
        self.__MotCaché2=''
        for let in self.__mot :
            if let==lettre or let in self.trouve:
                self.__MotCaché2+=let
                self.trouve+=lettre
            else : 
                self.__MotCaché2+='*'
        self.labelm.config(text="Mot : {}".format(self.__MotCaché2))
        
##En cas de victoire
        if self.__MotCaché2==self.__mot:
            for lettre in self.__lettre : lettre.config(state = DISABLED)
            self.labelm.config(text="Bravo ! vous avez gagné le Mot est : {}".format(self.__mot))
            conn = sqlite3.connect('Pendu.db')
            curseur = conn.cursor()
            cmd= "INSERT INTO Partie (idjoueur ,mot ,score) VALUES ('{}', '{}', '{}') ;".format(self.id,self.__mot,1.0)
            curseur.execute(cmd)
            conn.commit()    
            conn.close()

        elif lettre not in self.__mot:
            self.__nbManques+=1
            self.__canevas_pendu.listeshape[self.__nbManques-1].setState("normal")

#En cas de défaite
            if self.__nbManques == 10:
                for lettre in self.__lettre : lettre.config(state = DISABLED)
                self.labelm.config(text="vous avez perdu, le Mot est : {}".format(self.__mot))
                score=0
                for i in range (len(self.__MotCaché2)) :
                    if self.__MotCaché2[i] == self.__mot[i]:
                        score+=1/len(self.__MotCaché2)
                conn = sqlite3.connect('Pendu.db')
                curseur = conn.cursor()
                cmd= "INSERT INTO Partie (idjoueur ,mot ,score) VALUES ('{}', '{}', '{}') ;".format(self.id,self.__mot,score)
                curseur.execute(cmd)
                conn.commit()    
                conn.close()
              

    #Fonctions pour la configuration des couleurs
    def couleurArrierePendu(self):
        color = askcolor(title='Sélectionnez une couleur')[1]
        self.__canevas_pendu.configure(bg=color)
    
    def couleurFondFenetre(self):
        color = askcolor(title='Sélectionnez une couleur')[1]
        self.fond_fenetre=color
        self.configure(bg=self.fond_fenetre)
        
   
#Méthode triche
    def Undo(self):
        if self.__nbManques != 0 and self.__nbManques!= 10 : #Si le joueur a déjà fait un erreur 
                                                             #et n'a pas encore perdu
            self.__canevas_pendu.listeshape[self.__nbManques-1].setState("hidden") #on cache le dernier élément du Pendu
            self.__nbManques-=1             #on donne au joueur une tentative de plus
  
#Identification des joueurs
    def Entrer(self) :
        self.Cadre2.pack_forget()
        conn = sqlite3.connect('Pendu.db')
        curseur = conn.cursor()
        curseur.execute("SELECT * FROM Joueur WHERE pseudo='{}';".format(self.pseudo.get()))
        C = curseur.fetchall()
        if len(C)>=1 :
            self.id=C[0][0]
            
        if len(C)==0:              #Si le joueur n'a jamais joué avant, on lui ajoute dans la table Joueur
            curseur2 = conn.cursor()
            cmd= "INSERT INTO joueur (pseudo) VALUES ('{}');".format(self.pseudo.get())
            curseur2.execute(cmd)
            curseur.execute("SELECT * FROM Joueur WHERE pseudo='{}';".format(self.pseudo.get()))
            C = curseur.fetchall()
            self.id=C[0][0]
                    
        conn.commit()    
        conn.close()

"Programme principal"
if __name__ == '__main__':
	fen = FenPrincipale()
	fen.mainloop()