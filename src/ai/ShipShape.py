
from typing import Generator


class ShipRect:
    
    def __init__(self, left : int, right : int, top : int, bottom : int):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    def collidesWith(self, other : 'ShipRect') -> bool:
        return self.left <= other.right and self.right >= other.left and self.top <= other.bottom and self.bottom >= other.top
    
    def includesPoint(self, point : tuple[int]) -> bool:
        return self.left <= point[0] <= self.right and self.top <= point[1] <= self.bottom

class ShipShape:

    HORIZONTAL = 0
    VERTICAL = 1

    def __init__(self, length : int, cell : tuple[int], orientation : int):
        self.length = length
        self.cell = cell
        self.orientation = orientation
    
    def getOccupiedRect(self) -> ShipRect:
        if self.orientation == ShipShape.HORIZONTAL:
            return ShipRect(self.cell[0], self.cell[0] + self.length - 1, self.cell[1], self.cell[1])
        else:
            return ShipRect(self.cell[0], self.cell[0], self.cell[1], self.cell[1] + self.length - 1)
    
    def getBlockedRect(self) -> ShipRect:
        if self.orientation == ShipShape.HORIZONTAL:
            return ShipRect(self.cell[0] - 1, self.cell[0] + self.length, self.cell[1] - 1, self.cell[1] + 1)
        else:
            return ShipRect(self.cell[0] - 1, self.cell[0] + 1, self.cell[1] - 1, self.cell[1] + self.length)


    def occupiedTiles(self) -> Generator[tuple[int], None, None]:
        if self.orientation == ShipShape.HORIZONTAL:
            for i in range(self.length):
                yield (self.cell[0] + i, self.cell[1])
        elif self.orientation == ShipShape.VERTICAL:
            for i in range(self.length):
                yield (self.cell[0], self.cell[1] + i)
    
    def blockedTiles(self) -> Generator[tuple[int], None, None]:
        tiles = []
        if self.orientation == ShipShape.HORIZONTAL:
            for i in range(-1, self.length + 1):
                yield (self.cell[0] + i, self.cell[1])
                yield (self.cell[0] + i, self.cell[1] - 1)
                yield (self.cell[0] + i, self.cell[1] + 1)
        elif self.orientation == ShipShape.VERTICAL:
            for i in range(-1, self.length + 1):
                yield (self.cell[0], self.cell[1] + i)
                yield (self.cell[0] - 1, self.cell[1] + i)
                yield (self.cell[0] + 1, self.cell[1] + i)
        return tiles
    
    def interferesWith(self, other : 'ShipShape') -> bool:
        return self.getBlockedRect().collidesWith(other.getOccupiedRect())
    
    def isInBoardBounds(self, boardWidth : int, boardHeight : int) -> bool:
        if self.cell[0] < 0 or self.cell[1] < 0:
            return False

        if self.orientation == ShipShape.HORIZONTAL:
            boardWidth -= self.length
        elif self.orientation == ShipShape.VERTICAL:
            boardHeight -= self.length
        
        return self.cell[0] <= boardWidth and self.cell[1] <= boardHeight

