import sys
import os
import json

from maya import cmds 
from PySide6 import QtWidgets
def charger_config():
 try: 
  with open("rules.json", "r", encoding="utf-8") as f:
    data = json.load(f)

 except FileNotFoundError:
  print ("Erreur : rules.json est introuvable. ")


class OutlinerOrganizer(QtWidgets.QDialog):
  def __int__(self):

     super().__init__()

     self.setWindowTitle("outliner Organizer")

     self.resize(400,300)

     # changer la configuration
     self.config = charger_config()

     self.creer_interface()