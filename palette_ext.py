from displayio import Palette

class PaletteExt:
    # Wrapper for displayio.Palette to add white and black
    def __init__(self, color_count):
        self.palette = Palette(color_count+2)
        self.WHITE = color_count + 1
        self.palette[self.WHITE] = 0xffffff
        self.BLACK = color_count
        self.palette[self.BLACK] = 0x000000
    
    def __setitem__(self, key, newvalue):
        self.palette[key] = newvalue

