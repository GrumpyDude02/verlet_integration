from random import random, randrange
import pygame,sys
from numpy import sqrt


import pygame,sys
from pygame.math import Vector2 as vc

pygame.init()
window=pygame.display.set_mode((1280,700))
clock=pygame.time.Clock()

class Particle:
    def __init__(self,pos,old_pos,acc,anchor) :
        self.pos=vc(pos[0],pos[1])
        self.old_pos=vc(old_pos[0],old_pos[1])
        self.vel=vc()
        self.friction=0.012
        self.acc=acc
        self.anchor=anchor
        self.rect=pygame.Rect(self.pos[0]-20,self.pos[1]-20,40,40)

    def move(self):
        if not self.anchor:
            self.vel=self.pos-self.old_pos
            self.old_pos=self.pos
            #self.vel.x*=self.friction
            self.pos=self.pos+self.vel+self.acc*0.03*0.03
        else:
            self.rect=pygame.Rect(self.pos[0]-20,self.pos[1]-20,40,40)
            pygame.draw.rect(window,(255,0,0),self.rect,5)
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                print('true')
                if pygame.mouse.get_pressed()[0]:
                    self.pos.x=pygame.mouse.get_pos()[0]
                    self.pos.y=pygame.mouse.get_pos()[1]
                    self.rect.center=(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
        

    def keepinwindow(self,radius,width,height):
        if self.pos.y+radius>height:
            self.vel.y*=0.75
            self.pos.y=height-radius
            self.old_pos.y=self.pos.y+self.vel.y
        if self.pos.y-radius<0:
            self.vel.y*=0.75
            self.pos.y=radius
            self.old_pos.y=self.pos.y+self.vel.y
        if self.pos.x+radius>width:
            self.vel.x*=0.75
            self.pos.x=width-radius
            self.old_pos.x=self.pos.x+self.vel.x
        if self.pos.x-radius<0:
            self.vel.x*=0.75
            self.pos.x=radius
            self.old_pos.x=self.pos.x+self.vel.x
    
class Link:
    def __init__(self,p1,p2,distance):
        self.p1=p1
        self.p2=p2
        self.resting_distance=distance

    def constraint(self):
        dx=self.p1.pos.x-self.p2.pos.x
        dy=self.p1.pos.y-self.p2.pos.y

        d=sqrt(dx*dx+dy*dy)

        differnce=(self.resting_distance-d)/d*0.5

        offset_x=dx*differnce*0.8
        offset_y=dy*differnce*0.8
        if not self.p1.anchor:
            self.p1.pos.x+=offset_x
            self.p1.pos.y+=offset_y
        if not self.p2.anchor:
            self.p2.pos.x-=offset_x
            self.p2.pos.y-=offset_y

    def drawlink(self,screen):
        if self.p1.anchor:   
            pygame.draw.line(screen,(255,255,255),self.p1.pos,self.p2.old_pos,2)
        elif self.p2.anchor:
            pygame.draw.line(screen,(255,255,255),self.p1.old_pos,self.p2.pos,2)
        else:
            pygame.draw.line(screen,(255,255,255),self.p1.old_pos,self.p2.old_pos,2)






particul0=Particle((600,20),(600,20),vc(0,0),True)

particules=[particul0]

links=[]

a=20


cloth=[[Particle((0,0),(0,0),vc(0,1),False) for i in range(50)]for j in range(50)]
cloth_links=[]

y=30
for i in range(20):
    x=400
    for j in range(20):
        anchor=False
        if i==0 and j==0 or i==0 and j==49:
            anchor=True
        cloth[i][j]=Particle((x,y),(x,y),vc(0,10),anchor)
        x+=10
    y+=10

for i in range(19):
    for j in range(19):
        cloth_links.append(Link(cloth[i][j],cloth[i][j+1],10))
        cloth_links.append(Link(cloth[i][j],cloth[i+1][j],10))



while True:
    event=pygame.event.poll()
    if event.type==pygame.QUIT:
        sys.exit()
    window.fill((0,0,0))
    for i in range(50):
        for j in range(50):
            pygame.draw.circle(window,(255,255,255),cloth[i][j].pos,1)
            cloth[i][j].move()
            cloth[i][i].keepinwindow(1,1280,700)
    
    for link in cloth_links:
        link.constraint()
        link.drawlink(window)
    pygame.display.flip()
    fp=clock.get_fps()
    clock.tick(60)
    print(fp)
