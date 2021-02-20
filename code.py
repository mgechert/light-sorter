import time
import board
import displayio
import random
import adafruit_imageload
from adafruit_matrixportal.matrixportal import MatrixPortal

# Display width and height
WIDTH = 64
HEIGHT = 64

# --- Display setup ---
mp = MatrixPortal(
    status_neopixel=board.NEOPIXEL,
    debug=True,
    width=WIDTH,
    height=HEIGHT,
)

def load_bmp(bmp_file):
    # Load the BMP and palette from file
    src_bmp, src_pal = adafruit_imageload.load(
        bmp_file,
        bitmap=displayio.Bitmap,
        palette=displayio.Palette,
    )

    # Create a bitmap + palette 2 colors larger (so we always white + black)
    out_bmp = displayio.Bitmap(src_bmp.width, src_bmp.height, len(src_pal)+2)
    out_pal = displayio.Palette(len(src_pal)+2)
    out_pal[len(src_pal)+1] = 0xffffff
    out_pal[len(src_pal)] = 0x000000
    for i in range(len(src_pal)):
        out_pal[i] = src_pal[i]
    for i in range(src_bmp.width * src_bmp.height):
        out_bmp[i] = src_bmp[i]

    return out_bmp, out_pal

def swap_pixels(row, i, j, bitmap, palette):
    print(f'Swap row {row} cols {i} and {j}')
    i_old = bitmap[i,row]
    j_old = bitmap[j,row]

    # Flash the pixels to be swapped white, then black
    bitmap[i,row] = bitmap[j,row] = len(palette)-1
    time.sleep(0.5)
    bitmap[i,row] = bitmap[j,row] = len(palette)-2
    time.sleep(0.5)

    bitmap[i,row] = j_old
    bitmap[j,row] = i_old

bmp, pal = load_bmp('./images/rainbow3.bmp')
tile_grid = displayio.TileGrid(bmp, pixel_shader=pal)
group = displayio.Group()
group.append(tile_grid)
mp.display.show(group)

while True:
    swap_pixels(
        row=random.randrange(HEIGHT),
        i=random.randrange(WIDTH),
        j=random.randrange(WIDTH),
        bitmap=bmp,
        palette=pal
    )
