class Player:
    def __init__(self,name,hp,att):             #Id card
        self.name = name
        self.hp = hp
        self.att = att
        self.armor =None
        self.weapon=None

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

    def set_weapon(self,weapon):                    #Remplace l'arme de self par une nouvelle
        print(self.name,"a équipé",'"',weapon.name,'"',"(Dégats:",weapon.get_damage_value(),")")
        self.weapon=weapon

    def has_armor(self):
        return self.armor is not None

    def set_armor(self,armor):
        print(self.name,"a équipé",'"',armor.name,'"',"(Points d'armure:",armor.get_armor_point(),")")
        self.armor=armor
