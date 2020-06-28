import pygame
from Exception import *
import math
from stats_IO import *


class Tower:
    ATTACK_TIMER = 0

    TOWER_IMG = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "tower/tower1.jpg")), (50, 50))
    # name: [cost, power, attack_speed, r, img]
    TOWER_DICT = readTower()

    def __init__(self, name, x, y):
        """
        create new tower object by selecting from TOWER_DICT
        """
        if name not in self.TOWER_DICT.keys():
            raise CantFindTower
        self.name = name
        self.cost = self.TOWER_DICT[name]["cost"]
        self.ATT = self.TOWER_DICT[name]["ATT"]
        self.attackSpeed = self.TOWER_DICT[name]["attack_speed"]
        self.range = self.TOWER_DICT[name]["range"]
        self.img = pygame.transform.scale(pygame.image.load(os.path.join(image_path, self.TOWER_DICT[name]["img"])),
                                          (50, 50))
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
        target_enemy.hp -= self.ATT
        if target_enemy.hp <= 0:
            target_enemy.isDead = True

    def draw(self, screen):
        screen.blit(self.img)


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
        self.x = the_map.route[self.tick * self.speed][0]
        self.y = the_map.route[self.tick * self.speed][1]

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))


class Map:
    MAP_DICT = readMap()

    def __init__(self, map_name, init_route=False):
        self.map_name = map_name
        # route is a list of coordinates shows where the enemy should go
        if not init_route:
            self.route = self.MAP_DICT[map_name]["route"]
        else:
            self.route = [init_route]
        self.img = pygame.transform.scale(pygame.image.load(os.path.join(image_path, self.MAP_DICT[map_name]["img"])),
                                          (600, 400))
        print(self.MAP_DICT[map_name]["img"])

    def extend_route(self, pos):
        """extend current route to the new position(x,y)"""
        x = pos[0]
        y = pos[1]
        last_x = self.route[-1][0]
        last_y = self.route[-1][1]
        li = []
        # looks for all the integer coordinates between route's last coordinate and pos
        # find max (|x - last_x|, |y - last_y|) and use it to find the other
        if abs(x - last_x) >= abs(y - last_y) and not (abs(x - last_x) == 0):
            for i in range(last_x, x, -(last_x - x) // (abs(last_x - x))):
                difference = i - last_x - (last_x - x) // (abs(last_x - x))
                li += [(last_x + difference, round(last_y + (y - last_y) / (x - last_x) * difference))]
        elif abs(x - last_x) < abs(y - last_y) and not (abs(y - last_y) == 0):
            for i in range(last_y, y, -(last_y - y) // abs(last_y - y)):
                difference = i - last_y - (last_y - y) // abs(last_y - y)
                li += [(round(last_x + (x - last_x) / (y - last_y) * difference), last_y + difference)]
        self.route += li

    def makeRoute(self):
        pygame.init()
        running = 1

        screen = pygame.display.set_mode((600, 450))
        while running:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                running = 0

            # pygame.transform.scale(pygame.image.load(os.path.join(image_path, self.MAP_DICT[map_name]["img"])),
            # (600, 400))
            i = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "map/map1.jpg")), (600, 400))
            screen.blit(i, (0, 50))
            # screen.blit(self.img, (0, 50))

            if event.type == pygame.MOUSEBUTTONDOWN:
                # break the game loop if we done inputting routes
                if pygame.mouse.get_pos()[1] < 50:
                    running = 0
                    break
                self.extend_route(pygame.mouse.get_pos())
            pygame.display.flip()
        # save to stats file
        updateRoute(self.map_name, self.route)
        print(self.route)


class Base:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp


class Game:
    def __init__(self):
        self.map = readMap()
        self.tower_list = []
        self.Enemy_list = []

    # def builtTower(self, name, x, y):


enemy1 = Enemy("enemy1", 50, 10)
