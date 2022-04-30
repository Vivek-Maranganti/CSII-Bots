import pygame
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('Assets/Player/tempMonkeyPlayer.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (200, 400))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        pass

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity

    def update(self):
        self.player_input()
        self.apply_gravity()


class Obstacles(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Assets/Obstacles/PlatformNormal.png')
        self.rect = self.image.get_rect(center = (200, 650))

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False) and player.sprite.gravity > 0:
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

obstacle_group = pygame.sprite.Group()
obstacle_group.add(Obstacles())


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
    obstacle_group.draw(screen)
    obstacle_group.update()

    pygame.display.update()