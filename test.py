from mob import Mob
from player import Player
from weapon import Weapon
from armor import Armor
player1=Player("Kid",100,5)
gode=Weapon("Lol",25)
armure_raul=Armor("armure raul",10)
Raul=Mob("Raul",500,gode,armure_raul)
player1.welcome()
Raul.spawn()
print()
player1.attack_target(Raul)
deodorant=Weapon("deodorant",50)
player1.set_weapon(deodorant)
player1.attack_target(Raul)

