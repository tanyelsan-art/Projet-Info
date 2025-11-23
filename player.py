import random
import time

class Player:
    def __init__(self,name,hp,att):             #Id card (stats+equip)
        self.name = name
        self.hp = hp
        self.hp_max=hp                          #Pour ne pas soigner au dessus des pv max
        self.att = att

        self.armor =None                        #Commence sans armure ni arme
        self.weapon=None
        self.potions=3                          #Commence avec 3 popo
        self.inventory=[]

    def welcome (self):               #Présente le joeur
        print("Bienvenue",self.name,"/ PV:",self.hp,"/ Att:",self.att)

    def get_name(self):                 #Retourne le prénom
        return self.name

    def get_hp(self):
        return self.hp

    def get_att(self):
        return self.att
    def get_armor(self):
        return self.armor

    def take_damage(self,damage):             #self prend des dégats
        self.hp -= damage
        print("PV restant(s):",self.hp)

    def attack_target(self,target):                #self inflige des dégats a target (dégats d'arme si équipée)
        input("Appuyez sur enter pour lancer le dé")
        dé_20=random.randint(1,20)
        bonus_malus_dé=1
        print(f"Vous lancé le dé à 20 faces... résultats:{dé_20}")
        time.sleep(2)
        if dé_20<3:
            print("Vous avez glissé chef, vous ratez votre coup ")
            bonus_malus_dé-=1                                       #dégats seront nul
        elif 3<=dé_20<5:
            print("Vous éffleurez l'ennemi")
            bonus_malus_dé-=0.3                                     #dégats diminué de 30%
        elif dé_20>=18:
            print("Coup CRITIQUE! (dégats doublés)")                #degats x2
            bonus_malus_dé+=1
        else:
            print("Coup réussi")                                    #dégats normaux

        if self.has_weapon():                                       #Si le joueur a une arme il tappe plus fort
            if target.has_armor():                                  #Si l'ennemi a armure il faut enlever cela aux dégats
                damage=int((self.att+self.weapon.get_damage_value())*bonus_malus_dé-target.armor.get_armor_point())
            else:
                damage=int((self.att+self.weapon.get_damage_value())*bonus_malus_dé)
        else:
            if target.has_armor():
                damage=int(self.att*bonus_malus_dé-target.armor.get_armor_point())
            else:
                damage=int(self.att*bonus_malus_dé)
        if damage>0:
            if self.has_weapon():
                print(f"{self.name} attaque {target.name} avec {self.weapon.name} et lui inflige {damage} dégat(s)")
                target.take_damage(damage)
            else:
                print(f"{self.name} attaque {target.name} et lui inflige {damage} dégat(s)")
                target.take_damage(damage)

        else:
            print(self.name,"attaque",target.name,"mais c'est inéfficace")

    def has_weapon(self):                           #verifie si self posséde une arme
        return self.weapon is not None

    def set_weapon(self,weapon):                    #Remplace l'arme de self par une nouvelle
        print(self.name,"a équipé",'"',weapon.name,'"',"(Dégats:",weapon.get_damage_value(),")")
        self.weapon=weapon

    def has_armor(self):
        return self.armor is not None

    def set_armor(self,armor):
        print(self.name,"a équipé",'"',armor.name,'"',"(Points d'armure:",armor.get_armor_point(),")")
        self.armor=armor

    def use_potion(self):
        potion_heal_val=int(self.hp_max*0.40)

        if self.potions>0:
            HP_manquant=self.hp_max-self.hp
            heal_val=min(HP_manquant,potion_heal_val)               #Afin de pas regen + que pv max
            self.hp+=heal_val
            self.potions-=1
            print(f"{self.name} boit une potion et récupère {heal_val} PV! (Reste{self.potions} potion(s))")
        else:
            print("Vous n'avez plus de potion")

    def add_potion(self):
        self.potions+=1
        print(f"vous gagnez une potion ({self.potions} potion(s) restante(s))")
    def add_item(self,item):
        self.inventory.append(item)
        print(f"Vous rangez {item.name} dans votre inventaire")


    def affiche_inventaire(self):
        print("INVENTAIRE:")
        if not self.inventory:
            print("Votre sac est vide.")
            return False                            #Rien a utiliser (évite le crash)
        else:
            for i, item in enumerate(self.inventory):             #Boucle chaque item avec leurs indices respectif (cf enumerate)
                print(f"{i}) {item.name} ({item.description})")
            return True                         #Il y a des objets utilisable

    def use_item(self,index,target_mob):            #target mob needed pour les objets type:offensive
        if index >= 0 and index < len(self.inventory):              #Verfifie que l'index de l'item souhaité existe
            item_used=self.inventory.pop(index)         #Pop supp l'item et le renvoi
            print(f"Vous utilisez:{item_used.name} ")

            if item_used.item_type == "heal":                    #Verfie le type de l'item
                HP_manquant=self.hp_max-self.hp
                heal_val=min(HP_manquant,item_used.value)           #Afin de pas regen + que pv max
                self.hp+=heal_val
                print(item_used.get_stats_effects())

            if item_used.item_type == "offensive":
                print(item_used.get_stats_effects())
                target_mob.take_damage(item_used.value)
            return True
        else:
            print("Cet objet n'existe pas")
            return False                        #Pas d'objet (évite le crash si jamais)

