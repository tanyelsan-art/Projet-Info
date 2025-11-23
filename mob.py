

class Mob:
    def __init__(self,name,hp,weapon,armor):             #Id card
        self.name = name
        self.hp = hp
        self.armor =armor
        self.weapon=weapon          #Un ennemi en a d'office une donc dégat d'arme=att
        self.att=None

    def welcome (self):               #Présente le mob
        print(self.name,"est apparu",Colors.GREEN,"/ PV:",self.hp,Colors.CYAN,"/ Défense:",self.armor.get_armor_point(),Colors.RED,"/ Att:",self.weapon.get_damage_value(),Colors.RESET)

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
        dé_20=random.randint(1,20)
        bonus_malus_dé = 1
        print(f"{self.name} le dé à 20 faces... résultats:{dé_20}")
        time.sleep(2)
        if dé_20 < 3:
            print("Coup raté ")
            bonus_malus_dé -= 1  # dégats seront nul
        elif 3 <= dé_20 < 5:
            print("Il vous effleure")
            bonus_malus_dé -= 0.3  # dégats diminué de 30%
        elif dé_20 >= 18:
            print("Coup CRITIQUE! (dégats doublés)")  # degats x2
            bonus_malus_dé += 1
        else:
            print("Coup réussi")  # dégats normaux
        if self.has_weapon():
            if target.has_armor():
                damage=int((self.weapon.get_damage_value())*bonus_malus_dé-target.armor.get_armor_point())
            else:
                damage=int(self.weapon.get_damage_value()*bonus_malus_dé)
        else:
            if target.has_armor():
                damage=int((self.att)*bonus_malus_dé-target.armor.get_armor_point())
            else:
                damage=int(self.att*bonus_malus_dé)
        if damage>0:
            print(f"{self.name} attaque {target.name} avec {self.weapon.name} et inflige {damage} dégat(s)")
            target.take_damage(damage)
        else:
            print(self.name,"attaque",target.name,"mais c'est inéfficace")

    def has_weapon(self):                           #verifie si self posséde une arme
        return self.weapon is not None

    def has_armor(self):
        return self.armor is not None



def generate_mob(level_number):
        with open("data/mob_dico.json","r",encoding="utf-8") as f:
            mobs_list =json.load(f)
        info_mob=random.choice(mobs_list)                           #Choisi un mob random
        difficulty_coef=1+(level_number*0.30)

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
            armor_point=armor_val,
            description="Armure du monstre")

        final_HP=int(info_mob["base_HP"]*difficulty_coef)
        new_mob=Mob(
            name=info_mob["name"],
            hp=final_HP,
            weapon=mob_weapon,                      #Objet crée juste au dessus
            armor=mob_armor)
        return new_mob


