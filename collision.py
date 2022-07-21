from turtle import circle
import pygame


def circle_collide(circle1,circle2):
    dx=circle1.pos.x-circle2.pos.x
    dy=circle1.pos.y-circle2.pos.y

    if abs(dx*dx+dy*dy)<=(circle1.radius+circle2.radius)*(circle1.radius+circle2.radius) :
        return [True,dx*dx+dy*dy]
    else:
        return [False,dx*dx+dy*dy]


def SAT_collision():
    pass
    