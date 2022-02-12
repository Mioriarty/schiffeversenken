from re import S
from ai.Board import Board
from ai.ShipPlacement import ShipPlacement
from ai.ShipShape import ShipShape
import random


class BruteForceGameAi:

    SHIP_ALREADY_SEEN = 0b100000

    def __init__(self):
        self.possiblePlacements : set[ShipPlacement] = None

    
    def start(self, board : Board, numShips : dict[int, int]) -> None:
        self.possiblePlacements = set()

        allreadyFoundPlacement, numShips = self.__getAllreadyFoundShipPlacement(numShips)

        shipsToDo : list[int] = []
        for length, count in sorted(numShips.items(), reverse=True):
            shipsToDo += [ length ] * count
        
        self.__generatePossiblePlacements(shipsToDo, allreadyFoundPlacement, board)
        
        print(len(self.possiblePlacements))
    
    def __getAllreadyFoundShipPlacement(board : Board, numShips : dict[int, int]) -> tuple[ShipPlacement, dict[int, int]]:
        placement = ShipPlacement()

        for (x, y) in board.orderedIndex():
            if board.check((x, y), Board.SHIP):
                board[x, y] = BruteForceGameAi.SHIP_ALREADY_SEEN

                if board.check((x+1, y), Board.SHIP):
                    # horizontal ship
                    # calculate length and set to already seen
                    length = 1
                    while board.check((x+length, y), Board.Ship):
                        board[x+length, y] = BruteForceGameAi.SHIP_ALREADY_SEEN
                        length += 1
                    length -= 1
                    placement.add(ShipShape(length, (x, y), ShipShape.HORIZONTAL))

                else:
                    # vertical ship
                    # calculate length and set to already seen
                    length = 1
                    while board.check((x, y+length), Board.Ship):
                        board[x, y+length] = BruteForceGameAi.SHIP_ALREADY_SEEN
                        length += 1
                    length -= 1
                    placement.add(ShipShape(length, (x, y), ShipShape.VERTICAL))
                
                numShips[length] -= 1
                
        return placement, numShips


        

    def __generatePossiblePlacements(self, shipsToDo : list[int], crntPlacement : ShipPlacement, board : Board):
        if len(shipsToDo) == 0:
            if self.__areAllShipTilesCovered(board, crntPlacement):
                self.possiblePlacements.add(crntPlacement)
            return
        
        crntLength = shipsToDo.pop(0)

        for (x, y) in board.orderedIndex():
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


    def getNextShot(self, board : Board):
        return (0, 0) # TODO