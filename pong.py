# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
PAD_SPEED = 4
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

# this sets where the ball begins in the middle of the court
ball_pos = [WIDTH / 2, HEIGHT / 2]

# this sets the initial velocity of the ball
ball_vel = [0, 0]

# this sets where the paddles begin and that they begin stationary
paddle1_pos = 0
paddle2_pos = 0

paddle1_vel = 0
paddle2_vel = 0

# this sets the initial score to zero to zero

score1 = 0
score2 = 0

# helper function that spawns a ball by updating the 
# ball's position vector and velocity vector
# if right is True, the ball's velocity is upper right, else upper left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_pos = [WIDTH / 2, HEIGHT / 2]

    horz_speed = random.randrange(120, 240)
    vert_speed = random.randrange(60, 180)
    
    if right:
        ball_vel = [-(horz_speed / 60), -(vert_speed / 60)]
    else:
        ball_vel = [(horz_speed / 60), -(vert_speed / 60)]

# define event handlers

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2  # these are ints

    ball_init(True)
    
    score1 = 0
    score2 = 0
    
    paddle1_pos = (HEIGHT - PAD_HEIGHT) / 2
    paddle2_pos = (HEIGHT - PAD_HEIGHT) / 2
        
def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    right = True
    
    # update paddle's vertical position

    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel

    # keep paddles on the screen
    
    if paddle1_pos > (HEIGHT - PAD_HEIGHT):
        paddle1_pos = (HEIGHT - PAD_HEIGHT)
    elif paddle1_pos < 0:
        paddle1_pos = 0
        
    if paddle2_pos > (HEIGHT - PAD_HEIGHT):
        paddle2_pos = (HEIGHT - PAD_HEIGHT)
    elif paddle2_pos < 0:
        paddle2_pos = 0
    
    # draw mid line and gutters
    
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw paddles
    
    c.draw_line([HALF_PAD_WIDTH, paddle1_pos],[HALF_PAD_WIDTH, paddle1_pos + PAD_HEIGHT], PAD_WIDTH, "White")
    c.draw_line([WIDTH - HALF_PAD_WIDTH, paddle2_pos],[WIDTH - HALF_PAD_WIDTH, paddle2_pos + PAD_HEIGHT], PAD_WIDTH, "White")    
 
    # update ball
    
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # check for ends hitting and reverse direction
    
    if ball_pos[0] > (WIDTH - BALL_RADIUS - PAD_WIDTH):
        if (ball_pos[1] - paddle2_pos) < PAD_HEIGHT and (ball_pos[1] - paddle2_pos) > 0:
            ball_vel[0] = -1.1 * ball_vel[0]
            ball_vel[1] = 1.1 * ball_vel[1]
        else:
            score1 += 1
            ball_init(True)
        
    elif ball_pos[0] < (BALL_RADIUS + PAD_WIDTH): #ball hit left gutter
        if (ball_pos[1] - paddle1_pos) < PAD_HEIGHT and (ball_pos[1] - paddle1_pos) > 0:
            ball_vel[0] = - 1.1 * ball_vel[0]
            ball_vel[1] = 1.1 * ball_vel[1]
        else:
            score2 += 1
            ball_init(False)
            
    # check for top wall hitting and reverse direction
    
    if ball_pos[1] > (HEIGHT - BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
    elif ball_pos[1] < BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
            
    # draw ball and scores
    
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    c.draw_text(str(score1),[150, 60], 50, "White", "monospace")
    c.draw_text(str(score2),[430, 60], 50, "White", "monospace")
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    #controls velocity of right paddle
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel += PAD_SPEED
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel -= PAD_SPEED
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel += PAD_SPEED
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel -= PAD_SPEED
   
def keyup(key):
    global paddle1_vel, paddle2_vel

    if key == simplegui.KEY_MAP['down']:
        paddle2_vel -= PAD_SPEED
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel += PAD_SPEED
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel -= PAD_SPEED
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel += PAD_SPEED
        
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button("Reset Game", new_game)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# start frame
frame.start()
new_game()
