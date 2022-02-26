
from typing import Generator


class ShipRect:
    """
    Represents a rect on the board. Usally used for ships.

    Attributes:
        left (int): x coordinate of the left side of the rect.
        right (int): x coordinate of the right side of the rect.
        top (int): y coordinate of the top side of the rect.
        bottom (int): y coordinate of the bottom side of the rect.
    """
    
    def __init__(self, left : int, right : int, top : int, bottom : int):
        """
        Constructor of the ShipRect class.

        Args:
            left (int): x coordinate of the left side of the rect.
            right (int): x coordinate of the right side of the rect.
            top (int): y coordinate of the top side of the rect.
            bottom (int): y coordinate of the bottom side of the rect.
        """
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    def collidesWith(self, other : 'ShipRect') -> bool:
        """
        Checks if the rect overlaps with another ShipRect.

        Args:
            other (ShipRect): Other ShipRect to be checked against

        Returns:
            bool: Whether the 2 rects overlap.
        """
        return self.left <= other.right and self.right >= other.left and self.top <= other.bottom and self.bottom >= other.top
    
    def includesPoint(self, point : tuple[int]) -> bool:
        """
        Checks if the point / cell is in the rect.

        Args:
            point (tuple[int]): Other point / cell to be checked against

        Returns:
            bool: Whether the point is included.
        """
        return self.left <= point[0] <= self.right and self.top <= point[1] <= self.bottom

class ShipShape:
    """
    Represents a possible Ship position.

    Attributes:
        length (int): Length of the ship.
        cell (tuple[int]): Cell coordinate of the top left most cell the ship lives in.
        orientation (int): Specefies how the ship is laying on the board. Either HORIZONTAL or VERTICAL
    """

    HORIZONTAL = 0
    VERTICAL = 1

    def __init__(self, length : int, cell : tuple[int], orientation : int):
        """
        Construcor of the ShipShape class.

        Args:
            length (int): Length of the ship.
            cell (tuple[int]): Cell coordinate of the top left most cell the ship lives in.
            orientation (int): Specefies how the ship is laying on the board. Either HORIZONTAL or VERTICAL
        """
        self.length = length
        self.cell = cell
        self.orientation = orientation
    
    def getOccupiedRect(self) -> ShipRect:
        """
        Returns the ShipRect that covers all tiles that lie in the ship.

        Returns:
            ShipRect: ShipRect that covers all tiles that lie in the ship.
        """
        if self.orientation == ShipShape.HORIZONTAL:
            return ShipRect(self.cell[0], self.cell[0] + self.length - 1, self.cell[1], self.cell[1])
        else:
            return ShipRect(self.cell[0], self.cell[0], self.cell[1], self.cell[1] + self.length - 1)
    
    def getBlockedRect(self) -> ShipRect:
        """
        Returns the ShipRect that covers all tiles that lie in the ship and all surrounding tiles. Including the diagonal ones.

        Returns:
            ShipRect: ShipRect that covers all tiles that lie in the ship and all surrounding tiles. Including the diagonal ones.
        """
        if self.orientation == ShipShape.HORIZONTAL:
            return ShipRect(self.cell[0] - 1, self.cell[0] + self.length, self.cell[1] - 1, self.cell[1] + 1)
        else:
            return ShipRect(self.cell[0] - 1, self.cell[0] + 1, self.cell[1] - 1, self.cell[1] + self.length)


    def occupiedTiles(self) -> Generator[tuple[int], None, None]:
        """
        Enables to loop through all tiles that lie in the ship.

        Yields:
            Generator[tuple[int], None, None]: All tiles that lie in the ship.
        """
        if self.orientation == ShipShape.HORIZONTAL:
            for i in range(self.length):
                yield (self.cell[0] + i, self.cell[1])
        elif self.orientation == ShipShape.VERTICAL:
            for i in range(self.length):
                yield (self.cell[0], self.cell[1] + i)
    
    def blockedTiles(self) -> Generator[tuple[int], None, None]:
        """
        Enables to loop through all tiles that lie in the ship and all surrounding tiles. Including the diagonal ones.

        Yields:
            Generator[tuple[int], None, None]: All tiles that lie in the ship and all surrounding tiles. Including the diagonal ones.
        """
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
        """
        Checks if a ShipShape lies in such a way that, it does cross the other ShipShape and is not in the surrounding tiles.

        Args:
            other (ShipShape): The other ShipShape to check against.

        Returns:
            bool: If a ShipShape lies in such a way that, it does cross the other ShipShape and is not in the surrounding tiles.
        """
        return self.getBlockedRect().collidesWith(other.getOccupiedRect())
    
    def isInBoardBounds(self, boardWidth : int, boardHeight : int) -> bool:
        """
        Checks whether the whole ship is in the bounds of a board.

        Args:
            boardWidth (int): Amount of columns of the board.
            boardHeight (int): Amount of rows of the board.

        Returns:
            bool: If the whole ship is in the bounds of a board.
        """
        if self.cell[0] < 0 or self.cell[1] < 0:
            return False

        if self.orientation == ShipShape.HORIZONTAL:
            boardWidth -= self.length
        elif self.orientation == ShipShape.VERTICAL:
            boardHeight -= self.length
        
        return self.cell[0] <= boardWidth and self.cell[1] <= boardHeight

