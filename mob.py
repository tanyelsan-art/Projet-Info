class Mob:
    def __init__(self,name,hp,weapon,armor):             #Id card
        self.name = name
        self.hp = hp
        self.armor =armor
        self.weapon=weapon          #Un ennemi en a d'office une donc dégat d'arme=att
        self.att=None

    def spawn (self):               #Présente le mob
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
