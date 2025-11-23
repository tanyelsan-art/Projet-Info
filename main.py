import random               #Diff fction a import

import time

from systeme import loot_endlvl         #import tt les classes et fonctions nécéssaires
from player import Player

from mob import generate_mob
def game_launcher():
    print("Bienvenue dans le Xenoverse jeune aventurier")
    time.sleep(1)
    print("Ici, nul ne sait sur quoi tu vas tomber…(si ce n'est des entités dont on ne possède pas les droits d'auteur:))")
    time.sleep(1)
    print("Alors prépare toi au pire comme au meilleur. Bon courage!, tu vas en avoir besoin.")
    time.sleep(1)
    print("Vous affronterez des créatures en tout genre, en les attaquants tour par tour.")
    time.sleep(1)
    print("Après chaque affrontement, vous pourrez choisir entre 3 objets (une arme/une armure/un objet")
    time.sleep(1)
    print("Si vous équipez une arme, ca rajoute des dégâts supplémentaires et mettre une armure vous rend plus résistant. )")
    print("En équiper une 2e remplace la précédente")
    print("Une dernière chose, avant d'attaquer vous lancerez un dé à 20 faces.")
    time.sleep(0.5)
    print("Et selon le résultat, vous toucherez +/- votre adversaire; alors j'espère que c'est votre jour de chance :)")
def set_seed():
    print("Voulez-vous jouez avec une seed ? (évitez la 67... laissez vide pour aléatoire)")
    seed_input=input("Seed->")

    if seed_input!="":
        random.seed(seed_input)
        print(f"Seed utilisée: {seed_input}")
        return seed_input
    else:
        print("Seed aléatoire activée")
        return "seed random"

def combat(player,mob):
    print("Un monstre sauvage apparaît!!!(pas le budget pour la musique)")
    time.sleep(1)
    mob.welcome()

    while player.hp>0 and mob.hp>0:
        print(f"{player.name} ({player.hp}/{player.hp_max}PV) VS {mob.name} ({mob.hp}PV)")
        time.sleep(1)
        print("1) Attaquer")
        print(f"2) Boire potion ({player.potions} restante(s) )")
        print(f"3) Inventaire")

        choix_action=input("Choisissez l'action(1,2 ou 3)-> ")
        action_effectue=False                   #Nous dit si le joueur a deja joue son tour

        if choix_action=="1":
            player.attack_target(mob)
            action_effectue=True                #Le joueur a bel et bien joue

        elif choix_action=="2":
            player.use_potion()
            action_effectue=True

        elif choix_action=="3":
            if player.affiche_inventaire():                 #Verifie si inventaire pas vide
                choix_item_possible=[]                           #Si pas vide, on demande l'item souhaité mais si joueur écrit lettre -> crash
                for i in range(len(player.inventory)):      # on cree une liste avec tt les indice des item de l'inventaire
                    choix_item_possible.append(str(i))           #Converti i en str car input = str et le rajoute a la liste ( evite le bug)

                item_choisi=input("Quel item voulez-vous utilisez?")
                if item_choisi in choix_item_possible:          #verfie que l'indice de l'item choisi existe.
                    index=int(item_choisi)                      #On convertit en str pour que la fonction use item fonctionne
                    if player.use_item(index,mob):
                        action_effectue=True

                else:
                    print("Ce numéro n'est pas valide ")

            else:                                               #si inventaire est vide , il se passe rien
                pass

        else:
            print("Commande incorrecte")                        #joueur a choisis aucune des 3 options

        if mob.hp<=0:                                            #Si le mob est mort ca s'arrete la et il n'attaque pas en retour
            print(f"Vous avez vaincu {mob.name} !")
            return True

        if action_effectue:
            print('============================================================')
            time.sleep(3)
            print("Tour du monstre:")
            mob.attack_target(player)
            print('============================================================')


        if player.hp<=0:
            print("Vous avez succombé…")
            return False                        #Le joueur a perdu -> fin
    return False                                #Au cas ou y a un bug

def main():                                     #Lance le jeu
    game_launcher()
    seed_game=set_seed()
    print("Quel est ton nom, jeune padawan?")
    name=input("->")
    joueur=Player(name,120,40)              #defini le joueur grace a la class Player
    joueur.welcome()

    level=0                 #On commence au niveau 0 (tuto pour pas se faire one shot au début)

    while True:             #Boucle infini
        print(f"================================= Salle n°{level}==================================")
        input("Appuyez sur ENTER")
        monstre=generate_mob(level)
        combat_remporte=combat(joueur,monstre)

        if not combat_remporte:
            print(f"===GAME OVER===")
            print(f"Score= Lvl{level}")
            print(f"Seed utilisée: {seed_game}")
            break                           #Fin du prgrm


        else:
            loot_endlvl(level,joueur)
            level+=1
if __name__ == "__main__":                      #Lance le jeu uniquement si RUN
    main()






