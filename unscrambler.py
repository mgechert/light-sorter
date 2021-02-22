from random import randrange

class Unscrambler:
    def __init__(self, scrambler):
        self.scrambler = scrambler

    def unscramble_row(self, row, sorter):
        def swap(i, j):
            self.scrambler.swap_cols(row, i, j)
        sorter(self.scrambler.matrix[row], swap)
        
    @classmethod
    def quicksort(cls, arr, swap):
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

    @classmethod
    def bubblesort(cls, arr, swap):
        for j in range(len(arr)):
            for i in range(len(arr)-j-1):
                if arr[i] > arr[i+1]:
                    swap(i, i+1)