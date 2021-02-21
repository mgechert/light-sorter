from random import randrange

class Unscrambler:
    def __init__(self, scrambler):
        self.scrambler = scrambler

    def quicksort(self, row):
        arr = self.scrambler.matrix[row]
        def swap(i, j):
            self.scrambler.swap_pix(row, i, j)

        def qs(start, end):
            if start >= end:
                return

            # Pick a pivot randomly and swap it to the end
            swap(randrange(start, end), end-1)
            piv = arr[end-1]
            i = start
            for j in range(start, end):
                if arr[j] < piv:
                    swap(i, j)
                    i += 1
            swap(i, end-1)
            qs(start, i)
            qs(i+1, end)
        
        qs(0, len(arr))