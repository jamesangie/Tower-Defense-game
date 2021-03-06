import pygame
from Exception import *
import math
from stats_IO import *


class Tower:
    ATTACK_TIMER = 0

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
            if math.hypot(self.x - enemy.x, self.y - enemy.y) < self.range:
                self.target = enemy

    def attack(self, target_enemy, game):
        if self.ATTACK_TIMER % self.attackSpeed == 0:
            target_enemy.hp -= self.ATT
        if target_enemy.hp <= 0:
            target_enemy.isDead = True
            self.target = False
            game.gold += target_enemy.gold_drop
        elif math.hypot(self.x - target_enemy.x, self.y - target_enemy.y) < self.range:
            self.target = False
        self.ATTACK_TIMER += 1


    def draw(self, screen):
        screen.blit(self.img, (self.x - 25, self.y - 25))


class Enemy:
    # name: [speed, hp, gold_drop]
    ENEMY_DICT = readEnemy()

    def __init__(self, name, x, y):
        self.name = name
        self.speed = self.ENEMY_DICT[name]["speed"]
        self.img = pygame.transform.scale(pygame.image.load(os.path.join(image_path, self.ENEMY_DICT[name]["img"])),
                                          (50, 50))
        self.hp = self.ENEMY_DICT[name]["hp"]
        self.gold_drop = self.ENEMY_DICT[name]["gold_drop"]
        self.isDead = False
        self.tick = 0
        self.x = x
        self.y = y

    def move(self, the_map):
        self.tick += 1
        if len(the_map.route) <= self.tick * self.speed:
            self.isDead = True
        else:
            self.x = the_map.route[self.tick * self.speed][0]
            self.y = the_map.route[self.tick * self.speed][1]

    def draw(self, screen):
        screen.blit(self.img, (self.x - 25, self.y - 25))


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
                li += [[last_x + difference, round(last_y + (y - last_y) / (x - last_x) * difference)]]
        elif abs(x - last_x) < abs(y - last_y) and not (abs(y - last_y) == 0):
            for i in range(last_y, y, -(last_y - y) // abs(last_y - y)):
                difference = i - last_y - (last_y - y) // abs(last_y - y)
                li += [[round(last_x + (x - last_x) / (y - last_y) * difference), last_y + difference]]
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

            screen.blit(self.img, (0, 50))

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

    def draw(self, screen):
        screen.blit(self.img, (0, 50))


class Base:
    def __init__(self, hp):
        self.img = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "tower/base.jpg")), (50, 50))
        self.hp = hp

    def draw(self, screen, x, y):
        screen.blit(self.img, (x, y))


class Game:
    STATS = readStats()
    TICK = 0

    def __init__(self, base):
        self.map = Map("map1")
        self.towers = []
        self.enemies = []
        self.hp = base.hp
        self.base = base
        self.gold = 100

    def add_tower(self, tower_name, x, y):
        tower = Tower(tower_name, x, y)
        self.towers += [tower]

    def add_enemy(self, enemy_name, x, y):
        self.enemies += [Enemy(enemy_name, x, y)]

    # the method we call on every frame to run the game
    def tick(self, screen):
        self.map.draw(screen)

        for tower in self.towers:
            if not tower.target:
                tower.find_target(self.enemies)
            if tower.target != False:
                pygame.draw.line(screen, 1, (tower.x, tower.y), (tower.target.x, tower.target.y), 2)
                tower.attack(tower.target, self)
            tower.draw(screen)
        for enemy in self.enemies:
            if not enemy.isDead:

                enemy.move(self.map)
                enemy.draw(screen)
        self.base.draw(screen, self.map.route[-1][0], self.map.route[-1][1])
        self.TICK += 1

    def check_winning(self):
        for enemy in self.enemies:
            if not enemy.isDead:
                return False

    def check_lost(self):
        if self.hp <= 0:
            return True

    def building(self, event, screen, tower_name, building):
        if building and self.gold >= self.STATS["tower"][tower_name]["cost"]:
            tower = pygame.transform.scale(pygame.image.load(os.path.join(image_path,
                                                                          self.STATS["tower"][tower_name]["img"])),
                                           (50, 50))
            screen.blit(tower, (pygame.mouse.get_pos()[0] - 25, pygame.mouse.get_pos()[1] - 25))
            # shows the hit range of the tower
            pygame.draw.circle(screen, 1, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]),
                               self.STATS["tower"][tower_name]["range"], 2)
            # when click on good location in building phase, the tower is built.
            if (event.type == pygame.MOUSEBUTTONDOWN) and (pygame.mouse.get_pos()[1] > 50):
                # store the tower information in towers
                self.towers += [Tower(tower_name, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])]
                self.gold -= self.STATS["tower"][tower_name]["cost"]
                return True
            return False
        return True


enemy1 = Enemy("enemy1", 50, 10)
