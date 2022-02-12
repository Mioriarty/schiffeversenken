from ai.Board import Board
from ai.ShipPlacement import ShipPlacement
from ai.ShipShape import ShipShape
import random




class BruteForceGameAi:

    def __init__(self):
        self.possiblePlacements : set[ShipPlacement] = None

    
    def start(self, board : Board, numShips : dict[int, int]) -> None:
        self.possiblePlacements = set()

        shipsToDo : list[int] = []
        for length, count in sorted(numShips.items(), reverse=True):
            shipsToDo += [ length ] * count
        
        self.__generatePossiblePlacements(shipsToDo, ShipPlacement(), board)
        
        print(len(self.possiblePlacements))
        

    def __generatePossiblePlacements(self, shipsToDo : list[int], crntPlacement : ShipPlacement, board : Board):
        if len(shipsToDo) == 0:
            if self.__areAllShipTilesCovered(board, crntPlacement):
                self.possiblePlacements.add(crntPlacement)
            return
        
        crntLength = shipsToDo.pop(0)

        for x in range(board.width):
            for y in range(board.height):
                orientations = random.sample([ ShipShape.VERTICAL, ShipShape.HORIZONTAL ], 2)
                for orientation in orientations:
                    tempShip = ShipShape(crntLength, (x, y), orientation)

                    # does it even fit in currentplacement
                    if not tempShip.isInBoardBounds(board.width, board.height) or not crntPlacement.fitsIn(tempShip):
                        continue

                    # check if it matches the boards requirements
                    if not all(board.check(tile, Board.SHIP | Board.NO_INFO) for tile in tempShip.occupiedTiles()):
                        continue

                    self.__generatePossiblePlacements(shipsToDo.copy(), ShipPlacement(crntPlacement.ships + [ tempShip ]), board)

    
    def __areAllShipTilesCovered(self, board : Board, placement : ShipPlacement) -> bool:
        """occupiedTiles = placement.occupiedCells()

        for x in range(board.width):
            for y in range(board.height):
                if board.check((x, y), Board.SHIP):
                    if (x, y) not in occupiedTiles:
                        return False"""
        return True