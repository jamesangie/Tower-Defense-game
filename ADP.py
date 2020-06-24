import pygame
from Exception import *
import os

current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, 'venv/image')


class Tower:
    ATTACK_TIMER = 0

    TOWER_IMG = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "tower/tower1.jpg")), (50, 50))
    # name: [cost, power, attack_speed, r]
    TOWER_DICT = {"tower1": [50, 2, 2, 180]}

    def __init__(self, name, x, y):
        """create new tower object by selecting from TOWER_DICT"""
        if name not in self.TOWER_DICT.keys():
            raise CantFindTower
        self.name = name
        self.cost = self.TOWER_DICT[name][0]
        self.power = self.TOWER_DICT[name][1]
        self.attackSpeed = self.TOWER_DICT[name][2]
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
    ENEMY_IMG = [pygame.transform.scale(pygame.image.load(os.path.join(image_path, "enemy/enemy1.jpg")), (50, 50))]
    # name: [speed, hp, gold_drop]
    ENEMY_DICT = {"enemy1": [20, 100, 25]}

    def __init__(self, name, x, y):
        self.name = name
        self.speed = self.ENEMY_DICT[name][0]
        self.img = self.ENEMY_IMG[0]
        self.hp = self.ENEMY_DICT[name][1]
        self.gold_drop = self.ENEMY_DICT[name][2]
        self.tick = 0
        self.x = x
        self.y = y

    def get_pos(self):
        return self.x, self.y

    def move(self, map):
        self.tick += 1
        self.x = map.route[self.tick][0]
        self.y = map.route[self.tick][1]


class Map:
    MAP_IMG = [pygame.transform.scale(pygame.image.load(os.path.join(image_path, "map/map1.jpg")), (50, 50)),
               pygame.transform.scale(pygame.image.load(os.path.join(image_path, "map/map2.jpg")), (50, 50))]

    def __init__(self, map_id, route):
        self.map_id = map_id
        # route is a list of coordinates shows where the enemy should go
        self.route = route
        self.img = self.MAP_IMG[self.map_id - 1]

    def extend_route(self, pos):
        """extend current route to the new position(x,y)"""
        x = pos[0]
        y = pos[1]
        last_x = self.route[-1][0]
        last_y = self.route[-1][1]
        li = []
        if abs(x - last_x) >= abs(y - last_y):
            for i in range(last_x, x, -(last_x - x) // (abs(last_x - x))):
                li += [(last_x + i, round(last_y + (y - last_y) / (x - last_x) * i))]
        else:
            for i in range(last_y, y, -(last_y - y) // abs(last_y - y)):
                li += [(round(last_x + (x - last_x) / (y - last_y) * i), last_y + i)]
        self.route += li


class Base:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp


enemy1 = Enemy("enemy1", 50, 10)
