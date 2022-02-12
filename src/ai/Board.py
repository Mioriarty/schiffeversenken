import random
from typing import Generator


class Board:

    # internal values
    NO_INFO         = 0b00001
    CHECKED_NO_SHIP = 0b00010
    DEDUSED_NO_SHIP = 0b00100
    SHIP            = 0b01000
    SHIP_LIKELY     = 0b10000

    # values to submit
    SUBMIT_SHIP    = SHIP
    SUBMIT_NO_SHIP = CHECKED_NO_SHIP

    def __init__(self, width : int, height : int):
        self.width = width
        self.height = height

        self.data = [[Board.NO_INFO for _ in range(width)] for _ in range(height)]
    
    def __getitem__(self, cell : tuple[int]) -> int:
        return self.data[cell[0]][cell[1]]
    
    def __setitem__(self, cell : tuple[int], newVal : int) -> None:
        self.data[cell[0]][cell[1]] = newVal
    
    def check(self, cell : tuple[int], value : int) -> bool:
        return self.isInBounds(cell) and bool(self[cell] & value)
    
    def isInBounds(self, cell : tuple[int]) -> bool:
        return cell[0] >= 0 and cell[1] >= 0 and cell[0] < self.width and cell[1] < self.height

    def shuffledIndex(self) -> Generator[tuple[int], None, None]:
        for y in random.sample(list(range(self.height)), self.height):
            for x in random.sample(list(range(self.width)), self.width):
                yield (x, y)
    
    def orderedIndex(self) -> Generator[tuple[int], None, None]:
        for y in range(self.height):
            for x in range(self.width):
                yield (x, y)

    def print(self):
        for y in range(self.height):
            for x in range(self.width):
                val = self.data[x][y]

                if val == Board.NO_INFO:
                    print(".", end="")
                elif val == Board.CHECKED_NO_SHIP:
                    print("x", end="")
                elif val == Board.DEDUSED_NO_SHIP:
                    print("o", end="")
                elif val == Board.SHIP:
                    print("S", end="")
                elif val == Board.SHIP_LIKELY:
                    print("?", end="")
                else:
                    print("!", end="")
            print()
    


    