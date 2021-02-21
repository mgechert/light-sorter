import adafruit_imageload
from displayio import Bitmap, Palette
from palette_ext import PaletteExt
from random import randrange
from time import sleep

class Scrambler:
    def __init__(self, width, height, value_count):
        self.bitmap = Bitmap(width, height, value_count+2)
        # PaletteExt appends black and white to the palette
        self.BLACK = value_count
        self.WHITE = value_count + 1
      self.matrix = []
        for row in range(height):
            self.matrix.append(bytearray())
            nums = list(range(width))
            while len(nums) > 0:
                self.matrix[row].append(nums.pop(randrange(len(nums))))
    
    def __setitem__(self, key, newvalue):
        if type(key) == int:
            col = key % self.bitmap.width
            row = key // self.bitmap.width    
        elif type(key) == tuple:
            col, row = key
        else:
            raise ValueError()
        # matrix[row].index(col) is the "scrambled" column index
        new_col = self.matrix[row].index(bytes([col]))
        self.bitmap[new_col, row] = newvalue

    @classmethod
    def load_bitmap(cls, file):
        return adafruit_imageload.load(
            file,
            bitmap=cls,
            palette=PaletteExt,
        )

    def swap_cols(self, row, i, j):
        if i == j:
            return

        i_new, j_new = self.bitmap[j, row], self.bitmap[i, row]
        # Blink the pixels before swapping them
        for _ in range(3):
            self.bitmap[i, row] = self.bitmap[j, row] = self.BLACK
            sleep(0.1)
            self.bitmap[i, row] = self.bitmap[j, row] = self.WHITE
            sleep(0.05)

        self.matrix[row][i], self.matrix[row][j] = self.matrix[row][j], self.matrix[row][i]
        self.bitmap[i, row], self.bitmap[j, row] = i_new, j_new