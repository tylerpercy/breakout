# Tyler Percy
# 1/19/21
# PHY 2200

# A version of the popular 'breakout' game using vpython.

###########################
#                         #
#  Instructions:          #
#  - Install VPython      #
#    pip3 install vpython #
#  - Execute program      #
#    python3 breakout.py  #
#                         #
###########################

from vpython import *
import numpy as np
import random

def game():
    # constants
    R = 0.5e-10
    L = 28
    thick = L/50
    s = 2500 # initial speed

    # colors list
    cList = [color.red, color.orange, color.cyan, color.green]

    # brick class
    class brick():
        def __init__(self, x, y):
            # Initialize the block 
            self.b = box(pos=vec(-x,y,0),
                color=cList[random.randint(0,3)],
                size=vec(1.75,thick,thick))
        def collide(self, p):
                # Check if ball has collided with the block
                if (p.pos.x >= self.b.pos.x - 1) and (p.pos.x <= self.b.pos.x + 1) and (p.pos.y <= self.b.pos.y + .4 and p.pos.y >= self.b.pos.y - .4):
                    self.b.pos = vec(-999, -999, 0)
                    self.b.visible = False
                    return True
        def destroyed(self):
            return True if self.b.pos == (-999, -999, 0) else False


    scene = canvas(title='Breakout Game', width=800, height=600)

    # creating the outer walls
    Lwall = box(pos = vec(-L/2, 0, 0), size = vec(thick, L, thick), color=color.white) #left wall
    Rwall = box(pos = vec(L/2, 0, 0), size = vec(thick, L, thick), color=color.white)  #right wall
    Bwall = box(pos = vec(0, -L/2, 0), size = vec(L, thick, thick), color=color.white) #bottom wall
    Twall = box(pos = vec(0, L/2, 0), size = vec(L, thick, thick), color=color.white)  #top wall

    # array to hold bricks
    bricks = []

    bricks = [brick(x,y) for y in range(9,13) for x in range(-12, 14, 2)]

    # creating ball
    ball = sphere(pos = vec(0,-10,0), radius = .5, color = color.white)
    ball.v = s*hat(vec(2*random.random()-1, 2*4-1, 0))

    # platform
    pad = box(pos=vector(0,-11,0), color=color.white, size=vec(4,.5,.01))

    # time
    t = 0
    dt = 1e-5

    scene.pause("Click to start")

    running = True
    won = False

    # main loop
    while(running):
        rate(500)

        if all([brick.destroyed() for brick in bricks]): # if all bricks are broken
            won = True
            break

        ball.pos = ball.pos + ball.v*dt

        if ball.pos.y < -(L/2): # if ball hits floor
            break

        # Track the mouse so the pad can follow
        if scene.mouse.pos.x > -12 and scene.mouse.pos.x < 12:
            pad.pos.x = scene.mouse.pos.x
        elif scene.mouse.pos.x < -12:
            pad.pos.x = -11.5
        elif scene.mouse.pos.x > 12:
            pad.pos.x = 11.5


        # reflect from walls upon collision
        if(abs(ball.pos.x) > L/2): # reflect in x-direction
               ball.v.x = -ball.v.x
        if ball.pos.y > L/2:       # reflect off ceiling
               ball.v.y = -ball.v.y

        # reflect from and destroy block
        for brick in bricks:
            if brick.collide(ball) == 1:
                ball.v.y = -ball.v.y

        # reflect from platform
        if (ball.pos.x >= pad.pos.x - 3 and ball.pos.x <= pad.pos.x + 3) and (ball.pos.y <= pad.pos.y + .2 and ball.pos.y >= pad.pos.y - .2):
                ball.v.y = -ball.v.y

        t = t + dt

    if won == True:
        scene.pause("You win!")
        scene.delete()
        game()
    else:
        scene.pause("Game over!")
        scene.delete()
        game()
        
game()

