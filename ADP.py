import pygame


class Tower:
    ATTACK_TIMER = 0
    TOWER_IMG = pygame.transform.scale(pygame.image.load("venv/image/tower/tower1.jpg"), (50, 50))

    ## name: [cost, power, attack_speed, r]
    TOWER_DICT = {"tower1" : [50, 2, 2, 180]}

    def __init__(self, name, x, y):
        self.name = name
        self.cost = self.TOWER_DICT[name][0]
        self.power = self.TOWER_DICT[name][1]
        self.attackSpeed = self.[name][2]
        self.range = self.TOWER_DICT[name][3]
        self.x = x
        self.y = y

    def get_pos(self):
        return self.x, self.y

    def find_target(self, enemy_list):
        for enemy in enemy_list:
            if math.hypot(self.get_pos()[0] - enemy.get_pos()[0], self.get_pos()[1] - enemy.get_pos()[1]) < self.range:
                return enemy

    def attack(self, target_enemy):
        target_enemy.hp -= self.power


class Enemy:
    ENEMY_IMG = pygame.transform.scale(pygame.image.load("venv/image/enemy/enemy1.jpg"), (50, 50))
    ## name: [speed, hp, gold_drop]
    ENEMY_DICT = {"enemy1": [20, 100, 25]}

    def __init__(self, name, x, y):
        self.name = name
        self.speed = self.ENEMY_DICT[name][0]
        self.hp = self.ENEMY_DICT[name][1]
        self.gold_drop = self.ENEMY_DICT[name][2]
        self.x = x
        self.y = y

    def get_pos(self):
        return self.x, self.y

    def move(self):

class Map:
    MAP_IMG =
    def __init__(self, name):
        self.name = name


class Base:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp


tower1 = Tower("tower1")
enemy1 = Enemy("enemy1", 50, 10)
