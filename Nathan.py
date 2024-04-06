import pygame
from time import sleep
from random import randint

# Initialize pygame
pygame.init()

# Colors
BACKGROUND = (255, 0, 255)
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
BORDER = 10

# Game objects
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

class Target:
    def __init__(self, x, y, width, height, color=(255, 10, 100)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.health = 100
        self.max_health = 100
        self.health_width = 100
        self.isAlive = True
        self.x_dir = 0
        self.y_dir = 1

    def update(self):
        if self.y > WINDOW_HEIGHT - BORDER - self.height or self.y < BORDER:
            self.y_dir *= -1
        self.x += self.x_dir
        self.y += self.y_dir

    def render(self):
        self.update()
        pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (255, 0, 0), (self.x - self.width // 2, self.y - self.height // 2 - 10, self.health_width, 20))
        pygame.draw.rect(screen, (0, 255, 0), (self.x - self.width // 2, self.y - self.height // 2 - 10, self.health_width * self.health / self.max_health, 20))

    def collision_detect(self, obj_x, obj_y, damage):
        if self.x < obj_x < self.x + self.width and self.y < obj_y < self.y + self.height:
            self.health -= damage
            if self.health <= 0:
                self.isAlive = False
            return True
        return False

class Gun:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = 100
        self.max_health = 100
        self.health_width = 100
        self.movement = 5

    def moveUp(self):
        self.y -= self.movement

    def moveDown(self):
        self.y += self.movement

    def render(self):
        pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (255, 0, 0), (self.x - self.width // 2, self.y - self.height // 2 - 10, self.health_width, 20))
        pygame.draw.rect(screen, (0, 255, 0), (self.x - self.width // 2, self.y - self.height // 2 - 10, self.health_width * self.health / self.max_health, 20))

class Ball:
    def __init__(self, x, y, color=(0, 0, 255), dmg=0, lifesteal=False):
        self.x = x + 10
        self.y = y + 25
        self.x_dir = 5
        self.y_dir = 0
        self.color = color
        self.radius = 5
        self.status = True
        self.lifesteal = False
        self.dmg = dmg
        self.lifesteal = lifesteal

    def update(self):
        if self.x > WINDOW_WIDTH - BORDER:
            self.status = False
        self.x += self.x_dir
        self.y += self.y_dir

    def render(self):
        self.update()
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# Game setup
ballList = []
gunObj = Gun(100, 100, 50, 50)
targetObj = Target(400, 150, 30, 100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                ballList.append(Ball(x=gunObj.x, y=gunObj.y, dmg=10))
            elif event.key == pygame.K_w:
                gunObj.y -= 5
            elif event.key == pygame.K_s:
                gunObj.y += 5

    screen.fill(BACKGROUND)

    for ballObj in ballList.copy():
        if targetObj.collision_detect(ballObj.x, ballObj.y, damage=ballObj.dmg):
            ballList.remove(ballObj)
        elif ballObj.status:
            ballObj.render()
        else:
            ballList.remove(ballObj)

    targetObj.render()
    gunObj.render()

    if targetObj.isAlive == False:
        print("You win!")
        pygame.quit()

    sleep(0.01)
    pygame.display.update()
