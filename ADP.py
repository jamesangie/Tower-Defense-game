import pygame
import json
from Exception import *
import math
import os

current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, 'image')
stats_path = os.path.join(current_path, "STATS")


def initialize_stats():
    """
    clear all the info in the stats file
    :return: None
    """
    d = {"tower": {},"enemy": {}, "map": []}
    with open(os.path.join(stats_path, "object_stats"), 'w') as fhl:
        s1 = json.dumps(d)
        fhl.write(s1)


# Save the new Tower with stats into the stats file
def saveNewTower(name, cost, ATT, attack_speed, att_range):
    """
    Save the new Tower with stats into the stats file
    :return: None
    """
    with open(os.path.join(stats_path, "object_stats"), 'r') as fhs:
        s = fhs.read()
        stats = json.loads(s)
    stats["tower"][name] = {"cost": cost, "ATT": ATT, "attack_speed": attack_speed, "range": att_range}
    with open(os.path.join(stats_path, "object_stats"), 'w') as fhl:
        s1 = json.dumps(stats)
        fhl.write(s1)


def saveNewEnemy(name, speed, hp, gold_drop):
    with open(os.path.join(stats_path, "object_stats"), 'r') as fhs:
        s = fhs.read()
        stats = json.loads(s)
    stats["enemy"][name] = {"speed": speed, "hp": hp, "gold_drop": gold_drop}
    with open(os.path.join(stats_path, "object_stats"), 'w') as fhl:
        s1 = json.dumps(stats)
        fhl.write(s1)


class Tower:
    ATTACK_TIMER = 0

    TOWER_IMG = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "tower/tower1.jpg")), (50, 50))
    # name: [cost, power, attack_speed, r]
    TOWER_DICT = {"tower1": [50, 2, 2, 180]}

    def __init__(self, name, x, y):
        """
        create new tower object by selecting from TOWER_DICT
        """
        if name not in self.TOWER_DICT.keys():
            raise CantFindTower
        self.name = name
        self.cost = self.TOWER_DICT[name][0]
        self.power = self.TOWER_DICT[name][1]
        self.attackSpeed = self.TOWER_DICT[name][2]
        self.range = self.TOWER_DICT[name][3]
        self.target = False
        self.x = x
        self.y = y

    def get_pos(self):
        return self.x, self.y

    def find_target(self, enemy_list):
        """
        find the new enemy in tower's attack range
        :param enemy_list: list(Enemy)
        :return: None
        """
        for enemy in enemy_list:
            if math.hypot(self.get_pos()[0] - enemy.get_pos()[0], self.get_pos()[1] - enemy.get_pos()[1]) < self.range:
                self.target = enemy

    def attack(self, target_enemy):
        target_enemy.hp -= self.power
        if target_enemy.hp <= 0:
            target_enemy.isDead = True





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
        self.isDead = False
        self.tick = 0
        self.x = x
        self.y = y

    def get_pos(self):
        return self.x, self.y

    def move(self, the_map):
        self.tick += 1
        self.x = the_map.route[self.tick][0]
        self.y = the_map.route[self.tick][1]


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
        # looks for all the integer coordinates between route's last coordinate and pos
        # find max (|x - last_x|, |y - last_y|) and use it to find the other
        if abs(x - last_x) >= abs(y - last_y) and not(abs(x - last_x) == 0):
            for i in range(last_x, x, -(last_x - x) // (abs(last_x - x))):
                difference = i - last_x - (last_x - x) // (abs(last_x - x))
                li += [(last_x + difference, round(last_y + (y - last_y) / (x - last_x) * difference))]
        elif abs(x - last_x) < abs(y - last_y) and not(abs(y - last_y) == 0):
            for i in range(last_y, y, -(last_y - y) // abs(last_y - y)):
                difference = i - last_y - (last_y - y) // abs(last_y - y)
                li += [(round(last_x + (x - last_x) / (y - last_y) * difference), last_y + difference)]
        self.route += li


class Base:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp


enemy1 = Enemy("enemy1", 50, 10)
