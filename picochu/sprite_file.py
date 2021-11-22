# Inspired by Tutorial for Raspberry Pi Pico Games using Sprites
# http://www.penguintutor.com/programming/picogamesprites
class SpriteFile:
    height = None
    width = None
    filename = None

    def __init__(self, display):

        self.display = display

        # If enable then black is converted into transparency
        self.enable_transparency = True

    # Image property can be used to change the image
    # if use <instance>.image = newfile then it will load that file instead
    @property
    def image(self):
        return self.filename

    @image.setter
    def image(self, new_value):
        self.filename = new_value

    def draw(self, display_buffer, topleft_x=0, topleft_y=0):
        color_bytes = bytearray(2)
        with open(self.filename, "rb") as file:
            # skip sprite size data
            self.width = ord(file.read(1))
            self.height = ord(file.read(1))

            for y in range(0, self.height):
                # Check y is in range
                if topleft_y + y < 0 or topleft_y + y >= self.display.get_height():
                    continue
                # buffer pos of display
                display_buffer_pos = self.display_buffer_pos(topleft_x, topleft_y + y)
                for x in range(0, self.width):
                    # Check x is in range
                    if topleft_x + x < 0 or topleft_x + x >= self.display.get_width():
                        continue
                    color_bytes[0] = ord(file.read(1))
                    color_bytes[1] = ord(file.read(1))
                    # If transparent then don't copy
                    if self.enable_transparency and color_bytes[0] == 0 and color_bytes[1] == 0:
                        continue
                    display_buffer[display_buffer_pos + (x * 2)] = color_bytes[0]
                    display_buffer[display_buffer_pos + (x * 2) + 1] = color_bytes[1]

            file.close()

    # return buffer pos of a x,y coord
    def display_buffer_pos(self, x, y):
        buffer_pos = (x * 2) + (y * self.display.get_width() * 2)
        return buffer_pos
