# Display different sprites by clicking Pico Display's buttons
# with a loop that checks to see if buttons are pressed.

# import picodisplay as display  # Comment this line out to use PicoDisplay
import picodisplay2 as display  # Uncomment this line to use PicoDisplay2
import utime
import time
import gc

from sprite_file import SpriteFile

print("%sx%s" % (display.get_width(), display.get_height()))
print("Free memory: %s" % gc.mem_free())

# Initialise display with a bytearray display buffer
display_buffer_size = display.get_width() * display.get_height() * 2
display_buffer = bytearray(display_buffer_size)

display.init(display_buffer)
display.set_backlight(0.4)
current_sprite = 0
sprites = [
    {"name": "picochu-sprite-05.spr", "left": 138, "top": 106},
    {"name": "picochu-sprite-01.spr", "left": 99, "top": 105},
    {"name": "picochu-sprite-02.spr", "left": 84, "top": 106},
    {"name": "picochu-sprite-03.spr", "left": 78, "top": 98},
    {"name": "picochu-sprite-04.spr", "left": 62, "top": 106},
    {"name": "picochu-sprite-06.spr", "left": 138, "top": 105},
    {"name": "picochu-sprite-07.spr", "left": 112, "top": 106},
    {"name": "picochu-sprite-08.spr", "left": 72, "top": 106},
]


# sets up a handy function we can call to clear the screen
def clear():
    display.set_pen(255, 211, 62)
    display.clear()
    display.update()


clear()  # clear

display.set_pen(255, 0, 0)
sprite = SpriteFile(display)


# This is based on a binary image file (RGB565) with the same dimensions as the screen

def display_next_sprite():
    global current_sprite, sprites
    print("display_next_sprite")
    next_sprite = current_sprite + 1

    if next_sprite >= len(sprites):
        next_sprite = 0

    display_sprite_by_id(next_sprite)


def display_previous_sprite():
    print("display_previous_sprite")
    global current_sprite, sprites
    next_sprite = current_sprite - 1

    if next_sprite < 0:
        next_sprite = len(sprites) - 1

    display_sprite_by_id(next_sprite)


def display_sprite_by_id(number):
    global current_sprite
    print("display_sprite_by_number: %s" % number)
    current_sprite = number
    sprite_to_display = sprites[number]
    display_sprite(
        filename=sprite_to_display.get("name"),
        topleft_x=sprite_to_display.get("left"),
        topleft_y=sprite_to_display.get("top")
    )
    # display current sprite id
    display.set_pen(0, 0, 0)
    display.text("%s:" % number, 2, 230, display.get_width(), 1)
    display.update()


def display_sprite(filename, topleft_x=0, topleft_y=0):
    global sprite
    print("display_sprite[%s]: %sx%s" % (filename, topleft_x, topleft_y))
    clear()
    display.set_pen(0, 0, 0)
    display.text("Button Y pressed", 10, 10, 240, 4)
    display.update()
    sprite.image = filename
    clear()  # clear again
    start = time.time()
    print("sprite.draw:before: %s [left:%s top:%s]" % (filename, topleft_x, topleft_y))
    sprite.draw(display_buffer, topleft_x, topleft_y)
    end = time.time()
    print("sprite.draw:after")
    elapsed_time = str(end - start)
    print("elapsed time: %s" % elapsed_time)  # Time in seconds, e.g. 5.38091952400282

    # display estimated time
    display.set_pen(0, 0, 0)
    display.text(elapsed_time, 10, 230, display.get_width(), 1)

    # display logo
    display.text("@printminion", 249, 230, display.get_width(), 1)
    display.update()


display_sprite_by_id(0)
display.set_pen(255, 0, 0)

while True:
    if display.is_pressed(display.BUTTON_A):  # if a button press is detected then...
        print("BUTTON_A")
        display_previous_sprite()
    elif display.is_pressed(display.BUTTON_B):
        print("display.BUTTON_B")
        display_sprite("picochu-sprite-02.spr", topleft_x=84, topleft_y=106)
    elif display.is_pressed(display.BUTTON_X):
        print("display.BUTTON_X")
        display_next_sprite()
    elif display.is_pressed(display.BUTTON_Y):
        print("display.BUTTON_Y")
        display_sprite("picochu-sprite-04.spr", topleft_x=62, topleft_y=105)

    utime.sleep(0.1)  # this number is how frequently the Pico checks for button presses
