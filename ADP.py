import pygame


class Tower:
    def __init__(self, name, image, cost, attack, attack_speed, r):
        self.name = name
        self.image = image
        self.cost = cost
        self.attack = attack
        self.attackSpeed = attack_speed
        self.range = r


class Enemy:
    def __init__(self, name, image, speed, hp):
        self.name = name
        self.image = image
        self.speed = speed
        self.hp = hp


class Map:
    def __init__(self, name, image):
        self.name = name
        self.image = image

tower1 = Tower("normal tower", "venv/image/tower/tower1.jpg", 10, 2, 2, 180)
enemy1 = Enemy("Monster", "venv/image/enemy/enemy1.jpg", 50, 10)