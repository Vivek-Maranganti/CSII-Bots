import pygame
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('Assets/Player/tempMonkeyPlayer.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (200, 400))
        self.gravity = 0
        self.rightAccelaration = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            while self.rightAccelaration < 15:
                self.rightAccelaration += 1
            self.rect.x += self.rightAccelaration
            if self.rect.x > 400:
                self.rect.x = 0
        else: self.rightAccelaration = 0

        if keys[pygame.K_LEFT]:
            while self.rightAccelaration > -15:
                self.rightAccelaration -= 1
            self.rect.x += self.rightAccelaration
            if self.rect.x < 0:
                self.rect.x = 400
        else: self.rightAccelaration = 0


    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity

    def update(self):
        self.player_input()
        self.apply_gravity()


class Platforms(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Assets/Obstacles/PlatformNormal.png')
        self.rect = self.image.get_rect(center = (200, 650))

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, platform_group, False) and player.sprite.gravity > 0:
        player.sprite.gravity -= (player.sprite.gravity + 27)

def Background():
    background = pygame.image.load('Assets/Background/tempBackground.png').convert_alpha()
    screen.blit(background, (0,0))


pygame.init()
screen = pygame.display.set_mode((400, 800))
clock = pygame.time.Clock()
pygame.display.set_caption('Doo-Doo Jump')

player = pygame.sprite.GroupSingle()
player.add(Player())

platform_group = pygame.sprite.Group()
platform_group.add(Platforms())


while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
    Background()
    collision_sprite()
    player.draw(screen)
    player.update()
    platform_group.draw(screen)
    platform_group.update()

    pygame.display.update()