import pygame
import math
from ADP import *



# activate the pygame library
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()

# Initializing global variables
running = 1
screen = pygame.display.set_mode((600, 450))

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

gold = 100
pygame.display.set_caption("Tower Defence")
font = pygame.font.Font('freesansbold.ttf', 17)
font_tower_cost = pygame.font.Font('freesansbold.ttf', 7)
text = font.render('Gold: '+str(gold), True, green, blue)
text_cost = font_tower_cost.render('30', True, green, blue)
costRect = text_cost.get_rect()
costRect.center = (40, 5)
goldRect = text.get_rect()
goldRect.center = (500, 20)
speed = 20

interface = pygame.Rect(0, 0, 600, 50)

# introducing time makes game running
time = pygame.time.Clock()
enemy_timer = 5000  # /1000 = seconds

base = Base(100)
game = Game(base)
game.add_enemy("enemy1",-5,266)
building = False

# Game loop
while running:
    # background image displayed
    event = pygame.event.poll()

    if event.type == pygame.QUIT:
        running = 0
        print("you win!")


    # create the map
    screen.fill((0, 0, 0))
    #screen.blit(image, (0, 50))

    # create the building interface
    pygame.draw.rect(screen, (255, 255, 255, 255), interface)
    screen.blit(pygame.transform.scale(pygame.image.load(
        os.path.join(image_path, "tower/tower1.jpg")), (35, 35)), (5, 5))
    screen.blit(font.render('50', True, green, (0, 0, 0)), costRect)
    ticks = time.tick(15)

    game.tick(screen)

    if event.type == pygame.MOUSEBUTTONDOWN:
        # when we want to build a tower:
        if (5 <= pygame.mouse.get_pos()[0] <= 45) and (5 <= pygame.mouse.get_pos()[1] <= 45):
            # building phase is on, then there is a tower image goes along with the pointer
            building = True
    if building:
        building = not(game.building(event, screen, "tower1", building))


    # let each tower find its enemy and attack
    for t in range(0, 0):
        # tower: [float x, float y, bool have_target, enemy_key target]
        this_tower = tower_dict[t]
        tx = this_tower[0]
        ty = this_tower[1]
        screen.blit(tower, (tx-25, ty-25))
        if len(this_tower) > 3 and this_tower[3] in defeated:
            this_tower = (tx, ty, False)
        # if the tower doesn't have a enemy to hit now, look for an enemy
        if not(this_tower[2]):
            for e in enemy_dict.keys():
                this_enemy = enemy_dict[e]
                if in_range((this_enemy[0], this_enemy[1]), (tx+25, ty+25), 180) and e not in defeated:
                    tower_dict[t] = (tx, ty, True, e)
        else:
            # find it's enemy
            if this_tower[3] not in defeated:
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
                    if hp2 <= 0:
                        # Add defeated enemy to defeated list
                        defeated += [this_tower[3]]
                        # killing enemy gives gold
                        gold += 20

                else:
                    enemy_dict[this_tower[3]] = enemy_dict[this_tower[3]][0], enemy_dict[this_tower[3]][1], hp2

    # display rect at certain pos
    # pygame.draw.rect(serface=screen, color=1, rect=a, width=5)

    # Display gold
    screen.blit(font.render('Gold: ' + str(game.gold), True, green, blue), goldRect)

    pygame.display.flip()