from functools import partial
import pygame


import pygame,sys
from pygame.math import Vector2 as vc

pygame.init()
window=pygame.display.set_mode((600,600))
clock=pygame.time.Clock()

class Particle:
    def __init__(self,pos,old_pos) :
        self.pos=vc(pos[0],pos[1])
        self.old_pos=vc(old_pos[0],old_pos[1])
        self.vel=vc()
        self.friction=0.012

    def move(self):
        acc=vc(0,1)
        self.vel=self.pos-self.old_pos
        self.old_pos=self.pos
        #self.vel.x*=self.friction
        self.pos=self.pos+self.vel+acc

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
    
            

particule=Particle((350,0),(300,0))
particul2=Particle((60,0),(360,10))

while True:
    event=pygame.event.poll()
    if event.type==pygame.QUIT:
        sys.exit()
    window.fill((0,0,0))
    pygame.draw.circle(window,(255,255,255),particule.pos,20)
    pygame.draw.circle(window,(255,255,255),particul2.pos,20)
    particule.move()
    particul2.move()
    particule.keepinwindow(20,600,600)
    particul2.keepinwindow(20,600,600)
    pygame.display.flip()
    clock.tick(60)
