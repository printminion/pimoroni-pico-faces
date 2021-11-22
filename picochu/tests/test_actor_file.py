from PIL import Image
from picochu.sprite_file import SpriteFile

display_width = 320
display_height = 240

display_buffer_size = display_width * display_height * 2
display_buffer = bytearray([150] * display_buffer_size)


class Display:
    def __init__(self, width, height):
        self.display_width = width
        self.display_height = height

    def get_width(self):
        return self.display_width

    def get_height(self):
        return self.display_height


display = Display(display_width, display_height)

sprite = SpriteFile(display)
sprite.image = "../picochu-sprite-04.spr"
sprite.draw(display_buffer, topleft_x=65, topleft_y=105)

image = Image.frombuffer("RGB", (display_width, display_height), bytes(display_buffer), "raw", "BGR;16", 0, 1)

image.save("test_actor_file.png")
image.show()
