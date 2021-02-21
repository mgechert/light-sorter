import adafruit_imageload
from displayio import Bitmap, Palette
from random import randrange

class Scrambler:
    def __init__(self, width, height, value_count):
        self.bitmap = Bitmap(width, height, value_count)
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
        # matrix[row][col] has the scrambled column index
        self.bitmap[self.matrix[row][col], row] = newvalue

    @classmethod
    def load_bitmap(cls, file):
        return adafruit_imageload.load(
            file,
            bitmap=cls,
            palette=Palette,
        )

    def swap_pix(self, row, i, j):
        if i == j:
            return
        self.matrix[row][i], self.matrix[row][j] = self.matrix[row][j], self.matrix[row][i]
        self.bitmap[i, row], self.bitmap[j, row] = self.bitmap[j, row], self.bitmap[i, row]

    

    