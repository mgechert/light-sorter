import time
import board
from displayio import TileGrid, Group
import gc
from scrambler import Scrambler
from adafruit_matrixportal.matrixportal import MatrixPortal

# Display width and height
WIDTH = 64
HEIGHT = 64

# --- Board setup ---
mp = MatrixPortal(
    status_neopixel=board.NEOPIXEL,
    debug=True,
    width=WIDTH,
    height=HEIGHT,
)

def log_free_mem(txt="Memory free"):
    print(f"mem_free() {txt} {gc.mem_free()} bytes")

# def load_scrambled_bmp(file):
#     return adafruit_imageload.load(
#         file,
#         bitmap=Scrambler,
#         palette=displayio.Palette,
#     )


log_free_mem('after init')
scrambler, palette = Scrambler.load_bitmap('./images/rainbow2.bmp')
log_free_mem('Img loaded')
gc.collect()
log_free_mem('garbage collect')
tile_grid = TileGrid(scrambler.bitmap, pixel_shader=palette)
group = Group()
group.append(tile_grid)
mp.display.show(group)

# Turn it off after 15s so it doesn't glare in my eyes...
time.sleep(15.0)
displayio.release_displays()

while True:
    pass