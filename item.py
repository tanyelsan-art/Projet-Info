import json
import random
from armor import Armor
from weapon import Weapon
class Item:
    def __init__(self,name,description,type,value):
        self.name = name
        self.description = description
        self.type = type            #heal ou buff hp ou buff att ou offensive
        self.value = value

    def get_stats_effects(self):
        if self.type == "heal":
            return f"Soigne {self.value} PV"
        elif self.type == "buff_att":
            return f"+{self.value} ATK (Permanent)"
        elif self.type == "buff_HP":
            return f"+{self.value} PV MAX (Permanent)"
        elif self.type == "offensive":
            return f"{self.name} inflige {self.value} dégats"



def generate_items(level_number):
        with open('data/items.json',"r",encoding="utf-8") as item_file:
            items_list=json.load(item_file)
        info_item=random.choice(items_list)                 #Choisi un item random pour la fin de niveau

        new_item=Item(                                      #Crée l'objet en question
            info_item["name"],
            info_item["description"],
            info_item["type"],
            info_item["value"])
        return new_item
