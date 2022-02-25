from ai.Board import Board
from ai.ShipShape import ShipShape

# by: https://www.youtube.com/watch?v=Sef2-aHGZDU
class ProAi:

    def __init__(self):
        self.propabilities = None
    
    def update(self, board : Board, numShips : dict[int, int]) -> None:
        possibleShipLocations = self.__getAllPossibleShipLocations(board)
        

        self.propabilities = [ [0 for _ in range(board.width) ] for _ in range(board.height) ]

        for (length, count) in numShips.items():
            if count == 0:
                continue
                
            props = self.__cellPropsForShip(board, possibleShipLocations, length)

            for (x, y) in board.orderedIndex():
                self.propabilities[x][y] += props[x][y] * count
        

    def __cellPropsForShip(self, board : Board, possibleShipLocations : list[tuple[int]], length : int) -> list[list[float]]:
        orientations = [ ShipShape.VERTICAL, ShipShape.HORIZONTAL ]
        props = [ [0 for _ in range(board.width) ] for _ in range(board.height) ]
        placementCount = 0

        for (x, y) in possibleShipLocations:
            for orientation in orientations:
                tempShip = ShipShape(length, (x, y), orientation)

                # is the ship on the board
                if not tempShip.isInBoardBounds(board.width, board.height):
                    continue

                # check if it matches the boards requirements
                if not all(board.check(tile, Board.NO_INFO) for tile in tempShip.occupiedTiles()):
                    continue
                    
                # register ship
                placementCount += 1
                for (shipX, shipY) in tempShip.occupiedTiles():
                    props[shipX][shipY] += 1
        
        if placementCount == 0:
            raise ValueError(f"Ship of length {length} coudnt be placed on the board")

        
        # normalize everything to 1
        for (x, y) in board.orderedIndex():
            props[x][y] = (props[x][y] / placementCount)**2
        
        return props

    def __getAllPossibleShipLocations(self, board : Board) -> list[tuple[int]]:
        return [ (x, y) for x, y in board.orderedIndex() if board.check((x, y), Board.NO_INFO) and (board.check((x+1, y), Board.NO_INFO) or board.check((x, y+1), Board.NO_INFO)) ]
    
    def getNextShot(self, board : Board, numShips : dict[int, int]) -> tuple[int]:
        self.update(board, numShips)

        bestProp = -1
        bestCell = (-1, -1)

        for (x, y) in board.shuffledIndex():
            if self.propabilities[x][y] > bestProp:
                bestProp = self.propabilities[x][y]
                bestCell = (x, y)
        
        return bestCell