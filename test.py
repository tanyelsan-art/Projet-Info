from player import Player
from weapon import Weapon
player1=Player("Kid",100,5,20)
Mob_test=Player("Mob",500,1,10)
player1.welcome()
print()
player1.attack_target(Mob_test)
Mob_test.attack_target(player1)
stick=Weapon("Bâton",10)
player1.set_weapon(stick)
player1.attack_target(Mob_test)

