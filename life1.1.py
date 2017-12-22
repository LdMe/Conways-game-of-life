import pygame
import random
from time import sleep

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
LEFT = (1,0,0)
RIGHT = (0,0,1)
class lista:
    def __init__(self):
        self.zombies = []
        self.objects = []
        self.houses = []
        self.rocks = []
        self.trees = []
        self.people = []
        self.bullets = []
        self.bushes = []
        self.patches = []
        self.reserved = []
        self.schools = []
        self.guns = []
        self.selected =[]
        self.selectnum = 0
        self.warehouses = []
        self.crops= []
    def addZ(self, z):
        self.zombies.append(z)
    def addO(self, z):
        self.objects.append(z)
    def addH(self, z):
        self.houses.append(z)
    def addR(self, z):
        self.rocks.append(z)
    def addRS(self, z):
        self.reserved.append(z)####RESERVED PATCHES
    def addT(self, z):
        self.trees.append(z)
    def addP(self, z):
        self.people.append(z)
    def addpatches(self, z):
        self.patches.append(z)
    def addB(self, z):
        self.bushes.append(z)
    def addBT(self, z):
        self.bullets.append(z)
    def addC(self, z):
        self.crops.append(z)
    def addG(self, z):
        self.guns.append(z)
    def addS(self, z):
        self.schools.append(z)
    def addW(self, z):
        self.warehouses.append(z)
    def addSP(self, z):
        self.selected.append(z)

class patches:
    def __init__(self,x,y,scale,n):
        self.xpos = x
        self.ypos = y
        self.num = n
        self.died= 0
        self.live = 0
        self.alive = 0
        self.reserved = 0
        self.scale = scale
        self.rect = pygame.Rect(self.xpos,self.ypos,scale,scale)
    def distance(self,x,y):
        distance = abs(self.xpos - x )+ abs(self.ypos - y)
        return distance
    def reserve(self,obj,L):
        if(self.xpos - obj.rect.left >= 0 and self.xpos - obj.rect.right <= 0):
            if(self.ypos - obj.rect.top >= 0 and self.ypos - obj.rect.bottom <= 0):
                self.reserved = 1
                if(self not in L.reserved):
                    L.reserved.append(self)

    def dereserve(self,obj,L):
        if(self.xpos - obj.rect.left >= 0 and self.xpos - obj.rect.right <= 0):
            if(self.ypos - obj.rect.top >= 0 and self.ypos - obj.rect.bottom <= 0):
                self.reserved = 0
                if(self  in L.reserved):
                    L.reserved.remove(self)
    def setneighbors(self,L,x,y,scale):
        self.neighbors = []
        north = 0
        south = 0
        east = 0
        west = 0
        if(self.num % (x / scale) > 0):
           west = 1
           self.neighbors.append(L.patches[self.num - 1])
        if(self.num  % (x / scale) < (x /scale) - 1):
            east  = 1
            self.neighbors.append(L.patches[self.num + 1])
        if(self.num < ((x / scale)* (y/ scale))- (x /scale)  ):
            south = 1
            self.neighbors.append(L.patches[self.num + (x /scale)])
        if(self.num >=  (x /scale)):
            north = 1
            self.neighbors.append(L.patches[self.num - (x /scale)])
        if(north and west):
            self.neighbors.append(L.patches[self.num - (x /scale)- 1 ] )
        if(north and east):
            self.neighbors.append(L.patches[self.num - (x /scale)+ 1 ] )
        if(south and west):
            self.neighbors.append(L.patches[self.num + (x /scale)- 1 ] )
        if(south and east):
            self.neighbors.append(L.patches[self.num + (x /scale)+ 1 ] )
    def die(self):
        self.died = 1
        self.live = 0
        
    def born(self):
        self.live = 1
        self.died = 0
    def proccess(self):
        if(self.died):
            self.alive = 0
            self.died = 0
        elif(self.live ):
            self.alive = 1
            self.live  = 0
    def survive(self,L):
        counter = 0
        for i in self.neighbors:
            if(i.alive):
                counter = counter + 1
        if(counter < 2 or counter > 3 and self.alive):
            self.die()
        elif(not self.alive and counter == 3):
            self.born()
    def show(self,screen):
        if(self.alive):
            pygame.draw.rect(screen, WHITE,(self.xpos,self.ypos,self.scale,self.scale))
            pygame.draw.rect(screen, BLACK,(self.xpos + 1,self.ypos + 1,self.scale - 1 ,self.scale - 1))
        else:
            pygame.draw.rect(screen, BLACK,(self.xpos,self.ypos,self.scale,self.scale))
            pygame.draw.rect(screen, WHITE,(self.xpos + 1,self.ypos + 1,self.scale - 1 ,self.scale - 1))
            
def clear(L):
    for p in L.patches:
                    p.die()
                    p.proccess()
def reset(L):
    for p in L.patches:
        if(random.random() < 0.9):
                    p.die()
        else:
                    p.born()
        p.proccess()
def setquasar(patch,L,x,y,scale):
    patch.born()
    for i in range (0,5):
        
        L.patches[patch.num - i].born()
        L.patches[patch.num - i + 2 * int(x/ scale) ].born()
        
        L.patches[patch.num - i].proccess()
        L.patches[patch.num - i + 2 * int(x/ scale) ].proccess()
    L.patches[patch.num + 1 +  int(x/ scale) ].born()
    L.patches[patch.num - 5 +  int(x/ scale) ].born()
    L.patches[patch.num + 1 +  int(x/ scale) ].proccess()
    L.patches[patch.num - 5 +  int(x/ scale) ].proccess()
    return

    
def detectaction(L, screen,x,y,scale):
    for event in pygame.event.get():
        
        if(event.type == pygame.MOUSEBUTTONDOWN ):
             pos =pygame.mouse.get_pos()
             button =(pygame.mouse.get_pressed())
             if(button ==  RIGHT):
                 for p in L.patches:
                     if(abs(((p.scale / 2) +p.xpos) - pos[0])<= 5 and abs(((p.scale / 2) +p.ypos) - pos[1]) <= 5):
                         setquasar(p,L,x,y,scale)
                         return
                     
                 
             
             for p in L.patches:
                 if(abs(((p.scale / 2) +p.xpos) - pos[0])<= 5 and abs(((p.scale / 2) +p.ypos) - pos[1]) <= 5):
                     if(p.alive):
                         p.die()
                     else:
                         
                         p.born()
                     p.proccess()
                     pygame.draw.rect(screen, BLACK,(p.xpos,p.ypos,p.scale,p.scale))
                     return
        elif(event.type == pygame.KEYDOWN ):
            
            if (event.key == pygame.K_ESCAPE):
                return 1
            if (event.key == pygame.K_SPACE):
                return 2
            if (event.key == pygame.K_c):
                clear(L)
            if (event.key == pygame.K_r):
                reset(L)
        
def start (L, screen):
    for p in L.patches:
            p.survive(L)
    for p in L.patches:
            p.proccess()
            p.show(screen)
    pygame.display.update()           
def main():

    game = pygame.init()
 #   fondo = pygame.image.load("ground.png")
    L = lista()
    scale = 20
    X = 600
    Y = 400
#    fondo = pygame.transform.scale(fondo,(900,800))
    screen = pygame.display.set_mode((X,Y))
    n = 0
    started = 0
    for i in range (Y / scale):
        for j in range(X / scale):
            patch1 = patches(j * scale,i * scale, scale,n)
            
            L.addpatches(patch1)
            n =  n + 1
    
    for p in L.patches:
        p.setneighbors(L,X,Y,scale)
        if(random.random() > 0.5):
            p.born()
    reset(L)
    while (1):
        a = detectaction(L, screen,X,Y,scale)
        if(a == 1):
            return
        elif(a ==2):
            if(not started):
                started = 1
            else:
                started = 0
        if(started):
            start(L, screen)
            sleep(0.1)
        for p in L.patches:
            p.show(screen)
 #       c = L.patches[int((X * Y)/ ((scale  * 2) ** 2 ))]
#        pygame.draw.rect(screen, RED,(c.xpos,c.ypos,c.scale,c.scale))
#        c.setneighbors(L,X,Y,scale)
#        for p in c.neighbors:
            
#            pygame.draw.rect(screen, GREEN,(p.xpos,p.ypos,p.scale,p.scale))
            
        pygame.display.update()             

main()   
    
            
