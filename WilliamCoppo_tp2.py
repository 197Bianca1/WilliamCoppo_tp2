import sys
import os
import json

from maya import cmds 
from PySide6 import QtWidgets

#fonction qui charge les regle de couleur de json
def charger_config():
 
 # contruction du chemain du fichier rule jsaon qui doit trouver
 chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "rules.json")
 
 
 try: 
  # ouverture du fichier en lecture
  with open(chemin, "r", encoding="utf-8") as f:
    # lit le contenue du json
    return json.load(f)

# affiche un avertisement si le fichier est introuvable
 except FileNotFoundError:
     cmds.warning("rules.json introuvable")
     return {}


# classe principale qui continen l'inteface et fonction affichage
class OutlinerOrganizer(QtWidgets.QDialog):
  def __init__(self):

    #initiliser la feneêtre piside6
     super().__init__()

     # définir le titre de la fenetre
     self.setWindowTitle("outliner Organizer")

     # définir la argeur et la hauteur de la fenetre
     self.resize(300,200)

     # changer les règle du fichier json
     self.config = charger_config()

     # créer les cases à cocher et le bouton
     self.creer_interface()

  # fonction qui construit l'interface graphique
  def creer_interface(self):

   # creer une disposition verticale pour remplacer les éléments
   layout = QtWidgets.QVBoxLayout(self)
   
   # case qui permet d activer ou d esactivé les couleur
   self.couleur = QtWidgets.QCheckBox("Appliquer les couleur")
   layout.addWidget(self.couleur)

   # case qui permet d activer ou d esactiver le trie
   self.tri = QtWidgets.QCheckBox("trier par ordre alphabétique")
   layout.addWidget(self.tri)

   #case qui permet d activer ou d esactiver la selection
   self.tous = QtWidgets.QCheckBox("tous selectionner")
   layout.addWidget(self.tous)

   # cree le bouton organiser
   bouton = QtWidgets.QPushButton("organiser")
   # permet au bouton de fonctionner au click
   bouton.clicked.connect(self.organiser)
   # aajoute le bouton au widget
   layout.addWidget(bouton)

  # fonction qui permet de selectionner tout 
  def obtenir_objet(self):

    # vérifie si tout est sélectionner 
    if self.tous.isChecked():
    
      # sélectionne tout les objet
      cmds.select(all=True)

      # récupère les objets de type transforme avec leur chemain complet
      return cmds.ls(type="transform", long=True) or []

    # si la case n,est pas cocher elle récupère uniquement ce qui est sélectionner
    return cmds.ls(selection=True, type="transform", long=True) or []

  #fonction qui donne la couleur pour le nom
  def trouver_couleur(self, objet):

    # récupère le nom de l,objet sans la hiéarchie
    nom = objet.split("|") [-1]

    # parcour les préfixe et les couleur 
    for prefixe, couleur in self.config.items():
      # si le nom a le préfixe associer avec lui
      if prefixe in nom:
        # il lui retourne la couleur associer
        return couleur
    # il ne retorune rien si rien corespond    
    return None

  # fonction qui applique la couleur corespondant
  def appliquer_couleurs(self,objets):

    # parcoure tout les objet récupéré
    for objet in objets:

      # cherche la couleur rechercher
      couleur = self.trouver_couleur(objet)

      # modifier avec les couleur les objet reconue par json
      if couleur is not None:
        # active l,affiche des couleur dans le ouliner
        cmds.setAttr(objet + ".useOutlinerColor", True )
        # définit les couleur de l objet 
        cmds.setAttr(objet +".outlinerColor", couleur[0],couleur[1],couleur[2],type="double3" )

  # fontrion qui trie les objet
  def trier_objets(self,objets):

    # cree une liste vide pour les objet a triee
    objets_a_trier = []

    # parcour les objet récuéré
    for objet in objets:
      # ajoute seulement associer au règle
      if self.trouver_couleur(objet) is not None:
        objets_a_trier.append(objet)

    # trie les objet uniqument avec le nom 
    objets_a_trier.sort(key=lambda objet: objet.split("|")[-1].lower())

    # parcour les objet en ordre alphabetic
    for objet in objets_a_trier:
      # vérifie qui est toujour dans la scene
      if cmds.objExists(objet):
        #le déplace a la fin
        cmds.reorder(objet, back=True)

  # fonction de organiser
  def organiser(self):

    # recupere les objet selon de tout selectionner
    objets = self.obtenir_objet()

    # arrete si aucun objet recuperer
    if not objets:
      cmds.warning("Aucun objet sélectionné.")
      return

    # groupe d annulation pour regrouper les operation
    cmds.undoInfo(openChunk = True, chunkName = "OutlinerOrganizer")

    try:
      # applique les couleur si elle est cocher
      if self.couleur.isChecked():
        self.appliquer_couleurs(objets)
      # trie les objet si elle est cocher
      if self.tri.isChecked():
        self.trier_objets(objets)

    finally :
      #ferme le grouper d'a nualtion
      cmds.undoInfo(closeChunk=True)
# cree un instance de l outie
fenetre = OutlinerOrganizer()

# affiche la fenetre a l ecran 
fenetre.show()