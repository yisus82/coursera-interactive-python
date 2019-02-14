# Implementation of classic arcade game Pong

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
PADDLE_ACC = 4

# Variables
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0.0, 0.0]
paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT / 2
paddle1_vel = 0.0
paddle2_vel = 0.0
score1 = 0
score2 = 0


# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel  # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel[0] = - random.randrange(120, 240) / 60
    ball_vel[1] = - random.randrange(60, 180) / 60
    if right:
        ball_vel[0] = - ball_vel[0]


# Helper function to check collisions with the paddles
# It returns -1 when the vertical direction of the ball has to change
def check_collision(side):
    points = range(int(ball_pos[1]) - BALL_RADIUS, int(ball_pos[1]) + BALL_RADIUS)
    if side == "Left":
        for p in points:
            if (p >= paddle1_pos - PAD_HEIGHT / 2) and (p <= paddle1_pos + PAD_HEIGHT / 2):
                if ball_vel[1] < 0 and ball_pos[1] > paddle1_pos:
                    return -1
                elif ball_vel[1] > 0 and ball_pos[1] < paddle1_pos:
                    return -1
                return 1
    elif side == "Right":
        for p in points:
            if (p >= paddle2_pos - PAD_HEIGHT / 2) and (p <= paddle2_pos + PAD_HEIGHT / 2):
                if ball_vel[1] < 0 and ball_pos[1] > paddle2_pos:
                    return -1
                elif ball_vel[1] > 0 and ball_pos[1] < paddle2_pos:
                    return -1
                return 1
    return 0


# Helper function to update the ball
def update_ball():
    global score1, score2
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        col = check_collision("Left")
        if col != 0:
            ball_vel[0] = - ball_vel[0]
            ball_vel[1] = col * ball_vel[1]
            ball_vel[0] *= 1.1
            ball_vel[1] *= 1.1
            ball_pos[0] += ball_vel[0]
            ball_pos[1] += ball_vel[1]
        else:
            score2 += 1
            ball_init(True)
    elif ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
        col = check_collision("Right")
        if col != 0:
            ball_vel[0] = - ball_vel[0]
            ball_vel[1] = col * ball_vel[1]
            ball_vel[0] *= 1.1
            ball_vel[1] *= 1.1
            ball_pos[0] += ball_vel[0]
            ball_pos[1] += ball_vel[1]
        else:
            score1 += 1
            ball_init(False)
    elif (ball_pos[1] <= BALL_RADIUS) or (ball_pos[1] >= HEIGHT - BALL_RADIUS):
        ball_vel[1] = - ball_vel[1]
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]
    else:
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]


# Helper function to update the paddles
def update_paddles():
    global paddle1_pos, paddle2_pos
    if (paddle1_pos + paddle1_vel > PAD_HEIGHT / 2) and (paddle1_pos + paddle1_vel < HEIGHT - PAD_HEIGHT / 2):
        paddle1_pos += paddle1_vel
    elif paddle1_pos + paddle1_vel <= PAD_HEIGHT / 2:
        paddle1_pos = PAD_HEIGHT / 2
    elif paddle1_pos + paddle1_vel >= HEIGHT - PAD_HEIGHT / 2:
        paddle1_pos = HEIGHT - PAD_HEIGHT / 2
    if (paddle2_pos + paddle2_vel > PAD_HEIGHT / 2) and (paddle2_pos + paddle2_vel < HEIGHT - PAD_HEIGHT / 2):
        paddle2_pos += paddle2_vel
    elif paddle2_pos + paddle2_vel <= PAD_HEIGHT / 2:
        paddle2_pos = PAD_HEIGHT / 2
    elif paddle2_pos + paddle2_vel >= HEIGHT - PAD_HEIGHT / 2:
        paddle2_pos = HEIGHT - PAD_HEIGHT / 2


# define event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2  # these are ints
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    paddle1_vel = 0.0
    paddle2_vel = 0.0
    score1 = 0
    score2 = 0
    ball_init(True)


def draw(c):
    # update paddle's vertical position, keep paddle on the screen
    update_paddles()

    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # draw paddles
    tl1 = [0, paddle1_pos - PAD_HEIGHT / 2]
    tr1 = [PAD_WIDTH, paddle1_pos - PAD_HEIGHT / 2]
    bl1 = [0, paddle1_pos + PAD_HEIGHT / 2]
    br1 = [PAD_WIDTH, paddle1_pos + PAD_HEIGHT / 2]
    c.draw_polygon([tl1, bl1, br1, tr1], 1, "White", "White")
    tl2 = [WIDTH - PAD_WIDTH, paddle2_pos - PAD_HEIGHT / 2]
    tr2 = [WIDTH, paddle2_pos - PAD_HEIGHT / 2]
    bl2 = [WIDTH - PAD_WIDTH, paddle2_pos + PAD_HEIGHT / 2]
    br2 = [WIDTH, paddle2_pos + PAD_HEIGHT / 2]
    c.draw_polygon([tl2, bl2, br2, tr2], 1, "White", "White")

    # update ball
    update_ball()

    # draw ball and scores
    c.draw_circle(ball_pos, BALL_RADIUS, 12, "White", "White")
    c.draw_text(str(score1), [WIDTH / 4, 20], 20, "White")
    c.draw_text(str(score2), [3 * WIDTH / 4, 20], 20, "White")


def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["W"]:
        paddle1_vel = -PADDLE_ACC
    elif key == simplegui.KEY_MAP["S"]:
        paddle1_vel = PADDLE_ACC
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -PADDLE_ACC
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = PADDLE_ACC


def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["W"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["S"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", init, 100)

# start frame
init()
frame.start()
