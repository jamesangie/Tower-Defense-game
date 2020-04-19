import pygame
import math

running = 1
screen = pygame.display.set_mode((600, 400))

speed = 50
# function that move some coordinates at constant speed.
def update_object(ticks):
    return (float(speed) * ticks / 1000)



# a = pygame.Rect(50, 100, 50, 50)
# create enemy and tower image using the resized pic
enemy = pygame.transform.scale(pygame.image.load("venv/image/enemy/enemy1.jpg"), (50, 50))
tower = pygame.transform.scale(pygame.image.load("venv/image/tower/tower1.jpg"), (50, 50))

# introduce time to make the objects move at constant speed
time = pygame.time.Clock()
ticks = 0

# stats of the enemy, x is the initial pos. hp is health
x = 10
hp = 10



while running:
    # background image displayed
    event = pygame.event.poll()
    image = pygame.image.load("venv/image/map/map2.jpg")
    if event.type == pygame.QUIT:
        running = 0

    if event.type == pygame.MOUSEBUTTONDOWN:
        print(pygame.mouse.get_pos())


    # create the map
    screen.fill((0, 0, 0))
    screen.blit(image, (0, 0))

    # make the enemy move
    ticks = time.tick(30)
    x += update_object(ticks)

    # create enemy and tower. Enemy can move at a constant speed
    screen.blit(enemy, (x, 150))
    screen.blit(tower, (259, 253))

    # hit range of the tower
    pygame.draw.circle(screen, 1, (283, 284), 180, 2)

    # check if tower can hit the enemy
    if math.hypot(x-283, 150-284) < 180:
        print("we meet the enemy! Attack!!!")

    if x > 539:
        print("you lose!")
        running = 0
    # display rect at certain pos
    # pygame.draw.rect(serface=screen, color=1, rect=a, width=5)


    pygame.display.flip()