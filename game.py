import pygame
import math
import ADP


running = 1
screen = pygame.display.set_mode((600, 450))

speed = 50

gold = 100


# function that move some coordinates at constant speed.
def move_enemy(ticks):
    return float(speed) * ticks / 1000


attackSpeed = 0

ammoSpeed = 10

a = pygame.Rect(100, 50, 0, 0)


# Function that checks if object1 with coordinate p1 is in the attack range of object2 with coordinate p2 and range r
def in_range(p1, p2, r):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1]) < 180


def attack(hp, ticks):

    return hp - float(attackSpeed) * ticks / 1000


# a = pygame.Rect(50, 100, 50, 50)
# create enemy and tower image using the resized pic
enemy = pygame.transform.scale(pygame.image.load("venv/image/enemy/enemy1.jpg"), (50, 50))
tower = pygame.transform.scale(pygame.image.load("venv/image/tower/tower1.jpg"), (50, 50))
base = pygame.transform.scale(pygame.image.load("venv/image/tower/base.jpg"), (50, 50))
# introduce time to make the objects move at constant speed
time = pygame.time.Clock()
ticks = 0

# stats of the enemy, x is initial pos. hp is health
x = -10
y = 271
hp = 10

attackTimer = 1

while running:
    # background image displayed
    event = pygame.event.poll()
    image = pygame.transform.scale(pygame.image.load("venv/image/map/map1.jpg"), (600, 400))
    if event.type == pygame.QUIT:
        running = 0

    if event.type == pygame.MOUSEBUTTONDOWN:
        print(pygame.mouse.get_pos())

    pygame.draw.rect(screen, 0, a, 10)

    # create the map
    screen.fill((0, 0, 0))
    screen.blit(image, (0, 50))

    # make the enemy move along the route
    ticks = time.tick(30)
    if (x < 100 and y == 271) or (y <= 154 and x < 219) or (219 < x < 379 and y >= 305) or (x >= 379 and y < 227):
        x += move_enemy(ticks)
    elif (y > 154 and x < 219) or (x > 379 and y < 315):
        y -= move_enemy(ticks)
    else:
        y += move_enemy(ticks)
    #print(x, y)

    # create enemy base and tower. Enemy can move at a constant speed
    screen.blit(enemy, (x-25, y-25))
    screen.blit(tower, (259, 253))
    screen.blit(base, (596, 228))

    # hit range of the tower
    pygame.draw.circle(screen, 1, (283, 284), 180, 2)

    # check if tower can hit the enemy
    if in_range((x, 175), (283, 284), 180):
        # attack action has two steps: 1 reduce health, 2 show ammo motion
        hp = attack(hp, ticks)
        # recreate a ammo when the last hit the target
        if attackTimer == ammoSpeed:
            attackTimer = 1
        # draw ammo
        pygame.draw.rect(screen, 100, pygame.Rect(283-5+(x-283)*attackTimer/ammoSpeed, 284-5+(y-284)
                                                  * attackTimer / ammoSpeed, 10, 10), 10)
        # increase attackTimer so that the ammo can move along the line
        attackTimer += 1

        pygame.draw.line(screen, 1, (283, 284), (x, y), 2)
        if hp < 0:
            print("you win!")
            running = 0

    if x > 600:
        print("you lose!")
        running = 0
    # display rect at certain pos
    # pygame.draw.rect(serface=screen, color=1, rect=a, width=5)

    pygame.display.flip()