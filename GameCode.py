import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Assets/Player/tempMonkeyPlayer.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, .5)
        self.rect = self.image.get_rect(midbottom = (200, 600))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.centerx -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.centerx += 5

    def player_parameters(self):
        if self.rect.right < 0: self.rect.left = 400
        if self.rect.left > 400: self.rect.right = 0

    def apply_gravity(self):
        self.gravity += .3
        if self.rect.y>400 or self.gravity > 0:
            self.rect.y += self.gravity
        else:
            self.rect.y = 399

    def update(self):
        self.player_parameters()
        self.player_input()
        self.apply_gravity()


class Platform(pygame.sprite.Sprite):
    def __init__(self,type,ycoord):
        super().__init__()
        self.type = type
        self.velocity = choice([3,-3])
        if type=="normal":
            self.image = pygame.image.load('Assets/Obstacles/PlatformNormal.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image, 0, .4)
            self.rect = self.image.get_rect(center = (randint(25,370), ycoord))
        elif type=="broken":
            self.image = pygame.image.load('Assets/Obstacles/BreakPlatform.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image, 0, .4)
            self.rect = self.image.get_rect(center = (randint(20, 370), ycoord))
        else:
            self.image = pygame.image.load('Assets/Obstacles/MovingPlatform.png').convert_alpha()
            self.image = pygame.transform.rotozoom(self.image, 0, .4)
            self.rect = self.image.get_rect(center = (200, ycoord))

    def movex(self):
        if self.type == "moving":
            self.rect.x += self.velocity
            if self.rect.x > 340 or self.rect.x < 20:
                self.velocity *= -1

    def movey(self):
        if player.sprite.rect.y<400 and player.sprite.gravity<0:
            self.rect.y+=-player.sprite.gravity

    def touch(self):
        leftx =  player.sprite.rect.left
        rightx = player.sprite.rect.right
        centerx = player.sprite.rect.centerx
        bottomy = player.sprite.rect.bottom
        colly = self.rect.bottom+5>bottomy and self.rect.top-5<bottomy
        collx = (centerx > self.rect.left and centerx < self.rect.right) or (rightx > self.rect.left and rightx < self.rect.right) or (leftx > self.rect.left and leftx < self.rect.right)
        if collx and colly and player.sprite.gravity > 0:
            player.sprite.gravity = -10
            if self.type == "broken":
                self.kill()

    def update(self):
        self.movex()
        self.movey()
        self.touch()
            


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
topplat = Platform("normal", 650)
topplat.rect.center = (200,650)
platform_group.add(topplat)




while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
    Background()
    # collision_sprite()
    player.draw(screen)
    player.update()
    if topplat.rect.bottom>20:
        topplat = Platform(choice(["normal", "normal", "normal", "normal", "broken", "moving"]), topplat.rect.bottom - randint(50,120))
        platform_group.add(topplat)
    platform_group.draw(screen)
    platform_group.update()

    pygame.display.update()