import pygame,sys
from numpy import sqrt


import pygame,sys
from pygame.math import Vector2 as vc

pygame.init()
window=pygame.display.set_mode((600,600))
clock=pygame.time.Clock()

class Particle:
    def __init__(self,pos,old_pos,acc,origin) :
        self.pos=vc(pos[0],pos[1])
        self.old_pos=vc(old_pos[0],old_pos[1])
        self.vel=vc()
        self.friction=0.012
        self.acc=acc
        self.origin=origin
        self.rect=pygame.Rect(self.pos[0]-20,self.pos[1]-20,40,40)

    def move(self):
        if not self.origin:
            self.vel=self.pos-self.old_pos
            self.old_pos=self.pos
            #self.vel.x*=self.friction
            self.pos=self.pos+self.vel+self.acc
        else:
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

        differnce=(self.resting_distance-d)/d

        offset_x=dx*0.5*differnce
        offset_y=dy*0.5*differnce
        if not self.p1.origin:
            self.p1.pos.x+=offset_x
            self.p1.pos.y+=offset_y

        self.p2.pos.x-=offset_x
        self.p2.pos.y-=offset_y

    def drawlink(self,screen):
        pygame.draw.line(screen,(255,255,255),self.p1.pos,self.p2.pos,2)






particul0=Particle((300,20),(300,20),vc(0,0),True)
particul2=Particle((350,20),(350,20),vc(0,1),False)
particul3=Particle((400,20),(350,20),vc(0,1),False)
particul4=Particle((300,20),(300,20),vc(0,1),False)

link1=Link(particul0,particul2,100)
link2=Link(particul2,particul3,100)
link3=Link(particul3,particul4,100)


while True:
    event=pygame.event.poll()
    if event.type==pygame.QUIT:
        sys.exit()
    window.fill((0,0,0))
    pygame.draw.circle(window,(255,255,255),particul0.pos,20)
    pygame.draw.circle(window,(255,255,255),particul2.pos,20)
    pygame.draw.circle(window,(255,255,255),particul3.pos,20)
    pygame.draw.circle(window,(255,255,255),particul4.pos,20)
    particul0.move()
    particul2.move()
    particul3.move()
    particul4.move()
    link1.constraint()
    link1.drawlink(window)
    link2.constraint()
    link2.drawlink(window)
    #link3.constraint()
    #link3.drawlink(window)
    #particul0.keepinwindow(20,600,600)
    particul2.keepinwindow(20,600,600)
    pygame.display.flip()
    clock.tick(60)
