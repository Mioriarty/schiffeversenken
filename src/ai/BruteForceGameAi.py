from numpy import place
from ai.Board import Board
from ai.ShipPlacement import ShipPlacement
from ai.ShipShape import ShipShape
import random


class BruteForceGameAi:

    def __init__(self):
        self.possiblePlacements : set[ShipPlacement] = None
        self.cellPropabilities = {}

    
    def start(self, board : Board, numShipsLeft : dict[int, int]) -> None:
        self.possiblePlacements = set()

        possibleShipLocations = self.__getAllPossibleShipLocations(board)

        board.print()
        print(possibleShipLocations)

        shipsToDo : list[int] = []
        for length, count in sorted(numShipsLeft.items(), reverse=True):
            shipsToDo += [ length ] * count
        
        self.__generatePossiblePlacements(shipsToDo, ShipPlacement(), possibleShipLocations, board)
        
        print(len(self.possiblePlacements))

        

    def __generatePossiblePlacements(self, shipsToDo : list[int], crntPlacement : ShipPlacement, possibleShipLocations : list[tuple[int]], board : Board):
        if len(shipsToDo) == 0:
            self.__submitPossibleShipPlacement(crntPlacement)
            return
        
        crntLength = shipsToDo.pop(0)

        for (x, y) in possibleShipLocations:
            orientations = random.sample([ ShipShape.VERTICAL, ShipShape.HORIZONTAL ], 2)
            for orientation in orientations:
                tempShip = ShipShape(crntLength, (x, y), orientation)

                # is the ship on the board
                if not tempShip.isInBoardBounds(board.width, board.height):
                    continue

                # check if it matches the boards requirements
                if not all(board.check(tile, Board.NO_INFO) for tile in tempShip.occupiedTiles()):
                    continue
            
                # check if it fits in the ship placement
                if not crntPlacement.fitsIn(tempShip):
                    continue

                self.__generatePossiblePlacements(shipsToDo.copy(), ShipPlacement(crntPlacement.ships + [ tempShip ]), possibleShipLocations, board)

    def __getAllPossibleShipLocations(self, board : Board) -> list[tuple[int]]:
        return [ (x, y) for x, y in board.orderedIndex() if board.check((x, y), Board.NO_INFO) and (board.check((x+1, y), Board.NO_INFO) or board.check((x, y+1), Board.NO_INFO)) ]

    def __submitPossibleShipPlacement(self, placement : ShipPlacement) -> None:
        self.possiblePlacements.add(placement)
        
        for cell in placement.occupiedCells():
            if cell in self.cellPropabilities:
                self.cellPropabilities[cell] += 1
            else:
                self.cellPropabilities[cell] = 1
    
    def getNextShot(self):
        print("Calc next shot")
        print(self.cellPropabilities)
        print("Possible Placements: " + str(len(self.possiblePlacements)))
        bestCell = (-1, -1)
        bestProp = -1

        for cell, prop in self.cellPropabilities.items():
            if prop > bestProp:
                bestCell = cell
                bestProp = prop
        
        return bestCell

    
    def submitInfo(self, pos : tuple[int], state : int) -> None:
        isHit = state == Board.SHIP
        toRemove = { placement for placement in self.possiblePlacements if placement.cellOccupied(pos) != isHit }

        for placement in toRemove:
            self.__removePossibleShipPlacement(placement)
        
        # should be accessabel but not an option to shoot at
        self.cellPropabilities[pos] = -2

    def __removePossibleShipPlacement(self, placement : ShipPlacement) -> None:
        for cell in placement.occupiedCells():
            self.cellPropabilities[cell] -= 1
        
        self.possiblePlacements.remove(placement)
