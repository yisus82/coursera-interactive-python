# implementation of Spaceship - program template for RiceRocks
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import random

# globals for user interface
width = 800
height = 600
score = 0
lives = 3
time = 0
started = False

# points added to score when a missile hits a rock
rock_points = 10
# minimum distance from the ship for a spawned rock
min_dist_to_ship = 100
# points to increment velocity of rocks
points_per_level = 100


class ImageInfo:
    def __init__(self, center, size, radius=0, lifespan=None, animated=False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5, 5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")


# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]


def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def draw(self, canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]],
                              self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        # canvas.draw_circle(self.pos, self.radius, 1, "White", "White")

    def update(self):
        # update angle
        self.angle += self.angle_vel

        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % width
        self.pos[1] = (self.pos[1] + self.vel[1]) % height

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1

        self.vel[0] *= .99
        self.vel[1] *= .99

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()

    def increment_angle_vel(self):
        self.angle_vel += .05

    def decrement_angle_vel(self):
        self.angle_vel -= .05

    def shoot(self):
        # global a_missile
        global missile_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    # Sprite class


class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound=None):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0] * self.age, self.image_center[1]],
                              self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)

    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius

    def collide(self, other_object):
        return (dist(self.get_position(), other_object.get_position()) < (
                    self.get_radius() + other_object.get_radius()))

    def update(self):
        # update angle
        self.angle += self.angle_vel

        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % width
        self.pos[1] = (self.pos[1] + self.vel[1]) % height

        # update age
        self.age += 1
        if self.age < self.lifespan:
            return True
        else:
            return False


# helper function to check for collisions between other_object and every element of group
def group_collide(group, other_object):
    global explosion_group
    remove = set([])
    collisions = 0
    for obj in group:
        if obj.collide(other_object):
            remove.add(obj)
            collisions += 1
            a_explosion = Sprite(obj.get_position(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(a_explosion)
            # if ship collides, generate an extra explosion
            if type(other_object) is type(my_ship):
                a_explosion = Sprite(other_object.get_position(), [0, 0], 0, 0, explosion_image, explosion_info,
                                     explosion_sound)
                explosion_group.add(a_explosion)
    group.difference_update(remove)
    return collisions


# helper function to check for collisions between other_group and every element of group
def group_group_collide(group, other_group):
    remove = set([])
    collisions = 0
    for object in group:
        col = group_collide(other_group, object)
        if col > 0:
            collisions += col
            remove.add(object)
    group.difference_update(remove)
    return collisions


# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()


def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)


# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, timer
    center = [width / 2, height / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        start()


# helper function to start the game
def start():
    global score, lives
    score = 0
    lives = 3
    timer.start()
    soundtrack.play()


# helper function to call the update and draw methods for each sprite in the group     
def process_sprite_group(canvas, sprite_group):
    remove = set([])
    for sprite in sprite_group:
        if sprite.update():
            sprite.draw(canvas)
        else:
            remove.add(sprite)
    sprite_group.difference_update(remove)


def draw(canvas):
    global time, started, lives, score

    # animate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [width / 2, height / 2],
                      [width, height])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]],
                      [width / 2 + 1.25 * wtime, height / 2], [width - 2.5 * wtime, height])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]],
                      [1.25 * wtime, height / 2], [2.5 * wtime, height])

    # draw ship
    my_ship.draw(canvas)
    # a_rock.draw(canvas)
    # a_missile.draw(canvas)

    # update ship
    my_ship.update()
    # a_rock.update()
    # a_missile.update()

    # process sprites
    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)
    process_sprite_group(canvas, explosion_group)

    # check if missiles collide with rocks
    score += group_group_collide(missile_group, rock_group) * rock_points

    # check if ship collides with rocks
    lives -= group_collide(rock_group, my_ship)
    if lives < 1:
        init()

    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [width / 2, height / 2],
                          splash_info.get_size())


# timer handler that spawns a rock    
def rock_spawner():
    # global a_rock
    global rock_group
    if len(rock_group) < 12:
        rock_pos = [random.randrange(0, width), random.randrange(0, height)]
        # if rock is too close to the ship generate a new rock_pos
        while dist(rock_pos, my_ship.get_position()) < min_dist_to_ship:
            rock_pos = [random.randrange(0, width), random.randrange(0, height)]
        rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
        # increments velocity based on score
        rock_vel = [rock_vel[0] * (1 + score / points_per_level), rock_vel[1] * (1 + score / points_per_level)]
        rock_avel = random.random() * .2 - .1
        a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
        rock_group.add(a_rock)


# initialize stuff
frame = simplegui.create_frame("Asteroids", width, height)


# helper function to initialize ship and sprite groups
def init():
    global my_ship, rock_group, missile_group, explosion_group, started
    my_ship = Ship([width / 2, height / 2], [0, 0], 0, ship_image, ship_info)
    # a_rock = Sprite([width / 3, height / 3], [1, 1], 0, .1, asteroid_image, asteroid_info)
    rock_group = set([])
    # a_missile = Sprite([2 * width / 3, 2 * height / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
    missile_group = set([])
    explosion_group = set([])
    started = False
    timer.stop()
    soundtrack.pause()
    soundtrack.rewind()


# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
# timer.start()
frame.start()
init()
