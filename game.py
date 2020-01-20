import os
import pygame

LEFT = 0
RIGHT = 1
DOWN = 2
UP = 3
PUNCH = 4
KICK = 5
BLOCK = 6

pygame.init()

font = pygame.font.SysFont("arial",30)

screenWidth = 640
screenHeight = 480
win = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Game")
bg = pygame.image.load("res/bg.jpg")

class SpriteSheet(object):
    
    def __init__(self, file_name):
        self.spriteSheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height))
        image.blit(self.spriteSheet, (0,0), (x,y,width,height))

        #resize
        image = pygame.transform.scale(image, (width*4, height*4))

        #green
        image.set_colorkey((0,255,0))

        return image


class player(object):
    def __init__(self, x, y, width, height,charNumber):
        self.x = x
        self.y = y
        self.spriteWidth = width
        self.spriteHeight = height
        self.width = width*4
        self.height = height*4
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.idleCounter = 0
        self.isPunch = False
        self.attackCounter = 0
        self.isKick = False
        self.attacking = False
        self.isRecover = False
        self.recoverTime = 10
        self.isDuck = False
        self.isLowKick = False
        self.isLowPunch = False
        self.isAirKick = False
        self.isAirPunch = False
        self.isBlock = False
        self.isKnockedUp = False
        self.isFlinch = False
        self.stunTime = 10
        self.isFlinch


        self.hp = 100
        self.didAttackHit = False
        self.wins = 0

        #movement state: left, right, down
        #attack state: punch kick
        #air/jump state
        
        

        if charNumber == 0:
            sprite_sheet = SpriteSheet("res/Char_3.png")
            self.direction = "R"
        elif charNumber == 1:
            sprite_sheet = SpriteSheet("res/Char_4.png")
            self.direction = "L"


        self.walkRight = sprite_sheet.get_image(64,64,width,height)
        self.walkLeft = sprite_sheet.get_image(0,64,width,height)
        self.idle = []
        for i in range(4):
            image = sprite_sheet.get_image((i+8)*64,0,width,height)
            self.idle.append(image)
        self.block = sprite_sheet.get_image(0*width,3*height,width,height)
        self.jump = sprite_sheet.get_image(15*width,2*height,width,height)
        self.punch = sprite_sheet.get_image(0*width,2*height,width,height)
        self.kick = sprite_sheet.get_image(8*width,2*height,width,height)
        self.duck = sprite_sheet.get_image(16*width,0*height,width,height)
        self.lowKick = sprite_sheet.get_image(15*width,0*height,width,height)
        self.lowPunch = sprite_sheet.get_image(14*width,0*height,width,height)
        self.airPunch = []
        for i in range(2):
            image = sprite_sheet.get_image((i+12)*width,3*height,width,height)
            self.airPunch.append(image)
        self.airKick = []
        for i in range(2):
            image = sprite_sheet.get_image((i+12)*width,2*height,width,height)
            self.airKick.append(image)
        self.flinch = sprite_sheet.get_image(3*width,3*height,width,height)

        self.knockedUp = []
        image = sprite_sheet.get_image(4*width,3*height,width,height)
        self.knockedUp.append(image)
        image = sprite_sheet.get_image(5*width,3*height,width,height)
        self.knockedUp.append(image)
        image = sprite_sheet.get_image(7*width,3*height,width,height)
        self.knockedUp.append(image)

        if charNumber == 1:
            self.flip()

    def flip(self):
        self.jump = pygame.transform.flip(self.jump,True,False)
        self.walkRight,self.walkLeft = pygame.transform.flip(self.walkLeft,True,False),pygame.transform.flip(self.walkRight,True,False) #walking swap
        self.duck = pygame.transform.flip(self.duck,True,False)
        self.punch = pygame.transform.flip(self.punch,True,False)
        self.block = pygame.transform.flip(self.block,True,False)
        self.kick = pygame.transform.flip(self.kick,True,False)
        self.lowKick = pygame.transform.flip(self.lowKick,True,False)
        self.lowPunch = pygame.transform.flip(self.lowPunch,True,False)
        self.flinch = pygame.transform.flip(self.flinch,True,False)
        for i in range(len(self.idle)):
            self.idle[i] = pygame.transform.flip(self.idle[i],True,False)
        for i in range(len(self.airKick)):
            self.airKick[i] = pygame.transform.flip(self.airKick[i],True,False)
        for i in range(len(self.airPunch)):
            self.airPunch[i] = pygame.transform.flip(self.airPunch[i],True,False)
        for i in range(len(self.knockedUp)):
            self.knockedUp[i] = pygame.transform.flip(self.knockedUp[i],True,False)



    def draw(self,win):
        if self.isKnockedUp:
            if self.stunTime > 30:
                win.blit(self.knockedUp[0],(self.x,self.y))
                #Stun animation
                self.y -= (self.stunTime-30)**2 * 0.6
            elif self.stunTime > 20:
                win.blit(self.knockedUp[1],(self.x,self.y))
                self.y += (self.stunTime-20)**2 * 0.6
            elif self.stunTime >= 0:
                win.blit(self.knockedUp[2],(self.x,self.y))
            
            if self.stunTime <= 40 and self.stunTime >= 20:
                if self.direction == "R" and self.x > -self.width/4:
                    self.x -= 5
                elif self.direction == "L" and self.x < screenWidth - self.width + self.width/4:
                    self.x += 5

            if self.stunTime == 0:
                self.isKnockedUp = False
            
            self.stunTime -= 1
        elif self.isFlinch:
            #ADD FLINCH CODE
            test = 0
        elif self.isAirKick:
            if self.attackCounter + 1 >= 14:
                self.attackCounter = 0

            win.blit(self.airKick[self.attackCounter//7],(self.x,self.y))
            self.attackCounter += 1

            if not self.isJump:
                self.attackCounter = 0
                self.isAirKick = False
                self.attacking = False
                self.isRecover = True
                self.recoverTime = 10
                self.didAttackHit = False
        elif self.isAirPunch:
            if self.attackCounter <= 5:
                win.blit(self.airPunch[0],(self.x,self.y))
            else:
                win.blit(self.airPunch[1],(self.x,self.y))

            self.attackCounter += 1

            if not self.isJump:
                self.attackCounter = 0
                self.isAirPunch = False
                self.attacking = False
                self.isRecover = True
                self.recoverTime = 10
                self.didAttackHit = False

        elif self.left:
            win.blit(self.walkLeft,(self.x,self.y))
        elif self.right:
            win.blit(self.walkRight,(self.x,self.y))
        elif self.isPunch:
            if self.attackCounter == 5:
                self.attackCounter = 0
                self.isPunch = False
                self.attacking = False
                self.isRecover = True
                self.recoverTime = 10
            else:
                win.blit(self.punch,(self.x,self.y))
                self.attackCounter += 1
        elif self.isKick:
            if self.attackCounter == 25:
                self.attackCounter = 0
                self.isKick = False
                self.attacking = False
                self.isRecover = True
                self.recoverTime = 10
            else:
                win.blit(self.kick,(self.x,self.y))
                self.attackCounter += 1
        elif self.isLowKick:
            if self.attackCounter == 15:
                self.attackCounter = 0
                self.isLowKick = False
                self.attacking = False
                self.isRecover = True
                self.recoverTime = 10
            else:
                win.blit(self.lowKick,(self.x,self.y))
                self.attackCounter += 1
        elif self.isLowPunch:
            if self.attackCounter == 10:
                self.attackCounter = 0
                self.isLowPunch = False
                self.attacking = False
                self.isRecover = True
                self.recoverTime = 10
            else:
                win.blit(self.lowPunch,(self.x,self.y))
                self.attackCounter += 1
        elif self.isBlock:
            win.blit(self.block, (self.x, self.y))
        elif self.isDuck:
            win.blit(self.duck,(self.x,self.y))
        elif self.isJump:
            win.blit(self.jump,(self.x,self.y))
        else:
            if self.idleCounter + 1 >= 80:
                self.idleCounter = 0

            win.blit(self.idle[self.idleCounter//20],(self.x,self.y))
            self.idleCounter += 1

def reset():
    for i in range(2):
        p[i].hp = 100
    p[0].x = -64
    p[1].x = 640-(3*64)
def hitDetection(i):
    #j is the other player
    j = 0
    if i == 0:
        j = 1

    damageReduction = 1
    if p[j].isBlock:
        damageReduction = 3
    
    if p[i].isPunch == True and p[i].attackCounter == 0 and abs(p[j].x - p[i].x) <= p[j].width/2 and not p[j].isJump:
        p[j].hp -= 5
        if p[j].isBlock:
            p[j].isBlock = False
            p[j].isRecover = True
            p[j].recoverTime = 20
    if p[i].isKick == True and p[i].attackCounter == 0 and abs(p[j].x - p[i].x) <= p[j].width/2 and abs(p[j].y - p[i].y) <= p[j].height/2 and not p[j].isKnockedUp:
        p[j].hp -= 10/damageReduction

        if not p[j].isDuck and not p[j].isBlock:
            p[j].isKnockedUp = True
            p[j].stunTime = 40
        
    if p[i].isLowPunch == True and p[i].attackCounter == 0 and abs(p[j].x - p[i].x) <= p[j].width/2 and not p[j].isJump:
        p[j].hp -= 5
        if p[j].isBlock:
            p[j].isBlock = False
            p[j].isRecover = True
            p[j].recoverTime = 20
    if p[i].isLowKick == True and p[i].attackCounter == 0 and abs(p[j].x - p[i].x) <= p[j].width/2 and not p[j].isJump:
        p[j].hp -= 10/damageReduction
    if p[i].isAirPunch == True and not p[i].didAttackHit and abs(p[j].x - p[i].x) <= p[j].width/2 and not p[j].isDuck and abs(p[j].y - p[i].y) <= p[j].height/4:
        p[j].hp -= 5
        if p[j].isBlock:
            p[j].isBlock = False
            p[j].isRecover = True
            p[j].recoverTime = 20
        p[i].didAttackHit = True
    if p[i].isAirKick == True and not p[i].didAttackHit and abs(p[j].x - p[i].x) <= p[j].width/2 and not p[j].isDuck and abs(p[j].y - p[i].y) <= p[j].height/4:
        p[j].hp -= 10/damageReduction
        p[i].didAttackHit = True



def input(i):
    imageOffset = p[i].spriteWidth

    controls = None

    if i == 1:
        controls = [pygame.K_LEFT,pygame.K_RIGHT,pygame.K_DOWN,pygame.K_UP,pygame.K_j,pygame.K_k,pygame.K_l]
    elif i == 0:
        controls = [pygame.K_a,pygame.K_d,pygame.K_s,pygame.K_w,pygame.K_f,pygame.K_g,pygame.K_h]

    if keys[controls[PUNCH]] and not p[i].attacking and not p[i].isRecover and not p[i].isJump and not p[i].isDuck and not p[i].isKnockedUp:
        p[i].isPunch = True
        p[i].attacking = True
        p[i].right = False
        p[i].left = False
        p[i].idleCounter = 0
    elif keys[controls[KICK]] and not p[i].attacking and not p[i].isRecover and not p[i].isJump and not p[i].isDuck and not p[i].isKnockedUp:
        p[i].isKick = True
        p[i].attacking = True
        p[i].right = False
        p[i].left = False
        p[i].idleCounter = 0
    elif keys[controls[KICK]] and not p[i].attacking and not p[i].isRecover and not p[i].isJump and p[i].isDuck and not p[i].isKnockedUp:
        p[i].isLowKick = True
        p[i].attacking = True
        p[i].right = False
        p[i].left = False
        p[i].idleCounter = 0
    elif keys[controls[PUNCH]] and not p[i].attacking and not p[i].isRecover and not p[i].isJump and p[i].isDuck and not p[i].isKnockedUp:
        p[i].isLowPunch = True
        p[i].attacking = True
        p[i].right = False
        p[i].left = False
        p[i].idleCounter = 0
    elif keys[controls[KICK]] and not p[i].attacking and not p[i].isRecover and p[i].isJump and not p[i].isDuck and not p[i].isKnockedUp:
        p[i].isAirKick = True
        p[i].attacking = True
        p[i].right = False
        p[i].left = False
        p[i].idleCounter = 0
    elif keys[controls[PUNCH]] and not p[i].attacking and not p[i].isRecover and p[i].isJump and not p[i].isDuck and not p[i].isKnockedUp:
        p[i].isAirPunch = True
        p[i].attacking = True
        p[i].right = False
        p[i].left = False
        p[i].idleCounter = 0
    elif keys[controls[BLOCK]] and not p[i].isRecover and not p[i].isKnockedUp:
        p[i].isBlock = True
        p[i].right = False
        p[i].left = False
        p[i].idleCounter = 0
    elif keys[controls[LEFT]] and (p[i].x > -imageOffset and (not p[i].attacking or p[i].isJump)) and not p[i].isKnockedUp:
        p[i].x -= p[i].vel
        p[i].right = False
        p[i].left = True
        p[i].isDuck = False
        p[i].idleCounter = 0
    elif keys[controls[RIGHT]] and (p[i].x < screenWidth - p[i].width + imageOffset and (not p[i].attacking or p[i].isJump)) and not p[i].isKnockedUp:
        p[i].x += p[i].vel
        p[i].left = False
        p[i].right = True
        p[i].isDuck = False
        p[i].idleCounter = 0
    #if keys[pygame.K_UP] and p[i].y > p[i].vel:
        #p[i].y -= p[i].vel
    elif keys[controls[DOWN]] and not p[i].isKnockedUp:
        p[i].isDuck = True
        p[i].left = False
        p[i].right = False
        p[i].idleCounter = 0
    else:
        p[i].right = False
        p[i].left = False
        p[i].isDuck = False
        p[i].isBlock = False
        

    if not p[i].isJump and not p[i].attacking and not p[i].isRecover and not p[i].isBlock and not p[i].isKnockedUp:
        if keys[controls[UP]]:
            p[i].isJump = True
            p[i].right = False
            p[i].left = False
    elif p[i].isJump:
        if p[i].jumpCount >= -10:
            neg = 1
            if p[i].jumpCount < 0:
                neg = -1
            p[i].y -= (p[i].jumpCount ** 2) * 0.40 * neg
            p[i].jumpCount -= 20/24
        else:
            p[i].isJump = False
            p[i].jumpCount = 10
            p[i].isRecover = True
            p[i].recoverTime = 10

    if p[i].isRecover:
        if p[i].recoverTime == 0:
            p[i].isRecover = False
            p[i].recoverCounter = 10 #default recover time
        else:
            p[i].recoverTime -= 1

def redrawGameWindow():
    win.blit(bg, (0,0))
    #win.fill((0,0,0))
    #pygame.draw.rect(win,(255,0,0),(p[i].x,p[i].y,p[i].width,p[i].height))

    #HP
    pygame.draw.rect(win, (168,26,26),(10,10,p[0].hp*3,30))
    pygame.draw.rect(win, (168,26,26),(330,10,p[1].hp*3,30))

    #text
    #text = font.render("SCORE: " + str(p[0].wins) + "|" + str(p[1].wins),True, (255,255,255))
    #win.blit(text,(50,50))


    p[0].draw(win)
    p[1].draw(win)
    pygame.display.update()
        



#Game loop
p = [player(-64,250,64,64,0), player(640-(3*64),250,64,64,1)]
clock = pygame.time.Clock()
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #Input
    keys = pygame.key.get_pressed()
    input(0)
    input(1)

    hitDetection(0)
    hitDetection(1)

    if (p[0].hp <= 0):
        #player 2 wins
        p[1].wins += 1
        reset()
    elif p[1].hp <= 0:
        #player 1 wins
        p[0].wins += 1
        reset()



    #Determines what direction the player is facing
    if p[0].x >= p[1].x and p[0].direction == "R" and p[1].direction == "L":
        p[0].direction = "L"
        p[1].direction = "R"
        p[0].flip()
        p[1].flip()
    elif p[0].x < p[1].x and p[0].direction == "L" and p[1].direction == "R":
        p[0].direction = "R"
        p[1].direction = "L"
        p[0].flip()
        p[1].flip()
    
    redrawGameWindow()
    clock.tick(60)
    
    

pygame.quit()