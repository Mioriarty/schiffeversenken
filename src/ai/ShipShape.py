class ShipShape:

    HORIZONTAL = 0
    VERTICAL = 1

    def __init__(self, length : int, cell : tuple[int], orientation : int):
        self.length = length
        self.cell = cell
        self.orientation = orientation

    def occupiedTiles(self) -> list[tuple[int]]:
        tiles = []
        if self.orientation == ShipShape.HORIZONTAL:
            for i in range(self.length):
                tiles.append((self.cell[0] + i, self.cell[1]))
        elif self.orientation == ShipShape.VERTICAL:
            for i in range(self.length):
                tiles.append((self.cell[0], self.cell[1] + i))
        return tiles
    
    def blockedTiles(self) -> list[tuple[int]]:
        tiles = []
        if self.orientation == ShipShape.HORIZONTAL:
            for i in range(-1, self.length + 1):
                tiles.append((self.cell[0] + i, self.cell[1]))
                tiles.append((self.cell[0] + i, self.cell[1] - 1))
                tiles.append((self.cell[0] + i, self.cell[1] + 1))
        elif self.orientation == ShipShape.VERTICAL:
            for i in range(-1, self.length + 1):
                tiles.append((self.cell[0], self.cell[1] + i))
                tiles.append((self.cell[0] - 1, self.cell[1] + i))
                tiles.append((self.cell[0] + 1, self.cell[1] + i))
        return tiles
    
    def interferesWith(self, other : 'ShipShape') -> bool:
        blockedTiles = self.blockedTiles()
        for otherTile in other.occupiedTiles():
            if otherTile in blockedTiles:
                return True
        return False
    
    def isInBoardBounds(self, boardWidth : int, boardHeight : int) -> bool:
        if self.cell[0] < 0 or self.cell[1] < 0:
            return False

        if self.orientation == ShipShape.HORIZONTAL:
            boardWidth -= self.length
        elif self.orientation == ShipShape.VERTICAL:
            boardHeight -= self.length
        
        return self.cell[0] <= boardWidth and self.cell[1] <= boardHeight
