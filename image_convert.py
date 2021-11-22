import png

# Example code from Tutorial for Raspberry Pi Pico Games using Sprites
# http://www.penguintutor.com/programming/picogamesprites

infile = "./assets/picochu-sprite-06.png"
# output sprite file
outfile = "picochu-sprite-06.spr"


def color_to_bytes(color):
    r, g, b = color
    arr = bytearray(2)
    arr[0] = r & 0xF8
    arr[0] += (g & 0xE0) >> 5
    arr[1] = (g & 0x1C) << 3
    arr[1] += (b & 0xF8) >> 3
    return arr


png_reader = png.Reader(infile)
image_data = png_reader.asRGBA8()

with open(outfile, "wb") as file:
    print("PNG file \nwidth {}\nheight {}\n".format(image_data[0], image_data[1]))
    # First two bytes are width & height
    file.write(bytes([image_data[0]]))
    file.write(bytes([image_data[1]]))

    for row in image_data[2]:
        for r, g, b, a in zip(row[::4], row[1::4], row[2::4], row[3::4]):
            # print ("This pixel {:02x}{:02x}{:02x} {:02x}".format(r, g, b, a))
            # Special case if transparency is less than 128 (half transparency)
            # then use both bytes as zero
            img_bytes = bytearray(2)

            if a < 128:
                img_bytes[0] = 0
                img_bytes[1] = 0
            else:
                # convert to (RGB565)
                img_bytes = color_to_bytes((r, g, b))
                # if [0,0] then change otherwise transparent
                if img_bytes[0] == 0 and img_bytes[1] == 0:
                    # Add 1 to value of blue (least noticeable)
                    img_bytes[1] = 32

            file.write(img_bytes)

file.close()
