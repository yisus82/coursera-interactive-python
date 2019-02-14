# implementation of card game - Memory

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random


# helper function to initialize globals
def init():
    global cards, exposed, state, moves
    cards = [i % 8 for i in range(16)]
    random.shuffle(cards)
    exposed = []
    state = 0
    moves = 0


# define event handlers
def mouseclick(pos):
    global moves, state, exposed
    i = pos[0] // 50
    if i not in exposed:
        if state == 0:
            state = 1
            exposed.append(i)
        elif state == 1:
            state = 2
            moves += 1
            exposed.append(i)
        else:
            state = 1
            if cards[exposed[-1]] != cards[exposed[-2]]:
                exposed.pop()
                exposed.pop()
            exposed.append(i)


# cards are logically 50x100 pixels in size    
def draw(canvas):
    label.set_text("Moves = " + str(moves))
    for i in range(16):
        if i in exposed:
            canvas.draw_polygon([[50 * i, 0], [50 * i, 100], [50 * (i + 1), 100], [50 * (i + 1), 0]], 1, "Red")
            canvas.draw_text(str(cards[i]), [50 * i + 15, 60], 32, "White")
        else:
            canvas.draw_polygon([[50 * i, 0], [50 * i, 100], [50 * (i + 1), 100], [50 * (i + 1), 0]], 1, "Red", "Green")


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
label = frame.add_label("Moves = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()
