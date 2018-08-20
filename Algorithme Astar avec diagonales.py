# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 20:10:04 2018

@author: Bastien
"""

## Dï¿½finitions initiales

"""
On va dï¿½finir les coordonnï¿½es des points tels que :
- ce soit des tuples
- leur valeur dans map nous indique si c'est un mur ou non
    . -> rien
    # -> mur
    E -> dï¿½part
    A#i -> article nï¿½i
    S -> arrivï¿½e
    o -> dï¿½jï¿½ passï¿½
"""
import numpy as np

np.infty

h =50 #hauteur de la grille
l =50 #largeur de la grille

#initialisation de la grille vide :
map = {}
#on utilise un dictionnaire pour affecter des valeurs aux emplacements


### Calcul de distance : dï¿½finition de notre heuristique

def dist(coordA,coordB):
    return ((coordA[0] - coordB[0])**2 + (coordA[1] - coordB[1])**2)**(1/2)

#C'est ï¿½a que l'on comptabilisera comme heuristique dans notre cas (distance la plus courte possible)

### Dï¿½finition de la carte
class Point:
    "x, y, cout, heuristique, mur (Booleen), txt"
    #(Cout infini pour que seul les points dï¿½finis puissent ï¿½tre pris en compte lors de la rï¿½solution)
    def __init__(self, x=0, y=0, c=np.Infinity, h=0, w=False, txt = " "):
        self.x = x
        self.y = y
        self.c = c
        self.h = h
        self.mur = w
        self.txt = txt

def affiche(map):
    txt = ''
    for i in range(l+1):
        txt+='__'
    txt+='\n'
    for j in range(h):
        txt+= '|'
        for i in range(l):
            txt += map[(i, j)].txt +'|'
        txt += '\n'
    
    for i in range(l+1):
        txt+='__'
    print(txt)

sortie=Point(4,49)


#On commence avec une grille sans mur ni lieu visitï¿½
for i in range(l):
    for j in range(h):
        map[(i, j)] = Point(i, j, np.Infinity, dist([i,j],[sortie.x,sortie.y]))

entree=Point(0, 0, 0, 0)

#les murs :
murs = {(1,1),(1,2),(3,4),(3,5),(0,5),(1,5),(2,5),(4,5),(5,5),(7,5),(7,6)}

for i in murs:
    map[i].w=True
    map[i].txt="M"




affiche(map)
"""
###
entree,map[entree]=(0, 0), 0
#sortie,map[sortie]=(3, 4), 'S'
sortie,map[sortie]=(5, 9), 'S'
#erreur=map[(10, 5)]
affiche(map)
"""


def is_outofrange(coord):
    if (coord[0] > l) or (coord[1] > h):
        return True
    else:
        return False

def is_Wall(coord):
    if map[coord] == 'M':
        return True
    else:
        return False






## Algorithme A*



### Code

def compare(coord1, coord2): #Compare les heuristiques de 2 points
    if map[coord1].h < map[coord2].h:
        return 1
    elif map[coord1].h == map[coord2].h:
        return 0
    else:
        return -1

def ajouttri (list, x): #Ajoute x à la liste de manière à ce qu'elle soit triée
#par heuristique croissante
    for i in range(len(list)):
        if x.h <= list[i].h:
            list.insert(i, x)
            return list

def voisin(elem):
    res=[]
    x=elem.x
    y=elem.y
    for i in [1,0,-1]:
        for j in [1,0,-1]:
            try:
                X = map[(x+i,y+j)]
            except:
                ()
            else:
                if X.txt != 'M' and i+j !=0:
                    res+= [(x+i, y+j)]
    return res

"""
def voisin(elem):
    res=[]
    x=elem.x
    y=elem.y
    try:
        N= map[(x,y+1)]
    except:
        ()
    else:
        if N.txt != 'M':
            res+= [(x,y+1)]
    finally:
        try:
            S= map[(x,y-1)]
        except:
            ()
        else:
            if S.txt != 'M':
                res+= [(x,y-1)]
        finally:
            try:
                E= map[(x+1,y)]
            except:
                ()
            else:
                if E.txt != 'M':
                    res+= [(x+1,y)]
            finally:
                try:
                    O= map[(x-1,y)]
                except:
                    ()
                else:
                    if O.txt != 'M':
                        res+= [(x-1,y)]
                finally:
                    return res

"""
#class Point:
#    "x, y, cout, heuristique, mur (Booleen), txt"

def remonte(map, elem, entree):
    "on remonte le chemin une fois les distances calculees de l'entree jusqu'a la sortie"
    distmini = elem.c
    voisins = voisin(elem)
    map[(elem.x , elem.y)].txt = 'S'
    res = [elem]
    map[(entree.x, entree.y)]= entree
    
    while len(voisins) >0 :
        for vois in voisins:
            marche = map[vois]
            #print( "voisins sont : ", voisins)
            #print("Marche.c" , marche.c, "(", marche.x, "," , marche.y,")")
            if marche.c == 0:
                voisins = []
                map[(marche.x , marche.y)].txt = 'E'
                #affiche(map)
                return ("le chemin est : ", res, " de longueur : ", len(res))
            if marche.c < distmini and marche.txt != 'M' :
                distmini = marche.c
                #print("liste", liste, "passe", passe)
                map[(marche.x , marche.y)].txt = '%'
                voisins = voisin(marche)
                res += [marche]
    

import time
def chemin(map, entree, sortie):
    global t0
    t0 = time.time()
    passe=[] #deja essayes
    liste=[entree] #pas encore essayes
    
    while len(liste)>0:
        elem = liste.pop(0)
        
        if elem.x == sortie.x and elem.y == sortie.y:
            #remonter le chemin
            res=remonte(map, elem, entree)
            affiche(map)
            t1 = time.time()
            print(t1-t0)
            return(res)
            
            """for i in range(len(passe)-1, 0, -1):
                marche = passe[i]
                print('cout',marche.c)
                if marche.c < distmini:
                    distmini = marche.c
                    #print("liste", liste, "passe", passe)
                    map[(marche.x , marche.y)].txt = 'ï¿½'
            affiche(map)
            return "fini"
        """
        
        else:
            voisins = voisin(elem)
            #print(voisins)
            """On verifie si le point existe deja dans le dictionnaire"""
            passe.append(elem)
            for i in range(len(voisins)):
                v= voisins.pop(0)
                #print(v)
                try: 
                    passe.index((map[v]))
                except:
                    try:
                        j=liste.index((map[v]))
                    except:
                                                
                        vois=map[v]
                        #print(liste,voisins,passe)
                        vois.c = elem.c + dist([vois.x,vois.y],[sortie.x, sortie.y])
                        vois.h = vois.c + dist([vois.x,vois.y],[sortie.x, sortie.y])
                        vois.txt = '.'
                        liste.append(vois)
                        #print(liste)
                    else:
                        if liste[j].h > map[v].h :
                            vois=map[v]
                            #print(liste,voisins,passe)
                            vois.c = elem.c + dist([vois.x,vois.y],[sortie.x, sortie.y])
                            vois.h = vois.c + dist([vois.x,vois.y],[sortie.x, sortie.y])
                            liste.append(vois)
                            vois.txt = '.'
                            #print(liste)<
    print("erreur")


print((chemin(map, entree, sortie))[2:4])















