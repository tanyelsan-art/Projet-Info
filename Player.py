class Player:
    def __init__(self,name,hp,att):             #Id card
        self.name = name
        self.hp = hp
        self.att = att

    def welcome (self):               #Présente le joeur
        print("Bienvenue",self.name,"/ HP:",self.hp,"/ Att:",self.att)

    def get_name(self):                 #Retourne le prénom
        return self.name

    def get_hp(self):
        return self.hp

    def get_att(self):
        return self.att

    def take_damage(self,take_dammage):             #self prend des dégats
        self.hp -= take_dammage
        print("PV restant(s):",self.hp)

    def attack_target(self,target):                #self inflige des dégats a target
        print(self.name,"attaque",target.name,"et lui inflige",self.att,"dégat(s)")
        target.take_damage(self.att)

player1=Player("Kid",100,5)
Mob_test=Player("Mob",500,10)
player1.welcome()
print()
player1.attack_target(Mob_test)
Mob_test.attack_target(player1)
