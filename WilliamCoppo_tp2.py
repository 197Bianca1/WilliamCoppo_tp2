import sys
import os
import json

from maya import cmds 
from PySide6 import QtWidgets

def charger_config():
 try: 
  with open("rules.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    return data

 except FileNotFoundError:
  print ("Erreur : rules.json est introuvable. ")
  return {}


class OutlinerOrganizer(QtWidgets.QDialog):
  def __init__(self):

     super().__init__()

     self.setWindowTitle("outliner Organizer")

     self.resize(300,200)

     # changer la configuration
     self.config = charger_config()

     self.creer_interface()
  
  def creer_interface(self):
   
   layout = QtWidgets.QVBoxLayout(self)

   self.couleur = QtWidgets.QCheckBox("Appliquer les couleur")
   layout.addWidget(self.couleur)

   self.tri = QtWidgets.QCheckBox("trier par ordre alphabétique")
   layout.addWidget(self.tri)

   self.tous = QtWidgets.QCheckBox("tous selectionner")
   layout.addWidget(self.tous)

   bouton = QtWidgets.QPushButton("organiser")
   bouton.clicked.connect(self.organiser)
   layout.addWidget(bouton)

  def obtenir_objet(self):

    if self.tous.isChecked():

      return cmds.ls(type="transform", long=True) or []

    return cmds.ls(selection=True, type="transform", long=True) or []

  def trouver_couleur(self, objet):

    nom = objet.split("|") [-1]

    for prefixe, couleur in self.config.items():
      if nom.startswith(prefixe):
        return couleur
    return None

  def appliquer_couleurs(self,objets):

    for objet in objets:

      couleur = self.trouver_couleur(objet)

      if couleur is not None:
        cmds.setAttr(objet + ".useOutlinerColor", True )

        cmds.setAttr(objet +".outlinerColor", couleur[0],couleur[1],couleur[2],type="double3" )

  def trier_objets(self,objets):
    
    objets_a_trier = []

    for objet in objets:
      if self.trouver_couleur(objet) is not None:
        objets_a_trier.append(objet)

    objets_a_trier.sort(key=lambda objet: objet.split("|")[-1].lower())

    for objet in objets_a_trier:
      if cmds.objExists(objet):
        cmds.reorder(objet, back=True)

  def organiser(self):

    objets = self.obtenir_objet()

    if not objets:
      cmds.warning("Aucun objet sélectionné.")
      return

    cmds.undoInfo(openChunk = True, chunkName = "OutlinerOrganizer")

    try:

      if self.couleur.isChecked():
        self.appliquer_couleurs(objets)

      if self.tri.isChecked():
        self.trier_objets(objets)

    finally :
      cmds.undoInfo(closeChunk=True)

fenetre = OutlinerOrganizer()
fenetre.show()
