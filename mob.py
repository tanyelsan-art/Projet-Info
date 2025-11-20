import json
import random
from weapon import Weapon
from armor import Armor

class Mob:
    def __init__(self,name,hp,weapon,armor):             #Id card
        self.name = name
        self.hp = hp
        self.armor =armor
        self.weapon=weapon          #Un ennemi en a d'office une donc dégat d'arme=att
        self.att=None

    def welcome (self):               #Présente le mob
        armor_val = self.armor.get_armor_point() if self.armor else 0
        dmg_val = self.weapon.get_damage_value() if self.weapon else 0
        print(self.name,"est apparu","/ PV:",self.hp,"/ Défense:",self.armor.get_armor_point(),"/ Att:",self.weapon.get_damage_value())

    def get_name(self):                 #Retourne le prénom
        return self.name

    def get_hp(self):
        return self.hp

    def get_att(self):
        return self.att

    def get_weapon(self):
        return self.weapon

    def take_damage(self,damage):             #self prend des dégats
        self.hp -= damage
        print("PV restant(s):",self.hp)

    def attack_target(self,target):                #self inflige des dégats a target (dégats d'arme si équipée)
        if self.has_weapon():
            if target.has_armor():
                damage=self.weapon.get_damage_value()-target.armor.get_armor_point()
            else:
                damage=self.weapon.get_damage_value()
        else:
            if target.has_armor():
                damage=self.att-target.armor.get_armor_point()
            else:
                damage=self.att
        if damage>0:
            print(self.name, "attaque", target.name, "et lui inflige",damage, "dégat(s)")
            target.take_damage(damage)
        else:
            print(self.name,"attaque",target.name,"mais c'est inéfficace")

    def has_weapon(self):                           #verifie si self posséde une arme
        return self.weapon is not None

    def has_armor(self):
        return self.armor is not None



def spawn_mob(level_number):
        with open("data/mob_dico.json","r",encoding="utf-8") as f:
            mobs_list =json.load(f)
        info_mob=random.choice(mobs_list)                           #Choisi un mob random
        difficulty_coef=1+(level_number*0.1)

        info_weapon=info_mob["weapon_ref"]                          #Construction de l'arme du mob (objet)
        final_damage=int(info_weapon["base_damage"]*difficulty_coef)

        mob_weapon=Weapon(
            name=info_weapon["name"],
            damage=final_damage,
            description="Arme du monstre")

        armor_val=info_mob["armor_points"]                          #Construction de l'armure (objet)
        armor_val=int(armor_val*difficulty_coef)

        mob_armor=Armor(
            name="Armure du monstre",
            armor_point=armor_val)

        final_HP=int(info_mob["base_HP"]*difficulty_coef)
        new_mob=Mob(
            name=info_mob["name"],
            hp=final_HP,
            weapon=mob_weapon,                      #Objet crée juste au dessus
            armor=mob_armor)
        return new_mob


