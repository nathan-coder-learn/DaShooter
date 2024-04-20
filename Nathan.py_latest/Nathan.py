import pygame
from time import sleep
from random import randint

# Initialize pygame
pygame.init()

# Colors
BACKGROUND = (255, 0, 255)
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500
BORDER = 10
x = 1
gun = 0
cont = 0
contour = 100
def_contour = 100
sound1 = pygame.mixer.Sound("impact-152508.mp3")
state = 'start'
# Game objects
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
status = "Nutin'"
dmg_dealt = 0
bolt = 0
conti = 0
shoots = 0
successful_shots = 0
accuracy = 'NIL'
class Target:
    def __init__(self, x, y, width, height, color=(255, 10, 100)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.max_health = 5000
        self.health = self.max_health
        self.health_width = 100
        self.isAlive = True
        self.x_dir = 0
        self.y_dir = 1
        self.count = 100
        self.index = 1

    def update(self):
        if self.y > WINDOW_HEIGHT - BORDER - self.height or self.y < BORDER:
            self.y_dir *= -1
        self.x += self.x_dir
        self.y += self.y_dir

    def render(self):
        self.update()
        self.count -= 1 # DECREASE COUTN
        pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (255, 0, 0), (self.x - self.width // 2, self.y - self.height // 2 - 10, self.health_width, 20))
        pygame.draw.rect(screen, (0, 255, 0), (self.x - self.width // 2, self.y - self.height // 2 - 10, self.health_width * (self.health / self.max_health), 20))

    def collision_detect(self, obj_x, obj_y, damage):
            if self.x < obj_x < self.x + self.width and self.y < obj_y < self.y + self.height:
                self.health -= damage
                if self.health <= 0:
                    self.isAlive = False
                return True
            return False
    def rebirth(self):
        self.index += 0.5
        self.max_health = self.max_health*self.index
        self.health = self.max_health
        self.isAlive = True
class Gun:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = 200
        self.max_health = 200
        self.health_width = 100
        self.movement = 5
        self.hisAlive = True
        self.bomb_count = 0
        self.bomb = 0
        self.nukes = 0

    def moveUp(self):
        self.y -= self.movement

    def moveDown(self):
        self.y += self.movement

    def increaseHealth(self):
        self.health = self.max_health

    def render(self):
        pygame.draw.rect(screen, (100, 100, 100), (self.x, self.y, self.width, self.height)) # RED
        pygame.draw.rect(screen, (255, 0, 0), (self.x - self.width // 2, self.y - self.height // 2 - 10, self.health_width, 20)) # GREEN
        pygame.draw.rect(screen, (0, 255, 0), (self.x - self.width // 2, self.y - self.height // 2 - 10, self.health_width * self.health / self.max_health, 20))

        if self.health <self.max_health:
            self.health += 0.03

        # BOMB
        self.bomb_count += 1
        if self.bomb_count >= 1500:
            self.bomb += 1
            self.bomb_count = 0
            print(f"New Bomb added. Current Count : {self.bomb}")
        
        if self.bomb > 0:
            pygame.draw.circle(screen, (255,0,0), (self.x, self.y),12)
        if self.bomb >= 10:
            self.bomb = 0
            self.nukes +=1
            print(f"New Nuke added. Current Count : {self.nukes}")
        if self.nukes >= 1:
            pygame.draw.circle(screen, (0,255,0), (self.x+20, self.y),12)
    
    def collision_detect(self, obj_x, obj_y, damage):
        if self.x < obj_x < self.x + self.width and self.y < obj_y < self.y + self.height:
            self.health -= damage
            if self.health <= 0:
                self.hisAlive = False
            return True
        return False
    def rebirth(self):
        self.hisAlive  = True
        self.health =  self.max_health

class Ball:
    def __init__(self, x, y, dir, color=(0, 0, 255), dmg=0, lifesteal=False, radius=5):
        self.x = x + 10
        self.y = y + 25
        self.x_dir = dir
        self.y_dir = 0
        self.color = color
        self.radius = radius
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


class Screen:
    def __init__(self, text, center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2), font=pygame.font.Font('freesansbold.ttf', 50)) :
        self.font = font
        self.label = text
        self.TextLabel = self.font.render(str(self.label), True, (0,0,0), (255, 0, 255))
        self.TextRect = self.TextLabel.get_rect(center=center)

    def update(self, text, center):
        self.label = text
        self.TextLabel = self.font.render(str(self.label), True, (0,0,0), (255, 0, 255))
        self.TextRect = self.TextLabel.get_rect(center=center)
        screen.blit(self.TextLabel, self.TextRect)

# Game setup
ballList = []
gunObj = Gun(WINDOW_WIDTH * 0.2, WINDOW_HEIGHT * 0.5, 50, 50)
targetObj = Target(WINDOW_WIDTH - (WINDOW_WIDTH * 0.2), WINDOW_HEIGHT * 0.5, 30, 100)
count = 100
count_of_count = 0
wait_count = 10
wait_flag = True
p1a = Screen(f"rebirths:{x-1}", center=(WINDOW_WIDTH//10, WINDOW_HEIGHT//10),font=pygame.font.Font('freesansbold.ttf', 15))
p2a = Screen(f"bombs:{gunObj.bomb}", center=(WINDOW_WIDTH//10, -WINDOW_HEIGHT//9),font=pygame.font.Font('freesansbold.ttf', 15))
p3a = Screen(f"nukes:{gunObj.nukes}", center=(WINDOW_WIDTH//10, -WINDOW_HEIGHT//10),font=pygame.font.Font('freesansbold.ttf', 15))
p4a = Screen(f"ammo:100", center=(WINDOW_WIDTH//10, -WINDOW_HEIGHT//8), font=pygame.font.Font('freesansbold.ttf', 15))
p5a = Screen(f"You dealt a total of {dmg_dealt} damage.",center=(WINDOW_WIDTH//10, -WINDOW_HEIGHT//7), font=pygame.font.Font('freesansbold.ttf', 15))
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if state == "start": # to move to playing
                state = "playing"
            elif state == "playing":
                if event.key == pygame.K_SPACE and gun == 0:
                    if not targetObj.health <= 0:
                        ballList.append(Ball(x=gunObj.x+40, y=gunObj.y, dir = 5+x/3, dmg=30+x))
                        status = "nart"
                        shoots += 1
                if event.key == pygame.K_3:
                    if gunObj.bomb >= 1:
                        gunObj.bomb -= 1
                        ballList.append(Ball(x=gunObj.x+40, y=gunObj.y, dir = 3, dmg=800*x, radius=15))
                        shoots+=1
                elif event.key == pygame.K_2:
                    if gunObj.nukes >= 1:
                        gunObj.nukes -= 1
                        for i in range(50):
                            ballList.append(Ball(x=gunObj.x+40, y=gunObj.y, dir = 5, color=(0, 255, 0),dmg=100*x, radius=3))
                            shoots+=1
                elif event.key == pygame.K_r:
                    yesorno = input("Are you sure you want to restart? yes/no(type ONLY either one or restart will not be successful)")
                    if yesorno == 'yes':
                        rebirth = 0
                        gun = 0
                        contour = 100
                        gunObj.nukes = 0
                        x = 8
                        gunObj.bomb = 0
                        gunObj.max_health = 200
                        gunObj.health = gunObj.max_health
                        targetObj.max_health = 5000
                        targetObj.health = targetObj.max_health
                elif event.key == pygame.K_q:
                    gun = 1
                    def_contour = 100*x
                    if contour > def_contour:
                        contour = def_contour
                elif event.key == pygame.K_e:
                    gun = 2
                    def_contour =10*x
                    if contour > def_contour:
                        contour = def_contour
                elif event.key == pygame.K_f:
                    gun = 0
                    contour = 1e+1000
                elif event.key == pygame.K_p:
                    state = 'paused'
    screen.fill(BACKGROUND)

    # AUTOFIRE
    if state == 'start':
        if bolt == 0:
            var1 = ('1. Press W and S to move the gun')
            var2 = ('2. Press space to shoot')
            var3 = ('3. Press key q Or eto change gun type and also automatically shoot at intervals')
            var4 = ('4.Press key r to restart')
            var5 =('5.Press f to switch to manual shooting mode')
            var6 = ('6.Press 3 to launch a bomb(you have limited bombs)')
            var67 = ('7.Press p to pause the game.')
            var7 = ('8.Press 2 to launch a nuke(FAR MORE LIMITED!)(Refer to text file for full instructions)')
            instructions = Screen(var1, font=pygame.font.Font('freesansbold.ttf', 5))
            bolt += 1
        ass1 = Screen('Press any button to start', center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2), font=pygame.font.Font('freesansbold.ttf', 20))
        ass2 = Screen(var1, center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//10), font=pygame.font.Font('freesansbold.ttf', 20))
        ass3 = Screen(var2, center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//10+(20)), font=pygame.font.Font('freesansbold.ttf', 20))
        ass4 = Screen(var3, center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//10+(20*2)), font=pygame.font.Font('freesansbold.ttf', 20))
        ass5 = Screen(var4, center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//10+(20*3)), font=pygame.font.Font('freesansbold.ttf', 20))
        ass6 = Screen(var5, center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//10+(20*4)), font=pygame.font.Font('freesansbold.ttf', 20))
        ass7 = Screen(var6, center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//10+(20*5)), font=pygame.font.Font('freesansbold.ttf', 20))
        ass8 = Screen(var7, center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//10+(20*7)), font=pygame.font.Font('freesansbold.ttf', 20))
        ass9 = Screen(var67, center=(WINDOW_WIDTH//2,WINDOW_HEIGHT//10+(20*6)), font=pygame.font.Font('freesansbold.ttf', 20))
        screen.blit(ass1.TextLabel, ass1.TextRect)
        screen.blit(ass2.TextLabel, ass2.TextRect)
        screen.blit(ass3.TextLabel, ass3.TextRect)
        screen.blit(ass4.TextLabel, ass4.TextRect)
        screen.blit(ass5.TextLabel, ass5.TextRect)
        screen.blit(ass6.TextLabel, ass6.TextRect)
        screen.blit(ass7.TextLabel, ass7.TextRect)
        screen.blit(ass8.TextLabel, ass8.TextRect)
        screen.blit(ass9.TextLabel, ass9.TextRect)
    elif state == 'playing':
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            gunObj.moveUp()
        elif pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            gunObj.moveDown()
        if count <= 0: 
            
            if not(wait_flag):
                if targetObj.health > 2500: 
                    ballList.append(Ball(x=targetObj.x-20, y=targetObj.y, dir=-5*x, dmg=0.5*x))
                    count = 9.5
                elif targetObj.health < 1000:
                    ballList.append(Ball(x=targetObj.x-20, y=targetObj.y, dir = -8*x, dmg=3*x))
                    count = 5
                else:
                    ballList.append(Ball(x=targetObj.x-20, y=targetObj.y, dir=-6*x, dmg=1.5*x))
                    count = 9.5
                count_of_count += 1
                wait_count += 1*x
                if wait_count == 100:
                    wait_flag = True
            else:
                wait_count -= 1
                temp = []
                #temp.append(Ball(x=targetObj.x-20, y=targetObj.y, dir = -12, dmg=randint(15, 1000)/100))
                if wait_count == 0:
                    wait_flag = False
        else:
            count -= 1 
        if count_of_count >= 320:
            count = 1000
            count_of_count = 0
        # Player autofire minigun mode
        if gun == 1:
                if cont >= 20/x and contour > 1:
                    ballList.append(Ball(x=gunObj.x+40, y=gunObj.y, dir=5+(x/5), dmg=40+x)) 
                    contour -= 1
                    status = "nutin"
                    cont = 0
                elif cont < 20/x:
                    cont += 1 
                else:
                    cont = -150
                    contour = def_contour
                    status = "reloading..."

        for ballObj in ballList.copy():
            if targetObj.collision_detect(ballObj.x, ballObj.y, damage=ballObj.dmg):
                dmg_dealt += ballObj.dmg
                shoots += 1
                successful_shots += 1
                print(dmg_dealt)
                ballList.remove(ballObj)
                sound1.play()
                
            elif gunObj.collision_detect(ballObj.x, ballObj.y, damage=ballObj.dmg):
                ballList.remove(ballObj)
                
            elif ballObj.status:
                ballObj.render()
            else:
                ballList.remove(ballObj)
        if gun == 2:
                if cont >= 150/x and contour > 1:
                    ballList.append(Ball(x=gunObj.x+40, y=gunObj.y, dir=12+(x/5), dmg=150+x))
                    contour -= 1
                    shoots += 1
                    status = "nutin"
                    cont = 0
                elif cont < 150/x:
                    cont += 1 
                else:
                    cont = -250
                    contour = def_contour
                    status = "reloading..."

        if targetObj.health <= 0:
            state = '...'
            x += 1
            ballList = []
            pygame.display.update()
            state = 'start'
            targetObj.rebirth()
            gunObj.rebirth()
            state = 'playing'
        elif gunObj.health <= 0:
            state = 'end'
        else:
            targetObj.render()
            gunObj.render()
    elif state == 'end':
        accuracy = (successful_shots/shoots)*100
        f11f= f'You dealt {dmg_dealt} damage.'
        f22f =f'You defeated the boss {x-1} times.'
        f33f = f'You had an accuracy of {accuracy}%.'
        s1 = Screen('You died :(',center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//20),font=pygame.font.Font('freesansbold.ttf', 15))
        s2 = Screen(f11f,center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2.5),font=pygame.font.Font('freesansbold.ttf', 15))
        s3 = Screen(f22f,center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//4),font=pygame.font.Font('freesansbold.ttf', 15))
        s4 = Screen(f33f, center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//10), font=pygame.font.Font('freesansbold.ttf', 15))
        screen.blit(s1.TextLabel, s1.TextRect)
        screen.blit(s2.TextLabel, s2.TextRect)
        screen.blit(s3.TextLabel, s3.TextRect)
        screen.blit(s4.TextLabel, s4.TextRect)
    elif state == '...':
        pass

    elif state == 'paused':
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_p]:
            state = 'start'
        targetObj.render()
        gunObj.render()
            

    sleep(0.01)
    p1a.update(text=f"rebirths:{x-1}", center=(WINDOW_WIDTH//10, WINDOW_HEIGHT//10))
    p2a.update(text=f"bombs:{gunObj.bomb}", center=(WINDOW_WIDTH//10, WINDOW_HEIGHT//1.115))
    p3a.update(text=f"nukes:{gunObj.nukes}", center=(WINDOW_WIDTH//10, WINDOW_HEIGHT//1.2))
    if not status == 'reloading...':
        p4a.update(text=f"ammo:{contour}", center=(WINDOW_WIDTH//10, WINDOW_HEIGHT//1.35))
    else:
        p4a.update(text=f"ammo:{status}", center=(WINDOW_WIDTH/10, WINDOW_HEIGHT//1.35))
    p5a.update(text=f"You dealt {dmg_dealt} damage.",center=(WINDOW_WIDTH//8, WINDOW_HEIGHT//1.45) )
    conti += 1
    pygame.display.update()