from displayio import Bitmap
import gc
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
        gc.collect()
    
    def __setitem__(self, key, newvalue):
        if type(key) == tuple:
            col, row = key
        elif type(key) == int:
            col = key % self.bitmap.width
            row = key // self.bitmap.width
        
        # matrix[row][col] has the scrambled column index
        self.bitmap[self.matrix[row][col], row] = newvalue