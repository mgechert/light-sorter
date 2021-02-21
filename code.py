import time
import board
from displayio import TileGrid, Group, release_displays
import gc
from scrambler import Scrambler
from unscrambler import Unscrambler
from adafruit_matrixportal.matrixportal import MatrixPortal

from random import randrange

# Display width and height
WIDTH = 64
HEIGHT = 64

def log_free_mem(txt="Memory free"):
    print(f"mem_free() {txt} {gc.mem_free()} bytes")

# Initialize board
mp = MatrixPortal(
    status_neopixel=board.NEOPIXEL,
    debug=True,
    width=WIDTH,
    height=HEIGHT,
)

# Rotate so the board overhangs the "bottom"
mp.display.rotation = 270

# Test loading and displaying a scrambled image
log_free_mem('after init')
scrambler, palext = Scrambler.load_bitmap('./images/rainbow2.bmp')
log_free_mem('Img loaded')
gc.collect()
log_free_mem('garbage collect')
tile_grid = TileGrid(scrambler.bitmap, pixel_shader=palext.palette)
group = Group()
group.append(tile_grid)
mp.display.show(group)

unscrambler = Unscrambler(scrambler, step_time=0.01)
log_free_mem('unscrambler init')

# Test unscrambling w/quicksort
for r in range(HEIGHT):
    unscrambler.quicksort(r)
    gc.collect()
    log_free_mem(f'{r+1} rows unscrambled')

# Turn it off after 15s so it doesn't glare in my eyes...
# time.sleep(15.0)
# release_displays()

while True:
    pass

