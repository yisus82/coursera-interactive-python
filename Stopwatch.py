# template for "Stopwatch: The Game"

# Import modules
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# define global variables
started = False
attempts = 0
points = 0
tenths = 0
score = "0/0"
time = "0:00.0"


# define helper function format that converts integer
# counting tenths of seconds into formatted string A:BC.D
def format(t):
    global time
    d = str(t % 10)
    seconds = t // 10
    bc = seconds % 60
    if bc < 10:
        b = "0"
        c = str(bc)
    else:
        b = str(bc)[0]
        c = str(bc)[1]
    a = str(seconds // 60)
    time = a + ":" + b + c + "." + d


# Helper functions
def update_score():
    """ Updates the score string. """
    global score, points, attemps
    score = str(points) + "/" + str(attempts)


# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    """ Starts the given timer (only if it's not started yet). """
    global timer, started
    if not started:
        # Starts the timer
        timer.start()
        started = True


def stop():
    """ Stops the given timer (only if it's started). """
    global timer, started, attempts, points
    if started:
        # Stops the timer
        timer.stop()
        started = False
        # Increments the number of attemps
        attempts = attempts + 1
        # If it's a whole second increments the number of points
        if (tenths % 10 == 0):
            points = points + 1
        update_score()


def reset():
    """ Stops the given timer and reset all the global variables. """
    # Stops the timer
    global timer, started, attempts, points, tenths
    timer.stop()
    started = False
    attempts = 0
    points = 0
    update_score()
    tenths = 0
    format(tenths)


# define event handler for timer with 0.1 sec interval
def tick():
    """ Increments the tenths of second. """
    global tenths
    tenths = tenths + 1
    format(tenths)


# Handler to draw on canvas
def draw(canvas):
    canvas.draw_text(score, (75, 25), 18, "Green")
    canvas.draw_text(time, (50, 100), 26, "White")


# create frame
frame = simplegui.create_frame("Stopwatch: The Game", 200, 200)

# register event handlers
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, tick)
frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)

# start frame
frame.start()
