import random
import json
from gc import get_stats

from item import Item
from item import generate_items
from weapon import Weapon
from weapon import  generate_weapon
from armor import Armor
from armor import generate_player_armor
from mob import Mob
from mob import generate_mob
from player import Player

def loot_endlvl(level_number,player):
    print(f"Récompense de fin du niveau {level_number} :")

    player.add_potion()                #Gagne une potion a chaque niveau

    print(f"Choisissez une récompense supplémentaire:")             #Crée 3 options et les affiches ensuites
    choix1_weapon=generate_weapon(level_number)
    choix2_armor=generate_player_armor(level_number)
    choix3_item = generate_items(level_number)

    print(f"1) Arme: {choix1_weapon.name}")
    print(f"   Infos:{choix1_weapon.description}")
    print(f"   Stats:{choix1_weapon.damage } dégats")

    print(f"2) Armure: {choix2_armor.name}")
    print(f"   Infos:{choix2_armor.description}")
    print(f"   Stats:{choix2_armor.armor_point} ")

    print(f"3) Item: {choix3_item.name}")
    print(f"   Type:{choix3_item.type}")
    print(f"   Infos:{choix3_item.description}")

    while True:                                     #Boucle de choix
        print("(1,2 ou 3)")
        choix_joueur=input("->")
        if choix_joueur == "1":
            player.set_weapon(choix1_weapon)            #Si il choisit 1, le joueur prend l'arme du choix 1 (générée depuis la classe)
            break
        elif choix_joueur == "2":
            player.set_armor(choix2_armor)
            break
        elif choix_joueur == "3":                       #Utilse les buff instant ou range dans l'inventaire le resre
            if choix3_item.type=="buff_att":
                player.att += choix3_item.value
                print(choix3_item.get_stats_effects())
                break
            elif choix3_item.type=="buff_HP":
                player.hp_max += choix3_item.value
                print(choix3_item.get_stats_effects())
                break
            elif choix3_item.type=="heal":
                if choix3_item.name=="potion":
                    player.add_potion()
                else:
                    player.add_item(choix3_item)
                break
            elif choix3_item.type=="offensive":
                player.add_item(choix3_item)
                break
        else:
            print("Choix invalide")

