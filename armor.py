import random
import json

base_armor_stats =5

class Armor:
    def __init__(self,name,description,armor_point):
        self.name = name
        self.armor_point = armor_point
        self.description = description
    def get_armor_point(self):
        return self.armor_point
    def get_name(self):
        return self.name

def generate_player_armor(level_number):
    with open("data/armor_player.json","r",encoding="utf-8") as armor_file:
        armor_liste=json.load(armor_file)
        info_armor=random.choice(armor_liste)               #Choix armure random

        armor_coef=1+(level_number*0.3)
        final_armor_points=int(base_armor_stats*armor_coef)     #Calcul de l'armure

        new_armor=Armor(
            name=info_armor["name"],
            description=info_armor["description"],
            armor_point=final_armor_points)
        return new_armor

