import pygame
from sys import exit
import random
from random import randint, choice
import numpy as np



class Network(object):

    #initialize neural network with weights and biases and set fitness to 0
    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x) 
                        for x, y in zip(sizes[:-1], sizes[1:])]
        self.fitness = 0

    # sigmoid activation function to normalize values
    def sigmoid(self,z):
        return 1.0/(1.0+np.exp(-z))

    # passes inputs through network and returns output
    def feedforward(self, a):
        for b, w in zip(self.biases, self.weights):
            a = self.sigmoid(np.dot(w, a)+b)
        return np.argmax(a)


#player class
class Player(pygame.sprite.Sprite):
    
    def __init__(self,network):
        super().__init__()
        # Creates necessary properties for the Player
        self.image = pygame.image.load('Assets/Player/tempMonkeyPlayer.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, .5)
        self.rect = self.image.get_rect(midbottom = (200, 600))
        self.gravity = 0
        self.network = network
        self.alive = True
        self.score = 0
        self.timer = 0

    # finds the coordinates of the closest above platform, and the closest below platform, and gives this information as input to the AI along with its gravity
    def getinputAI(self):
        coords = []
        for platform in platform_group:
            coords.append((platform.rect.x-self.rect.x,platform.rect.y-self.rect.y))
        minposy = 3000
        maxnegy = -3000
        xy1 = [0,0]
        xy2 = [0,0]
        for x,y in coords:
            if y>=0:
                if y < minposy:
                    xy1 = [x,y]
                    minposy = y
            else:
                if y > maxnegy:
                    xy2 = [x,y]
                    maxnegy = y
        return [xy1[0],xy1[1],xy2[0],xy2[1],self.gravity]

    # Creates keys which can move the player to the right or left
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.centerx -= 6
        if keys[pygame.K_RIGHT]:
            self.rect.centerx += 6
        # Used by AI to move right or left
        if self.key == 0:
            self.rect.centerx -= 6
        elif self.key == 2:
            self.rect.centerx += 6

    # Keeps the player on the screen and kills the player if he falls down
    def player_parameters(self):
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > 400: self.rect.right = 400
        if self.rect.top > 800:
            self.network.fitness = self.score
            self.alive = False

    # Moves the screen downward if the player reaches halfway up the screen
    def apply_gravity(self):
        self.gravity += .3
        if self.rect.y>400 or self.gravity > 0:
            self.rect.y += self.gravity
        else:
            # If the player is above the half point, it will be moved just below the half point
            self.rect.y = 399

    # Kills player if it doesn't move upward for too long
    def idle(self):
        self.timer+=1
        if self.timer>420:
            self.network.fitness = self.score
            self.alive = False
    
    #applies functions and finds key to press based on AI
    def update(self):
        self.player_parameters()
        self.apply_gravity()
        self.key = self.network.feedforward(self.getinputAI())        
        self.player_input()
        self.idle()
        


class Platform(pygame.sprite.Sprite):
    def __init__(self,type,ycoord):
        super().__init__()
        self.type = type
        # type "moving" can move left OR right, rather than having all of them move in the same direction
        self.velocity = choice([3,-3])
        # creating the different types of platforms
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
            self.rect = self.image.get_rect(center = (randint(100,300), ycoord))

    # moves the "moving" platforms to the right or left while in certain screen parameters
    def movex(self):
        if self.type == "moving":
            self.rect.x += self.velocity
            if self.rect.x > 340 or self.rect.x < 20:
                # switches direction of platform after it touches the edge
                self.velocity *= -1

    # if the player is above the half point while still moving upward, the platforms will move downward, making it look like the screen is moving upward
    def movey(self):
        if player.sprite.rect.y<400 and player.sprite.gravity<0:
            self.rect.y-=player.sprite.gravity
            player.sprite.score-=player.sprite.gravity/100
            if player.sprite.gravity<-2:
                player.sprite.timer = 0
        if self.rect.y > 800:
            self.kill()

    # custom collision fuction to make it so a collision will only be counted if the bottom of the Player touches a Platform
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

    #applies functions
    def update(self):
        self.movex()
        self.movey()
        self.touch()
            
#initialization of basic pygame elements such as background, font, clock, display, and sprite groups
pygame.init()
screen = pygame.display.set_mode((400, 800))
clock = pygame.time.Clock()
pygame.display.set_caption('Doo-Doo Jump')
background = pygame.image.load('Assets/Background/tempBackground.png').convert_alpha()
player = pygame.sprite.GroupSingle()
platform_group = pygame.sprite.Group()
topplat = Platform("normal", 650)
test_font = pygame.font.Font(None,50)


#resets the game
def reset_game():
    player.empty()
    platform_group.empty()
    platform_group.add(topplat)

#neural network functions----------------------------------------------------

#selects the top 15 networks from the last generation
def selection(networks):
    bob = networks
    bob.sort(key=lambda network: network.fitness, reverse = True)
    topnets = bob[:15]
    return topnets

#takes two parent matrices and switches some genes to make two child matrices
def mcrossover(w1, w2, b1, b2):
    s = w1.shape
    m1 = w1.flatten()
    m2 = w2.flatten()
    n = m1.size
    newm1 = np.empty(n)
    newm2 = np.empty(n)
    newb1 = np.empty(b1.size)
    newb2 = np.empty(b1.size)
    r = randint(0,n-1)
    y = r/s[1]
    if y%1 != 0:
        bruh = random.random()
        if bruh>.5: y+=1
    y = int(y)
    for i in range(r):
        newm1[i] = m1[i]
        newm2[i] = m2[i]
    for i in range(r, n):
        newm1[i] = m2[i]
        newm2[i] = m1[i]
    for i in range(y):
        newb1[i] = b1[i]
        newb2[i] = b2[i]
    for i in range(y, b1.size):
        newb1[i] = b2[i]
        newb2[i] = b1[i]
    return [newm1.reshape(s),newm2.reshape(s),newb1,newb2]

#mutates a neural network by changing 5% of the values to new random numbers
def mutate(net):
    mrate = .05
    netc = Network(net.sizes)
    for i in range(2):
        netc.weights[i] = net.weights[i]
        netc.biases[i] = net.biases[i]

    for i in netc.biases:
        for j in range(len(i)):
            if random.random()<mrate:
                i[j] = np.random.randn()
    for i in netc.weights:
        for j in range(i.shape[0]):
            for k in range(i.shape[1]):
                if random.random()<mrate:
                    i[j,k] = np.random.randn()
    return netc    

#uses matrix crossover function to create two child neural networks from two parent networks
def ncrossover(net1,net2):
    child1 = Network([5,8,3])
    child2 = Network([5,8,3])
    for i in range(2):
        a = mcrossover(net1.weights[i],net2.weights[i],net1.biases[i],net2.biases[i])
        child1.weights[i] = a[0]
        child2.weights[i] = a[1]
        child1.biases[i] = a[2]
        child2.biases[i] = a[3]
    return [child1,child2]

#created new population bases on old population -- makes the best networks have children that move on to the next generation
def newpop(oldpop):
    NNs = []
    for i in range(20):
        NNs.append(Network([5,8,3]))
    topnets = selection(oldpop)
    for i in range(20):
        n1 = choice(topnets)
        n2 = choice(topnets)
        b = ncrossover(n1,n2)
        NNs.append(b[0])
        NNs.append(b[1])
    NNs.extend(topnets)
    for i in range(20,len(NNs)):
        NNs[i] = mutate(NNs[i])
    NNs.extend(topnets)
    return NNs

# --------------------------------------------------------------------------------

#main execution code----------------------------------------------------------------
gen = 0
NNs = []

#adds 100 random neural networks
for i in range(100):
    NNs.append(Network([5,8,3]))

# game loop
while True:
    print("Gen: " + str(gen))
    for nn in NNs:
        topplat = Platform("normal", 650)
        topplat.rect.centerx = 200
        reset_game()
        player.add(Player(nn))
        while player.sprite.alive:
            clock.tick(900) # sets game speed -- can change to train faster
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Drawing everything onto the screen
            screen.blit(background, (0,0))
            player.draw(screen)
            player.update() # updates player with movement and AI
            score_surf = test_font.render(f'{int(player.sprite.score)}', False, (64, 64, 64))
            score_rect = score_surf.get_rect(center = (200, 50))
            if topplat.rect.bottom>20: # generates new platforms as the platforms move down
                topplat = Platform(choice(["normal"]), topplat.rect.bottom - randint(50,90))
                platform_group.add(topplat)
            platform_group.draw(screen)
            screen.blit(score_surf, score_rect)
            platform_group.update() # updates platforms

            pygame.display.update() # updates main display
    gen+=1
    NNs = newpop(NNs)
    