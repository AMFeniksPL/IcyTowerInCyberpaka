import pygame
from pygame.locals import *
import random

class Platform:
    image = pygame.image.load("Platform.png")
    counter = 0

    def __init__(self, x, y):
        Platform.counter += 1
        self.x = x
        self.y = y
        self.image = pygame.image.load("Platform.png")

        if Platform.counter % 10 == 0:
            self.image = pygame.transform.scale(pygame.image.load("Platform.png"), (SCREEN_WIDTH, self.image.get_height()))
            self.x = 0

        self.Rect = Rect(self.x, self.y, self.image.get_width(), self.image.get_height() / 3)
        Platform.counter += 1

    def draw(self):
        screen.blit(self.image, (self.x + offsetX, self.y + offsetY))


# Rozpoczyna działanie PyGame
pygame.init()

# Dzięki tym dwóm linijkom mamy stałe 60 klatek na sekundę;
clock = pygame.time.Clock()
fps = 60

# Parametry okna zapisane do zmiennych:
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Gierka')


# Ładowanie obrazków do gry;

# ZMIENNE GRACZA
playerX = SCREEN_WIDTH/2
playerY = SCREEN_HEIGHT/2

playerVelocityX = 0
playerVelocityY = 0

hero = pygame.image.load('Hero.png')
playerRect = Rect(playerX, playerY, hero.get_width(), hero.get_height())
canJump = False

platformList = []
for i in range(500):
    posX = random.randint(10, SCREEN_WIDTH - Platform.image.get_width() - 10)
    posY = 400 - 100 * i
    platformList.append(Platform(posX, posY))



offsetX = 0
offsetY = 0


run = True
while run:

    # Zegar gry
    clock.tick(fps)

    keys = pygame.key.get_pressed()
    if keys[K_UP] and canJump:
        playerVelocityY = - (10 + 0.7 * abs(playerVelocityX))
        canJump = False
    if keys[K_LEFT]:
        playerVelocityX -= 1
    if keys[K_RIGHT]:
        playerVelocityX += 1
    if keys[K_w]:
        offsetY += 3

    # Dodanie siły grawitacji do gry;
    playerVelocityY += 0.5
    print(playerVelocityY)

    # Dodanie siły oporu:
    playerVelocityX *= 0.98
    playerVelocityY *= 0.98

    playerX += playerVelocityX
    playerY += playerVelocityY



    # Sprawdzanie, czy gracz nie wyszedł poza ekran;
    if playerX < 0:
        playerX = 0
        playerVelocityX *= -1

    if playerX > SCREEN_WIDTH - hero.get_width():
        playerX = SCREEN_WIDTH - hero.get_width()
        playerVelocityX *= -1

    if playerY > SCREEN_HEIGHT - hero.get_height():
        playerY = SCREEN_HEIGHT - hero.get_height()
        playerVelocityY = 0
        canJump = True



    # Kolizje platformy i gracza
    playerRect = Rect(playerX, playerY, hero.get_width(), hero.get_height())


    for platform in platformList:
        if playerRect.colliderect(platform.Rect) and playerVelocityY > 0:
            playerY = platform.y - hero.get_height()
            playerVelocityY = 0
            playerVelocityX *= 0.95
            canJump = True

    offsetY += 1


    if playerY + offsetY < 250:
        offsetY += abs(playerY + offsetY - 250)/30

    if playerY + offsetY > SCREEN_HEIGHT:
        run = False

    # Rysowane obiektów na ekranie
    screen.fill((0, 0, 30))
    screen.blit(hero, (playerX + offsetX, playerY + offsetY))

    for platform in platformList:
        platform.draw()


    # To jest TURBOWAŻNE I NIE USUWAJ TEGO!!!
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    # To tworzy nową klatkę gry; :)
    pygame.display.update()

pygame.quit()