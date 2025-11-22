import json
import random

base_damage_weapon=10


class Weapon:
    def __init__(self, name, damage, description):
        self.name = name
        self.damage = damage
        self.description = description

    def get_name(self):
        return self.name
    def get_damage_value(self):
        return self.damage
    def get_description(self):  # Petit ajout utile
        return self.description


def generate_weapon(level_number):
    with open("data/weapon_dico.json","r",encoding="utf-8") as f:       #Charge le fichier Json
        list_weapons_json=json.load(f)

    info_weapons=random.choice(list_weapons_json)             #Choisi une arme random
    coef_damage_weapon = 1+(level_number*0.3)
    final_damage=int(base_damage_weapon*coef_damage_weapon)     #Calcul les degats d'armes

    new_weapon= Weapon(
        name=info_weapons["name"],
        damage=final_damage,
        description=info_weapons["description"])
    return new_weapon


