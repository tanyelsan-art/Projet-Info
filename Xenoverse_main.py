import random
import json
import time

class Colors:
    """Class permettant de modifier la couleur du texte affiché dans la console
    (Reset permet de remettre la couleur originale)"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'

class Player:
    """Class qui contient toutes les fonctions relatives au joueur"""
    def __init__(self, name, hp, att):
        """Carte d'identité du joueur (stats+items)
        l'inventaire est une liste vide qui va se remplir avec des objets récupérés en fin de niveau"""
        self.name = name
        self.hp = hp
        self.hp_max = hp                          # Pour ne pas soigner au dessus des pv max
        self.att = att

        self.armor = None                        # Commence sans armure ni arme
        self.weapon = None
        self.potions = 3                          # Commence avec 3 popo
        self.inventory = []

    def welcome(self):
        """Présente le joueur et affiche les stats principales"""
        print("Bienvenue", Colors.BLUE, self.name, Colors.GREEN, "/ PV:", self.hp, Colors.RESET, Colors.RED, "/ Att:", self.att, Colors.RESET)

    def get_name(self):
        """Renvoie le nom du joueur"""
        return self.name

    def get_hp(self):
        """Renvoie les hp du joueur"""
        return self.hp

    def get_att(self):
        """Renvoie l'att du joueur"""
        return self.att
    def get_armor(self):
        """"Renvoie l'armure du joueur"""
        return self.armor

    def take_damage(self, damage):
        """Self prend 'damage' dégats (calculés dans la fonction d'après)"""
        self.hp -= damage
        print("PV restant(s):", self.hp)

    def attack_target(self, target):
        """Commence par choisir 'aléatoirement' une valeur entre 1 et 20
        selon le résultat -> donne un coef de 'réussite' de l'att

        Ensuite regarde si le joueur possède une arme (et ajoute les dégats d'arme au dégats infligés si c'est le cas)
        Dans les 2 cas, regarde si l'ennemi possède une armure et réduit les dégats infligés si c'est le cas
        Si les dégats sont positifs, inflige les dégats à l'adversaire (nécessaire pour éviter de soigner l'ennemi)
          sinon attaque inéfficace"""
        input("Appuyez sur enter pour lancer le dé")
        dé_20 = random.randint(1, 20)
        bonus_malus_dé = 1
        print(f"Vous lancez le dé à 20 faces... résultats: {dé_20}")
        time.sleep(2)
        if dé_20 < 3:
            print("Vous avez glissé chef, vous ratez votre coup ")
            bonus_malus_dé -= 1                                       # dégats seront nul
        elif 3 <= dé_20 < 5:
            print("Vous effleurez l'ennemi")
            bonus_malus_dé -= 0.3                                     # dégats diminués de 30%
        elif dé_20 >= 18:
            print(f"{Colors.RED}Coup CRITIQUE!{Colors.RESET} (dégâts doublés)")                # dégats x2
            bonus_malus_dé += 1
        else:
            print("Coup réussi")                                    # dégats normaux

        if self.has_weapon():
            if target.has_armor():
                damage = int((self.att + self.weapon.get_damage_value()) * bonus_malus_dé - target.armor.get_armor_point())
            else:
                damage = int((self.att + self.weapon.get_damage_value()) * bonus_malus_dé)
        else:
            if target.has_armor():
                damage = int(self.att * bonus_malus_dé - target.armor.get_armor_point())
            else:
                damage = int(self.att * bonus_malus_dé)
        if damage > 0:
            if self.has_weapon():
                print(f"{self.name} attaque {target.name} avec {self.weapon.name} et lui inflige {damage} dégât(s)")
                target.take_damage(damage)
            else:
                print(f"{self.name} attaque {target.name} et lui inflige {damage} dégât(s)")
                target.take_damage(damage)

        else:
            print(self.name, "attaque", target.name, "mais c'est inefficace")

    def has_weapon(self):
        """Vérifie si le joueur a une arme"""
        return self.weapon is not None

    def set_weapon(self, weapon):
        """ Remplace l'arme du joueur par une nouvelle, si pas d'arme l'équipe"""
        print(self.name, "a équipé", '"', weapon.name, '"', "(Dégâts supp:", weapon.get_damage_value(), ")")
        self.weapon = weapon

    def has_armor(self):
        """Vérifie si le joueur a une armure """
        return self.armor is not None

    def set_armor(self, armor):
        """Donne l'armure au joueur ou remplace l'ancienne"""
        print(self.name, "a équipé", '"', armor.name, '"', "(Points d'armure:", armor.get_armor_point(), ")")
        self.armor = armor

    def use_potion(self):
        """ Utilise une potion de soin
         1) vérifie si le joueur a une potion
         2) calcul les hp manquants pour éviter de soigner au dessus des PV max
         3) soigne le joueur et lui enlève une potion"""
        potion_heal_val = int(self.hp_max * 0.40)

        if self.potions > 0:
            HP_manquant = self.hp_max - self.hp
            heal_val = min(HP_manquant, potion_heal_val)               # Afin de pas regen + que pv max
            self.hp += heal_val
            self.potions -= 1
            print(f"{Colors.GREEN}{self.name} boit une potion et récupère {heal_val} PV! (Reste {self.potions} potion(s)){Colors.RESET}")
        else:
            print("Vous n'avez plus de potion")

    def add_potion(self):
        """Ajoute une potion au joueur """
        self.potions += 1
        print(f"{Colors.GREEN}vous gagnez une potion ({self.potions} potion(s) restante(s)){Colors.RESET}")
    def add_item(self, item):
        """Ajoute un item dans l'inventaire (pourra être utilisé plus tard) """
        self.inventory.append(item)
        print(f"Vous rangez {item.name} dans votre inventaire")


    def affiche_inventaire(self):
        """Affiche l'inventaire
        1)Vérifie si l'inventaire est vide ("return False si vide)
        2)Si pas boucle chaque item de l'inventaire et l'affiche accompagné de son indice et return True"""
        print("INVENTAIRE:")
        if not self.inventory:
            print(f"{Colors.RED}Votre sac est vide.{Colors.RESET}")
            return False                            # Rien a utiliser (évite le crash)
        else:
            for i, item in enumerate(self.inventory):             # Boucle chaque item avec leurs indices respectif (cf enumerate)
                print(f"{i}) {item.name} ({item.description})")
            return True                         # Il y a des objets utilisable

    def use_item(self, index, target_mob):
        """ Va permettre d'utiliser un item (variable target_mob nécéssaire pour les items offensifs)
        1) Vérifie si l'item associé à l'index éxiste (si pas, return False et le joueur peut quand même jouer sans crash)
        2) Pop supprime l'item et le renvoie
        3) Vérifie le type de l'item et applique l'effet souhaité et return True (donc le joueur a bel et bien utilisé un item)
        """
        if index >= 0 and index < len(self.inventory):
            item_used = self.inventory.pop(index)         # Pop supp l'item et le renvoi
            print(f"Vous utilisez: {item_used.name} ")

            if item_used.item_type == "heal":
                HP_manquant = self.hp_max - self.hp
                heal_val = min(HP_manquant, item_used.value)           # Afin de pas regen + que pv max
                self.hp += heal_val
                print(item_used.get_stats_effects())

            if item_used.item_type == "offensive":
                print(item_used.get_stats_effects())
                target_mob.take_damage(item_used.value)
            return True
        else:
            print("Cet objet n'existe pas")
            return False                        # Pas d'objet (évite le crash si jamais)


class Item:
    """Class d'un item"""
    def __init__(self, name, description, item_type, value):
        """Définit l'item et ses stats"""
        self.name = name
        self.description = description
        self.item_type = item_type            # heal ou buff hp ou buff att ou offensive
        self.value = value

    def get_stats_effects(self):
        """Affiche l'effet souhaité (ne fait rien d'autre)"""
        if self.item_type == "heal":
            return f"Soigne {self.value} PV"
        elif self.item_type == "buff_att":
            return f"+{self.value} ATK (Permanent)"
        elif self.item_type == "buff_HP":
            return f"+{self.value} PV MAX (Permanent)"
        elif self.item_type == "offensive":
            return f"{self.name} inflige {self.value} dégâts"
        else:
            return None             #Sécurité supplémentaire


def generate_items(level_number=1): # Ajout de level_number pour compatibilité
    """Crée un item
    1) Ouvre le Json, crée une liste et y ajoute tous les items possibles
    2) En choisi un aléatoirement"""
        with open('data/items.json', "r", encoding="utf-8") as item_file:
            items_list = json.load(item_file)
        info_item = random.choice(items_list)                 # Choisi un item random pour la fin de niveau

        new_item = Item(                                      # Crée l'objet en question
            info_item["name"],
            info_item["description"],
            info_item["type"],
            info_item["value"])
        return new_item


class Mob:
    def __init__(self, name, hp, weapon, armor):             # Id card
        self.name = name
        self.hp = hp
        self.armor = armor
        self.weapon = weapon          # Un ennemi en a d'office une donc dégat d'arme=att
        self.att = None

    def welcome(self):               # Présente le mob
        print(self.name, "est apparu", Colors.GREEN, "/ PV:", self.hp, Colors.CYAN, "/ Défense:", self.armor.get_armor_point(), Colors.RED, "/ Att:", self.weapon.get_damage_value(), Colors.RESET)

    def get_name(self):                 # Retourne le prénom
        return self.name

    def get_hp(self):
        return self.hp

    def get_att(self):
        return self.att

    def get_weapon(self):
        return self.weapon

    def take_damage(self, damage):             # self prend des dégats
        self.hp -= damage
        print("PV restant(s):", self.hp)

    def attack_target(self, target):                # self inflige des dégats a target (dégats d'arme si équipée)
        dé_20 = random.randint(1, 20)
        bonus_malus_dé = 1
        print(f"{self.name} lance le dé à 20 faces... résultats: {dé_20}")
        time.sleep(2)
        if dé_20 < 3:
            print("Coup raté ")
            bonus_malus_dé -= 1  # dégats seront nul
        elif 3 <= dé_20 <= 5:
            print("Il vous effleure")
            bonus_malus_dé -= 0.3  # dégats diminué de 30%
        elif dé_20 >= 18:
            print("Coup CRITIQUE! (dégâts doublés)")  # degats x2
            bonus_malus_dé += 1
        else:
            print("Coup réussi")  # dégats normaux
        if self.has_weapon():
            if target.has_armor():
                damage = int((self.weapon.get_damage_value()) * bonus_malus_dé - target.armor.get_armor_point())
            else:
                damage = int(self.weapon.get_damage_value() * bonus_malus_dé)
        else:
            if target.has_armor():
                damage = int((self.att) * bonus_malus_dé - target.armor.get_armor_point())
            else:
                damage = int(self.att * bonus_malus_dé)
        if damage > 0:
            print(f"{self.name} attaque {target.name} avec {self.weapon.name} et inflige {damage} dégât(s)")
            target.take_damage(damage)
        else:
            print(self.name, "attaque", target.name, "mais c'est inefficace")

    def has_weapon(self):                           # verifie si self posséde une arme
        return self.weapon is not None

    def has_armor(self):
        return self.armor is not None


def generate_mob(level_number):
        with open("data/mob_dico.json", "r", encoding="utf-8") as f:
            mobs_list = json.load(f)
        info_mob = random.choice(mobs_list)                           # Choisi un mob random
        difficulty_coef = 1 + (level_number * 0.30)

        info_weapon = info_mob["weapon_ref"]                          # Construction de l'arme du mob (objet)
        final_damage = int(info_weapon["base_damage"] * difficulty_coef)

        mob_weapon = Weapon(
            name=info_weapon["name"],
            damage=final_damage,
            description="Arme du monstre")

        armor_val = info_mob["armor_points"]                          # Construction de l'armure (objet)
        armor_val = int(armor_val * difficulty_coef)

        mob_armor = Armor(
            name="Armure du monstre",
            armor_point=armor_val,
            description="Armure du monstre")

        final_HP = int(info_mob["base_HP"] * difficulty_coef)
        new_mob = Mob(
            name=info_mob["name"],
            hp=final_HP,
            weapon=mob_weapon,                      # Objet crée juste au dessus
            armor=mob_armor)
        return new_mob


base_damage_weapon = 10

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
    with open("data/weapon_dico.json", "r", encoding="utf-8") as f:       # Charge le fichier Json
        list_weapons_json = json.load(f)

    info_weapons = random.choice(list_weapons_json)             # Choisi une arme random
    coef_damage_weapon = 1 + (level_number * 0.25)
    final_damage = int(base_damage_weapon * coef_damage_weapon)     # Calcul les degats d'armes

    new_weapon = Weapon(
        name=info_weapons["name"],
        damage=final_damage,
        description=info_weapons["description"])
    return new_weapon


base_armor_stats = 10

class Armor:
    def __init__(self, name, description, armor_point):
        self.name = name
        self.armor_point = armor_point
        self.description = description
    def get_armor_point(self):
        return self.armor_point
    def get_name(self):
        return self.name

def generate_player_armor(level_number):
    with open("data/armor_player.json", "r", encoding="utf-8") as armor_file:
        armor_liste = json.load(armor_file)
        info_armor = random.choice(armor_liste)               # Choix armure random

        armor_coef = 1 + (level_number * 0.25)
        final_armor_points = int(base_armor_stats * armor_coef)     # Calcul de l'armure

        new_armor = Armor(
            name=info_armor["name"],
            description=info_armor["description"],
            armor_point=final_armor_points)
        return new_armor


def loot_endlvl(level_number, player):
    print("=======================================")
    time.sleep(2)
    print(f"{Colors.YELLOW}Récompense de fin du niveau {level_number} :{Colors.RESET}")
    time.sleep(1)

    player.add_potion()                # Gagne une potion a chaque niveau
    time.sleep(1)
    print(f"Choisissez une récompense supplémentaire:")             # Crée 3 options et les affiches ensuites
    time.sleep(1)
    choix1_weapon = generate_weapon(level_number)
    choix2_armor = generate_player_armor(level_number)
    choix3_item = generate_items(level_number)

    print(f"1) Arme: {choix1_weapon.name}")
    print(f"   Infos: {choix1_weapon.description}")
    print(f"   Stats: {choix1_weapon.damage} dégâts supp")

    print(f"2) Armure: {choix2_armor.name}")
    print(f"   Infos: {choix2_armor.description}")
    print(f"   Stats: {choix2_armor.armor_point} ")

    print(f"3) Item: {choix3_item.name}")
    print(f"   Type: {choix3_item.item_type}")
    print(f"   Infos: {choix3_item.description}")

    while True:                                     # Boucle de choix
        print("(1, 2 ou 3)")
        choix_joueur = input("-> ")
        if choix_joueur == "1":
            player.set_weapon(choix1_weapon)            # Si il choisit 1, le joueur prend l'arme du choix 1 (générée depuis la classe)
            break
        elif choix_joueur == "2":
            player.set_armor(choix2_armor)
            break
        elif choix_joueur == "3":                       # Utilse les buff instant ou range dans l'inventaire le resre
            if choix3_item.item_type == "buff_att":
                player.att += choix3_item.value
                print(choix3_item.get_stats_effects())
                break
            elif choix3_item.item_type == "buff_HP":
                player.hp_max += choix3_item.value
                print(choix3_item.get_stats_effects())
                break
            elif choix3_item.item_type == "heal":
                if choix3_item.name == "potion":
                    player.add_potion()
                else:
                    player.add_item(choix3_item)
                break
            elif choix3_item.item_type == "offensive":
                player.add_item(choix3_item)
                break
        else:
            print("Choix invalide")


def game_launcher():
    print("Bienvenue jeune aventurier dans le...")
    time.sleep(2)
    print(Colors.GREEN + r"""
       _   __ _______   ______ _    ____________  _____ ______
      | |/ // ____/ | / / __ \ |   / / ____/ __ \/ ___// ____/
      |   // __/ /  |/ / / / / | / / __/ / /_/ /\__ \/ __/
     /   |/ /___/ /|  / /_/ /| |/ / /___/ _, _/___/ / /___
    /_/|_/_____/_/ |_/\____/ |___/_____/_/ |_|/____/_____/
    """ + Colors.RESET)
    time.sleep(2)
    print("Ici, nul ne sait sur quoi tu vas tomber… (si ce n'est des entités dont on ne possède pas les droits d'auteur :))")
    time.sleep(1)
    print("Alors prépare-toi au pire comme au meilleur. Bon courage, tu vas en avoir besoin !")
    time.sleep(1)
    print("Vous affronterez des créatures en tout genre, en les attaquant tour par tour.")
    time.sleep(1)
    print("Après chaque affrontement, vous pourrez choisir entre 3 objets (une arme / une armure / un objet).")
    time.sleep(1)
    print("Si vous équipez une arme, elle infligera des dégâts supplémentaires et mettre une armure vous rend plus résistant.")
    print("En équiper une 2e remplace la précédente.")
    print("Une dernière chose : avant d'attaquer vous lancerez un dé à 20 faces.")
    time.sleep(0.5)
    print("Et selon le résultat, vous toucherez +/- votre adversaire. Alors j'espère que c'est votre jour de chance :)")

def set_seed():
    print("Voulez-vous jouer avec une seed ? (évitez 'python'... laissez vide pour aléatoire)")
    seed_input = input("Seed -> ")

    if seed_input != "":
        random.seed(seed_input)
        print(f"Seed utilisée : {seed_input}")
        return seed_input
    else:
        print("Seed aléatoire activée")
        return "Seed random"

def combat(player, mob):
    print("Un monstre sauvage apparaît !!! (pas le budget pour la musique)")
    time.sleep(1)
    mob.welcome()

    while player.hp > 0 and mob.hp > 0:
        print(f"{player.name} {Colors.GREEN}{player.hp}/{player.hp_max}PV {Colors.RESET}({player.att} dégâts de base)  {Colors.RED} VS {Colors.RESET}  {mob.name} {Colors.GREEN}({mob.hp}PV){Colors.RESET}")
        time.sleep(1)
        print(Colors.RED + "1) ", "Attaquer", Colors.RESET)
        print(f"{Colors.GREEN}2) Boire potion ({player.potions} restante(s)){Colors.RESET}")
        print(f"{Colors.YELLOW}3) Inventaire{Colors.RESET}")

        choix_action = input("Choisissez l'action (1, 2 ou 3) -> ")
        action_effectue = False                   # Nous dit si le joueur a deja joue son tour

        if choix_action == "1":
            player.attack_target(mob)
            action_effectue = True                # Le joueur a bel et bien joue

        elif choix_action == "2":
            player.use_potion()
            action_effectue = True

        elif choix_action == "3":
            if player.affiche_inventaire():                 # Verifie si inventaire pas vide
                choix_item_possible = []                           # Si pas vide, on demande l'item souhaité mais si joueur écrit lettre -> crash
                for i in range(len(player.inventory)):      # on cree une liste avec tt les indice des item de l'inventaire
                    choix_item_possible.append(str(i))           # Converti i en str car input = str et le rajoute a la liste (evite le bug)

                item_choisi = input("Quel item voulez-vous utiliser ? ")
                if item_choisi in choix_item_possible:          # verfie que l'indice de l'item choisi existe.
                    index = int(item_choisi)                      # On convertit en str pour que la fonction use item fonctionne
                    if player.use_item(index, mob):
                        action_effectue = True

                else:
                    print("Ce numéro n'est pas valide.")

            else:                                               # si inventaire est vide, il se passe rien
                pass

        else:
            print("Commande incorrecte")                        # joueur a choisis aucune des 3 options
            print("============================================")

        if mob.hp <= 0:                                            # Si le mob est mort ca s'arrete la et il n'attaque pas en retour
            print(f"Vous avez vaincu {mob.name} !")
            return True

        if action_effectue:
            print('============================================================')
            time.sleep(3)
            print("Tour du monstre :")
            mob.attack_target(player)
            print('============================================================')
            time.sleep(1.5)

        if player.hp <= 0:
            print("Vous avez succombé…")
            return False                        # Le joueur a perdu -> fin
    return False                                # Au cas ou y a un bug

def main():                                     # Lance le jeu
    game_launcher()
    seed_game = set_seed()
    print("Quel est ton nom, jeune padawan ?")
    name = input("-> ")
    joueur = Player(name, 120, 40)              # defini le joueur grace a la class Player
    joueur.welcome()

    level = 0                 # On commence au niveau 0 (tuto pour pas se faire one shot au début)

    while True:             # Boucle infini
        print(f"================================= Salle n°{level} ==================================")
        input("Appuyez sur ENTER")
        monstre = generate_mob(level)
        combat_remporte = combat(joueur, monstre)

        if not combat_remporte:
            print(f"=== GAME OVER ===")
            print(f"Score = Lvl {level}")
            print(f"Seed utilisée : {seed_game}")
            break                           # Fin du prgrm

        else:
            loot_endlvl(level, joueur)
            level += 1

if __name__ == "__main__":                      # Lance le jeu uniquement si RUN
    main()

