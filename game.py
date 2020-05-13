import pygame
import math
import ADP

# Initializing global variables
running = 1
screen = pygame.display.set_mode((600, 450))

gold = 100

speed = 20


# function that move some coordinates at constant speed.
def move_enemy(ticks, alpha):  # alpha is variable that adjust the speed when there is multiple enemy
    return float(speed) * ticks * float(alpha) / 1000


# Function that checks if object1 with coordinate p1 is in the attack range of object2 with coordinate p2 and range r
def in_range(p1, p2, r):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1]) < r


# Attack that reduce enemy's health
def attack(hp, ticks):
    return hp - float(attackSpeed) * ticks / 1000


# create enemy and tower image using the resized pic
enemy = pygame.transform.scale(pygame.image.load("venv/image/enemy/enemy1.jpg"), (50, 50))
tower = pygame.transform.scale(pygame.image.load("venv/image/tower/tower1.jpg"), (50, 50))
base = pygame.transform.scale(pygame.image.load("venv/image/tower/base.jpg"), (50, 50))
image = pygame.transform.scale(pygame.image.load("venv/image/map/map1.jpg"), (600, 400))
interface = pygame.Rect(0, 0, 600, 50)

# introducing time makes game running
time = pygame.time.Clock()
ticks = 0

# stats of the enemy, (x,y) is initial pos. hp is health
x_ini = -10
y_ini = 271
hp_ini = 10
enemy_count = 2
enemy_dict = {"enemy1": (x_ini, y_ini, hp_ini), "enemy2": (x_ini-100, y_ini, hp_ini)}


# stats of the tower,
tower_x = 0
tower_y = 0
attackSpeed = 2
ammoSpeed = 10
has_target = False  # If the tower has enemy in range or not
building = False
tower_dict = {}
tower_count = 1
attackTimer = 1

# Game loop
while running:
    # background image displayed
    event = pygame.event.poll()

    if event.type == pygame.QUIT:
        running = 0

    if event.type == pygame.MOUSEBUTTONDOWN:
        # when we want to build a tower:
        if (5 <= pygame.mouse.get_pos()[0] <= 45) and (5 <= pygame.mouse.get_pos()[1] <= 45):
            # building phase is on, then there is a tower image goes along with the pointer
            building = True
        print(pygame.mouse.get_pos())

    # create the map
    screen.fill((0, 0, 0))
    screen.blit(image, (0, 50))

    # create the building interface
    pygame.draw.rect(screen, (255, 255, 255, 255), interface)
    screen.blit(pygame.transform.scale(tower, (40, 40)), (5, 5))
    ticks = time.tick(30)

    for e in enemy_dict.keys():
        x = enemy_dict[e][0]
        y = enemy_dict[e][1]
        hp = enemy_dict[e][2]
        # make the enemy move along the route
        if (x < 100 and y == 271) or (y <= 154 and x < 219) or (219 < x < 379 and y >= 305) or (x >= 379 and y < 227):
            x += move_enemy(ticks, enemy_count)
        elif (y > 154 and x < 219) or (x > 379 and y < 315):
            y -= move_enemy(ticks, enemy_count)
        else:
            y += move_enemy(ticks, enemy_count)
        enemy_dict[e] = x, y, hp
        # create enemy and base. Enemy can move at a constant speed
        screen.blit(enemy, (x-25, y-25))
    screen.blit(base, (596-50, 228-25))

    # when in building phase
    if building:
        screen.blit(tower, (pygame.mouse.get_pos()[0]-25, pygame.mouse.get_pos()[1]-25))
        # shows the hit range of the tower
        pygame.draw.circle(screen, 1, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), 180, 2)
        # when click on good location in building phase, the tower is built.
        if (event.type == pygame.MOUSEBUTTONDOWN) and (pygame.mouse.get_pos()[1] > 50):
            # quit building phase
            building = False
            # store the tower information in tower_dict
            tower_dict["tower"+str(tower_count)] = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], False
            tower_count += 1

    # let each tower find its enemy and attack
    for t in tower_dict.keys():
        # tower: [float x, float y, bool have_target, enemy_key target]
        this_tower = tower_dict[t]
        tx = this_tower[0]
        ty = this_tower[1]
        screen.blit(tower, (tx-25, ty-25))
        # if the tower doesn't have a enemy to hit now, look for an enemy
        if not(this_tower[2]):
            for e in enemy_dict.keys():
                this_enemy = enemy_dict[e]
                if in_range((this_enemy[0], this_enemy[1]), (tx+25, ty+25), 180):
                    tower_dict[t] = (tx, ty, True, e)
        else:
            # find it's enemy
            this_towers_enemy = enemy_dict[this_tower[3]]
            hp2 = this_towers_enemy[2]
            # recreate a ammo when the last hit the target
            if attackTimer == ammoSpeed:
                attackTimer = 1
                # attack action has two steps: 1 reduce health, 2 show ammo motion
                hp2 = hp2 - 0.7

            # draw ammo
            pygame.draw.rect(screen, 100, pygame.Rect(tx-5+(this_towers_enemy[0]-tx)*attackTimer/ammoSpeed, ty-5+(this_towers_enemy[1]-ty) * attackTimer /
                                                      ammoSpeed, 10, 10), 10)
            # increase attackTimer so that the ammo can move along the line
            attackTimer += 1

            pygame.draw.line(screen, 1, (tx, ty), (this_towers_enemy[0], this_towers_enemy[1]), 2)
            # when the enemy is out of range or the enemy is dead, remove the enemy from the dict
            if hp2 < 0 or not(in_range((this_towers_enemy[0], this_towers_enemy[1]), (tx+25, ty+25), 180)):
                tower_dict[t] = (tx, ty, False)
                # if the enemy is dead, remove it from all towers' targets.
                if hp2 < 0:
                    # remove enemy from the dict
                    del enemy_dict[this_tower[3]]
                    for any_tower in tower_dict.keys():
                        if tower_dict[any_tower][2] is True:
                            if tower_dict[any_tower][3] == [this_towers_enemy]:
                                tower_dict[any_tower] = tower_dict[any_tower][0], tower_dict[any_tower][1], False
            else:
                enemy_dict[this_tower[3]] = enemy_dict[this_tower[3]][0], enemy_dict[this_tower[3]][1], hp2


    if x > 600:
        print("you lose!")
        running = 0
    # display rect at certain pos
    # pygame.draw.rect(serface=screen, color=1, rect=a, width=5)

    pygame.display.flip()