import pygame


class Tower:
    def __init__(self, name, image, cost, attack, r):
        self.name = name
        self.image = image
        self.cost = cost
        self.attack = attack
        self.attackSpeed = attackSpeed
        self.range = r


class Enemy:
    def __init__(self, name, image, speed, hp):
        self.name = name
        self.image = image
        self.speed = speed
        self.hp = hp

